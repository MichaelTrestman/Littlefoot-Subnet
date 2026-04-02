---
title: "Subnet Littlefoot: Carbon Footprint Intelligence for Bittensor"
subtitle: "Version 0.1 — Working Draft for Discussion"
author: 
  - "[Michael Trestman](https://github.com/MichaelTrestman)"  
date: February 2026
header-includes:
  - |
    ```{=latex}
    \let\oldtableofcontents\tableofcontents
    \renewcommand{\tableofcontents}{\newpage\oldtableofcontents}
    ```
abstract: |
  AI compute is scaling rapidly, and efficiency in managing its environmental impact due to power consumption has not kept pace. Data centers obscure their energy usage, cloud providers offer unverifiable carbon estimates, and mining operations have no incentive to report their footprint. The result: AI's environmental impact is growing blindly.

  Subnet Littlefoot is designed to create a countervailing economic pressure, toward **minimizing the carbon footprint of high quality AI and other digital services**, by incentivizing power-use efficiency and transparency. This subnet acts as an incentive overlay on existing Bittensor subnets, incentivizing and subsidizing miners who verifiably operate in low-carbon-intensity grid regions and make other carboon-footprint optimizations.

  Littlefoot produces a unique digital commodity: **carbon footprint intelligence** for Bittensor subnet mining. **Carbon footprint intelligence** has two aspects, transparency and efficiency, which are directly incentivized:

  - **efficiency** in the form of verifiable choices in infrastructure deployment that improve the ultimate carbon footprint of the sourced power for the digital commodity offered by other Bittensor subnets. 
  - **transparency** in the form of verified attestations about power usage and related metrics. Miners provide location verification data and carbon intensity attestations. Validators verify these attestations against external APIs and score miners on the accuracy, completeness, and freshness of their intelligence.

  At launch, the mechanism focuses on **geographic location intelligence**, as this factor both dominates emissions (10–30$\times$ differences) and can be reliably verified via provider APIs, network latency measurements, or other independent verification methods. However, the incentive mechanism will evolve to incorporate real-time power measurement, datacenter efficiency (PUE), time-of-day grid variation, and other optimization variables that prove viable. This will resolve increasingly 
  fine-grained differences between miners and create high scope for continuous, adaptive 
  improvement, while remaining grounded in what can be most reliably verified. This project aims to create a market for increasingly sophisticated carbon footprint intelligence, driving innovation in smart, efficient, mining across Bittensor, maturing and improving the ecosystem as a whole.

---

# The Problem

## AI's Growing Energy Footprint

AI compute is driving unprecedented growth in global electricity consumption. Data centers consumed approximately **415 TWh globally in 2024** (1.5% of total global electricity), and are projected to more than **double to ~945 TWh by 2030** (3% of global electricity), equivalent to Japan's current annual consumption [^1][^2][^3]. AI-specific workloads accounted for 14-15% of data center energy in 2024 and are projected to reach 27% by 2027 [^4]. A single ChatGPT query requires approximately **10× more electricity than a standard Google search** [^5][^6], while training large language models like GPT-4 consumes tens of gigawatt-hours [^7]. In the United States alone, AI power demand is projected to exceed **50 GW by 2030** [^8], and data centers already account for over **4% of total US electricity consumption** [^9].

This rapid expansion puts the evolution of AI technology at odds with public interest, driving mistrust and resentment. In 2025, community opposition led to the cancellation of at least **25 data center projects**—a fourfold increase over 2024—with nearly **$98 billion in proposed investments blocked or delayed** between March and June alone [^10][^11]. Class action lawsuits and environmental challenges have targeted major tech companies including xAI, Microsoft, Meta, and OpenAI, over air pollution, water consumption, and energy transparency [^12][^13][^14]. Environmental justice concerns are particularly acute: data centers are disproportionately sited in non-white, working-class communities, with facilities using **300,000 gallons of water daily** and diesel backup generators emitting toxic particulate matter linked to increased asthma and heart disease rates [^15][^16]. Over **200 environmental organizations** have called for a nationwide freeze on new data center construction until environmental impacts are fully assessed [^17]. This opposition reflects a broader pattern where AI infrastructure expansion faces bipartisan local resistance, driven by rising utility costs, environmental degradation, and deep-seated mistrust of industry secrecy and development practices [^18][^19].

## The Incentive Gap

Current approaches to environmental accountability in compute are systematically inadequate, creating a market failure where ineffective methods are preferred over genuine transparency.

**Corporate ESG reports** are predominantly self-reported and unaudited, with **58% of major US corporations revising their emissions data** over the last decade—understating emissions twice as frequently as overstating [^20]. Despite **82% of organizations claiming to prioritize environmental sustainability**, only **21% have developed detailed climate transition plans with verifiable targets** [^21]. While regulations like the EU's Corporate Sustainability Reporting Directive are moving toward mandatory disclosure, enforcement remains inconsistent, and **96% of companies with climate pledges exhibit at least one red flag** such as excluding Scope 3 emissions or lacking interim targets [^22].

**Carbon offsets** face a credibility crisis. A 2024 systematic review of over 2,000 projects found that only **12% of carbon credits represent real emission reductions** [^23][^24]. Sector-specific failures are even starker: **0% of renewable energy credits** and **0.4% of cookstove credits** are effective, with benefits often overstated by **1,000%** [^24][^25]. Major fraud cases in 2024, including SEC and DOJ actions against CQC Impact Investors for schemes involving false data submission, have contributed to the voluntary carbon market shrinking **61% between 2022 and 2023** [^26][^27].

**Sustainability pledges** lack meaningful enforcement mechanisms. A study of 1,041 firms with emissions targets ending in 2020 found that **9% of targets failed and 31% "disappeared" entirely**, with no significant market reaction, environmental score changes, or media backlash—suggesting initial announcements are rewarded while failures are ignored [^28][^29]. This accountability gap persists despite growing regulatory pressure, with companies increasingly engaging in "greenhushing" (intentionally under-communicating progress) to avoid legal risks [^30].

**Green marketing** has become a major legal liability. In 2024–2025, regulators globally intensified enforcement against vague environmental claims, with the UK Competition and Markets Authority now able to impose fines of **up to 10% of annual global turnover** for deceptive marketing [^31][^32]. High-profile cases include class-action lawsuits against Procter & Gamble for "responsible forestry" claims, investigations into ASOS and Boohoo for unsubstantiated "sustainable" clothing claims, and challenges to Apple and Delta's "carbon neutral" assertions [^33][^34]. Australia issued over **AU$40 million in penalties in 2025** for dubious sustainability claims [^35].

The status quo where ineffective approaches are preferred can be seen as a ruthless but rational response to economic conditions that fail to reward transparency and responsible behavior generally. From this perspective, transparency is often seen as a liability, risking scrutiny and potential regulation. The rational choice is resistance, minimal compliance, and competition to distort the signal rather than change their behavior.


