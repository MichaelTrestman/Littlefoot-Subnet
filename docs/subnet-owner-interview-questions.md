# Subnet Owner Interview Questions for Littlefoot Design

**Purpose**: Gather insights from subnet owners to inform Littlefoot's design, verify assumptions, and identify integration opportunities.

**Target Subnets**: Lium (SN51), Chutes (SN64), ComputeHorde (SN12), Templar, IOTA (SN120), Hippius (SN13), and other compute-intensive subnets

---

## Section 1: Miner Infrastructure & Hosting

### Q1: Where do your miners typically host their infrastructure?
- [ ] Primarily cloud providers (AWS, GCP, Azure)
- [ ] Primarily bare metal providers (Latitude.sh, Hyperstack, etc.)
- [ ] Mixed (some cloud, some bare metal)
- [ ] Colocation facilities
- [ ] Home/self-hosted
- [ ] Don't know / No visibility

**Follow-up**: What percentage would you estimate for each category?

### Q2: Which specific providers do you know your miners use?
*Ask for names like Latitude.sh, Hyperstack, AWS, GCP, Azure, OVH, Hetzner, etc.*

### Q3: Do miners in your subnet control their own infrastructure?
- [ ] Yes, miners own/rent and manage their hardware
- [ ] No, our subnet provides infrastructure to miners
- [ ] Mixed model
- [ ] Uncertain

**Follow-up**: If mixed, what percentage control their own infrastructure?

### Q4: How much flexibility do miners have to relocate or change providers?
- [ ] Very flexible - can easily move between providers
- [ ] Somewhat flexible - possible but with friction
- [ ] Difficult - significant investment/setup required
- [ ] Essentially locked in - relocation extremely costly
- [ ] Not applicable

**Why this matters for Littlefoot**: Need to understand if carbon incentives can actually influence location decisions.

---

## Section 2: Compute Workload Characteristics

### Q5: What is the primary type of compute work your miners perform?
- [ ] Model training (full fine-tuning)
- [ ] Model inference (serving/generation)
- [ ] GPU rental / general compute
- [ ] Data processing / ETL
- [ ] Validation compute (cross-checking other miners)
- [ ] Other: _______

