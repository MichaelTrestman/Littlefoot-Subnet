from __future__ import annotations

import csv
import io
import json
import os
import sys
import time
import urllib.request
from dataclasses import dataclass
from typing import Iterable, Literal

import click
import requests


OutputFormat = Literal["csv", "md"]

# GCP Cloud Billing Catalog service ID for "Compute Engine"
# (This is stable and avoids needing to page through all services.)
GCP_COMPUTE_ENGINE_SERVICE_ID = "6F81-5844-456A"


@dataclass(frozen=True)
class PriceRow:
    provider: str
    sku: str
    region: str
    unit: str
    price: float
    currency: str
    notes: str = ""


def _print_csv(rows: list[PriceRow]) -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(["provider", "sku", "region", "unit", "price", "currency", "notes"])
    for r in rows:
        writer.writerow([r.provider, r.sku, r.region, r.unit, f"{r.price:.10g}", r.currency, r.notes])


def _print_md(rows: list[PriceRow]) -> None:
    # Minimal markdown table; caller can paste into docs.
    headers = ["provider", "sku", "region", "unit", "price", "currency", "notes"]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        print(
            "| "
            + " | ".join(
                [
                    r.provider,
                    r.sku,
                    r.region,
                    r.unit,
                    f"{r.price:.10g}",
                    r.currency,
                    r.notes or "",
                ]
            )
            + " |"
        )


def _emit(rows: list[PriceRow], fmt: OutputFormat) -> None:
    if fmt == "csv":
        _print_csv(rows)
    elif fmt == "md":
        _print_md(rows)
    else:
        raise click.ClickException(f"Unknown format: {fmt}")


@dataclass(frozen=True)
class LandscapeRow:
    provider: str
    region: str
    anchor_instance: str
    offered: str  # "Y" | "N"
    usd_per_hour: str  # keep as string so blanks are representable
    mapped_grid_area: str
    grid_intensity_gco2_per_kwh: str  # keep as string so blanks are representable
    notes: str = ""


def _emit_landscape(rows: list[LandscapeRow], fmt: OutputFormat) -> None:
    headers = [
        "provider",
        "region",
        "anchor_instance",
        "offered",
        "usd_per_hour",
        "mapped_grid_area",
        "grid_intensity_gco2_per_kwh",
        "notes",
    ]

    if fmt == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(headers)
        for r in rows:
            writer.writerow(
                [
                    r.provider,
                    r.region,
                    r.anchor_instance,
                    r.offered,
                    r.usd_per_hour,
                    r.mapped_grid_area,
                    r.grid_intensity_gco2_per_kwh,
                    r.notes,
                ]
            )
        return

    if fmt == "md":
        print("| " + " | ".join(headers) + " |")
        print("|" + "|".join(["---"] * len(headers)) + "|")
        for r in rows:
            print(
                "| "
                + " | ".join(
                    [
                        r.provider,
                        r.region,
                        r.anchor_instance,
                        r.offered,
                        r.usd_per_hour,
                        r.mapped_grid_area,
                        r.grid_intensity_gco2_per_kwh,
                        r.notes or "",
                    ]
                )
                + " |"
            )
        return

    raise click.ClickException(f"Unknown format: {fmt}")


AWS_REGION_TO_LOCATION = {
    # Common regions; extend as needed. AWS Pricing API uses this "Location" string.
    "us-east-1": "US East (N. Virginia)",
    "us-east-2": "US East (Ohio)",
    "us-west-1": "US West (N. California)",
    "us-west-2": "US West (Oregon)",
    "ca-central-1": "Canada (Central)",
    "eu-west-1": "EU (Ireland)",
    "eu-central-1": "EU (Frankfurt)",
    "eu-north-1": "EU (Stockholm)",
    "ap-northeast-1": "Asia Pacific (Tokyo)",
    "ap-northeast-2": "Asia Pacific (Seoul)",
    "ap-southeast-1": "Asia Pacific (Singapore)",
    "ap-southeast-2": "Asia Pacific (Sydney)",
}