| Actor | Current Incentive | Result |
|-------|-------------------|--------|
| Data centers | Minimize costs, avoid scrutiny | Hide energy usage |
| Cloud providers | Sell compute, not accountability | Vague carbon estimates |
| Mining operations | Maximize profit | No reporting unless required |
| Hardware vendors | Sell units | Efficiency claims unverified |

# The Littlefoot Solution: Carbon Footprint Intelligence

As a distributed general incentivization engine for digital commodity production,  Bittensor has a unique ability to solve intelligence-engineering problems that corporations cannot, and the crisis of efficiency and transparency described above is a perfect example. A Bittensor subnet is perfectly positioned to act as a general incentive layer to shape the behavior of producers of digital commodities (such as storage, compute, or model inference) to make it more carbon efficient. Carbon efficiency can be measured precisely and reliably, as can the quality of data about carbon efficiency; therefore, these two qualities of optimization and transparency can be distilled into a digital commodity, which we call **carbon footprint intelligence**.

This commodity has great value, because it represents the ability of Bittensor to meet the challenges of carbon sustainability in digital services, one of the critical challenges for humanity in the 21st century, and one which corporate big tech has convincingly demonstrated its indequacy to solve.

**Carbon footprint intelligence** has two aspects, efficiency and transparency, which are directly incentivized:

  - **efficiency** in the form of choices in infrastructure deployment that improve the ultimate carbon footprint of the sourced power for the digital commodity offered by other Bittensor subnets. 
  - **transparency** in the form of publicly verifiable information about the above

Littlefoot aims to provide this commodity for existing subnets on Bittensor by acting as an emissions overlay for suitable existing subnets. Each supported primary subnet will have its own tailored mechanism, since the specifics of location verification and carbon optimization differ by subnet architecture.

Two overlay patterns can accomodate subnets, depending on where the majority of compute is performed:

1. **Miner-compute overlays** — For subnets where miners perform and control the compute (Templar, IOTA, Lium, Chutes, Hippius). Miners register on Littlefoot and their rewards depend on their primary subnet weight ($W_i$) combined with carbon efficiency.

2. **Validator-compute overlays** — For subnets where validators perform the compute (Ridges, Gradients). Validators register as Littlefoot miners and their rewards depend on their validation workload (bond count) combined with carbon efficiency.

For miner-compute overlays: miners that register on Littlefoot must be receiving emissions on one of the supported primary subnets (Lium SN51, Chutes SN64, Templar, IOTA, Hippius SN13, etc.). If a miner's primary subnet weight drops to zero ($W_i = 0$), their Littlefoot score becomes zero and they receive no Littlefoot emissions. Miners then provide additional data (or read-only infra access to this data) to Littlefoot validators, concerning the carbon footprint of the work they do for the primary subnet.

For validator-compute overlays: validators from subnets like Ridges (SN62) register as Littlefoot miners and provide attestation data about their validator infrastructure. Their Littlefoot score is based on their validation workload (number of active bonds) rather than subnet weight.

**What miners provide:**

- Carbon efficient decision-making: the most important work that miners do for Littlefoot is to reduce the carbon footprint of the work they are doing on other Bittensor subnets. A Littlefoot miner must first of all succeed as a miner on another subnet, which we can refer to as the miner's 'primary' subnet. The work that miner does for Littlefoot is to optimize their carbon footprint while succeeding on the primary subnet, in ways that are not necessarily incentivized by the primary subnet's incentive mechanism.
- Participation in attestation process: miners provide validators with the data and access (API keys) required to verify their behavior.

**What validator code does:**

- checks the integrity of miners attestation
- rate miners' carbon intelligence in a meaningful, exploit resistant way that rewards excellent, carbon-optimized performance on the primary subnet; it's critical that the littlefoot incentive mechanism not interfere with the primary subnets' IMs. it should encourage miners to optimize on the primary subnet while encouraging and subsidizing responsible decisions that nudge the carbon usage of the primary subnet in a more responsible direction; so we want to be able to influence top miners and not piss off the primary subnet owners.

## Core Incentive Mechanism

Littlefoot operates as an incentive overlay that subsidizes miners who make carbon-efficient decisions while maintaining strong performance on their primary subnets. The mechanism is designed to complement, not interfere with, primary subnet incentive mechanisms.

**Requirements for miners:**

1. **Must be active on a primary subnet** — Miners must be receiving emissions on one of the supported primary subnets (Lium SN51, Chutes SN64, Templar, IOTA, Hippius SN13, etc.). If a miner's primary subnet weight drops to zero ($W_i = 0$), they receive no Littlefoot rewards.
2. **Make carbon-efficient decisions** — The primary work miners do for Littlefoot is to additionally optimize their carbon footprint while succeeding competitively on the primary subnet.
3. **Provide verifiable intelligence** — Miners participate in the attestation process by providing data and access (API keys) required for validators to verify their carbon footprint.

The Littlefoot score for miner $i$ balances:

- Their **primary subnet performance** ($W_i$ — weight on primary subnet such as Lium SN51, Chutes SN64, Templar, IOTA, Hippius SN13, etc.) — This ensures miners maintain excellence on their primary subnet
- Their **carbon efficiency** ($C_i$ — carbon intensity of verified location) — This rewards cleaner infrastructure choices
- Their **intelligence quality** ($\sigma_i$ — verification confidence, accuracy, completeness, freshness of attestations)

The core scoring function for miner $i$ is:

$$
S_i = \frac{W_i \cdot \sigma_i}{C_i}
$$

where:

| Symbol | Term | Description |
|--------|------|-------------|
| $S_i$ | Score | Littlefoot efficiency score (higher = better) |
| $W_i$ | Subnet Weight | Performance on underlying subnet (Lium SN51, Chutes SN64, Templar, IOTA, Hippius SN13, etc.) |
| $C_i$ | Carbon Intensity | Grid emissions (gCO2/kWh) for verified location |
| $\sigma_i$ | Signal Strength | Verification confidence multiplier $\in (0, 1]$, representing the quality of carbon footprint intelligence produced (accuracy, completeness, freshness of attestations) |

The normalized weight determining emission distribution is then:

$$
\hat{W}_i = \frac{S_i}{\sum_{j=1}^{n} S_j}
$$


**How the scoring function preserves primary subnet incentives:**

The scoring function $S_i = \frac{W_i \cdot \sigma_i}{C_i}$ ensures that:

- Miners with zero primary subnet performance ($W_i = 0$) receive no Littlefoot rewards
- Miners are incentivized to maintain or improve their primary subnet performance ($W_i$) while optimizing carbon efficiency ($C_i$)
- The mechanism rewards top primary subnet performers who also make carbon-efficient choices, without disrupting primary subnet rankings

This overlay design means Littlefoot complements primary subnet incentive mechanisms rather than competing with them. The goal is to influence top miners to make carbon-efficient decisions without interfering with primary subnet operations or upsetting primary subnet owners.

**Variant for validator-compute overlays:**

For subnets where validators perform the compute (like Ridges SN62, Gradients SN56), a modified scoring function replaces $W_i$ with validator workload:

$$
S_i = \frac{B_i \cdot \sigma_i}{C_i}
$$

where $B_i$ is the number of active validator-miner bonds (a proxy for validation workload). This allows carbon optimization even on subnets where miners don't control the infrastructure. See the "Validator-Compute Subnets" section in Target Subnets for details.

At launch, we verify where miners compute and reward cleaner locations. Geography is our starting point because it satisfies two critical criteria: **high impact** (10-30× differences in carbon intensity) and **reliable verification** (provider APIs give ground truth).

But subnets are long-term projects, and Littlefoot's incentive mechanism will evolve. The verification system that validators run will adapt over time to:

- Incorporate new data sources as they become verifiable (real-time power, PUE, time-of-day grid variation)
- Resolve increasingly fine-grained differences between miners
- Respond to gaming attempts with more sophisticated verification
- Integrate emerging attestation technologies and provider APIs

Geography is one lever—likely to remain important—but not the only lever forever. The goal is to optimize the incentive mechanism continuously, always grounded in what can be reliably verified, while maintaining the overlay nature that complements rather than interferes with primary subnet operations.


## Emission Balancing Across Overlay Mechanisms

Because Littlefoot overlays multiple primary subnets, it is natural to implement **one incentive mechanism per supported primary subnet overlay** using Bittensor’s multi-mechanism capability [^36]. This introduces a subnet-level design question: **how should Littlefoot split its total emissions across mechanisms**?

### Default policy: equal split across a curated supported set

We default to an **even emission split** across the set of supported primary subnets (and therefore across their corresponding mechanisms):

$$
\text{split}_k = \frac{1}{N}
$$

where $N$ is the number of supported overlay mechanisms.

This choice is intentionally **agnostic** to token price, primary-subnet tokenomics, or estimated carbon footprint. Those signals are noisy and can create perverse incentives or governance disputes (e.g., rewarding “looking dirty,” rewarding hype, or subsidizing marginal subnets). An equal split is:

- **Hard to game** (no obvious metric to manipulate)
- **Cheap to compute and update**
- **Stable and legible** to the community (no opaque weighting)
- **Aligned with Littlefoot’s overlay role** (complement primary incentives rather than becoming a meta-tokenomics optimizer)

### The importance of curation

With emissions being split evenly across supported primary subnets, the critical decision is which primary subnets are supported. This cannot be automated because supporting a primary subnet requires subnet-specific validator code and careful, ongoing evaluation of the success of the current design against currently supported subnets (that may need to be removed if they are not working), and candidate subnets to add. Littlefoot therefore expects to maintain a **small, carefully selected, regularly pruned supported set of subnets** (e.g. $N \le 10$), reviewed periodically, adding overlays only when they are maintainable and likely to produce real carbon-efficiency improvements.

### Governance direction: decentralized and contract-based (TBD)

Since supported-set membership and mechanism configuration are high-leverage decisions, Littlefoot favors a **decentralized, contract-based governance scheme** for adding/removing supported primary subnets and managing mechanism configuration. The exact approach is not finalized, but we expect to mimic the logic of the current proposal for Bittensor’s network-level governance, at the level of a subnet governance smart-contract[^37]. 


# Carbon Footprint Intelligence: Attestation and Verification Methods

## What Miners Provide: Carbon Footprint Intelligence

Miners on Littlefoot must first be active miners on a primary subnet (Lium SN51, Chutes SN64, Templar, IOTA, Hippius SN13, etc.). Their primary work for Littlefoot is to make carbon-efficient decisions while maintaining performance on their primary subnet. This carbon footprint intelligence is delivered through verified attestations that include:

1. **Location claim** — Where the miner claims to operate (region, datacenter, coordinates)
2. **Verification method** — How the location can be verified (provider API, colocation proof, etc.)
3. **Verification credentials** — Access needed to verify (API keys, service accounts, proofs)
4. **Carbon intensity claim** — Claimed carbon intensity for the location (gCO2/kWh)
5. **Timestamp** — When the attestation was created
6. **Supporting evidence** — Any additional data supporting the claim

**Intelligence format (example attestation):**
```json
{
  "location": "us-west-1",
  "provider": "latitude",
  "server_id": "server_123",
  "api_key": "lat_...",
  "carbon_intensity_claim": 250,
  "timestamp": 1704067200,
  "evidence": {
    "provider_api": true,
    "rtt_measurements": true,
    "supporting_docs": []
  }
}
```

## How Validators Verify Carbon Intelligence

Validators verify carbon footprint intelligence by computing a signal aggregation function over evidence from a variety of sources. The responsibilities of validator code will include:

1. **Querying provider APIs** — Use miner-provided credentials to verify location claims
2. **Cross-referencing carbon data** — Look up carbon intensity from external APIs (Electricity Maps, WattTime)
3. **Scoring intelligence quality** — Evaluate accuracy, completeness, and freshness of carbon footprint intelligence
4. **Combining evidence signals** — Combine independent signals into a single verification confidence score

  

Verification is a multi-signal inference problem: different pieces of evidence have different strengths, can conflict, and can be combined.

Littlefoot’s approach is to treat verification as an **evidence aggregation** problem and compute a **verification confidence** `sigma_i` in `[0, 1]` for miner `i`. Concretely, `sigma_i` is a posterior probability:

$$
\sigma_i \;=\; P(H_i \mid \text{evidence})
$$

```text
sigma_i = P(H_i | evidence)
```

Here \(H_i\) is the hypothesis that miner i has truthfully reported their data during the previous tempo (*not* a percentage of the time they were telling the truth).


So \(\sigma_i\) is the validator’s **confidence that the miner is telling the truth about the relevant claim**, given the evidence observed so far.

This framing matches Littlefoot’s philosophy: **reward miners for producing *new, decision-relevant information*** about their footprint.





### Skeptical prior (default: assume the claim is false)

At launch, validators should start from a deliberately skeptical prior \(P(H_i)\) (i.e., assume the claim is more likely wrong than right *until* evidence accumulates). This is not “anti-miner”; it is pro-information:

- It prevents the subnet from overpaying for **unverified claims**.
- It ensures miners only earn the full benefit of a low-carbon location when they produce **verifiable evidence**.
- It avoids rewarding *unnecessary* evidence: once \(\sigma_i\) is already near 1, additional redundant signals have little effect (diminishing returns).

### Evidence updates (Bayesian-flavored log-odds)

Validators update the prior with evidence signals \(e_1, e_2, \dots, e_K\). In a full Bayesian system, each signal contributes a likelihood ratio. For an MVP that is easy to implement and hard to game, we can use a calibrated **log-odds accumulator**:

$$
\text{logit}(\sigma_i) = b + \sum_{k=1}^{K} w_k \, s_{i,k}
$$

Pseudocode:

```text
logit_sigma_i = b + sum_{k=1..K} (w_k * s_i_k)
sigma_i = sigmoid(logit_sigma_i)
```

where:

