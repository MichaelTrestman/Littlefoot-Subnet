---
# Round 1
# Mechanism Weighting (Emission Split) — Creative Exploration + Red Team

This document games out how Littlefoot should split emissions across **multiple incentive mechanisms** (one mechanism per supported primary subnet overlay), per Bittensor’s multi-mechanism design. See: [Multiple Incentive Mechanisms Within Subnets](https://docs.learnbittensor.org/subnets/understanding-multiple-mech-subnets).

## Problem statement

Littlefoot’s thesis is to act as a **carbon-efficiency incentive overlay** on other Bittensor subnets. In the whitepaper, “each supported primary subnet will have its own tailored mechanism” (`WHITEPAPER.md`). The open question is:

- How should Littlefoot allocate its subnet emissions across those mechanisms?

This is *not* about how validators score miners **within** a mechanism (that’s the per-overlay scoring function). This is about **inter-mechanism allocation**: how much of the total emission pool each overlay-mechanism gets.

## Design goals (what “good” looks like)

- **Non-gameable / low-manipulability**: Subnet owners or miners should not be able to cheaply distort Littlefoot’s split in their favor.
- **Alignment with Littlefoot’s mission**: More Littlefoot emissions should generally mean more real-world carbon-impact opportunity (or at least not systematically anti-correlate with it).
- **Simplicity + low ops overhead**: Easy to explain, easy to implement, hard to misconfigure.
- **Stability**: Avoid rapid oscillations that create strategic uncertainty and “emissions chasing.”
- **Extensibility**: As multi-mech limits evolve (docs note a current runtime cap of 2 mechanisms), the policy should generalize to \(N\) mechanisms cleanly.
- **Political acceptability**: Must not look like Littlefoot is “picking winners” among primary subnets in a way that triggers social blowback or creates adversarial relationships.

## Constraints / realities

- **Multi-mech is an on-chain split**: the subnet creator can apportion emissions across mechanisms.
- **Data quality varies**: token prices, volumes, “impact,” and even carbon proxies are noisy and can be manipulated at the margins.
- **Overlay is secondary**: primary subnets already drive the dominant incentives; Littlefoot is (initially) a marginal-but-meaningful subsidy.
- **Validator workload externality**: multiple mechanisms are not “free.” Validators must evaluate/weight each mechanism; adding mechanisms increases operational load and creates more surface area for mistakes and gaming.

## Creative exploration: candidate policies

### 1) Equal split across supported subnets (agnostic)

**Policy**: If Littlefoot supports \(N\) primary subnets (and thus \(N\) mechanisms), set:

\[
\text{split}_k = 1/N
\]

**Why it’s attractive**

- **Hard to game**: You can’t inflate your share by pumping a metric.
- **Cheap and robust**: no oracles, no feeds, no fiddly parameters.
- **Explains well**: “Littlefoot treats supported subnets equally.”
- **Avoids mission drift**: doesn’t quietly turn Littlefoot into a bet on tokenomics.

**Downsides**

- **Not impact-optimized**: equal funding might underfund high-leverage overlays and overfund low-leverage ones.
- **Opportunity cost**: Littlefoot could miss chances to disproportionately move the biggest carbon needles.

**Implementation detail**

- Decide what “supported subnet count” means operationally (e.g., “has a live mechanism” vs “in docs/roadmap”).
- Handle onboarding/offboarding with a smoothing rule (see “Guardrails”).

### 2) Market-based split (weight by primary subnet token price / market cap / liquidity)

**Policy**: allocate more emissions to overlays on subnets whose alpha is “more valuable” in TAO or USD terms (or by market cap/liquidity proxies).

**Intuition**

- If a subnet is economically important, improving its carbon footprint could “influence Bittensor more overall.”

**Pros**

- Targets “where the money is,” which may correlate with attention, usage, and real compute.

**Cons**

- **Highly gameable** (especially in thin markets): price/liquidity can be manipulated.
- **Misaligned proxy risk**: price can reflect hype, not compute volume or carbon footprint.
- **Reinforces winner-take-more**: already-successful subnets get even more external subsidy.
- **Perception risk**: looks like Littlefoot is endorsing certain subnets as “more important.”

### 3) “Need-based” split (weight toward smaller / weaker subnets)

**Policy**: allocate more to subnets with lower token price, lower emissions, lower stake, etc.

**Intuition**

- Help subnets that otherwise wouldn’t attract top miners; create a “leveling” effect.

**Pros**

- Could increase *marginal* influence where incentives are weak.

**Cons**

- **Wastes emissions** on marginal/irrelevant subnets if the “weakness” is structural.
- **Adverse selection**: attracts subnets that are weak for good reasons.
- Still gameable (actors can depress signals to appear “needy”).

### 4) Carbon-impact split (weight by estimated absolute carbon footprint)

**Policy**: allocate more emissions to overlays on subnets with higher absolute carbon burn (estimated compute volume × carbon intensity).

**Pros**

- Directly aligned with “make more difference.”

**Cons (big)**

- **Perverse incentives**: subnets might seek to look “dirtier” or burn more to attract Littlefoot emissions.
- **Measurement problems**: absolute footprint is hard to estimate credibly without deep instrumentation.
- **Boundary ambiguity**: what counts as the subnet’s footprint (validators? redundancy? miner off-chain work?) can be contested.

### 5) “Marginal abatement” split (weight by expected carbon reduction per Littlefoot dollar)

**Policy**: allocate based on the predicted *marginal* carbon reduction achieved by adding Littlefoot subsidy to that primary subnet overlay.

**Pros**

- The economically “correct” objective: optimize impact per unit emission.

**Cons**

- **Extremely hard**: requires modeling miner behavior, elasticity, and feasible relocation options.
- **Subjective priors**: quickly becomes a political fight in the community.
- **Easy to Goodhart**: the moment you measure/optimize, actors optimize the metric.

### 6) Participation-based split (weight by active overlay participants)

**Policy**: split proportional to the number of active miners (or validators, for validator-compute overlays) participating in each mechanism.

**Pros**

- “Pay where there’s adoption,” prevents dead mechanisms from draining emissions.

**Cons**

- **Bootstrap trap**: hard for new overlays to get started without emissions.
- **Sybil pressure**: encourages low-quality registrations to inflate counts.
- Counts can be gamed unless “active” is tightly defined.

### 7) Revenue/usage-based split (weight by real workload)

**Policy**: allocate to overlays based on (estimated) request volume, GPU-hours, training steps, jobs completed, etc., on the primary subnet.

**Pros**

- Closer to “real-world impact” than token price.

**Cons**

- Hard cross-subnet comparability and trustworthy measurement.
- Risks embedding each primary subnet’s own measurement quirks into Littlefoot governance.

### 8) Governance / discretionary split (human-in-the-loop)

**Policy**: set splits by owner discretion (or DAO vote) on a cadence, using qualitative judgment.

**Pros**

- Flexible; can respond to real-world context and “unknown unknowns.”

**Cons**

- **Centralization / politics**: looks and feels like favoritism.
- **Attack surface**: lobbying, bribery, coalition dynamics.
- Hard to explain and defend objectively.

### 9) Hybrid: equal baseline + small “tilt” with caps

**Policy**: start with equal split, then allow a bounded adjustment based on a chosen metric:

\[
\text{split}_k = \frac{1}{N} + \Delta_k,\quad \sum_k \Delta_k = 0,\quad |\Delta_k| \le \epsilon
\]

**Pros**

- Preserves the non-gameable core while allowing mild optimization.

**Cons**

- Requires agreement on tilt metric(s); introduces complexity and some gaming.

**If used, keep it boring**

- Small \(\epsilon\) (e.g. 5–10% absolute deviation from equal).
- Slow updates (monthly/quarterly) and smoothing.

## Recommendation (default)

**Default policy**: **Equal split across supported primary subnets**.

Rationale:

- It is the **least gameable** and easiest to explain.
- It avoids turning Littlefoot into a tokenomics/meta-governance layer.
- It keeps engineering focus on the thing Littlefoot is uniquely good at: **verifiable carbon intelligence**, not cross-subnet economic forecasting.

This is consistent with the whitepaper’s posture of being an overlay that “complements, not interferes with, primary subnet incentive mechanisms.”

## Guardrails (to make equal split robust in practice)

Even “equal split” needs rules for edge cases. Suggested guardrails:

- **Activation threshold**: a mechanism counts for splitting only if it is “live,” meaning it has (a) a defined scoring implementation, and (b) at least \(M\) active participants meeting a minimum quality bar.
- **Smoothing / ramp**: when adding a new supported subnet, ramp its split from 0 → \(1/N\) over \(T\) epochs to avoid sudden shocks.
- **Sunset rule**: if a mechanism is dead (no qualifying activity for \(X\) days), its share is redistributed evenly among active mechanisms.
- **Cap churn**: do not change the supported set more than once per period (e.g. monthly), to reduce strategic churn and ops load.

## Red team critique (be mean)

### “Equal split is too dumb; you’ll waste emissions”

**Attack**: Equal split can subsidize overlays that are low-impact or structurally unable to move to cleaner grids (latency-bound, fixed infra, etc.). That’s real opportunity cost.

**Mitigation**:

- Equal split *across a curated supported set* is still selective. The leverage lives in the **support criteria**, not the split formula.
- Use an **activation threshold + sunset rule** so emissions do not flow to dead/low-quality mechanisms indefinitely.

### “Equal split will be gamed via ‘support set capture’”

**Attack**: If equal split is fixed, then the only way to get more emissions is to get included in the supported set (or keep competitors out). Actors will lobby, fork narratives, or pressure governance.

**Mitigation**:

- Make support criteria explicit and technical (verification feasibility, workload class, expected carbon leverage).
- Time-box support review windows and require objective checklists.
- Prefer “support fewer, high-leverage overlays” over “support everything.”

### “Equal split enables a dilution / DoS attack”

**Attack**: If emissions are evenly split, then increasing \(N\) reduces each mechanism’s share. A malicious or misaligned governance process could add many low-quality “supported” overlays to:

- dilute the subsidy enough that *no* overlay meaningfully moves miner behavior
- increase validator workload until validation quality drops (or validators quit), harming the whole subnet

**Mitigation**:

- Set an explicit **max supported overlays** \(N_{\max}\) (even if the chain currently caps mechanisms; this is a policy constraint for the future).
- Require **activation thresholds** and a **ramp** before a mechanism counts toward the split.
- Treat “supporting a subnet” as a high-bar decision with a cooldown (monthly/quarterly windows).

### “Perverse incentives still exist: miners might choose subnets based on Littlefoot”

**Attack**: Even with equal split, miners may chase whichever overlay has the weakest competition for Littlefoot rewards, not necessarily where carbon impact is largest.

**Mitigation**:

- Ensure per-mechanism scoring is anchored to primary-subnet performance (as the whitepaper’s \(W_i\)-based overlay does), so low-performing opportunists can’t easily farm Littlefoot.
- Consider normalizing within each mechanism to reward only the top tranche of primary-subnet performers.

### “You’ll under-incentivize the biggest carbon pools”

**Attack**: If one supported primary subnet represents 80% of the carbon footprint, equal split underfunds it.

**Mitigation**:

- If this becomes true and measurable, move to the hybrid: **equal baseline + capped tilt** based on a robust, hard-to-manipulate usage proxy.
- Alternatively: keep equal split, but select additional overlays only if they clear a high expected-impact bar.

### “Owner-controlled splits create a governance credibility risk”

**Attack**: Even with a simple equal policy, the community may worry that the creator key can arbitrarily reweight mechanisms (favor friends, punish critics, chase politics). This can reduce staking confidence.

**Mitigation**:

- Commit in writing to a **default policy** (equal split) and a narrow set of allowed deviations (if any).
- Add **process constraints**: timelocks, fixed reweight cadence, and public rationale for changes.
- Keep deviations bounded (the “capped tilt” hybrid) if/when you ever introduce them.

### “Carbon-weighted splits are dangerous but maybe unavoidable”

**Attack**: If Littlefoot markets itself as “carbon impact,” people will ask why emissions aren’t allocated where impact is highest.

**Mitigation**:

- Position equal split as an **anti-Goodhart** choice: impact metrics are too gameable early; start agnostic until measurement matures.
- Commit to a **future upgrade path**: “We will consider a capped-tilt policy once we have reliable, hard-to-game workload telemetry.”

### “Mechanism count limits (2 today) make this feel premature”

**Attack**: If only 2 mechanisms are allowed right now (per docs), you’re over-designing.

**Mitigation**:

- The decision still matters: even with 2 overlays, a 50/50 vs 80/20 split is huge.
- A simple equal split is exactly what you want while the platform feature matures.

## Proposed “support set” criteria (where the real leverage is)

If equal split is the default, the *supported set* becomes the main strategic control. Suggested criteria:

- **Verification feasibility**: can we reliably verify location/attestation quality for this subnet’s participant type?
- **Latency tolerance**: will carbon-optimized location choices break the primary subnet’s product?
- **Compute intensity**: does this subnet plausibly represent meaningful energy usage?
- **Behavioral elasticity**: are participants likely able to relocate/optimize if subsidized?
- **Social acceptability**: is the overlay likely to be seen as complementary, not antagonistic?

## Conclusion

Equal split across supported primary subnets is a strong default because it is cheap, stable, and hard to game—and it avoids turning Littlefoot into a cross-subnet tokenomics optimizer. The red-team view is that the *real* attack surface is not the split formula but the **supported set selection** and the **within-mechanism scoring**, so those should carry most of the design attention and explicitness.

---
# Round 2

This revision incorporates a key background assumption:

- Littlefoot’s supported primary subnets (and therefore mechanisms) will be a **small, curated, regularly-pruned set** (e.g. \(N \le 10\)), and adding support is **manual** because it requires writing/maintaining subnet-specific validator code.

Under that assumption, “equal split” is not “spray emissions across anything that asks,” it is “treat a hand-selected, high-quality shortlist equally.”

## Round 2 proposal (updated)

### A) Default emission split: equal across the curated set

If \(N\) mechanisms are live and in the curated supported set:

\[
\text{split}_k = 1/N
\]

No price-weighting, carbon-footprint-weighting, or “need-based” weighting by default.

### B) The real control surface: the supported-set protocol

Since inclusion is manual anyway (validator code must exist), formalize the “supported set” as a first-class protocol artifact with:

- **A clear eligibility checklist** (verification feasibility, workload/latency class, expected carbon-leverage, maintenance burden)
- **A fixed review cadence** (e.g. monthly/quarterly windows)
- **Explicit add/remove criteria** (what “bad” looks like; what “good” looks like)
- **A bounded set size target** (e.g. “aim for 3–10 overlays; prefer depth over breadth”)

### C) Admission and removal mechanics (simple, practical)

Even with a curated list, you still want predictable mechanics:

- **Add**: implement overlay validator logic → ship → run in “candidate” mode (can exist but doesn’t count for split) → promote to “supported” at a review window.
- **Remove**: can be removed at review windows; reserve an emergency removal path only for security/critical correctness issues.
- **Ramp** (optional): if volatility is a concern, ramp new overlays into the split over \(T\) epochs; if not, skip and keep it simple.

### D) Within-mechanism design still matters

Equal split doesn’t guarantee impact if a mechanism is poorly designed. Continue to enforce:

- **Primary-subnet anchoring** (Littlefoot rewards should be tightly tied to real excellence on the primary subnet, as the whitepaper’s \(W_i\)-based overlay implies)
- **Strong verification tiers** and freshness requirements
- **Anti-farming rules** (avoid “easy” attestations becoming a side-income stream)

## Governance thought experiment: on-chain council contract (optional)

You floated a “smart contract council” that proposes/votes to add/remove supported subnets, inspired by Bittensor’s evolving governance direction.

- For Bittensor EVM background: `https://docs.learnbittensor.org/evm-tutorials`
- For the network-level governance direction you referenced: `https://governance-transition-notes.developer-docs-6uq.pages.dev/learn/roadmap#decentralized-governance`

### Minimal viable council contract (what it would do)

**State**

- `supportedSet: (netuid -> {status, addedAt, metadataHash})`
- `maxSupported: uint`
- `timelockDelay: uint` (e.g. 7–30 days)

**Roles / voters (one possible choice)**

- Council = top \(K\) Littlefoot validators by stake (and/or a blended set of validators + miners).
- Membership updates on an epoch boundary (or via explicit rotation rules).

**Actions**

- `proposeAdd(netuid, metadataHash)` / `proposeRemove(netuid, reasonHash)`
- `vote(proposalId, yay/nay)`
- `queue(proposalId)` once quorum + threshold hit
- `execute(proposalId)` after timelock

**Safety levers**

- **Timelock**: prevents sudden capture-driven churn.
- **Emergency brake**: optional pause capability (but this itself is a centralization risk).
- **Quorum + supermajority for removals**: reduce griefing.

### What stays off-chain (almost certainly)

Even with on-chain governance, the hard part can’t be automated:

- writing and maintaining the subnet-specific validator code
- deciding what constitutes “good enough verification” for an overlay
- integrating external data sources safely

So the best-case role of a contract is: **make the supported-set decision auditable and harder to rug**, not to replace judgment.

## Round 2 critique (focused on your assumptions)

### 1) Equal split is much stronger under a curated-set assumption

If you truly keep the set small and prune aggressively, the main earlier worry (“junk overlays drain emissions”) largely goes away.

**Residual risk**: not junk, but **stale overlays** (used to be good, now irrelevant) silently persisting.

**Mitigation**: review cadence + explicit removal criteria + published “supported set” status.

### 2) Manual curation creates a different failure mode: politics, not gaming metrics

The core attack becomes **influence over curation** (lobbying, coalition politics), not manipulation of token price or carbon estimates.

**Mitigations**:

- publish checklists and postmortems
- time-box decisions
- have “no new overlays unless we can maintain them” as a norm

### 3) Council contract reduces “creator key discretion,” but increases complexity risk

**Pros**:

- makes add/remove decisions more credible to outsiders (less “trust me”)
- creates a public paper trail of who voted for what

**Cons**:

- smart contract bugs become existential (especially around membership, quorum, execution)
- bribery/vote-buying becomes more direct
- voter apathy and capture risk are real (a quiet council is easier to steer)

### 4) The biggest practical bottleneck is still validator engineering capacity

Because each overlay requires custom code, the real scarcity is:

- “how many overlays can we actually implement and maintain safely?”

This pushes you toward **few, high-leverage overlays** and makes equal split feel natural: you’re not trying to optimize a large portfolio; you’re funding a small set of top bets.

### 5) Earlier “miners chase weak competition” critique should be reframed

Given a curated supported set, “weak competition” is less likely to mean “junk overlay,” and more likely to mean one of:

- the overlay is new and under-adopted (bootstrap dynamics)
- the overlay’s verification/scoring is weaker *relative to the other curated overlays*
- the overlay is genuinely high-elasticity, high-leverage (the virtuous interpretation)

So the key is to ensure that “easy Littlefoot ROI” comes from **real, verifiable carbon optimization**, not from a softer verification regime.