AWS_REGION_TO_GRID_AREA = {
    # Country-level proxy mapping; refine later if you want state/province granularity.
    "us-east-1": "United States of America",
    "us-east-2": "United States of America",
    "us-west-1": "United States of America",
    "us-west-2": "United States of America",
    "ca-central-1": "Canada",
    "eu-west-1": "Ireland",
    "eu-central-1": "Germany",
    "eu-north-1": "Sweden",
    "ap-northeast-1": "Japan",
    "ap-northeast-2": "South Korea",
    "ap-southeast-1": "Singapore",
    "ap-southeast-2": "Australia",
}


GCP_REGION_TO_GRID_AREA = {
    # Minimal starter mapping; extend as needed.
    "us-central1": "United States of America",
    "us-east1": "United States of America",
    "us-west1": "United States of America",
    "europe-west4": "Netherlands",
    "europe-north1": "Finland",
    "asia-southeast1": "Singapore",
}


def _cache_dir() -> str:
    d = os.path.join(os.path.dirname(__file__), ".cache")
    os.makedirs(d, exist_ok=True)
    return d


def _ember_latest_intensity_map(*, max_age_days: int = 30) -> dict[str, dict]:
    """
    Builds (and caches) latest grid CO2 intensity per Ember "Area".

    Returns:
      { Area: {"year": int, "value": float, "unit": "gCO2/kWh"} }

    Source:
      https://ember-energy.org/data/yearly-electricity-data
    """
    cache_path = os.path.join(_cache_dir(), "ember_latest_co2_intensity.json")
    now = time.time()
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cached = json.load(f)
            meta = cached.get("_meta", {})
            ts = float(meta.get("generated_at_unix", 0))
            if ts and (now - ts) < max_age_days * 86400:
                data = cached.get("data", {})
                if isinstance(data, dict) and data:
                    return data
        except Exception:
            pass

    url = "https://files.ember-energy.org/public-downloads/yearly_full_release_long_format.csv"
    with urllib.request.urlopen(url) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))

    best: dict[str, dict] = {}
    for row in reader:
        if row.get("Variable") != "CO2 intensity":
            continue
        area = row.get("Area")
        year_s = row.get("Year")
        val_s = row.get("Value")
        unit = row.get("Unit") or "gCO2/kWh"
        if not area or not year_s or not val_s:
            continue
        try:
            year = int(year_s)
            val = float(val_s)
        except ValueError:
            continue
        prev = best.get(area)
        if (prev is None) or (year > int(prev["year"])):
            best[area] = {"year": year, "value": val, "unit": unit}

    payload = {"_meta": {"generated_at_unix": now, "source": url}, "data": best}
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)
    except Exception:
        pass
    return best


def _ember_intensity_for_area(area: str, intensity_map: dict[str, dict]) -> tuple[str, str]:
    entry = intensity_map.get(area)
    if not entry:
        return "", f"no Ember intensity for area={area}"
    return f"{float(entry['value']):.4g}", f"Ember year={entry['year']}"


def _require_optional(dep_name: str, import_name: str):
    try:
        __import__(import_name)
    except Exception as e:
        raise click.ClickException(
            f"Missing optional dependency for {dep_name}. Install with: pip install -e \".[pricing]\".\n"
            f"Import error: {e}"
        )


def _aws_public_region_offer_url(region: str) -> str:
    """
    AWS publishes EC2 offer files publicly. This lets us fetch on-demand prices
    without credentials (useful for generating docs).
    """
    index_url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/region_index.json"
    with urllib.request.urlopen(index_url) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
    offers = data.get("regions", {})
    reg = offers.get(region)
    if not reg:
        raise click.ClickException(f"AWS public pricing index has no region {region}.")
    # currentVersionUrl is a relative path like "/offers/v1.0/aws/AmazonEC2/current/us-east-1/index.json"
    rel = reg.get("currentVersionUrl")
    if not isinstance(rel, str):
        raise click.ClickException(f"Unexpected AWS region index format for {region}.")
    return "https://pricing.us-east-1.amazonaws.com" + rel


