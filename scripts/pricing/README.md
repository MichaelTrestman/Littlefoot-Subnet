# Provider pricing data (fetch + reproducible tables)

The whitepaper occasionally benefits from **ground-truth pricing** (e.g., “what does it cost to run compute in region X vs Y?”). Rather than hand-entering price ranges, we can **fetch pricing directly from cloud provider catalogs** and regenerate a table periodically.

This folder contains a small CLI that fetches pricing for:

- AWS EC2 on-demand (via the AWS **Pricing API**)
- GCP Compute Engine (via the **Cloud Billing Catalog API**)

## Install optional dependencies

The core project dependencies are intentionally small. This pricing tool uses optional deps:

```bash
pip install -e ".[pricing]"
```

## AWS: EC2 on-demand $/hour by region

The AWS Pricing API requires AWS credentials (read-only is fine).

Example:

```bash
python3 -m scripts.pricing.fetch_pricing aws-ec2 \
  --instance-type m7i.2xlarge \
  --regions us-east-1 us-west-2 eu-west-1
```

Notes:

- AWS pricing uses a **human “Location” string** (e.g. `US East (N. Virginia)`) internally. The script maps common region codes to these strings and allows overrides.

## GCP: Compute Engine pricing (Cloud Billing Catalog API)

GCP catalog queries can be done with an **API key**:

```bash
export GOOGLE_API_KEY="..."
python3 -m scripts.pricing.fetch_pricing gcp \
  --sku-contains "N2 Standard Instance Core" \
  --regions us-central1 europe-west4
```

Because GCP pricing is frequently expressed per-vCPU and per-GiB-hour, the tool can optionally compute an **estimated full-machine** hourly price if you supply a spec:

```bash
python3 -m scripts.pricing.fetch_pricing gcp \
  --sku-contains "N2 Standard Instance Core" \
  --regions us-central1 europe-west4 \
  --vcpu 8

python3 -m scripts.pricing.fetch_pricing gcp \
  --sku-contains "N2 Standard Instance Ram" \
  --regions us-central1 europe-west4 \
  --mem-gib 32
```

Then you add the two outputs (core + RAM) to approximate the machine price.

## Output formats

By default the tool prints CSV to stdout. Use `--format md` to print a markdown table.

## Combined “landscape” table (recommended for the whitepaper)

This outputs a single table with:

`provider, region, anchor_instance, offered(Y/N), $/hr, mapped_grid_area, grid_intensity_gCO2_per_kWh`

Example:

```bash
python3 -m scripts.pricing.fetch_pricing landscape --format md
```

Notes:

- AWS pricing works without credentials (public offer files).
- GCP rows require `GOOGLE_API_KEY`.
- Latitude rows are **locations-only** until an API integration; edit `latitude_locations.json`.