- `b` encodes a skeptical prior (negative by default)
- `s_{i,k}` is the signed evidence score for signal `k`, constrained to `[-1, +1]` (supports `H_i` vs contradicts it)
- `w_k >= 0` is a weight reflecting how spoof-resistant and reliable the signal is
- `sigma_i = sigmoid(logit_sigma_i)` (squashes log-odds back into \([0, 1]\))

Interpretation:

- **Valence** (confirming vs disconfirming evidence) is the *sign* of \(s_{i,k}\).
- **Quantity / accumulation** is the sum over multiple signals and over time.
- **Strength / trustworthiness** is controlled by \(w_k\): hard-to-spoof signals move \(\sigma_i\) more per unit score than easy-to-spoof ones.

This is “Bayesian flavored” in the sense that independent evidence adds in log-odds space, but it avoids pretending we know exact likelihoods on day one.

### Evidence signals (examples)

Validators can incorporate any subset of signals; the key is that **multiple weaker signals can add up**, and a strong contradictory signal can sharply reduce confidence.

- **Provider API attestation (strong, spoof-resistant)**: cloud/bare-metal provider confirms region/metro for an instance/server ID.
- **Network RTT/latency triangulation (medium)**: multi-vantage RTT constraints that are consistent with the claimed geography over time.
- **IP/geolocation signals (weak-to-medium)**: IP geo DBs and ASN info (useful but not sufficient alone).
- **Colocation / facility documentation (medium)**: invoices, LOA, cage contracts, remote-hands confirmations, or other facility artifacts (format standardized over time).
- **Consistency over time (medium)**: location signals stable across epochs; sudden jumps reduce confidence.
- **Power/utilization evidence (future)**: verifiable telemetry or metered feeds where available; initially treated as supporting evidence rather than a requirement.

### Safety override (disqualifying evidence / “hard fail”)

For security and economic safety, validators may define *disqualifying evidence* events \(D_i\) that indicate a likely **direct mismatch** between the claim and reality (e.g., a strong provider attestation that contradicts the claimed region, or a sufficiently consistent set of independent weaker contradictions). In that case, the design intent is simple: **no emissions credit for that epoch**, regardless of claimed performance.

One clean way to express this is as an explicit veto on top of the soft accumulator:

$$
\tilde{\sigma}_i = \text{sigmoid}\!\left(b + \sum_{k=1}^{K} w_k \, s_{i,k}\right), \quad
\sigma_i =
\begin{cases}
0 & \text{if } D_i \\
\tilde{\sigma}_i & \text{otherwise}
\end{cases}
$$

This preserves the continuous “evidence adds up” behavior for ordinary cases, while making the anti-gaming intent clear when a decisive contradiction is detected.

### Operational rule

Validators compute \(\sigma_i\) from available signals each epoch. Rewards should depend on \(\sigma_i\) continuously.

Critically, this creates the right “information economics”:

- **If the miner provides no new evidence**, \(\sigma_i\) stays low (close to the skeptical prior), so Littlefoot does not subsidize unverified claims.
- **If the miner provides high-quality, hard-to-spoof evidence**, \(\sigma_i\) rises sharply, so the miner captures the benefit of clean location choices.
- **If the miner provides redundant evidence**, \(\sigma_i\) saturates and incremental reward from extra paperwork is minimal (diminishing returns).

If needed for safety, Littlefoot can impose a minimum confidence threshold, below which emissions are dropped to zero (in addition to any hard-fail disqualifying rules above).

## Intelligence Quality Scoring

Validators score carbon footprint intelligence on multiple dimensions:

1. **Accuracy** — Does the claimed location match verified location? Is the carbon intensity data correct?
2. **Completeness** — Did the miner provide *enough* of the attestation schema for this epoch (i.e., do we have coverage of the required evidence fields/categories), or are there gaps that materially limit verification?
3. **Freshness** — How recent is the intelligence? (Stale data gets penalized)
4. **Verification confidence** — How strongly does the combined evidence support the claim? (\(\sigma_i\))

The intelligence quality score $Q_i$ combines these factors:

$$
Q_i = \text{accuracy} \times \text{completeness} \times \text{freshness} \times \sigma_i
$$

Where \(\sigma_i\) is the aggregated verification confidence derived from evidence signals.

Importantly, “completeness” is **protocol-defined**, not hand-wavy: each target subnet (or each Littlefoot deployment/version) specifies an **attestation schema** (fields and evidence categories) and which items are *required* vs *optional*. Validators then compute completeness as a normalized coverage score, e.g.:

$$
\text{completeness}_i
=
\frac{\sum_{k \in \mathcal{R}} a_k \cdot \mathbf{1}[\text{item }k\text{ is present + parseable this epoch}]}{\sum_{k \in \mathcal{R}} a_k}
\in [0,1]
$$

where \(\mathcal{R}\) is the set of required items/categories and \(a_k\) are importance weights. This makes “enough information” explicit and upgradeable over time (as schemas harden and stronger evidence types become available).

Note: a more Bayesian treatment is to model **missingness as informative** (strategic withholding). Operationally, this can be implemented by adding explicit “missing/withheld required item” negative evidence signals into the \(\sigma_i\) accumulator, rather than treating missing items as neutral.

**Key principle:** Miners must be active on a primary subnet and provide carbon footprint intelligence to earn rewards. The primary work is making carbon-efficient decisions while succeeding on the primary subnet. Attestations enable validators to verify this work.


## Economic Analysis

What makes a subnet a good candidate for Littlefoot? From an economic perspective, it must be the case that a relatively small incentive (in terms of Littlefoot emissions) can have a relatively large effect on the carbon footprint.

The data suggests that more carbon-intensive compute is not always more expensive, but is often chosen for other reasons, including low latency and simple availability of options.

Clean grids are often cheap because hydro, geothermal, and nuclear have zero fuel costs. Cold climates (Iceland, Quebec, Norway) also have lower cooling costs. However, cleaner grids tend to have fewer datacenter options, since they usually correspond to tighter regulations, making it more difficult or expensive to run a data center. Remote locations also add network delay, which is a problem for latency-sensitive workloads.

An important practical constraint is that Littlefoot miners do not choose from “anywhere on Earth.” They choose from the set of locations that are feasible given:

- the **primary subnet’s architecture** and latency tolerance
- whatever **infrastructure mode** the miner uses (colocation, owned bare metal, bare metal providers, cloud VMs, marketplaces)
- the miner’s operational constraints (capacity availability, on-demand pricing, ability to manage hardware remotely)

This means that, in practice, the feasible location set can be much more limited than the global variation in grid carbon intensity would suggest. Even if Iceland/Quebec/Norway are extremely low-carbon, the relevant question for a given subnet is often: *is comparable GPU capacity actually available there, at acceptable latency and operational friction?*

To ground this, we can treat each infrastructure pathway as supplying a “menu” of viable locations. For example:

- **AWS** provides a fixed set of regions for any given instance class (and not all instance types are offered in all regions).
- **Bare-metal marketplaces** like Latitude.sh provide an explicit list of metro locations where servers can be provisioned.
- **Colocation and owned hardware** can access a broader set of metros, but are constrained by what facilities can practically host and support the required hardware, networking, and maintenance model.