def _aws_ec2_ondemand_hourly_price_public(
    instance_type: str,
    region: str,
    *,
    operating_system: str = "Linux",
    tenancy: str = "Shared",
    preinstalled_sw: str = "NA",
    capacitystatus: str = "Used",
    location_override: str | None = None,
) -> PriceRow:
    location = location_override or AWS_REGION_TO_LOCATION.get(region)
    if not location:
        raise click.ClickException(
            f"Unknown AWS region mapping for {region}. Provide --location-override for this region."
        )

    offer_url = _aws_public_region_offer_url(region)
    with urllib.request.urlopen(offer_url) as resp:
        offer = json.loads(resp.read().decode("utf-8", errors="replace"))

    products = offer.get("products", {})
    if not isinstance(products, dict) or not products:
        raise click.ClickException(f"Unexpected AWS offer format for {region}: missing products.")

    # Find matching SKU by attributes
    wanted = {
        "instanceType": instance_type,
        "location": location,
        "operatingSystem": operating_system,
        "tenancy": tenancy,
        "preInstalledSw": preinstalled_sw,
        "capacitystatus": capacitystatus,
    }
    matching_skus: list[str] = []
    for sku, prod in products.items():
        attrs = (prod or {}).get("attributes") or {}
        if all(str(attrs.get(k)) == v for k, v in wanted.items()):
            matching_skus.append(sku)

    if not matching_skus:
        raise click.ClickException(
            f"No AWS public pricing match for instance={instance_type}, region={region} (location={location})."
        )

    terms = offer.get("terms", {}).get("OnDemand", {})
    if not isinstance(terms, dict) or not terms:
        raise click.ClickException(f"Unexpected AWS offer format for {region}: missing OnDemand terms.")

    # Pick first matching SKU; if multiple, take the cheapest *positive* USD/Hrs.
    # Some offer files include non-hourly or zero-priced dimensions; ignore those.
    best: tuple[float, str, str] | None = None  # (price, unit, sku)
    for sku in matching_skus:
        sku_terms = terms.get(sku) or {}
        for _term_code, term in sku_terms.items():
            dims = (term or {}).get("priceDimensions") or {}
            for _dim_code, dim in dims.items():
                unit = str(dim.get("unit") or "")
                usd = (dim.get("pricePerUnit") or {}).get("USD")
                if usd is None:
                    continue
                try:
                    p = float(usd)
                except ValueError:
                    continue
                if unit not in {"Hrs", "Hours"}:
                    continue
                if p <= 0:
                    continue
                if best is None or p < best[0]:
                    best = (p, unit, sku)

    if best is None:
        raise click.ClickException(f"Could not extract USD price from AWS public offer for {region}.")

    price, unit, _sku = best
    return PriceRow(
        provider="aws",
        sku=f"ec2:{instance_type}",
        region=region,
        unit=unit or "Hrs",
        price=price,
        currency="USD",
        notes=f"public-offer; location={location}",
    )


