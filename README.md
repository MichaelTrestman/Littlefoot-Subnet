# Littlefoot: A Geographic Incentive Layer for Sustainable AI Compute

Littlefoot is a Bittensor subnet that incentivizes clean AI compute by rewarding miners who verifiably operate in low-carbon-intensity grid regions. It acts as an incentive overlay on existing Bittensor subnets (Lium SN51, Chutes SN64), subsidizing miners who meet efficiency benchmarks.

## Overview

Littlefoot creates a countervailing economic pressure by incentivizing transparency and power-use efficiency. The subnet focuses on **geographic location** as the primary factor because:

1. **High Impact**: Location creates 10-30× differences in carbon intensity
2. **Reliable Verification**: Provider APIs (Latitude.sh, AWS, GCP) give ground truth
3. **Measurable**: Can be verified without trusting miners

### Scoring Function

The core scoring function for miner $i$ is:

$$S_i = \frac{W_i}{C_i \cdot \sigma_i}$$

where:
- $W_i$ = Subnet Weight (performance on underlying subnet like Lium/Chutes)
- $C_i$ = Carbon Intensity (gCO₂/kWh) for verified location
- $\sigma_i$ = Signal Strength (verification confidence multiplier ∈ (0, 1])

The normalized weight determining emission distribution is:

$$\hat{W}_i = \frac{S_i}{\sum_{j=1}^{n} S_j}$$

**Result**: Miners in clean-grid locations (Iceland, Quebec, Norway) receive significantly higher rewards than those in coal-heavy regions (Poland, Ohio).

## Architecture

### Components

1. **`validator.py`** - Main validator loop that scores miners and sets weights
2. **`location_verification.py`** - Verifies miner locations via provider APIs
3. **`carbon_intensity.py`** - Maps locations to carbon intensity values
4. **`subnet_weights.py`** - Fetches miner weights from target subnets (Lium, Chutes)

### Verification Tiers

| Tier | Method | Confidence | Score Multiplier |
|------|--------|------------|-------------------|
| Tier 1 | Provider API (Latitude, AWS, GCP) | High | 1.0× |
| Tier 2 | Colocation attestation | Medium | 0.9× |
| Tier 3 | Multi-signal (latency + IP + reputation) | Low | 0.7× |
| Tier 0 | Unverified | None | 0.0× |

## Setup

### Prerequisites

- Python 3.12+
- Bittensor wallet with TAO for subnet registration
- Access to target subnets (Lium SN51, Chutes SN64) for weight fetching

### Installation

1. **Clone the repository** (if not already in your workspace):
   ```bash
   cd /path/to/your/workspace
   git clone <repository-url> littlefoot
   cd littlefoot
   ```

2. **Install dependencies**:
   ```bash
   pip install uv
   uv pip install -e .
   ```

   Or using standard pip:
   ```bash
   pip install -e .
   ```

3. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

### Configuration

Edit `.env` with your settings:

```bash
# Network Configuration
NETWORK=finney          # finney (mainnet), test (testnet), or local
NETUID=1                # Your subnet's netuid (after registration)

# Wallet Configuration
WALLET_NAME=default     # Name of your wallet
HOTKEY_NAME=default     # Name of your hotkey

# Target Subnets
LIUM_NETUID=51          # Lium subnet netuid
CHUTES_NETUID=64        # Chutes subnet netuid

# Logging
LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR
```

### Running the Validator

#### Local Development

```bash
python validator.py \
  --network finney \
  --netuid <your_netuid> \
  --coldkey <wallet_name> \
  --hotkey <hotkey_name> \
  --lium-netuid 51 \
  --chutes-netuid 64
```

#### Docker

1. **Build the image**:
   ```bash
   docker build -t littlefoot-validator .
   ```

2. **Run with docker-compose**:
   ```bash
   docker-compose up -d
   ```

3. **View logs**:
   ```bash
   docker-compose logs -f validator
   ```

