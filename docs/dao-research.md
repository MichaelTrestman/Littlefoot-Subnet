# DAO and Governance Options for Bittensor Subnets

**Research Date**: January 23, 2026  
**Context**: Exploring governance models for Littlefoot subnet to enable distributed decision-making on subjective parameters (e.g., emissions weighting across primary subnet mechanisms)

---

## Executive Summary

Bittensor provides **network-level governance** through a bicameral Senate system, but **subnet-level governance is currently limited to subnet owner control**. Subnet owners have sole authority over hyperparameters via `btcli sudo set` commands. To implement distributed governance for Littlefoot, we'll need to either:

1. **Off-chain governance** with on-chain execution by trusted multisig/owner
2. **Custom on-chain governance** built into validator logic
3. **Leverage alpha token economics** for weighted community input
4. **Adopt external DAO frameworks** (Aragon, Snapshot, etc.) adapted to Bittensor context

---

## Current Bittensor Governance Landscape

### Network-Level Governance (Triumvirate + Senate)

**Structure**: Bicameral legislature transitioning from foundation control to community ownership

- **Triumvirate**: 3 Opentensor Foundation employees who create proposals
- **Senate**: Up to 12 elected delegates with >2% of total network stake who vote on proposals

**Process**:
1. Triumvirate member creates proposal (e.g., subnet creation, hyperparameter changes, chain upgrades)
2. Senate votes using `btcli sudo senate-vote`
3. Requires 50% + 1 Senate approval
4. Triumvirate member must close/execute the proposal

**Purpose**: Network-wide decisions (subnet creation, protocol upgrades, global parameters)

**Limitations for Subnet Use**:
- Only applies to network-level decisions
- 2% stake threshold is very high (~millions of TAO)
- Designed for rare, high-stakes decisions, not operational subnet governance
- Subnet owners cannot delegate their administrative powers to Senate

### Subnet-Level Control (Owner Authority)

**Current Reality**: 
- Only the coldkey that created the subnet can modify hyperparameters
- No built-in mechanism for distributed governance at subnet level
- Subnet owners have unilateral control via `btcli sudo set`

**Configurable Parameters** (examples):
- ActivityCutoff, AdjustmentAlpha, AdjustmentInterval
- ImmunityPeriod, MaxValidators, Tempo
- WeightsRateLimit, registration settings
- Consensus features (liquid alpha, commit-reveal weights)

**Key Insight**: **Subnet governance is an unsolved design space in Bittensor**. Each subnet owner must implement their own governance if they want distributed decision-making.

---

## Dynamic TAO and Alpha Tokens

### What Dynamic TAO Introduces

**Launched**: February 13, 2025

**Core Mechanism**: Each subnet has an automated market maker (AMM) with:
- TAO reserve (network-wide currency)
- Alpha (α) reserve (subnet-specific token, 21M hard cap per subnet)

**Staking Changes**:
- Stakers exchange TAO for subnet's alpha token when entering
- Alpha price determined by TAO-to-alpha reserve ratio
- Market-driven subnet valuation (not centralized root network weights)

### Governance Implications

**What It Does**:
- Creates subnet-specific tokens that could theoretically be used for governance
- Stakers have economic alignment with specific subnets
- Alpha holders have skin in the game for subnet success

**What It Doesn't Do** (yet):
- No built-in voting mechanism for alpha holders
- No protocol-level support for alpha-based governance
- Alpha tokens are primarily for staking/emissions, not governance
- Transfer permissions are configurable but governance features aren't specified

**Potential**: Alpha tokens *could* be used as governance tokens in a custom DAO framework, representing stake-weighted voting power for subnet decisions.

---

## DAO Framework Options

### Option 1: Off-Chain Governance (Snapshot-Style)

**Model**: Community votes off-chain, subnet owner executes on-chain

**How It Works**:
1. Create proposals in off-chain forum/system (Snapshot, Commonwealth, custom)
2. Alpha holders vote (weighted by holdings)
3. Proposals that pass are executed by subnet owner or trusted multisig
4. Execution trust-based, not enforced by code

**Tools Available**:
- **Snapshot**: Gasless voting, token-weighted, flexible voting strategies
- **Commonwealth**: Discussion + voting combined
- **Custom forum + polling**: Discord/Discourse with structured voting