### Q6: How latency-sensitive are the workloads on your subnet?
- [ ] Extremely sensitive (<50ms matters for user experience)
- [ ] Moderately sensitive (100-200ms noticeable but acceptable)
- [ ] Not very sensitive (seconds don't matter)
- [ ] Batch/async workloads (minutes/hours acceptable)
- [ ] Mixed (different job types have different requirements)

**Why this matters**: Geographic distance to clean grids adds latency. Need to know if this is a dealbreaker.

### Q7: What percentage of work is real-time vs. batch/asynchronous?
- Real-time: ____%
- Batch/async: ____%
- Other: ____%

### Q8: Do miners perform most of the compute work, or do validators?
- [ ] Primarily miners (>80% of compute)
- [ ] Mostly miners (60-80% of compute)
- [ ] Split roughly evenly
- [ ] Mostly validators (60-80% of compute)
- [ ] Primarily validators (>80% of compute)

**Why this matters**: Littlefoot only works for subnets where miners do significant compute.

---

## Section 3: Hardware & Energy Usage

### Q9: What types of GPUs do your miners primarily use?
- [ ] A100 / H100 (high-end training)
- [ ] A6000 / A5000 (professional workstation)
- [ ] RTX 4090 / 3090 (consumer high-end)
- [ ] Mid-range consumer GPUs
- [ ] No GPUs / CPU only
- [ ] Mixed across wide range

### Q10: Approximately how many GPUs do your top miners run?
- Minimum to be competitive: _____
- Average among top 10%: _____
- Maximum you're aware of: _____

### Q11: Do you have any data or estimates about energy consumption on your subnet?
- [ ] Yes, we track it (please share if possible)
- [ ] No, but would be interested in finding out
- [ ] No, and it's not a priority
- [ ] Haven't thought about it

**Follow-up**: If yes, what's the estimated total power consumption or carbon footprint?

### Q12: Have any miners mentioned energy costs as a significant operational concern?
- [ ] Yes, frequently cited as major cost
- [ ] Sometimes mentioned
- [ ] Rarely mentioned
- [ ] Never mentioned
- [ ] Don't know

---

## Section 4: Verification & Data Access

### Q13: Do you currently verify where miners are operating from?
- [ ] Yes, we actively verify location
- [ ] Partially (we collect location data but don't verify)
- [ ] No, we have no visibility into miner locations
- [ ] No, but we'd like to

**Follow-up**: If yes, how do you verify? (IP geolocation, provider APIs, self-reporting, etc.)

### Q14: Do miners provide any infrastructure access to validators currently?
- [ ] Yes, API keys to verify hardware/location
- [ ] Yes, limited read-only access
- [ ] Yes, SSH or similar access
- [ ] No, no access provided
- [ ] Would be willing to if useful

**Examples**: Latitude.sh API keys, AWS/GCP service accounts, server management consoles

### Q15: How do you currently verify that miners are using the hardware they claim?
*Looking for existing verification mechanisms we could extend*

### Q16: What data about miners is readily available in your validator code?
- [ ] IP addresses
- [ ] Self-reported location
- [ ] Provider information
- [ ] Hardware specs
- [ ] Power consumption metrics
- [ ] API credentials for external services
- [ ] Other: _______

**Why this matters**: Need to understand what verification hooks already exist.

---

## Section 5: Miner Behavior & Economics

### Q17: What are the main cost factors for your miners?
Rank in order (1 = highest cost):
- [ ] GPU hardware / rental costs
- [ ] Electricity / power costs
- [ ] Network bandwidth costs
- [ ] Cooling / datacenter costs
- [ ] Software / licensing costs
- [ ] Other: _______

### Q18: How competitive is mining on your subnet?
- [ ] Extremely competitive - need latest hardware + optimization
- [ ] Very competitive - need good hardware and setup
- [ ] Moderately competitive - decent hardware sufficient
- [ ] Low competition - easy to mine profitably
- [ ] Uncertain

### Q19: How often do miners join/leave or change their setup?
- [ ] Very dynamic (frequent changes)
- [ ] Moderate turnover
- [ ] Stable miner set
- [ ] Very stable (same miners for months)

### Q20: What's the typical UID pressure on your subnet?
- [ ] Extremely high (very hard to get/keep UID)
- [ ] High (need consistent performance)
- [ ] Moderate (reasonable to maintain UID)
- [ ] Low (easy to register and stay)
- [ ] Very low (many open UIDs)

**Why this matters**: Affects whether low performers can persist (mentioned in conversation analysis).

---

## Section 6: Overlay Subnet Concerns

### Q21: How would you feel about an overlay subnet (like Littlefoot) that provides additional incentives to your miners?
- [ ] Very positive - would welcome it
- [ ] Somewhat positive - interested but cautious
- [ ] Neutral - depends on details
- [ ] Somewhat concerned
- [ ] Very concerned - potential issues

**Please explain your reasoning:**

### Q22: What concerns, if any, would you have about an overlay subnet?
Check all that apply:
- [ ] Could interfere with our incentive mechanism
- [ ] Might change miner rankings in undesirable ways
- [ ] Could create perverse incentives
- [ ] Adds complexity for miners
- [ ] Privacy/security concerns about data sharing
- [ ] Worried about ecosystem fragmentation
- [ ] No major concerns
- [ ] Other: _______

### Q23: Under what conditions would you actively support an overlay subnet for carbon efficiency?
*Open-ended - looking for specific requirements or concerns*

### Q24: How large would Littlefoot need to be (relative to your subnet) before you'd worry about interference?
- [ ] Even 10% of our size would be concerning
- [ ] 25-50% would start to be concerning
- [ ] 50-100% (equal size) would be concerning
- [ ] Only if larger than us would it be concerning
- [ ] Size doesn't matter, design matters

---

## Section 7: Carbon Footprint & Sustainability

### Q25: Is environmental impact / carbon footprint something you think about for your subnet?
- [ ] Yes, actively working on it
- [ ] Yes, interested but not sure how to address it
- [ ] Somewhat - nice to have but not priority
- [ ] No, not really a concern
- [ ] Haven't thought about it

### Q26: Have you or your miners ever discussed choosing locations based on clean energy?
- [ ] Yes, some miners specifically mentioned choosing clean locations
- [ ] Yes, discussed but not acted on
- [ ] Mentioned occasionally but not a decision factor
- [ ] No, never discussed
- [ ] Don't know

### Q27: If Littlefoot provided carbon footprint intelligence about your subnet, would that be valuable to you?
- [ ] Very valuable - would actively use it
- [ ] Somewhat valuable - interesting to know
- [ ] Neutral - nice but not actionable
- [ ] Not valuable
- [ ] Unsure

**Follow-up**: What would you do with this information?

### Q28: Do you think your miners would relocate or change providers if carbon-efficient locations were financially rewarded?
- [ ] Definitely - even small incentives would matter
- [ ] Probably - if incentives were meaningful
- [ ] Maybe - depends on how much extra earnings
- [ ] Probably not - relocation costs too high
- [ ] Definitely not - location is fixed for other reasons
- [ ] Unsure

**Follow-up**: What percentage of additional earnings would make relocation worthwhile? (e.g., 10%, 20%, 50%?)

---

## Section 8: Technical Integration

### Q29: Would you be willing to modify your validator code to integrate with Littlefoot?
- [ ] Yes, definitely open to it
- [ ] Yes, if integration is straightforward
- [ ] Maybe, depends on complexity and benefits
- [ ] Probably not - prefer to keep code simple
- [ ] No - don't want additional dependencies

### Q30: What information could you share with Littlefoot validators about your miners?
Check all that are feasible:
- [ ] Current weights/rankings
- [ ] Hardware specifications
- [ ] Provider information
- [ ] Location data (if available)
- [ ] API credentials for verification
- [ ] Power consumption estimates
- [ ] Job completion metrics
- [ ] None of the above
- [ ] Other: _______

### Q31: How do you envision the relationship between your subnet and Littlefoot?
- [ ] Completely independent - no coordination needed
- [ ] Loose coupling - share data but no direct integration
- [ ] Moderate integration - some shared verification
- [ ] Tight integration - coordinated incentive mechanisms
- [ ] Unsure

### Q32: Would you want visibility into how Littlefoot scores your miners?
- [ ] Yes, need full transparency
- [ ] Yes, summary metrics sufficient
- [ ] Nice to have but not required
- [ ] Don't care
- [ ] Prefer not to know (avoid influence)

---

## Section 9: Validator Infrastructure

### Q33: Where do your validators typically run?
- [ ] Cloud providers
- [ ] Bare metal / dedicated servers
- [ ] Home/self-hosted
- [ ] Mixed
- [ ] Don't track this

**Why this matters**: Validators also have carbon footprint, though Littlefoot V1 focuses on miners.

### Q34: Do validators in your subnet also consume significant compute?
- [ ] Yes, validators do heavy computation
- [ ] Moderate - some compute but less than miners
- [ ] No, validators are lightweight
- [ ] Varies significantly

**Follow-up**: If yes, what percentage of total subnet compute do validators represent?

---

## Section 10: Future Vision

### Q35: If Littlefoot successfully reduced the carbon footprint of Bittensor mining, how would that affect your subnet?
*Open-ended - looking for perceived benefits, risks, opportunities*

### Q36: What features would make Littlefoot most valuable to you as a subnet owner?
Check all that apply:
- [ ] Public carbon footprint reporting for our subnet
- [ ] Helping miners optimize for cost + carbon
- [ ] Attracting environmentally-conscious miners/validators
- [ ] Reducing regulatory risk
- [ ] Improving public perception of Bittensor
- [ ] Providing infrastructure optimization insights
- [ ] Other: _______

### Q37: What would make Littlefoot integration seamless for your subnet?
*Open-ended - looking for practical requirements*

### Q38: Any other thoughts, concerns, or suggestions about Littlefoot?
*Open-ended*

---

## Section 11: Specific Technical Questions (For Compute Subnets)

### Q39: For GPU/compute subnets - Do miners run jobs continuously or sporadically?
- [ ] Continuous (always processing)
- [ ] Frequent bursts (multiple times per hour)
- [ ] Occasional (few times per day)
- [ ] Rare (ad-hoc basis)
- [ ] Varies widely

### Q40: How long do typical mining jobs take?
- Average duration: _____
- Range: _____ to _____

### Q41: Can jobs be paused and resumed, or must they complete in one session?
- [ ] Can pause/resume easily
- [ ] Can pause but with cost
- [ ] Must complete in one session
- [ ] Varies by job type

**Why this matters**: Affects feasibility of relocating mid-job.

---

## Section 12: Data for Research

### Q42: Would you be willing to share historical data with Littlefoot for research purposes?
Types of data that would be valuable:
- [ ] Miner locations over time (IP-based or self-reported)
- [ ] Hardware configurations
- [ ] Provider information
- [ ] Power consumption (if available)
- [ ] Job characteristics (duration, type, size)
- [ ] Performance metrics
- [ ] No, privacy/competitive concerns
- [ ] Other: _______

### Q43: Could we analyze your subnet's current carbon footprint as a case study?
- [ ] Yes, definitely interested
- [ ] Yes, if methodology is sound
- [ ] Maybe, need more details
- [ ] Probably not
- [ ] No

**What we'd provide**: Estimated current carbon footprint, geographic distribution analysis, optimization recommendations

---

## Contact & Follow-Up

### Q44: Can we follow up with more detailed technical questions if needed?
- [ ] Yes
- [ ] Maybe
- [ ] No

### Q45: Would you be interested in participating in early Littlefoot testing?
- [ ] Yes, very interested
- [ ] Yes, somewhat interested
- [ ] Maybe, depends on timing and effort
- [ ] Probably not
- [ ] No

### Q46: How would you prefer to stay updated on Littlefoot development?
- [ ] Direct communication (email/Discord)
- [ ] Public updates (blog posts, announcements)
- [ ] Monthly newsletter
- [ ] Only major milestones
- [ ] Prefer not to be contacted

---

## Post-Interview Notes (For Interviewer)

**Subnet**: ___________  
**Owner/Contact**: ___________  
**Date**: ___________  
**Key Takeaways**:
- 
- 
- 

**Action Items**:
- 
- 
- 

**Integration Feasibility** (1-5 scale): _____  
**Carbon Impact Potential** (1-5 scale): _____  
**Owner Enthusiasm** (1-5 scale): _____

**Recommended Priority for Littlefoot V1**:
- [ ] High - Target for initial launch
- [ ] Medium - Strong candidate for V2
- [ ] Low - Consider for later versions
- [ ] Not suitable - fundamental barriers exist

---

## Question Categories Summary

- **Infrastructure (Q1-Q4)**: Understanding hosting and flexibility
- **Workload (Q5-Q8)**: Latency sensitivity and compute distribution
- **Hardware (Q9-Q12)**: Energy usage and hardware requirements
- **Verification (Q13-Q16)**: Existing verification mechanisms
- **Economics (Q17-Q20)**: Cost factors and competitiveness
- **Overlay Concerns (Q21-Q24)**: Potential issues with Littlefoot
- **Sustainability (Q25-Q28)**: Current carbon awareness
- **Integration (Q29-Q32)**: Technical feasibility
- **Validators (Q33-Q34)**: Validator infrastructure
- **Vision (Q35-Q38)**: Future opportunities
- **Technical Details (Q39-Q41)**: Job characteristics
- **Research (Q42-Q43)**: Data sharing possibilities
- **Follow-up (Q44-Q46)**: Ongoing communication

---

## Using This Questionnaire

**Interview Format Options**:

1. **Full Structured Interview** (60-90 minutes)
   - Walk through all questions in order
   - Record and transcribe for analysis
   - Best for primary target subnets

2. **Focused Interview** (30-45 minutes)
   - Skip sections less relevant to specific subnet
   - Focus on concerns and integration feasibility
   - Good for secondary candidates

3. **Written Survey** (async)
   - Send questionnaire for subnet owner to complete
   - Follow up on interesting responses
   - Efficient for initial screening

4. **Casual Conversation** (flexible)
   - Use questions as talking points
   - Adapt based on conversation flow
   - Best for relationship building

**Priority Questions** (if time is limited):
- Q3, Q6, Q8 (Feasibility fundamentals)
- Q21, Q22, Q23 (Overlay concerns)
- Q28 (Behavioral response to incentives)
- Q29, Q30 (Integration willingness)
- Q11 (Carbon awareness)

**Red Flags to Watch For**:
- Validators do most compute (Q8) → Littlefoot won't work
- Extremely latency-sensitive (Q6) → Geographic distribution problematic
- Fixed/immobile infrastructure (Q4) → Can't respond to incentives
- Hostile to overlay concept (Q21) → Integration will be difficult
- No data access possible (Q14, Q30) → Verification impossible