Littlefoot’s near-term carbon leverage therefore depends heavily on **availability constraints**: what locations are actually accessible to miners participating in each target subnet, and how those options change over time.

Colocation and owned hardware are a major part of how real Bittensor mining happens. They are also often the most direct path to meaningful carbon optimization, because miners can choose facilities with cleaner grids, better power contracts, and better thermals.

The trade-offs include **verification and operational heterogeneity**:

- **More operational variance**: procurement, remote hands, longer lead times, and heterogeneous facility capabilities.
- **More intensive/uncertain verification work**: you may not have a single corporate API that attests location/power, so validators need a stronger attestation + cross-check process.

Littlefoot is explicitly designed to support miners who want to get creative about how they are sourcing comopute. Provider APIs are *one* convenient verification tool (especially at launch), but their use should not be incentivized. The point is to create a market for **carbon footprint intelligence** across *whatever infrastructure miners actually use*, using the best available verification methods:

- **Facility/location attestations** (including colocation facility documentation where available)
- **Multi-signal checks** (network latency/RTT triangulation, IP signals, consistency over time)
- **Power and utilization evidence** as it becomes verifiable (e.g. power telemetry, metered feeds, audited statements, or other mechanisms the ecosystem standardizes on)

### What information is most valuable next

To make this “provider menu” concrete (and keep it current), the most valuable incremental data to collect and publish is:

- **Feasible location menus by pathway**: i.e. where miners actually are and therefore where other miners could be, in terms of cloud regions, bare-metal marketplace metros, and colo/owned-hardware.
- **Inventory / capacity constraints** (where obtainable): whether relevant GPU classes are actually in stock in those locations.
- **Repeatable pricing snapshots**: \$/hour for standardized “anchor” instances per region (CPU + GPU) *and/or* comparable bare-metal offerings, to understand cost trade-offs alongside carbon.
- **Region→grid mapping**: provider region/metro → grid carbon-intensity proxy (country/state/subregion), plus the underlying data source.
- **Standardized attestation schemas for colo/BYO**: what a miner must provide so validators can verify location and (eventually) power and PUE without relying on a single vendor API.

We can fetch and regenerate parts of this automatically (provider region menus + pricing + carbon-intensity lookup) to avoid stale, hand-entered numbers.

The table below is an **illustrative “provider menu” snapshot**. Carbon intensity is a grid proxy from Ember (gCO2/kWh) [^38]. AWS prices are on-demand \$/hour for an anchor GPU instance type (p4d.24xlarge) from AWS’s public price catalog [^43]. Latitude metros are from Latitude’s published locations list [^44] (pricing not included yet).

| Pathway | Provider | Region / metro | Anchor compute | Offered | \$/hour | Grid area proxy | Grid CO2 intensity (gCO2/kWh) |
|---------|----------|----------------|----------------|---------|--------|-----------------|----------------------------------|
| Cloud VM | AWS | us-east-1 | p4d.24xlarge | Yes | 21.96 | United States of America | 383.8 |
| Cloud VM | AWS | eu-north-1 | p4d.24xlarge | Yes | 23.72 | Sweden | 35.33 |
| Cloud VM | AWS | ap-southeast-1 | p4d.24xlarge | Yes | 26.35 | Singapore | 498.7 |
| Cloud VM | AWS | ca-central-1 | p4d.24xlarge | Yes | 25.25 | Canada | 185.3 |
| Bare metal marketplace | Latitude | Frankfurt | — | Yes | — | Germany | 331.6 |
| Bare metal marketplace | Latitude | Amsterdam | — | Yes | — | Netherlands | 253.2 |
| Bare metal marketplace | Latitude | London | — | Yes | — | United Kingdom | 217.1 |
| Bare metal marketplace | Latitude | São Paulo | — | Yes | — | Brazil | 106.1 |
| Bare metal marketplace | Latitude | Tokyo 3 | — | Yes | — | Japan | 483.4 |
| Bare metal marketplace | Latitude | Sydney | — | Yes | — | Australia | 553.8 |

Littlefoot targets subnets with high energy usage and latency-tolerant workloads, where location-based carbon efficiency incentives can have maximum impact. Two overlay patterns enable broad applicability: **miner-compute overlays** (where miners control infrastructure) and **validator-compute overlays** (where validators perform the work). Our research has identified several primary targets across different compute categories.

# Candidate Subnets

This section discusses a number of subnets that are good potential candidates to be 'primary subnets' for Littlefoot mining.


## Training Subnets — Highest Energy Impact

### Templar

Templar is a decentralized training framework that enables large-scale model training across heterogeneous compute resources. Miners train models on assigned data subsets, compute gradients, compress them, and share with peers.

**Why Templar is ideal:**
- **Extremely high energy usage** — Model training is the most power-intensive AI workload (10-100× more than inference)
- **Latency-tolerant** — Training is batch process, not real-time. Gradient sharing can tolerate network delays
- **Distributed compute** — Miners run training on their infrastructure, location is verifiable
- **High value target** — Training is where most AI carbon footprint comes from
- **Infrastructure-based** — Miners provide compute infrastructure, aligns with location verification

### IOTA (SN120)

IOTA is a framework for pretraining large language models using pipeline-parallel architecture. The orchestrator distributes model layers across heterogeneous miners and streams activations between them.

**Why IOTA is ideal:**
- **Extremely high energy usage** — LLM pretraining is one of the most power-intensive AI workloads
- **Latency-tolerant** — Pipeline-parallel training is batch process, activations can tolerate network delays
- **Orchestrator pattern** — Central coordination means location verification can be integrated
- **Infrastructure-based** — Miners provide training infrastructure, location is verifiable

**Strategic Insight:** Training subnets (Templar, IOTA) represent the highest per-task energy usage (10-100× inference). If Littlefoot can incentivize clean-grid training infrastructure, the carbon impact would be massive.

## Inference/Compute Subnets — High Volume

### Lium (SN51)

Lium is a GPU rental marketplace where miners contribute machines and renters SSH in to run compute jobs.

**Why Lium is ideal:**
- **SSH-based access** — Latency-tolerant (users SSH in, not real-time API)
- **High energy usage** — GPU rental is power-intensive
- **Hardware verification** — Validators already verify GPU specs and performance
- **Direct machine access** — Could verify location via provider APIs (Latitude.sh, AWS, etc.)
- **Power data available** — NVML data already collected, enabling future power measurement

### Chutes (SN64)

Chutes is a serverless AI inference platform where miners serve model inference requests.

**Why Chutes is suitable:**
- **High energy usage** — GPU compute is power-intensive, carbon impact is significant
- **Hardware verification** — GraVal already verifies GPU authenticity, could extend to location
- **Miners use Latitude.sh** — Documented in their README, enabling location verification
- **API-based** — Miners expose endpoints, validators query them (good for overlay)
- **Latency concerns** — Serverless inference APIs need low latency (50-200ms added from clean grids could be deal-breaker for real-time workloads, but may work for batch/async workloads)