**Pros**:
- Fast to implement (no smart contract development)
- Flexible (can change voting rules easily)
- No gas costs for voters
- Can iterate on governance design quickly

**Cons**:
- Requires trust in executor (subnet owner or multisig)
- Not fully decentralized (execution is centralized)
- Vote results aren't binding on-chain
- Vulnerable to executor going rogue

**Best For**: Early-stage subnet governance, rapid iteration, when community trust exists

**Littlefoot Application**:
- Quarterly votes on emissions weighting across mechanisms
- Alpha holders (stakers) vote on allocation percentages
- Littlefoot owner/multisig updates subnet parameters based on results
- Could use Snapshot with custom strategy that reads alpha balances from chain

### Option 2: Multisig + Timelock

**Model**: Distribute control among trusted parties with delay mechanism

**How It Works**:
1. Create m-of-n multisig (e.g., 3-of-5) controlling subnet owner key
2. Add timelock: decisions announced, delay period before execution
3. Multisig members vote on parameter changes
4. After timelock expires, execute on-chain

**Tools**:
- **Gnosis Safe**: Standard multisig, substrate-compatible versions exist
- **Custom pallet**: Could build substrate pallet for multisig + timelock

**Pros**:
- More decentralized than single owner
- Timelock provides transparency and exit window
- On-chain execution (binding)
- Relatively simple to implement

**Cons**:
- Limited to small group (not community-wide governance)
- Multisig members are single points of failure
- Coordination overhead for signers
- Doesn't scale to large communities

**Best For**: Small trusted teams, transition from single owner, bootstrap governance

**Littlefoot Application**:
- Core team + community representatives form multisig
- Quarterly decisions on mechanism weights
- 48-hour timelock before execution
- Transparent, but not fully decentralized

### Option 3: Custom On-Chain Governance via Validator Logic

**Model**: Build governance into validator consensus mechanism

**How It Works**:
1. Validators propose parameter changes via special transactions
2. Validators vote weighted by stake/performance
3. Validator code enforces approved parameter changes
4. Subnet owner coldkey delegates authority to validator consensus

**Implementation Approaches**:
- **Consensus parameter updates**: Validators signal preferred values, converge on parameters
- **Validator voting epochs**: Periodic votes on specific proposals
- **Liquid democracy**: Validators delegate voting power to specialized decision-makers

**Pros**:
- Native to Bittensor architecture
- Validators already have skin in game (subnet-specific stake)
- Can align incentives with validator performance
- Fully on-chain and decentralized

**Cons**:
- Requires significant custom development
- Validators might not represent broader community
- Complex to implement securely
- Difficult to change governance rules once deployed

**Best For**: Mature subnets, when validator set is stable and representative, long-term governance

**Littlefoot Application**:
- Validators propose and vote on mechanism weights
- Voting power weighted by validator stake + performance
- Could implement quadratic voting or conviction voting for better representation
- Requires custom validator code development

### Option 4: Substrate Governance Pallets

**Model**: Use or adapt Polkadot/Substrate governance infrastructure

**Available Pallets**:
- **pallet_democracy**: Time-lock voting, conviction voting, adaptive quorum
- **pallet_conviction_voting**: Vote delegation, multi-track governance
- **Polkadot OpenGov**: Modern governance with simultaneous referenda, flexible tracks

**How It Works**:
1. Deploy governance pallet to subtensor (requires protocol upgrade OR...)
2. Use pallet off-chain and execute results on-chain via sudo
3. Adapt pallet logic to subnet-specific context

**Pros**:
- Battle-tested code (Polkadot/Kusama production use)
- Sophisticated features (conviction voting, delegation, tracks)
- Active development and community
- Substrate-native (good fit for Bittensor)

**Cons**:
- Requires subtensor protocol changes (unlikely to get approval for subnet-specific governance)
- Heavy infrastructure for a single subnet
- Complexity may be overkill
- Would need significant adaptation

**Best For**: If Bittensor decides to add protocol-level subnet governance support (network-wide initiative, not single subnet)

**Littlefoot Application**:
- Likely not feasible for single subnet
- Could advocate for protocol-level support in future
- Inspiration for custom governance design

### Option 5: Aragon OSx or Similar DAO Frameworks

**Model**: Deploy standalone DAO using external framework, use alpha tokens for voting

