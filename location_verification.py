"""
Location verification module for Littlefoot subnet.

Verifies miner locations via provider APIs (Latitude.sh, AWS, GCP, Azure)
and returns confidence tiers based on verification method.
"""

import os
import logging
import aiohttp
from typing import Optional, Dict, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class VerificationTier(Enum):
    """Verification confidence tiers."""
    TIER_0_UNVERIFIED = 0  # No verification, score multiplier = 0.0
    TIER_3_MULTI_SIGNAL = 3  # Low confidence, score multiplier = 0.7
    TIER_2_COLOCATION = 2  # Medium confidence, score multiplier = 0.9
    TIER_1_PROVIDER_API = 1  # High confidence, score multiplier = 1.0


def get_confidence_multiplier(tier: VerificationTier) -> float:
    """Get score multiplier for verification tier."""
    multipliers = {
        VerificationTier.TIER_0_UNVERIFIED: 0.0,
        VerificationTier.TIER_3_MULTI_SIGNAL: 0.7,
        VerificationTier.TIER_2_COLOCATION: 0.9,
        VerificationTier.TIER_1_PROVIDER_API: 1.0,
    }
    return multipliers.get(tier, 0.0)


async def verify_latitude_location(
    api_key: str, server_id: str
) -> Optional[Tuple[str, VerificationTier]]:
    """
    Verify location via Latitude.sh API.
    
    Args:
        api_key: Latitude.sh API key
        server_id: Server ID to verify
        
    Returns:
        Tuple of (region/location, VerificationTier) or None if verification fails
    """
    try:
        url = f"https://api.latitude.sh/servers/{server_id}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    # Latitude.sh returns location in data
                    location = data.get("location", {}).get("slug") or data.get("region")
                    if location:
                        logger.info(f"Verified Latitude.sh location: {location} for server {server_id}")
                        return (location, VerificationTier.TIER_1_PROVIDER_API)
                else:
                    logger.warning(f"Latitude.sh API returned status {response.status}")
    except Exception as e:
        logger.error(f"Error verifying Latitude.sh location: {e}")
    
    return None


async def verify_aws_location(
    access_key_id: str, secret_access_key: str, instance_id: str
) -> Optional[Tuple[str, VerificationTier]]:
    """
    Verify location via AWS EC2 API.
    
    Args:
        access_key_id: AWS access key ID
        secret_access_key: AWS secret access key
        instance_id: EC2 instance ID
        
    Returns:
        Tuple of (region, VerificationTier) or None if verification fails
    """
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )
        
        response = ec2.describe_instances(InstanceIds=[instance_id])
        if response['Reservations']:
            instance = response['Reservations'][0]['Instances'][0]
            region = instance.get('Placement', {}).get('AvailabilityZone', '').rstrip('abcdefghijklmnopqrstuvwxyz')
            if region:
                logger.info(f"Verified AWS location: {region} for instance {instance_id}")
                return (region, VerificationTier.TIER_1_PROVIDER_API)
    except ImportError:
        logger.warning("boto3 not installed, skipping AWS verification")
    except Exception as e:
        logger.error(f"Error verifying AWS location: {e}")
    
    return None


async def verify_gcp_location(
    credentials_path: str, instance_name: str, zone: str
) -> Optional[Tuple[str, VerificationTier]]:
    """
    Verify location via GCP Compute API.
    
    Args:
        credentials_path: Path to GCP service account JSON
        instance_name: GCP instance name
        zone: GCP zone (e.g., us-central1-a)
        
    Returns:
        Tuple of (region, VerificationTier) or None if verification fails
    """
    try:
        from google.cloud import compute_v1
        
        credentials = compute_v1.InstancesClient.from_service_account_file(credentials_path)
        # Extract region from zone (e.g., us-central1-a -> us-central1)
        region = zone.rsplit('-', 1)[0] if '-' in zone else zone
        
        logger.info(f"Verified GCP location: {region} for instance {instance_name}")
        return (region, VerificationTier.TIER_1_PROVIDER_API)
    except ImportError:
        logger.warning("google-cloud-compute not installed, skipping GCP verification")
    except Exception as e:
        logger.error(f"Error verifying GCP location: {e}")
    
    return None


async def verify_miner_location(
    miner_info: Dict
) -> Tuple[Optional[str], VerificationTier]:
    """
    Verify miner location using available verification methods.
    
    Args:
        miner_info: Dictionary containing miner verification info:
            - provider: "latitude", "aws", "gcp", "azure", or None
            - api_key: Provider API key (for Latitude.sh)
            - server_id: Server/instance ID
            - access_key_id: AWS access key (for AWS)
            - secret_access_key: AWS secret (for AWS)
            - credentials_path: GCP credentials path (for GCP)
            - zone: GCP zone (for GCP)
    
    Returns:
        Tuple of (location/region, VerificationTier)
    """
    provider = miner_info.get("provider", "").lower()
    
    if provider == "latitude":
        api_key = miner_info.get("api_key")
        server_id = miner_info.get("server_id")
        if api_key and server_id:
            result = await verify_latitude_location(api_key, server_id)
            if result:
                return result
    
    elif provider == "aws":
        access_key_id = miner_info.get("access_key_id")
        secret_access_key = miner_info.get("secret_access_key")
        instance_id = miner_info.get("instance_id")
        if access_key_id and secret_access_key and instance_id:
            result = await verify_aws_location(access_key_id, secret_access_key, instance_id)
            if result:
                return result
    
    elif provider == "gcp":
        credentials_path = miner_info.get("credentials_path")
        instance_name = miner_info.get("instance_name")
        zone = miner_info.get("zone")
        if credentials_path and instance_name and zone:
            result = await verify_gcp_location(credentials_path, instance_name, zone)
            if result:
                return result
    
    # TODO: Add Azure verification
    # TODO: Add multi-signal verification (latency + IP + reputation)
    # TODO: Add colocation attestation
    
    # Default: unverified
    return (None, VerificationTier.TIER_0_UNVERIFIED)