## How It Works

### For Validators

1. **Sync metagraph** - Get list of all miners on Littlefoot subnet
2. **Fetch subnet weights** - For each miner, get their weight on target subnets (Lium/Chutes)
3. **Verify locations** - Query miner verification info and verify via provider APIs
4. **Lookup carbon intensity** - Map verified location to carbon intensity (gCO₂/kWh)
5. **Calculate scores** - Apply scoring function: $S_i = W_i / (C_i \cdot \sigma_i)$
6. **Normalize and set weights** - Normalize scores and submit to chain

### For Miners

Miners need to provide location verification information. This can be done via:

1. **Chain commits** - Commit verification info on-chain (provider, API keys, server IDs)
2. **Direct queries** - Expose an endpoint that validators can query

**Example verification info**:
```json
{
  "provider": "latitude",
  "api_key": "lat_...",
  "server_id": "server_123"
}
```

Or for AWS:
```json
{
  "provider": "aws",
  "access_key_id": "AKIA...",
  "secret_access_key": "...",
  "instance_id": "i-1234567890abcdef0"
}
```

## Carbon Intensity Database

The subnet includes a carbon intensity database mapping locations to gCO₂/kWh values. Examples:

| Location | Carbon Intensity (gCO₂/kWh) | Relative to Coal |
|----------|----------------------------|------------------|
| Iceland | 28 | 32× cleaner |
| Quebec | 25 | 36× cleaner |
| Norway | 30 | 30× cleaner |
| France | 50 | 18× cleaner |
| Oregon (US) | 250 | 3.6× cleaner |
| Virginia (US) | 380 | 2.4× cleaner |
| Poland | 900 | Baseline (coal) |

The database can be extended with new regions as needed.

## Target Subnets

### Lium (SN51) - Primary Target

GPU rental marketplace where miners contribute machines and renters SSH in to run compute jobs.

**Why ideal:**
- Power data already collected via NVML
- Validators SSH into miners, enabling direct verification
- Minimal integration effort

### Chutes (SN64) - Co-Primary Target

Serverless AI inference platform where miners serve model inference requests.

**Why ideal:**
- Miners already use Latitude.sh (documented in their README)
- GraVal hardware attestation already verifies GPUs
- High energy usage makes efficiency particularly impactful

## Limitations at Launch (MVP)

The initial implementation has some limitations:

- **PUE (Power Usage Effectiveness)**: Not measured (datacenter overhead unknown)
- **Embodied carbon**: Manufacturing emissions ignored
- **Real-time grid variation**: Uses averages, not marginal emissions
- **Cooling efficiency**: Climate effects beyond location averages ignored

**Estimated error**: 30-60% on actual emissions accounting.

However, for the purpose of **ranking miners by carbon efficiency**, this error is acceptable because location dominates (10-30× differences). Rankings remain correct even with significant measurement error.

## Future Evolution

The verification system will evolve over time to:

- Add real-time carbon intensity via WattTime/ElectricityMaps APIs
- Incorporate power measurement where reliably verifiable (e.g., Lium's NVML data)
- Develop PUE estimation through provider partnerships
- Weight time-of-day effects as real-time grid APIs become standard
- Respond to gaming attempts with additional verification signals

## Contributing

Contributions are welcome! Areas for improvement:

- Additional provider API integrations (Azure, other bare metal providers)
- Enhanced carbon intensity database
- Multi-signal verification (latency + IP geolocation + reputation)
- Colocation attestation protocols
- Real-time grid carbon intensity integration

## License

[Add your license here]

## References

- [Littlefoot Whitepaper](./WHITEPAPER.md)
- [Bittensor Documentation](https://docs.bittensor.com)
- [Chi Subnet Template](https://github.com/opentensor/chi)

## Contact

[Add contact information]

---

**Let's change the world by incentivizing clean AI!** 🌱⚡