**Popular Frameworks**:
- **Aragon OSx**: Modular DAO framework, token voting, delegations
- **Moloch DAO**: Focused on grants/funding, ragequit mechanism
- **Colony**: Task-based governance, reputation system
- **DAOstack**: Holographic consensus for scalable governance

**How It Works (Aragon Example)**:
1. Deploy Aragon DAO on compatible chain (Ethereum, Polygon, etc.)
2. Mirror alpha token balances or create wrapper token
3. Create proposals for mechanism weights, validator rules, etc.
4. Token holders vote
5. Approved proposals executed by subnet owner or multisig

**Pros**:
- Rich feature set out of the box
- Professional UI/UX
- Plugin ecosystem for extensions
- Proven in production

**Cons**:
- Requires bridging to non-Bittensor chain
- Token mirroring adds complexity and sync issues
- Gas costs for voters (unless using L2)
- Execution still requires trust in subnet owner

**Best For**: Subnets wanting sophisticated governance without custom development, if willing to bridge/mirror tokens

**Littlefoot Application**:
- Deploy Aragon DAO on Polygon (low gas)
- Mirror alpha token balances or use separate governance token
- Quarterly proposals for mechanism weights
- Off-chain execution by Littlefoot owner/multisig
- Good UI for community engagement

### Option 6: Hybrid Token-Weighted Forum Voting

**Model**: Structured forum governance with token-weighted voting, executed by trusted party

**How It Works**:
1. Use forum platform (Discourse, Discord, custom)
2. Proposals submitted with structured format
3. Voting periods with token-weighted votes
4. Token weight verified via signed messages or chain queries
5. Results tallied and executed by subnet owner

**Implementation Tools**:
- **Discourse + plugins**: Forum with voting extensions
- **Discord + bots**: Custom bot reads alpha balances, conducts votes
- **Custom React app**: Purpose-built governance interface

**Pros**:
- Combines discussion and voting in one place
- Flexible and iterative
- Low technical barrier for voters
- Can verify token holdings without complex infrastructure

**Cons**:
- Manual verification can be cumbersome
- Potential for gaming if not carefully designed
- Execution trust-based
- Limited to simpler voting mechanisms

**Best For**: Community-focused subnets, when discussion context is critical, rapid experimentation

**Littlefoot Application**:
- Discourse forum for proposals and discussion
- Token-weighted voting via signed messages
- Monthly/quarterly decision-making cycles
- Transparent tallying, subnet owner execution

---

## Governance Design Considerations for Littlefoot

### What Needs Governance?

Based on the conversation summary, key subjective decisions requiring governance:

1. **Mechanism weight allocation**: How to distribute Littlefoot emissions across primary subnets
2. **Burn/recycle parameters**: When to burn vs. distribute emissions based on participant quality
3. **Verification tier multipliers**: Signal strength values for different attestation methods
4. **Adding/removing primary subnets**: Which subnets to support
5. **Carbon intensity thresholds**: Minimum impact requirements
6. **Emergency parameter adjustments**: Response to gaming or exploits

### Who Should Vote?

**Option A: Alpha Token Holders (Stakers)**
- Economic alignment with subnet success
- Skin in the game
- Already using Bittensor native tokens

**Option B: Validators**
- Operational experience with subnet
- Technical knowledge
- Direct implementation responsibility

**Option C: Hybrid**
- Alpha holders vote on strategic decisions (mechanism weights, subnet selection)
- Validators vote on operational parameters (verification tiers, thresholds)

**Option D: Miners on Primary Subnets**
- Affected parties have voice
- Complex to implement (cross-subnet voting)
- May not align with Littlefoot's interests

**Recommendation**: Start with **Alpha holders** (Option A) for legitimacy and simplicity, potentially add validator input later

### Voting Mechanisms

**Simple Majority**:
- 50% + 1 approval required
- Straightforward but vulnerable to attacks

**Quorum Requirements**:
- Minimum participation threshold (e.g., 10% of alpha supply must vote)
- Prevents decisions made by tiny minorities
- Risk of low participation blocking all decisions

**Conviction Voting** (Polkadot-style):
- Voters lock tokens for longer periods to increase vote weight
- Rewards long-term alignment
- More complex to implement and explain

**Quadratic Voting**:
- Cost to vote increases quadratically (1 vote = 1 token, 2 votes = 4 tokens, etc.)
- Reduces whale dominance
- Prevents 51% attacks by large holders

