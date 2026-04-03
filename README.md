# Littlefoot: Carbon Footprint Intelligence for Bittensor

Littlefoot is a Bittensor subnet that produces **carbon footprint intelligence** -- verified, actionable data about the carbon efficiency of compute on other Bittensor subnets. It acts as an incentive overlay on existing subnets, subsidizing miners who verifiably operate in low-carbon-intensity grid regions and provide high-quality attestation data.

Carbon footprint intelligence has two aspects, both directly incentivized:

- **Efficiency** -- verifiable infrastructure choices that reduce the carbon footprint of work performed on primary subnets
- **Transparency** -- verified attestations about location, power usage, and related metrics

## Scoring Function

The core scoring function for miner $i$ is:

$$S_i = \frac{W_i \cdot \sigma_i}{C_i}$$

where:
- $W_i$ = Subnet Weight (performance on a primary subnet)
- $C_i$ = Carbon Intensity (gCO2/kWh) for verified location
- $\sigma_i$ = Signal Strength (verification confidence multiplier $\in (0, 1]$)

The normalized weight determining emission distribution is:

$$\hat{W}_i = \frac{S_i}{\sum_{j=1}^{n} S_j}$$

This ensures:
- Miners with zero primary subnet performance ($W_i = 0$) receive no Littlefoot rewards
- Higher verification confidence ($\sigma_i$) increases score
- Lower carbon intensity ($C_i$) increases score
- The mechanism complements primary subnet incentives rather than competing with them

**Variant for validator-compute overlays** (subnets where validators perform the compute, e.g. Ridges SN62, Gradients SN56):

$$S_i = \frac{B_i \cdot \sigma_i}{C_i}$$

where $B_i$ is the number of active validator-miner bonds (a proxy for validation workload).

## Overlay Architecture

Littlefoot supports two overlay patterns depending on where compute is performed:

1. **Miner-compute overlays** -- For subnets where miners control the compute (Lium SN51, Chutes SN64, Templar, IOTA, Hippius SN13). Miners register on Littlefoot and their rewards depend on primary subnet weight ($W_i$) combined with carbon efficiency.

2. **Validator-compute overlays** -- For subnets where validators perform the compute (Ridges SN62, Gradients SN56). Validators register as Littlefoot miners and their rewards depend on bond count ($B_i$) combined with carbon efficiency.

Each supported primary subnet has its own incentive mechanism using Bittensor's multi-mechanism capability. Emissions are split evenly across supported overlays.

## Source Files

| File | Purpose |
|------|---------|
| `validator.py` | Main validator loop: scores miners and sets weights |
| `location_verification.py` | Verifies miner locations via provider APIs (Latitude.sh, AWS, GCP) |
| `carbon_intensity.py` | Maps locations to carbon intensity values (gCO2/kWh) |
| `subnet_weights.py` | Fetches miner weights from primary subnets |

## Verification Tiers

| Tier | Method | Confidence | $\sigma_i$ |
|------|--------|------------|-------------|
| Tier 1 | Provider API (Latitude, AWS, GCP) | High | 1.0 |
| Tier 2 | Colocation attestation | Medium | 0.9 |
| Tier 3 | Multi-signal (latency + IP + reputation) | Low | 0.7 |
| Tier 0 | Unverified | None | 0.0 |

## Setup

### Prerequisites

- Python 3.12+
- Bittensor wallet with TAO for subnet registration
- Active miner on a supported primary subnet

### Installation

```bash
pip install -e .
```

### Configuration

Copy `env.example` to `.env` and edit:

```bash
cp env.example .env
```

Key settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `NETWORK` | `finney` | `finney` (mainnet), `test` (testnet), or `local` |
| `NETUID` | `1` | Littlefoot subnet netuid |
| `WALLET_NAME` | `default` | Wallet name |
| `HOTKEY_NAME` | `default` | Hotkey name |
| `LIUM_NETUID` | `51` | Lium subnet netuid |
| `CHUTES_NETUID` | `64` | Chutes subnet netuid |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

### Running the Validator

```bash
python validator.py \
  --network finney \
  --netuid <your_netuid> \
  --coldkey <wallet_name> \
  --hotkey <hotkey_name>
```

All options can also be set via environment variables (see `env.example`).

## How It Works

### Validator Loop

1. Sync metagraph for the Littlefoot subnet
2. For each miner, fetch their weight on primary subnets ($W_i$)
3. Query miner verification info and verify location via provider APIs
4. Look up carbon intensity ($C_i$) for verified location
5. Get verification confidence ($\sigma_i$) from tier
6. Calculate score: $S_i = (W_i \cdot \sigma_i) / C_i$
7. Normalize scores and submit weights to chain

### For Miners

Miners provide location verification data so validators can verify their carbon footprint. This can be done via chain commits or direct query endpoints.

Example attestation:
```json
{
  "location": "us-west-1",
  "provider": "latitude",
  "server_id": "server_123",
  "api_key": "lat_...",
  "carbon_intensity_claim": 250,
  "timestamp": 1704067200
}
```

## Carbon Intensity Reference

| Location | gCO2/kWh | Relative to Coal |
|----------|----------|------------------|
| Quebec | 25 | 36x cleaner |
| Iceland | 28 | 32x cleaner |
| Norway | 30 | 30x cleaner |
| France | 50 | 18x cleaner |
| Oregon (US) | 250 | 3.6x cleaner |
| Virginia (US) | 380 | 2.4x cleaner |
| Poland | 900 | Baseline (coal) |

At launch, these are annual averages. Future iterations will incorporate real-time grid data via WattTime/ElectricityMaps APIs.

## Limitations (MVP)

- **PUE** not measured (datacenter overhead unknown)
- **Embodied carbon** not accounted for
- **Real-time grid variation** not yet used (annual averages only)
- **Cooling efficiency** beyond location averages ignored

Estimated error on absolute emissions: 30-60%. For the purpose of **ranking miners by carbon efficiency**, this is acceptable because location dominates (10-30x differences). Rankings remain correct even with significant measurement error.

## Future Direction

- Real-time carbon intensity via WattTime/ElectricityMaps APIs
- Power measurement integration where verifiable (e.g. Lium's NVML data)
- PUE estimation through provider partnerships
- Time-of-day grid variation weighting
- Additional provider integrations (Azure, other bare metal)
- Expanded verification signals for gaming resistance

## References

- [Littlefoot Whitepaper](./WHITEPAPER.md)
- [Bittensor Documentation](https://docs.bittensor.com)
