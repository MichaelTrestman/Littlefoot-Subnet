"""
Carbon intensity lookup module for Littlefoot subnet.

Maps geographic locations to carbon intensity values (gCO2/kWh).
"""

import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

# Carbon intensity database (gCO2/kWh)
# Based on average grid carbon intensity by region
# Sources: Electricity Maps, IEA, national grid data
CARBON_INTENSITY_DB: Dict[str, float] = {
    # Low-carbon regions (hydro, nuclear, geothermal)
    "iceland": 28,
    "is": 28,  # ISO code
    "quebec": 25,
    "qc": 25,
    "norway": 30,
    "no": 30,
    "france": 50,
    "fr": 50,
    
    # Medium-carbon regions (mix of renewables and fossil)
    "oregon": 250,
    "or": 250,
    "washington": 200,
    "wa": 200,
    "california": 300,
    "ca": 300,
    "virginia": 380,
    "va": 380,
    "texas": 450,
    "tx": 450,
    "ohio": 400,
    "oh": 400,
    
    # High-carbon regions (coal-heavy)
    "poland": 900,
    "pl": 900,
    "germany": 350,
    "de": 350,
    "china": 600,
    "cn": 600,
    
    # AWS regions (mapped to approximate carbon intensity)
    "us-east-1": 380,  # Virginia
    "us-east-2": 400,  # Ohio
    "us-west-1": 250,  # Oregon
    "us-west-2": 200,  # Washington
    "us-west-3": 300,  # California
    "eu-west-1": 200,  # Ireland (approximate)
    "eu-central-1": 350,  # Germany
    "ap-southeast-1": 500,  # Singapore (approximate)
    
    # GCP regions
    "us-central1": 400,  # Iowa (approximate)
    "us-east1": 380,  # South Carolina (approximate)
    "us-west1": 250,  # Oregon
    "europe-west1": 200,  # Belgium (approximate)
    "europe-west4": 350,  # Netherlands (approximate)
    
    # Latitude.sh regions
    "sjc": 300,  # San Jose, California
    "nyc": 380,  # New York (approximate)
    "ams": 350,  # Amsterdam
    "fra": 350,  # Frankfurt
    "lon": 250,  # London (approximate)
}


def normalize_location(location: str) -> str:
    """Normalize location string for lookup."""
    return location.lower().strip().replace("_", "-").replace(" ", "-")


def get_carbon_intensity(location: str) -> Optional[float]:
    """
    Get carbon intensity for a location.
    
    Args:
        location: Location identifier (region, country, city, etc.)
        
    Returns:
        Carbon intensity in gCO2/kWh, or None if not found
    """
    if not location:
        return None
    
    normalized = normalize_location(location)
    
    # Try exact match first
    if normalized in CARBON_INTENSITY_DB:
        intensity = CARBON_INTENSITY_DB[normalized]
        logger.debug(f"Found carbon intensity for {location}: {intensity} gCO2/kWh")
        return intensity
    
    # Try partial matches (e.g., "us-east-1a" -> "us-east-1")
    for key, value in CARBON_INTENSITY_DB.items():
        if normalized.startswith(key) or key in normalized:
            intensity = value
            logger.debug(f"Matched carbon intensity for {location} via {key}: {intensity} gCO2/kWh")
            return intensity
    
    logger.warning(f"Carbon intensity not found for location: {location}")
    return None


def get_default_carbon_intensity() -> float:
    """
    Get default carbon intensity for unverified locations.
    Uses global average (~475 gCO2/kWh).
    """
    return 475.0