**Rage Quit Mechanism** (Moloch-style):
- Minority can exit and take proportional assets if they disagree
- Protects minorities from tyranny of majority
- Complex to implement in subnet context

**Recommendation**: Start with **simple majority + quorum**, add **conviction voting** in V2 if governance participation is strong

### Voting Frequency and Stability

**Considerations**:
- Mechanism weights shouldn't change too frequently (miner planning horizon)
- Need ability to respond to emergencies (exploits, gaming)
- Balance stability with adaptability

**Proposed Cadence**:
- **Quarterly governance cycles**: Regular review of mechanism weights
- **Emergency proposals**: Fast-track for critical issues (7-day voting, higher quorum)
- **Annual strategic planning**: Adding/removing subnets, major design changes

### Proposal Process

**Structured Workflow**:
1. **Discussion Phase** (2 weeks): Community discusses in forum
2. **Formal Proposal** (1 week): Structured proposal submission with clear parameters
3. **Voting Phase** (1 week): Token-weighted voting
4. **Timelock** (48 hours): Transparency before execution
5. **Execution**: Subnet owner or multisig updates parameters

**Proposal Requirements**:
- Clear specification of changes
- Rationale and expected impact
- Risk assessment
- Minimum proposal threshold (e.g., 1% of alpha supply to propose)

---

## Recommended Path for Littlefoot

### Phase 1: Launch (Months 1-3)

**Governance Model**: Subnet owner control with community input

**Implementation**:
- Littlefoot owner retains control via coldkey
- Create public Discord/Discourse for community discussion
- Monthly community calls to discuss mechanism weights
- Owner makes decisions based on community input and data
- Transparent documentation of all decisions

**Why**: Focus on building the core product, gathering data, learning what governance decisions are actually needed

### Phase 2: Soft Governance (Months 4-6)

**Governance Model**: Off-chain voting with owner execution

**Implementation**:
- Deploy Snapshot space or similar
- Alpha holders vote on quarterly mechanism weights
- Owner commits to executing results (social contract)
- Implement basic multisig (3-of-5) for owner key as backup
- Track governance participation and engagement

**Why**: Test community interest in governance, iterate on voting mechanisms without heavy infrastructure investment

### Phase 3: Formal DAO (Months 7-12)

**Governance Model**: Full DAO with on-chain accountability

**Implementation Options** (choose based on Phase 2 learnings):

**Option A - Multisig + Timelock** (Conservative):
- 5-of-9 multisig of community members + core team
- 48-hour timelock on all decisions
- Token-weighted community voting via Snapshot
- Multisig bound by social contract to execute

**Option B - Aragon/External DAO** (Feature-Rich):
- Deploy Aragon DAO on Polygon
- Alpha token mirroring for voting
- On-chain proposals with automatic tallying
- Multisig executes on Bittensor

**Option C - Custom On-Chain** (Maximum Decentralization):
- Build governance into validator code
- Validators + alpha holders vote
- Parameter changes enforced by validator consensus
- No single owner key vulnerability

**Recommendation**: **Option A (Multisig + Timelock)** for optimal balance of decentralization, security, and implementation complexity

### Phase 4: Mature Governance (Year 2+)

**Evolution Path**:
- Incorporate validator voting alongside token holders
- Implement conviction voting for better time-preference alignment
- Potentially advocate for protocol-level subnet governance support in Bittensor
- Delegate specific decision types to specialized committees
- Automate routine decisions, focus governance on strategic choices

---

## Key Risks and Mitigations

### Risk 1: Low Participation

**Problem**: Apathetic token holders don't vote, decisions made by tiny minority

**Mitigations**:
- Quorum requirements
- Delegation (let engaged participants vote on behalf of others)
- Incentivize participation (small alpha rewards for voters)
- Make voting easy (gasless, good UI)

### Risk 2: Plutocracy (Whale Control)

**Problem**: Large holders dominate all decisions

**Mitigations**:
- Quadratic voting
- Conviction voting (time preference > capital)
- Validator input weighted separately
- Reputation/participation weighting in addition to tokens

### Risk 3: Governance Attacks

**Problem**: Adversary accumulates tokens to manipulate subnet

**Mitigations**:
- Timelock for transparency
- Conviction voting makes attacks expensive
- Emergency multisig override for existential threats
- Monitor token concentration, raise alarms

