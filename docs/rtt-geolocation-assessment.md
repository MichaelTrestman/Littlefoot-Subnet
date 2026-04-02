# RTT/Latency-Based Geolocation Feasibility Assessment

**For**: Littlefoot Subnet Tier 3 Verification  
**Date**: January 23, 2026

---

## TL;DR: Is This Feasible?

**Yes, but with important limitations:**
- ✅ Python libraries and tools exist
- ✅ Can detect VPNs/proxies and gross location spoofing
- ✅ ~100km accuracy achievable (city-level, not street-level)
- ⚠️ Requires multiple measurement points (validators in different locations)
- ⚠️ Won't give you precise datacenter identification
- ⚠️ Network routing can cause false positives/negatives
- ❌ Not suitable as sole verification method for high-confidence location

**Recommendation**: Use as **Tier 3 (low confidence)** fallback, not primary verification

---

## How It Works (Simplified)

### Basic Concept

1. **Speed of Light Limits**: Network signals travel at ~2/3 speed of light in fiber optic cables
2. **Distance = Time × Speed**: Round-trip time (RTT) correlates roughly with physical distance
3. **Triangulation**: Measure RTT from multiple known locations, draw circles, find intersection

### Example

If you ping a miner from:
- **New York** → 50ms RTT → ~5,000km radius
- **London** → 30ms RTT → ~3,000km radius  
- **Tokyo** → 150ms RTT → ~15,000km radius

The intersection of these circles narrows down the possible location. With good measurements, you can say "probably in Western Europe" but not "definitely in Amsterdam datacenter."

### Why It's Not Perfect

**Network Routing**: Packets don't travel in straight lines. A miner in San Francisco might route through Chicago to reach New York, making it look farther away.

**VPNs/Proxies**: Add extra hops and latency, but this is actually detectable (see below).

**Buffering Delays**: Routers introduce variable delays unrelated to distance.

---

## Available Python Tools

### 1. Basic RTT Measurement (Easy)

**Built-in Python Methods**:

```python
# Method 1: Using subprocess to ping
import subprocess
import re

def measure_rtt(host):
    """Simple ping-based RTT measurement"""
    result = subprocess.run(
        ['ping', '-c', '4', host],
        capture_output=True,
        text=True
    )
    # Parse output for average RTT
    match = re.search(r'avg = ([\d.]+)', result.stdout)
    return float(match.group(1)) if match else None

# Method 2: Using socket (more control)
import socket
import time

def measure_tcp_rtt(host, port=80):
    """Measure TCP handshake RTT"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    
    start = time.time()
    try:
        sock.connect((host, port))
        rtt = (time.time() - start) * 1000  # Convert to ms
        sock.close()
        return rtt
    except:
        return None
```

**Pros**: Simple, no dependencies  
**Cons**: Basic, doesn't handle complex cases

### 2. IP2Location (Database Lookup - Not RTT)

**Library**: `IP2Location-python`

```bash
pip install IP2Location
```

```python
import IP2Location

database = IP2Location.IP2Location("/path/to/IP2LOCATION.BIN")
rec = database.get_all(ip_address)

print(f"Country: {rec.country_long}")
print(f"Region: {rec.region}")
print(f"City: {rec.city}")
print(f"Latitude: {rec.latitude}")
print(f"Longitude: {rec.longitude}")
```

**Note**: This is database lookup, not RTT-based. Useful for comparison but not true latency verification.

**Accuracy**: City-level, but susceptible to VPN spoofing (just reports VPN exit node location).

### 3. Scapy (Advanced Packet Crafting)

**Library**: `scapy`

```bash
pip install scapy
```

```python
from scapy.all import IP, ICMP, sr1
import time

def scapy_ping(host):
    """Send ICMP packet and measure RTT"""
    packet = IP(dst=host)/ICMP()
    
    start = time.time()
    reply = sr1(packet, timeout=2, verbose=0)
    
    if reply:
        rtt = (time.time() - start) * 1000
        return rtt
    return None
```

**Pros**: Fine-grained control, can craft custom packets  
**Cons**: Requires root/admin privileges, more complex

### 4. Multi-Point Trilateration (Research Projects)

**GitHub Projects**:

- **[britram/trilateration](https://github.com/britram/trilateration)**: Quantifying errors in RTT-based trilateration
- **[nicofontanarosa/rtt-geo-location-anomaly-detector](https://github.com/nicofontanarosa/rtt-geo-location-anomaly-detector)**: Wireshark plugin for detecting VPN via RTT analysis
- **[dioptra-io/georesolver](https://github.com/dioptra-io/georesolver)**: IP geolocation resolution tools

**Status**: Research-grade code, not production-ready libraries, but demonstrates feasibility

---

## Practical Implementation for Littlefoot

### Multi-Validator Architecture

**Requirements**:
- **3-5 validators** in geographically diverse locations (US East, US West, Europe, Asia)
- Each validator measures RTT to miner
- Validators share measurements and compute triangulation
- Cross-check with claimed location

### Algorithm Outline

```python
class LatencyVerifier:
    def __init__(self, validator_locations):
        """
        validator_locations: dict mapping validator_id to (lat, lon)
        """
        self.validator_locations = validator_locations
    
    def measure_rtt_from_all_validators(self, miner_ip):
        """
        Each validator measures RTT to miner
        Returns: dict of {validator_id: rtt_ms}
        """
        measurements = {}
        for validator_id in self.validator_locations:
            rtt = self.measure_rtt(miner_ip)  # Run from that validator
            measurements[validator_id] = rtt
        return measurements
    
    def estimate_distance_from_rtt(self, rtt_ms):
        """
        Convert RTT to approximate distance
        Speed of light in fiber: ~200,000 km/s
        RTT includes round trip, so distance ≈ (RTT/2) × speed
        """
        speed_of_light_fiber = 200_000  # km/s
        distance_km = (rtt_ms / 1000 / 2) * speed_of_light_fiber
        return distance_km
    
    def triangulate(self, measurements):
        """
        Given RTT measurements from multiple validators,
        estimate miner location using circle intersection
        
        This is simplified - real implementation uses
        optimization algorithms (least squares, etc.)
        """
        circles = []
        for validator_id, rtt in measurements.items():
            center = self.validator_locations[validator_id]
            radius = self.estimate_distance_from_rtt(rtt)
            circles.append((center, radius))
        
        # Find intersection of circles
        # (Use library like scipy.optimize or custom geometry)
        estimated_location = self.find_circle_intersection(circles)
        return estimated_location
    
    def verify_claimed_location(self, miner_ip, claimed_lat, claimed_lon, 
                                 tolerance_km=500):
        """
        Check if claimed location is consistent with RTT measurements
        """
        measurements = self.measure_rtt_from_all_validators(miner_ip)
        estimated_location = self.triangulate(measurements)
        
        distance = self.haversine_distance(
            estimated_location, 
            (claimed_lat, claimed_lon)
        )
        
        if distance <= tolerance_km:
            return True, distance
        else:
            return False, distance
```

### VPN/Proxy Detection

**Key Signal**: Cross-layer latency discrepancies

```python
def detect_proxy(miner_ip):
    """
    Measure latency at different network layers
    VPNs create detectable anomalies
    """
    # Application-layer latency (HTTP request)
    http_rtt = measure_http_latency(miner_ip)
    
    # Network-layer latency (ICMP ping)
    icmp_rtt = measure_icmp_latency(miner_ip)
    
    # TCP-layer latency
    tcp_rtt = measure_tcp_handshake(miner_ip)
    
    # VPNs typically show inconsistencies
    if abs(http_rtt - icmp_rtt) > threshold:
        return "possible_proxy"
    
    # High latency to ALL measurement points = VPN
    if all(rtt > 200 for rtt in [http_rtt, icmp_rtt, tcp_rtt]):
        return "likely_vpn"
    
    return "direct_connection"
```

---

## Accuracy Expectations

### What RTT Geolocation CAN Do

✅ **Continent-level accuracy**: "This miner is in North America, not Europe"  
✅ **Region-level accuracy**: "This miner is on US East Coast, not West Coast"  
✅ **Detect gross fraud**: "Claims Iceland but pings from Virginia"  
✅ **VPN detection**: "Routing through proxy, location uncertain"  
✅ **City-level (with good conditions)**: ~100km accuracy with 3-5 measurement points

### What RTT Geolocation CANNOT Do

❌ **Datacenter identification**: "This is AWS us-east-1 vs us-east-2"  
❌ **Precise city location**: "This is Amsterdam vs Rotterdam"  
❌ **Distinguish nearby datacenters**: < 50km differences unreliable  
❌ **Work reliably with complex routing**: Multi-hop paths introduce errors  
❌ **Guarantee accuracy**: 100km is best-case, often 300-500km

---

## Research on Accuracy

### Academic Results

**BFT-PoLoc (2024)**: Byzantine-resistant proof of location using RTT
- **95%+ accuracy** under adversarial conditions
- Requires **majority-honest reference points** (validators)
- Uses **cryptographic verification** and **geometric constraints**
- 100km accuracy baseline for non-adversarial cases

**CalcuLatency (2018)**: VPN/proxy detection via cross-layer latency
- **One-third of proxy servers** misrepresent locations
- Cross-layer measurement detects proxies with high accuracy
- Low false positive rate for direct connections

**Limitations from Research**:
- Network routing dominates over geographic distance in many cases
- Buffering delays at intermediate hops introduce 20-50ms noise
- Works best for long-distance measurements (>1000km)
- Unreliable for distinguishing nearby locations (<200km)

---

## Implementation Effort Estimate

### Option A: Basic Multi-Validator RTT (Minimal)

**What it does**:
- Each validator pings miner, measures RTT
- Compare RTTs to expected values for claimed region
- Flag if inconsistent

**Code Complexity**: ~200-300 lines Python  
**Development Time**: 1-2 weeks  
**Accuracy**: Rough (continent/region level)

**Example**:
```python
# Validator in New York
if miner_claims_iceland and rtt < 50ms:
    flag = "suspicious"  # Iceland should be ~100ms from NY
```

### Option B: Proper Trilateration (Moderate)

**What it does**:
- 3-5 validators in different locations
- Each measures RTT, converts to distance
- Geometric intersection to estimate location
- Compare to claimed location with tolerance

**Code Complexity**: ~500-800 lines Python (with geometry libraries)  
**Development Time**: 3-4 weeks  
**Accuracy**: City-level (~100km)

**Libraries Needed**:
- `scipy` for optimization (circle intersection)
- `geopy` for distance calculations
- Standard networking tools

### Option C: Research-Grade with VPN Detection (High)

**What it does**:
- Everything in Option B
- Cross-layer latency measurements
- Byzantine-resistant verification (BFT-PoLoc style)
- Machine learning for anomaly detection

**Code Complexity**: ~2000+ lines Python  
**Development Time**: 2-3 months  
**Accuracy**: Best achievable (~100km, robust to attacks)

**Additional Libraries**:
- `scikit-learn` for ML models
- `cryptography` for Byzantine resistance
- Advanced networking tools (Scapy)

---

## Recommendation for Littlefoot

### Use RTT as Tier 3 Only

**Why**:
- Provider APIs (Tier 1) give exact datacenter location
- Colocation attestations (Tier 2) give strong confidence
- RTT (Tier 3) is broad-brush verification, not precise

**Appropriate Use Case**:
- Miner has no provider API access
- No colocation attestation available
- Last resort verification before "unverified" status

**Implementation**:
- Start with **Option A (Basic)** - minimal effort, good enough for Tier 3
- Each validator measures RTT to miner
- Check if RTT consistent with claimed region
- Flag if obviously inconsistent (e.g., claims Iceland but 20ms from all US validators)

### Example Tier 3 Logic

```python
def tier3_verification(miner_ip, claimed_region):
    """
    Rough verification using RTT from multiple validators
    """
    # Validators in NY, London, Tokyo
    rtts = {
        'ny': measure_rtt_from_ny(miner_ip),
        'london': measure_rtt_from_london(miner_ip),
        'tokyo': measure_rtt_from_tokyo(miner_ip)
    }
    
    # Expected RTT ranges for regions
    expected = {
        'iceland': {'ny': (80, 120), 'london': (20, 60), 'tokyo': (200, 300)},
        'us_east': {'ny': (5, 40), 'london': (70, 110), 'tokyo': (140, 200)},
        'germany': {'ny': (80, 120), 'london': (20, 60), 'tokyo': (200, 300)},
        # ... more regions
    }
    
    # Check consistency
    region_ranges = expected.get(claimed_region, None)
    if not region_ranges:
        return 0.7  # Unknown region, give moderate score
    
    consistent_count = 0
    for validator, (min_rtt, max_rtt) in region_ranges.items():
        if min_rtt <= rtts[validator] <= max_rtt:
            consistent_count += 1
    
    # Score based on consistency
    consistency = consistent_count / len(rtts)
    
    # Tier 3 multiplier: 0.7 if consistent, lower if not
    if consistency >= 0.67:  # 2 out of 3 validators agree
        return 0.7
    elif consistency >= 0.33:  # 1 out of 3
        return 0.5
    else:
        return 0.2  # Likely spoofing
```

### Signal Strength Mapping

From whitepaper:
- **Tier 1 (Provider API)**: σ = 1.0
- **Tier 2 (Colocation)**: σ = 0.9
- **Tier 3 (RTT)**: σ = 0.7 (if consistent) down to 0.2 (if suspicious)
- **Tier 0 (Unverified)**: σ = 0.0

**Tier 3 is acceptable** because:
- Better than nothing
- Can detect gross fraud (claims Iceland, actually in China)
- Low implementation cost (Option A: 1-2 weeks)
- Doesn't need to be precise for tier 3 use case

---

## Starter Code Example

```python
import subprocess
import re
from typing import Dict, Tuple

class SimplifiedRTTVerifier:
    """
    Minimal viable RTT verification for Littlefoot Tier 3
    Each validator runs this independently
    """
    
    # Expected RTT ranges (ms) from various validator locations
    # Format: {region: {validator_location: (min, max)}}
    EXPECTED_RTT = {
        'iceland': {
            'us_east': (80, 120),
            'us_west': (120, 160),
            'europe': (20, 60),
            'asia': (200, 300)
        },
        'us_east': {
            'us_east': (5, 40),
            'us_west': (60, 100),
            'europe': (70, 110),
            'asia': (140, 200)
        },
        'germany': {
            'us_east': (80, 120),
            'us_west': (120, 160),
            'europe': (5, 40),
            'asia': (200, 300)
        },
        # Add more regions...
    }
    
    def __init__(self, validator_location: str):
        """
        validator_location: 'us_east', 'europe', 'asia', etc.
        """
        self.validator_location = validator_location
    
    def measure_rtt(self, host: str, count: int = 4) -> float:
        """
        Measure average RTT to host using ping
        Returns RTT in milliseconds, or None if unreachable
        """
        try:
            result = subprocess.run(
                ['ping', '-c', str(count), host],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse ping output for average RTT
            # Example: "round-trip min/avg/max = 50.1/52.3/54.5 ms"
            match = re.search(r'avg[=/]\s*([\d.]+)', result.stdout)
            if match:
                return float(match.group(1))
            
        except (subprocess.TimeoutExpired, Exception) as e:
            print(f"Error measuring RTT to {host}: {e}")
        
        return None
    
    def verify_region_claim(
        self, 
        miner_ip: str, 
        claimed_region: str
    ) -> Tuple[float, str]:
        """
        Verify if miner's RTT is consistent with claimed region
        
        Returns: (signal_strength, status)
        signal_strength: 0.0 to 0.7 (Tier 3 max)
        status: human-readable verification status
        """
        # Measure RTT to miner
        rtt = self.measure_rtt(miner_ip)
        
        if rtt is None:
            return 0.0, "unreachable"
        
        # Get expected RTT range for this region from this validator
        region_expected = self.EXPECTED_RTT.get(claimed_region, {})
        expected_range = region_expected.get(self.validator_location)
        
        if not expected_range:
            return 0.5, f"unknown_region_or_validator"
        
        min_rtt, max_rtt = expected_range
        
        # Check if measured RTT falls within expected range
        if min_rtt <= rtt <= max_rtt:
            return 0.7, f"consistent (RTT={rtt}ms, expected {min_rtt}-{max_rtt}ms)"
        elif rtt < min_rtt * 0.7:
            # Suspiciously fast (likely same region, wrong claim)
            return 0.2, f"too_fast (RTT={rtt}ms, expected >{min_rtt}ms)"
        elif rtt > max_rtt * 1.3:
            # Much slower (VPN, proxy, or wrong region)
            return 0.3, f"too_slow (RTT={rtt}ms, expected <{max_rtt}ms)"
        else:
            # Borderline case
            return 0.5, f"borderline (RTT={rtt}ms, expected {min_rtt}-{max_rtt}ms)"

# Usage example
if __name__ == "__main__":
    # Validator in US East
    verifier = SimplifiedRTTVerifier(validator_location='us_east')
    
    # Check miner claiming to be in Iceland
    signal, status = verifier.verify_region_claim(
        miner_ip="1.2.3.4",
        claimed_region="iceland"
    )
    
    print(f"Signal strength: {signal}")
    print(f"Status: {status}")
```

---

## Conclusion

**RTT geolocation is feasible for Tier 3 (low-confidence) verification:**

✅ **Use it**: As fallback when provider APIs not available  
✅ **Keep it simple**: Basic multi-validator ping is sufficient  
✅ **Set expectations**: ~100km accuracy at best, region-level is realistic  
✅ **Implementation**: 1-2 weeks for basic version, reasonable effort  

❌ **Don't use it**: As sole high-confidence verification  
❌ **Don't expect**: Datacenter-level precision  
❌ **Don't over-invest**: Advanced trilateration not worth complexity for Tier 3  

**Recommended approach**: Implement Option A (Basic Multi-Validator RTT) for Tier 3. Validators in 2-3 locations measure RTT, check consistency with claimed region. Signal strength = 0.7 if consistent, lower if suspicious. Total implementation: ~200 lines Python, 1-2 weeks.