**Note:** Chutes' real-time inference requirements suggest latency sensitivity. Littlefoot may work better for batch/async workloads than real-time inference.

## Infrastructure Subnets — Compute/GPU Resources

### Hippius (SN13)

Hippius is a decentralized infrastructure subnet providing storage, compute, and GPU resources. The subnet supports multiple node types: StorageMiner, ComputeMiner, GpuMiner, StorageS3, and Validator.

**Why Hippius is suitable:**
- **Node type filtering confirmed** — RPC method `get_active_nodes_metrics_by_type(NodeType)` allows filtering by node type
- **Geolocation available** — `NodeMetricsData` includes `geolocation: Vec<u8>` field, available via RPC
- **High energy usage** — Compute and GPU miners are power-intensive
- **Latency-tolerant** — VM-based compute is generally latency-tolerant (not real-time inference)
- **Selective targeting** — Can target ComputeMiner and GpuMiner only, excluding low-energy StorageMiner nodes
- **Established subnet** — SN13, part of core Bittensor infrastructure

**Important Note:** Hippius geolocation is **self-reported** by miners' offchain workers (calls `ip-api.hippius.network` API). Validators do not independently verify this location within Hippius. Littlefoot verifies location independently using the same methods as other subnets: provider APIs (Latitude.sh, AWS, GCP) for cloud/bare metal providers, network latency/RTT triangulation (works for all miners), and other independent verification methods. The advantage of Hippius is node type filtering (can target ComputeMiner/GpuMiner), not geolocation reliability.

**Implementation:** Littlefoot can query `get_active_nodes_metrics_by_type(NodeType::ComputeMiner)` and `get_active_nodes_metrics_by_type(NodeType::GpuMiner)` to filter by node type. Location verification uses independent methods: provider APIs when available, network latency measurements from multiple validator locations, and multi-signal verification. Hippius's self-reported geolocation is used as a hint only.

## Validator-Compute Subnets — A Different Overlay Pattern

The mechanisms described above work for subnets where **miners control and perform the compute**. However, there is a second category of subnets where **validators perform the compute work**: code-submission subnets like Ridges (SN62) and Gradients (SN56), where miners submit code or outputs and validators execute/evaluate them.

For these subnets, Littlefoot can still create value by incentivizing validator carbon efficiency through a modified overlay mechanism.

### Ridges (SN62) — Validator-Compute Overlay

Ridges is a software agent competition where miners submit code and validators execute it to evaluate performance.

**Why the standard mechanism doesn't work:**
- Miners don't perform compute—they write and submit code
- Validators run the submitted code, creating the carbon footprint
- Validators control their own infrastructure and location

**Modified overlay approach:**
- **Ridges validators register as Littlefoot miners** (separate registration, same entities)
- Instead of using primary subnet miner weights ($W_i$), use **validator workload** as the performance metric
- Workload is measured by **number of validator-miner bonds**, which represents how many miners that validator is actively validating

**Modified scoring function:**

$$
S_i = \frac{B_i \cdot \sigma_i}{C_i}
$$

where:

|| Symbol | Term | Description |
|--------|------|-------------|
|| $S_i$ | Score | Littlefoot efficiency score for validator $i$ |
|| $B_i$ | Bond Count | Number of active validator-miner bonds (workload proxy) |
|| $C_i$ | Carbon Intensity | Grid emissions (gCO₂/kWh) for verified location |
|| $\sigma_i$ | Signal Strength | Verification confidence (attestation quality) |

**Why this works:**
- Validators doing more work (more bonds) receive more Littlefoot rewards
- But only if they operate efficiently (low carbon intensity)
- Carbon optimization doesn't affect validation correctness—running the same code in Iceland vs Poland produces identical results
- Directly addresses the validator redundancy problem (2-10 validators reproducing compute)

**Implementation:**
```python
# Littlefoot validators query Ridges metagraph
ridges_metagraph = get_metagraph(netuid=62)
bonds_i = torch.sum(ridges_metagraph.bonds[validator_uid] > 0)  # Count active bonds
carbon_intensity_i = verify_location_and_get_carbon_intensity(validator_i)
verification_quality_i = score_attestation_quality(validator_i)

littlefoot_score_i = (bonds_i * verification_quality_i) / carbon_intensity_i
```

**Key differences from miner-compute overlays:**
- Participants register as Littlefoot miners, not overlay their existing role
- Uses bond count instead of subnet weight as workload metric
- Targets validator infrastructure optimization rather than miner optimization
- Addresses inherent carbon inefficiency of validator redundancy patterns

**Other validator-compute candidates:**
- **Gradients (SN56)** — Similar code-submission pattern
- Any subnet where validators perform the majority of compute work

This validator-compute overlay pattern significantly expands Littlefoot's applicability beyond miner-compute subnets, enabling carbon optimization even in architectures where miners don't control the infrastructure.

## Future Targets

- **TAOHash (SN14)**: Bitcoin mining subnet. Higher integration effort due to ASIC verification challenges.
- **Other compute subnets**: Any subnet with miners in physical locations can be overlaid, provided miners are active on those subnets and workloads are latency-tolerant.


# Limitations at Launch

## What We Don't Measure (MVP)

- **PUE (Power Usage Effectiveness)**: We don't know datacenter overhead
- **Embodied carbon**: Manufacturing emissions are ignored
- **Real-time grid variation**: We use averages, not marginal emissions
- **Cooling efficiency**: Climate effects beyond location averages
- **Transmission losses**: Grid delivery losses ignored

## What This Means At Launch

Our initial carbon numbers are not precise. We estimate 30-60% error on actual emissions accounting.

However, for the purpose of **ranking miners by carbon efficiency**, this error is acceptable at launch because location dominates. We are not claiming to provide auditable carbon accounting—but we are providing a verifiable incentive for cleaner compute, which would be the best carbon footprint intelligence available, and far ahead of what is currently available..

## The Path Forward

These limitations are not permanent. As the subnet matures, carbon footprint intelligence requirements will evolve:

- **Real-time carbon intensity intelligence** — Miners provide real-time data from WattTime/ElectricityMaps APIs
- **Power measurement intelligence** — Where verifiable (e.g., Lium's NVML data, Hippius node metrics), miners provide intelligence about actual power consumption
- **PUE intelligence** — Miners provide datacenter efficiency intelligence as it becomes verifiable
- **Time-of-day variation intelligence** — Miners provide intelligence about grid carbon intensity at different times
- **Multi-factor intelligence** — Combine location, power, PUE, and time-of-day for comprehensive carbon footprint intelligence

The intelligence system evolves. What matters is that at each stage, the mechanism is grounded in **what can be reliably verified** and **what creates the right incentives**. Miners compete on the quality and sophistication of their carbon footprint intelligence, driving innovation in environmental transparency and optimization.


# Conclusion

Littlefoot produces a unique digital commodity: **carbon footprint intelligence** for compute infrastructure. This creates a market for environmental intelligence, rewarding miners who provide high-quality, verifiable carbon footprint intelligence while maintaining strong performance on primary compute subnets.

The approach is pragmatic and evolutionary:

1. **Two overlay patterns**: Miner-compute overlays (for subnets where miners control infrastructure) and validator-compute overlays (for code-submission subnets where validators perform the work)
2. **Start with the biggest verifiable lever**: Geographic location creates 10-30× differences and can be verified via provider APIs, network latency measurements, and other independent verification methods
3. **Target high-impact subnets**: Training subnets (Templar, IOTA) with highest per-task energy usage; inference/compute subnets (Lium, Chutes) with high volume; infrastructure subnets (Hippius) with selective targeting; and validator-compute subnets (Ridges, Gradients) that address validator redundancy inefficiency
4. **Produce a measurable commodity**: Carbon footprint intelligence that can be scored on accuracy, completeness, and freshness
5. **Ground incentives in epistemology**: Only reward what can be reliably verified; evolve intelligence requirements as capabilities improve
6. **Create market pressure for transparency**: Clean grids get more rewards, forcing the supply chain to compete on verifiability
7. **Let economics and verification compound**: Small incentives tip decisions; better verification enables finer distinctions

The goal is not to solve AI sustainability in one step. The goal is to create a financial mechanism that produces high-quality carbon footprint intelligence—one that evolves over time as verification technology improves and as we learn what works.

**What participants do on Littlefoot:**
- **Miner-compute overlays**: Active miners on primary subnets (Lium SN51, Chutes SN64, Templar, IOTA, Hippius SN13) register on Littlefoot and optimize carbon efficiency while maintaining primary subnet performance
- **Validator-compute overlays**: Validators from code-submission subnets (Ridges SN62, Gradients SN56) register as Littlefoot miners and optimize the carbon efficiency of their validation infrastructure
- All participants provide carbon footprint intelligence (location, verification methods, supporting data) through attestations
- Maintain intelligence quality (accuracy, completeness, freshness)
- Compete on carbon efficiency while succeeding on their primary subnet role

**What validators verify:**
- Intelligence accuracy against provider APIs and external carbon databases
- Intelligence completeness and freshness
- Verification confidence level (\(\sigma_i\)) derived from aggregated evidence signals
- Actionability of optimization insights

**The commodity value:**
High-quality carbon footprint intelligence enables better decision-making across the Bittensor network. This intelligence creates market pressure for cleaner compute and rewards miners who operate in low-carbon regions, while providing actionable data for optimizing carbon footprints across the ecosystem.

**The overlay design:**
Littlefoot operates as an incentive overlay that complements primary subnet mechanisms through two patterns: miner-compute overlays (using subnet weight $W_i$) and validator-compute overlays (using bond count $B_i$). Both patterns reward carbon efficiency while preserving primary subnet incentives—miners/validators must maintain strong primary subnet performance to benefit from carbon optimization. This design ensures primary subnet owners see Littlefoot as a complement that improves the ecosystem's carbon footprint without disrupting their incentive mechanisms.

**Staking as an Unfakeable Signal of Environmental Responsibility:**

Beyond its role in incentivizing carbon-efficient compute, Littlefoot stake represents a unique economic signal: an **unfakeable commitment to carbon intelligence and environmental responsibility**. Unlike traditional corporate sustainability approaches, staking in the Littlefoot subnet creates a verifiable, on-chain signal that cannot be gamed or greenwashed.

**The Problem with Traditional Sustainability Signals:**

Corporate sustainability pledges, carbon offsets, and ESG reporting suffer from fundamental credibility problems. These approaches are vulnerable to gaming because they rely on self-reporting, third-party verification that can be compromised, or financial transactions that can be reversed or disputed.

- **Sustainability pledges** can be abandoned without consequence—31% of corporate emissions targets simply "disappear" with no market reaction [^28][^29]
- **Carbon offsets** face a credibility crisis, with only 12% representing real emission reductions [^23][^24]
- **ESG reporting** is predominantly self-reported and unaudited, with 58% of major US corporations revising their emissions data [^20]
- **Green marketing** has become a legal liability, with regulators imposing fines up to 10% of annual global turnover for deceptive claims [^31][^32]

**Staking as a Superior Signal:**

Staking in Littlefoot creates an unfakeable signal because:
1. **On-chain verifiability**: Stake is publicly visible on the blockchain, cannot be hidden or misrepresented
2. **Economic commitment**: Staking requires capital at risk, creating a credible signal of conviction
3. **Alignment with outcomes**: Stake value is directly tied to the success of carbon intelligence production—stakers benefit when miners produce high-quality, verifiable carbon footprint intelligence
4. **No greenwashing possible**: The mechanism itself produces verifiable carbon intelligence; staking supports a system that creates real, measurable environmental impact
5. **Long-term alignment**: Staking creates long-term economic alignment with carbon efficiency, unlike one-time offset purchases or temporary pledges

This creates a new category of environmental commitment: **proof-of-stake environmental responsibility**, where economic commitment to carbon intelligence is verifiable, unfakeable, and directly tied to measurable environmental outcomes. For companies seeking to demonstrate genuine environmental responsibility beyond greenwashing, Littlefoot stake represents a credible, on-chain alternative to the broken systems of carbon offsets and sustainability pledges.

Subnets are long-term projects. Littlefoot's intelligence requirements will grow to incorporate new data sources, respond to gaming attempts, and resolve more fine-grained efficiency differences between miners. What will remains constant is the commitment to **verifiable, exploit-resistant incentives** that produce a real commodity: carbon footprint intelligence, while maintaining the overlay design that complements rather than competes with primary subnet operations.

---

# References

[^1]: IEA. "Energy and AI" (2025). https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai

[^2]: Goldman Sachs. "AI to drive 165% increase in data center power demand by 2030" (2025). https://www.goldmansachs.com/insights/articles/ai-to-drive-165-increase-in-data-center-power-demand-by-2030

[^3]: Nature. "Data centres will use twice as much energy by 2030 — driven by AI" (2025). https://www.nature.com/articles/d41586-025-01113-z

[^4]: Goldman Sachs Research (2025). https://www.goldmansachs.com/insights/articles/ai-to-drive-165-increase-in-data-center-power-demand-by-2030

[^5]: UNRIC. "Artificial intelligence: How much energy does AI use?" https://unric.org/en/artificial-intelligence-how-much-energy-does-ai-use/

[^6]: Epoch AI. "How much energy does ChatGPT use?" https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use

[^7]: MIT News. "Explained: Generative AI's environmental impact" (2025). https://news.mit.edu/2025/explained-generative-ai-environmental-impact-0117

[^8]: S&P Global. "Artificial intelligence power demand in US could top 50 GW by 2030" (2025). https://www.spglobal.com/energy/en/news-research/latest-news/electric-power/081325-artificial-intelligence-power-demand-in-us-could-top-50-gw-by-2030-epri

[^9]: LBNL. "2024 United States Data Center Energy Usage Report". https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report_1.pdf

[^10]: Heatmap. "Local Pushback, Canceled Data Centers Surged in 2025". https://heatmap.news/politics/data-center-cancellations-2025

[^11]: The Verge. "Communities are rising up against data centers — and winning" (2025). https://www.theverge.com/science/841169/ai-data-center-opposition

[^12]: Southern Environmental Law Center. "Elon Musk's xAI threatened with lawsuit over air pollution from Memphis data center" (2025). https://www.selc.org/press-release/elon-musks-xai-threatened-with-lawsuit-over-air-pollution-from-memphis-data-center/

[^13]: Milwaukee Journal Sentinel. "Suit filed to learn Lake Michigan water use at Microsoft data center" (2025). https://www.jsonline.com/story/news/local/2025/09/15/suit-filed-to-learn-lake-michigan-water-use-at-microsoft-data-center/86161113007/

[^14]: Daily Reporter. "Lawsuit seeks release of Meta data center energy records" (2025). https://dailyreporter.com/2025/12/11/lawsuit-seeks-release-of-meta-data-center-energy-records/

[^15]: Center for Biological Diversity. "Lawsuit Pushes California City to Reevaluate Data Center's Environmental Harms" (2024). https://biologicaldiversity.org/w/news/press-releases/lawsuit-pushes-california-city-to-reevaluate-data-centers-environmental-harms-2024-12-02/

[^16]: Kapor Foundation. "The Unequal Burden of Data Centers". https://kaporfoundation.org/datacenters-envt-health/

[^17]: Inside Climate News. "Environmental Groups Demand a Nationwide Freeze on Data Center Construction" (2025). https://insideclimatenews.org/news/08122025/environmental-groups-demand-data-center-construction-freeze/

[^18]: Inside Climate News. "A New Unifying Issue: Just About Everyone Hates Data Centers" (2025). https://insideclimatenews.org/news/13112025/inside-clean-energy-just-about-everyone-hates-data-centers/

[^19]: Capital B. "After a White Town Rejected a Data Center, Developers Targeted a Black Area". https://capitalbnews.org/data-center-south-carolina-black-community/

[^20]: Nature Climate Change. "Widespread revisions of self-reported emissions by major US corporations" (2025). https://www.nature.com/articles/s41558-025-02494-9

[^21]: Edie. "Greenwashing concerns rise sharply as brands fail to credibly demonstrate progress" (2024). https://www.edie.net/greenwashing-concerns-rise-sharply-as-brands-fail-to-credibly-demonstrate-progress/

[^22]: Research Square. "Red Flags in Green Promises: A Framework for Identifying Greenwashing Risk in Corporate Climate Pledges" (2024). https://assets-eu.researchsquare.com/files/rs-6802349/v2_covered_cd45303e-a609-4fa4-87f9-4001305af12a.pdf

[^23]: Nature Communications. "Systematic assessment of the achieved emission reductions of carbon crediting projects" (2024). https://www.nature.com/articles/s41467-024-53645-z

[^24]: ETH Zurich. "Systematic review of the actual emissions reductions of carbon offset projects across all major sectors" (2024). https://www.research-collection.ethz.ch/handle/20.500.11850/620307

[^25]: Bloomberg. "Carbon Credits Found to Be Mostly 'Ineffective' in Key Study" (2024). https://www.bloomberg.com/news/articles/2024-07-30/carbon-credits-found-to-be-mostly-ineffective-in-key-study

[^26]: Jones Day. "Recent Fraud Cases Show Companies Must Be Strategic When Purchasing Carbon Offsets" (2024). https://www.jonesday.com/en/insights/2024/12/recent-fraud-cases-show-companies-must-be-strategic-when-purchasing-carbon-offsets

[^27]: Nature Communications. "Demand for low-quality offsets by major companies undermines climate integrity of the voluntary carbon market" (2024). https://www.nature.com/articles/s41467-024-51151-w

[^28]: Nature Climate Change. "Limited accountability and awareness of corporate emissions target outcomes" (2024). https://www.nature.com/articles/s41558-024-02236-3

[^29]: Nature Climate Change. "Empty promises for emissions targets" (2024). https://www.nature.com/articles/s41558-024-02239-0

[^30]: Socialsuite. "The End of Greenwashing? 2025's Pivotal ESG Shift" (2025). https://www.socialsuitehq.com/articles/the-end-of-greenwashing-why-2025-is-a-pivotal-year-for-esg-accountability

[^31]: Provenance. "Retailer Greenwashing Examples 2025 - Major Cases and Key Lessons" (2025). https://www.provenance.org/news-insights/greenwashing-examples-2025-major-cases-and-key-lessons-for-retailers

[^32]: Baker McKenzie. "Green Claims Guide" (2025). https://www.bakermckenzie.com/-/media/files/insight/guides/2025/green-claims-guide.pdf

[^33]: Eco-Business. "20 brands called out for greenwashing in 2025" (2025). https://www.eco-business.com/news/20-brands-called-out-for-greenwashing-in-2025/

[^34]: The Sustainable Agency. "Greenwashing Examples for 2025 & 2026" (2025). https://thesustainableagency.com/blog/greenwashing-examples/

[^35]: Eco-Business. "20 brands called out for greenwashing in 2025" (2025). https://www.eco-business.com/news/20-brands-called-out-for-greenwashing-in-2025/

[^36]: Bittensor docs. "Multiple Incentive Mechanisms Within Subnets" (last edit Oct 2025). https://docs.learnbittensor.org/subnets/understanding-multiple-mech-subnets

[^37]: Bittensor developer docs. "Roadmap — Decentralized governance" (governance transition notes). https://governance-transition-notes.developer-docs-6uq.pages.dev/learn/roadmap#decentralized-governance

[^38]: Ember. "Yearly Electricity Data" (includes country-year `CO2 intensity` in gCO2/kWh; downloadable CSV). https://ember-energy.org/data/yearly-electricity-data

[^39]: U.S. Energy Information Administration (EIA). "Virginia Electricity Profile 2024" (Table 1: Carbon Dioxide (lbs/MWh)). https://www.eia.gov/electricity/state/virginia/

[^40]: U.S. Energy Information Administration (EIA). "Electricity Data Browser" (retail electricity price series by state and sector). https://www.eia.gov/electricity/data/browser/

[^41]: Eurostat (as republished by Trading Economics). "Germany - Electricity prices: Non-household, medium size consumers" (Dec 2024). https://tradingeconomics.com/germany/electricity-prices-non-household-medium-size-consumers-eurostat-data.html

[^42]: Hydro‑Québec. "Comparison of electricity prices" (rates in effect April 1, 2024; average prices excluding taxes; CAD). https://www.hydroquebec.com/business/customer-space/rates/comparison-electricity-prices.html

[^43]: AWS. Amazon EC2 on-demand pricing (public offer files; region index and per-region catalogs). https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/region_index.json

[^44]: Latitude.sh. "Locations" (published metro list). https://www.latitude.sh/locations