### Risk 4: Voter Fatigue

**Problem**: Too many decisions, community burnout

**Mitigations**:
- Batch related decisions quarterly
- Delegate routine decisions to multisig/validators
- Only govern truly subjective/strategic choices
- Clear, concise proposals with summaries

### Risk 5: Execution Trust

**Problem**: Owner/multisig doesn't execute vote results

**Mitigations**:
- Transparent communication and commitment
- Multisig distribution (no single point of failure)
- Community monitoring and social pressure
- Plan migration path to trustless execution

---

## Comparison Matrix

| Approach | Decentralization | Implementation Cost | Time to Deploy | Flexibility | Security |
|----------|-----------------|-------------------|----------------|------------|----------|
| Owner Control | ★☆☆☆☆ | Free | Immediate | ★★★★★ | ★★★☆☆ |
| Snapshot Voting | ★★☆☆☆ | Low | 1-2 weeks | ★★★★★ | ★★☆☆☆ |
| Multisig + Timelock | ★★★☆☆ | Medium | 2-4 weeks | ★★★☆☆ | ★★★★☆ |
| Custom Validator Governance | ★★★★☆ | High | 2-3 months | ★★☆☆☆ | ★★★★☆ |
| Aragon/External DAO | ★★★☆☆ | Medium | 3-6 weeks | ★★★★☆ | ★★★☆☆ |
| Substrate Pallets | ★★★★★ | Very High | 6+ months | ★★☆☆☆ | ★★★★★ |

---

## Resources and Tools

### Snapshot Integration
- **Snapshot Docs**: https://docs.snapshot.org
- **Strategies**: Can create custom strategy to read alpha balances from Bittensor chain
- **IPFS Storage**: Proposals stored decentrally

### Aragon
- **Aragon OSx**: https://aragon.org/aragonosx
- **Token Voting Plugin**: https://devs.aragon.org/docs/osx/plugins/token-voting
- **SDK**: JavaScript/TypeScript for integration

### Substrate Governance
- **pallet_democracy**: https://paritytech.github.io/polkadot-sdk/master/pallet_democracy
- **Polkadot OpenGov**: https://polkadot.com/blog/gov2

### Multisig
- **Gnosis Safe**: Industry standard, substrate-compatible versions exist
- **Substrate Multisig**: https://docs.substrate.io/reference/how-to-guides/basics/use-multisig/

### Community Platforms
- **Discourse**: Open-source forum software
- **Commonwealth**: Governance discussion + voting
- **Discord**: Real-time community communication

---

## Open Questions for Further Research

1. **Can alpha token balances be easily queried for snapshot voting?**
   - Need to investigate Bittensor chain APIs for alpha token state
   - Determine if on-chain snapshots are feasible

2. **What's the legal status of subnet governance tokens?**
   - Are alpha tokens securities?
   - Regulatory implications of governance features

3. **Have any other Bittensor subnets implemented governance?**
   - Learn from existing examples (SN118 mentioned as overlay subnet)
   - What worked and what didn't?

4. **Could Dynamic TAO be extended to support governance natively?**
   - Advocate for protocol-level governance features
   - What would be needed for Opentensor Foundation to support this?

5. **How to handle cross-subnet coordination?**
   - Littlefoot affects multiple primary subnets
   - Should primary subnet communities have input?

6. **What's the attack cost for governance?**
   - Model cost to acquire controlling stake
   - Economic security analysis

---

## Conclusion

**For Littlefoot specifically**, the recommended approach is:

**Immediate**: Owner control with community input  
**6 months**: Snapshot voting + trusted execution  
**12 months**: Multisig + timelock DAO  
**Long-term**: Custom validator-based governance or protocol-level support

The key insight is that **subnet-level governance is currently DIY in Bittensor**. There's no built-in solution, so Littlefoot needs to either:
1. Build custom governance
2. Adapt external tools (Snapshot, Aragon, etc.)
3. Start simple and iterate based on community engagement

Given the need for **subjective weighting decisions** and **distributed legitimacy**, governance is essential for Littlefoot's mission. The phased approach allows learning and adaptation while building community trust.

**Next Steps**:
1. Confirm alpha token balance queries are feasible
2. Set up community forum (Discord/Discourse)
3. Draft governance charter and voting procedures
4. Research Snapshot integration with Bittensor
5. Identify potential multisig members for future phase
