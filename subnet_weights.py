"""
Subnet weight fetcher for Littlefoot subnet.

Fetches miner weights from target subnets (Lium SN51, Chutes SN64)
to calculate W_i (subnet weight) in the Littlefoot scoring function.
"""

import os
import logging
import bittensor as bt
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def get_subnet_weight(
    miner_hotkey: str,
    netuid: int,
    subtensor: bt.Subtensor,
    metagraph: Optional[bt.Metagraph] = None
) -> float:
    """
    Get a miner's weight on a target subnet.
    
    Args:
        miner_hotkey: Miner's hotkey SS58 address
        netuid: Target subnet netuid
        subtensor: Subtensor instance
        metagraph: Optional metagraph (will be synced if not provided)
        
    Returns:
        Miner's normalized weight on the target subnet (0.0 to 1.0)
    """
    try:
        # Sync metagraph if not provided
        if metagraph is None:
            metagraph = bt.Metagraph(netuid=netuid, network=subtensor.network)
            metagraph.sync(subtensor=subtensor)
        
        # Find miner UID
        if miner_hotkey not in metagraph.hotkeys:
            logger.debug(f"Miner {miner_hotkey} not found on subnet {netuid}")
            return 0.0
        
        miner_uid = metagraph.hotkeys.index(miner_hotkey)
        
        # Get miner's stake/emission weight
        # The weight is proportional to the miner's stake + validator weights
        # We use the miner's total stake as a proxy for their subnet weight
        miner_stake = metagraph.S[miner_uid].item() if hasattr(metagraph, 'S') else 0.0
        
        # Normalize by total subnet stake
        total_stake = metagraph.S.sum().item() if hasattr(metagraph, 'S') else 1.0
        normalized_weight = miner_stake / total_stake if total_stake > 0 else 0.0
        
        logger.debug(
            f"Miner {miner_hotkey} on subnet {netuid}: "
            f"stake={miner_stake:.6f}, normalized_weight={normalized_weight:.6f}"
        )
        
        return normalized_weight
        
    except Exception as e:
        logger.error(f"Error fetching subnet weight for {miner_hotkey} on {netuid}: {e}")
        return 0.0


def get_max_subnet_weight(
    miner_hotkey: str,
    target_netuids: list[int],
    subtensor: bt.Subtensor
) -> float:
    """
    Get the maximum weight across all target subnets for a miner.
    
    This implements the logic: W_i = max(weight_on_lium, weight_on_chutes, ...)
    
    Args:
        miner_hotkey: Miner's hotkey SS58 address
        target_netuids: List of target subnet netuids (e.g., [51, 64])
        subtensor: Subtensor instance
        
    Returns:
        Maximum normalized weight across all target subnets
    """
    weights = []
    for netuid in target_netuids:
        weight = get_subnet_weight(miner_hotkey, netuid, subtensor)
        if weight > 0:
            weights.append(weight)
    
    if not weights:
        logger.debug(f"Miner {miner_hotkey} not found on any target subnets")
        return 0.0
    
    max_weight = max(weights)
    logger.debug(
        f"Miner {miner_hotkey} max weight across target subnets: {max_weight:.6f}"
    )
    return max_weight