def _aws_ec2_ondemand_hourly_price(
    instance_type: str,
    region: str,
    *,
    operating_system: str = "Linux",
    tenancy: str = "Shared",
    preinstalled_sw: str = "NA",
    capacitystatus: str = "Used",
    location_override: str | None = None,
) -> PriceRow:
    # Prefer AWS Pricing API if boto3 + credentials exist; otherwise fall back to public offer files.
    try:
        import boto3  # type: ignore
    except Exception:
        return _aws_ec2_ondemand_hourly_price_public(
            instance_type,
            region,
            operating_system=operating_system,
            tenancy=tenancy,
            preinstalled_sw=preinstalled_sw,
            capacitystatus=capacitystatus,
            location_override=location_override,
        )

    location = location_override or AWS_REGION_TO_LOCATION.get(region)
    if not location:
        raise click.ClickException(
            f"Unknown AWS region mapping for {region}. Provide --location-override for this region."
        )

    # Pricing API is only in a few regions; us-east-1 is standard.
    try:
        pricing = boto3.client("pricing", region_name="us-east-1")
    except Exception:
        return _aws_ec2_ondemand_hourly_price_public(
            instance_type,
            region,
            operating_system=operating_system,
            tenancy=tenancy,
            preinstalled_sw=preinstalled_sw,
            capacitystatus=capacitystatus,
            location_override=location_override,
        )

    filters = [
        {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_type},
        {"Type": "TERM_MATCH", "Field": "location", "Value": location},
        {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": operating_system},
        {"Type": "TERM_MATCH", "Field": "tenancy", "Value": tenancy},
        {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": preinstalled_sw},
        {"Type": "TERM_MATCH", "Field": "capacitystatus", "Value": capacitystatus},
    ]

    try:
        resp = pricing.get_products(ServiceCode="AmazonEC2", Filters=filters, MaxResults=100)
    except Exception:
        return _aws_ec2_ondemand_hourly_price_public(
            instance_type,
            region,
            operating_system=operating_system,
            tenancy=tenancy,
            preinstalled_sw=preinstalled_sw,
            capacitystatus=capacitystatus,
            location_override=location_override,
        )
    price_list = resp.get("PriceList", [])
    if not price_list:
        raise click.ClickException(
            f"No AWS pricing results for instance={instance_type}, region={region} (location={location})."
        )

    # Pick the first match; you can refine filters if you need e.g. GPU, size-flex, etc.
    offer = json.loads(price_list[0])
    terms = offer.get("terms", {}).get("OnDemand", {})
    if not terms:
        raise click.ClickException("Unexpected AWS offer format: missing OnDemand terms.")

    # There is typically one OnDemand term; grab first.
    term = next(iter(terms.values()))
    price_dimensions = term.get("priceDimensions", {})
    if not price_dimensions:
        raise click.ClickException("Unexpected AWS offer format: missing priceDimensions.")

    dim = next(iter(price_dimensions.values()))
    price_per_unit = dim.get("pricePerUnit", {})
    usd = price_per_unit.get("USD")
    if usd is None:
        raise click.ClickException("Unexpected AWS offer format: missing USD price.")

    return PriceRow(
        provider="aws",
        sku=f"ec2:{instance_type}",
        region=region,
        unit=dim.get("unit", "Hrs"),
        price=float(usd),
        currency="USD",
        notes=f"location={location}",
    )


def _gcp_get_services(api_key: str) -> list[dict]:
    url = "https://cloudbilling.googleapis.com/v1/services"
    resp = requests.get(url, params={"key": api_key}, timeout=60)
    resp.raise_for_status()
    return resp.json().get("services", [])


def _gcp_get_services_oauth(access_token: str) -> list[dict]:
    url = "https://cloudbilling.googleapis.com/v1/services"
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("services", [])


def _gcp_find_service_id(services: list[dict], display_name: str) -> str:
    for s in services:
        if s.get("displayName") == display_name:
            # name is like "services/6F81-5844-456A"
            name = s.get("name")
            if isinstance(name, str) and name.startswith("services/"):
                return name.split("/", 1)[1]
    raise click.ClickException(f'Could not find GCP service "{display_name}" in Cloud Billing Catalog API.')


def _gcp_list_skus(api_key: str, service_id: str, *, currency: str = "USD") -> Iterable[dict]:
    url = f"https://cloudbilling.googleapis.com/v1/services/{service_id}/skus"
    page_token: str | None = None
    while True:
        params = {"key": api_key, "currencyCode": currency, "pageSize": 5000}
        if page_token:
            params["pageToken"] = page_token
        resp = requests.get(url, params=params, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        for sku in data.get("skus", []) or []:
            yield sku
        page_token = data.get("nextPageToken")
        if not page_token:
            break


def _gcp_list_skus_oauth(access_token: str, service_id: str, *, currency: str = "USD") -> Iterable[dict]:
    url = f"https://cloudbilling.googleapis.com/v1/services/{service_id}/skus"
    page_token: str | None = None
    while True:
        params = {"currencyCode": currency, "pageSize": 5000}
        if page_token:
            params["pageToken"] = page_token
        resp = requests.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        for sku in data.get("skus", []) or []:
            yield sku
        page_token = data.get("nextPageToken")
        if not page_token:
            break


def _gcloud_access_token() -> str | None:
    """
    Returns an access token from gcloud if available.
    Uses user token (gcloud auth print-access-token).
    """
    import subprocess

    try:
        tok = (
            subprocess.check_output(["gcloud", "auth", "print-access-token"], stderr=subprocess.DEVNULL)
            .decode("utf-8", errors="replace")
            .strip()
        )
        return tok or None
    except Exception:
        return None


def _gcp_sku_hourly_price_usd(sku: dict) -> tuple[float, str]:
    # pricingInfo[0].pricingExpression.tieredRates[0].unitPrice.{units,nanos}
    pricing_info = (sku.get("pricingInfo") or [])
    if not pricing_info:
        raise click.ClickException("Unexpected GCP SKU format: missing pricingInfo.")
    expr = pricing_info[0].get("pricingExpression") or {}
    tiered = expr.get("tieredRates") or []
    if not tiered:
        raise click.ClickException("Unexpected GCP SKU format: missing tieredRates.")
    unit_price = tiered[0].get("unitPrice") or {}
    units = int(unit_price.get("units") or 0)
    nanos = int(unit_price.get("nanos") or 0)
    price = units + nanos / 1e9

    usage_unit = expr.get("usageUnit") or ""
    # Commonly "h" or "GiBy.h" or similar; keep as-is.
    return price, str(usage_unit)


@click.group()
def cli() -> None:
    """Fetch provider pricing for reproducible docs."""


@cli.command("aws-ec2")
@click.option("--instance-type", required=True, help="EC2 instance type, e.g. m7i.2xlarge")
@click.option(
    "--regions",
    multiple=True,
    required=True,
    help="AWS regions to query, e.g. --regions us-east-1 --regions eu-west-1",
)
@click.option("--format", "fmt", type=click.Choice(["csv", "md"]), default="csv")
@click.option(
    "--location-override",
    default=None,
    help='Override AWS "Location" string (advanced). Mostly useful if region mapping is missing.',
)
def aws_ec2(instance_type: str, regions: tuple[str, ...], fmt: OutputFormat, location_override: str | None) -> None:
    """Fetch AWS EC2 on-demand pricing by region."""
    rows: list[PriceRow] = []
    for r in regions:
        rows.append(
            _aws_ec2_ondemand_hourly_price(instance_type, r, location_override=location_override)
        )
    _emit(rows, fmt)


@cli.command("gcp")
@click.option(
    "--sku-contains",
    required=True,
    help='Substring match against SKU description, e.g. "N2 Standard Instance Core".',
)
@click.option(
    "--regions",
    multiple=True,
    required=True,
    help="GCP regions to include, e.g. us-central1 europe-west4",
)
@click.option("--format", "fmt", type=click.Choice(["csv", "md"]), default="csv")
@click.option("--api-key", default=lambda: os.environ.get("GOOGLE_API_KEY"), show_default="$GOOGLE_API_KEY")
@click.option("--currency", default="USD", show_default=True)
@click.option("--vcpu", type=int, default=None, help="Optional multiplier for per-vCPU SKUs.")
@click.option("--mem-gib", type=float, default=None, help="Optional multiplier for per-GiB RAM SKUs.")
def gcp_cmd(
    sku_contains: str,
    regions: tuple[str, ...],
    fmt: OutputFormat,
    api_key: str | None,
    currency: str,
    vcpu: int | None,
    mem_gib: float | None,
) -> None:
    """Fetch GCP Cloud Billing catalog pricing for matching SKUs."""
    access_token = None
    if not api_key:
        access_token = _gcloud_access_token()
        if not access_token:
            raise click.ClickException(
                "Missing GCP API credentials. Set GOOGLE_API_KEY (API key) or login with gcloud (gcloud auth login)."
            )

    service_id = GCP_COMPUTE_ENGINE_SERVICE_ID

    want = sku_contains.lower()
    want_regions = set(regions)
    rows: list[PriceRow] = []

    sku_iter = (
        _gcp_list_skus(api_key, service_id, currency=currency)
        if api_key
        else _gcp_list_skus_oauth(access_token, service_id, currency=currency)  # type: ignore[arg-type]
    )
    for sku in sku_iter:
        desc = str(sku.get("description") or "")
        if want not in desc.lower():
            continue

        sku_regions = set(sku.get("serviceRegions") or [])
        matched_regions = sorted(sku_regions.intersection(want_regions))
        if not matched_regions:
            continue

        price, usage_unit = _gcp_sku_hourly_price_usd(sku)

        multiplier = 1.0
        notes = []
        if vcpu is not None:
            multiplier *= float(vcpu)
            notes.append(f"vcpu={vcpu}")
        if mem_gib is not None:
            multiplier *= float(mem_gib)
            notes.append(f"mem_gib={mem_gib}")

        for reg in matched_regions:
            rows.append(
                PriceRow(
                    provider="gcp",
                    sku=desc,
                    region=reg,
                    unit=usage_unit,
                    price=price * multiplier,
                    currency=currency,
                    notes=", ".join(notes),
                )
            )

    if not rows:
        raise click.ClickException(
            "No matching GCP SKUs found for those regions. Try a broader --sku-contains."
        )

    _emit(rows, fmt)


@cli.command("landscape")
@click.option("--format", "fmt", type=click.Choice(["csv", "md"]), default="md")
@click.option(
    "--aws-regions",
    multiple=True,
    default=["us-east-1", "us-west-2", "eu-west-1", "eu-north-1", "ap-southeast-1", "ca-central-1"],
    show_default=True,
    help="AWS regions to include.",
)
@click.option(
    "--gcp-regions",
    multiple=True,
    default=["us-central1", "europe-west4", "europe-north1", "asia-southeast1"],
    show_default=True,
    help="GCP regions to include (requires GOOGLE_API_KEY).",
)
@click.option("--aws-cpu", default="m7i.48xlarge", show_default=True)
@click.option("--aws-gpu", default="p4d.24xlarge", show_default=True)
@click.option("--gcp-vcpu", type=int, default=32, show_default=True)
@click.option("--gcp-mem-gib", type=float, default=128.0, show_default=True)
@click.option(
    "--latitude-locations-json",
    default=os.path.join(os.path.dirname(__file__), "latitude_locations.json"),
    show_default=True,
    help="Path to a JSON list of Latitude locations (until API integration).",
)
def landscape_cmd(
    fmt: OutputFormat,
    aws_regions: tuple[str, ...],
    gcp_regions: tuple[str, ...],
    aws_cpu: str,
    aws_gpu: str,
    gcp_vcpu: int,
    gcp_mem_gib: float,
    latitude_locations_json: str,
) -> None:
    """Combined table for price + availability + grid intensity."""
    intensity_map = _ember_latest_intensity_map()
    out: list[LandscapeRow] = []

    def add_row(
        provider: str,
        region: str,
        anchor: str,
        offered: bool,
        usd_per_hour: float | None,
        grid_area: str,
        grid_intensity: str,
        notes: str = "",
    ) -> None:
        out.append(
            LandscapeRow(
                provider=provider,
                region=region,
                anchor_instance=anchor,
                offered="Y" if offered else "N",
                usd_per_hour="" if usd_per_hour is None else f"{usd_per_hour:.10g}",
                mapped_grid_area=grid_area,
                grid_intensity_gco2_per_kwh=grid_intensity,
                notes=notes,
            )
        )

    # AWS: big CPU + big GPU anchors
    for region in aws_regions:
        grid_area = AWS_REGION_TO_GRID_AREA.get(region, "UNKNOWN")
        intensity, note = _ember_intensity_for_area(grid_area, intensity_map) if grid_area != "UNKNOWN" else ("", "no mapping")
        for anchor in (aws_cpu, aws_gpu):
            try:
                pr = _aws_ec2_ondemand_hourly_price(anchor, region)
                add_row(
                    "aws",
                    region,
                    anchor,
                    True,
                    pr.price,
                    grid_area,
                    intensity,
                    notes="; ".join([note, pr.notes]).strip("; "),
                )
            except Exception as e:
                add_row(
                    "aws",
                    region,
                    anchor,
                    False,
                    None,
                    grid_area,
                    intensity,
                    notes="; ".join([note, f"unavailable: {e}"]).strip("; "),
                )

    # GCP: N2 anchor approximated as vCPU + RAM pricing.
    api_key = os.environ.get("GOOGLE_API_KEY")
    access_token = None if api_key else _gcloud_access_token()
    if api_key or access_token:
        try:
            service_id = GCP_COMPUTE_ENGINE_SERVICE_ID

            def _gcp_region_price(sku_contains: str, multiplier: float) -> dict[str, float]:
                want = sku_contains.lower()
                want_regions = set(gcp_regions)
                outp: dict[str, float] = {}
                sku_iter = (
                    _gcp_list_skus(api_key, service_id, currency="USD")
                    if api_key
                    else _gcp_list_skus_oauth(access_token, service_id, currency="USD")  # type: ignore[arg-type]
                )
                for sku in sku_iter:
                    desc = str(sku.get("description") or "")
                    if want not in desc.lower():
                        continue
                    sku_regions = set(sku.get("serviceRegions") or [])
                    matched = sku_regions.intersection(want_regions)
                    if not matched:
                        continue
                    price, usage_unit = _gcp_sku_hourly_price_usd(sku)
                    if usage_unit != "h":
                        # keep landscape simple: only hourly SKUs
                        continue
                    for reg in matched:
                        outp[reg] = price * multiplier
                    break
                return outp

            core = _gcp_region_price("N2 Standard Instance Core", float(gcp_vcpu))
            ram = _gcp_region_price("N2 Standard Instance Ram", float(gcp_mem_gib))
            for region in gcp_regions:
                grid_area = GCP_REGION_TO_GRID_AREA.get(region, "UNKNOWN")
                intensity, note = _ember_intensity_for_area(grid_area, intensity_map) if grid_area != "UNKNOWN" else ("", "no mapping")
                if region in core and region in ram:
                    add_row(
                        "gcp",
                        region,
                        f"n2-standard-{gcp_vcpu} (approx)",
                        True,
                        core[region] + ram[region],
                        grid_area,
                        intensity,
                        notes="; ".join([note, f"vcpu={gcp_vcpu}, mem_gib={gcp_mem_gib}"]).strip("; "),
                    )
                else:
                    add_row(
                        "gcp",
                        region,
                        f"n2-standard-{gcp_vcpu} (approx)",
                        False,
                        None,
                        grid_area,
                        intensity,
                        notes="; ".join([note, "missing SKU match for core/ram"]).strip("; "),
                    )
        except Exception as e:
            for region in gcp_regions:
                grid_area = GCP_REGION_TO_GRID_AREA.get(region, "UNKNOWN")
                intensity, note = _ember_intensity_for_area(grid_area, intensity_map) if grid_area != "UNKNOWN" else ("", "no mapping")
                add_row(
                    "gcp",
                    region,
                    f"n2-standard-{gcp_vcpu} (approx)",
                    False,
                    None,
                    grid_area,
                    intensity,
                    notes="; ".join([note, f"gcp error: {e}"]).strip("; "),
                )
    else:
        for region in gcp_regions:
            grid_area = GCP_REGION_TO_GRID_AREA.get(region, "UNKNOWN")
            intensity, note = _ember_intensity_for_area(grid_area, intensity_map) if grid_area != "UNKNOWN" else ("", "no mapping")
            add_row(
                "gcp",
                region,
                f"n2-standard-{gcp_vcpu} (approx)",
                False,
                None,
                grid_area,
                intensity,
                notes="; ".join([note, "set GOOGLE_API_KEY or login with gcloud to fetch GCP pricing"]).strip("; "),
            )

    # Latitude: locations-only until API (user-supplied file)
    try:
        with open(latitude_locations_json, "r", encoding="utf-8") as f:
            lat = json.load(f)
        if isinstance(lat, list):
            for entry in lat:
                if not isinstance(entry, dict):
                    continue
                loc = str(entry.get("location") or "")
                grid_area = str(entry.get("grid_area") or "UNKNOWN")
                intensity, note = _ember_intensity_for_area(grid_area, intensity_map) if grid_area != "UNKNOWN" else ("", "no mapping")
                add_row(
                    "latitude",
                    loc or "UNKNOWN",
                    "N/A",
                    True if loc else False,
                    None,
                    grid_area,
                    intensity,
                    notes="; ".join([note, "locations-only (no pricing yet)"]).strip("; "),
                )
    except FileNotFoundError:
        pass
    except Exception as e:
        add_row(
            "latitude",
            "N/A",
            "N/A",
            False,
            None,
            "UNKNOWN",
            "",
            notes=f"latitude locations file error: {e}",
        )

    _emit_landscape(out, fmt)


if __name__ == "__main__":
    cli()

