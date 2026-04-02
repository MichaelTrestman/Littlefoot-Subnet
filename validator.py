"""
Littlefoot Subnet Validator

A Geographic Incentive Layer for Sustainable AI Compute.

Scoring function: S_i = W_i / (C_i * σ_i)
where:
  - W_i = Subnet Weight (performance on underlying subnet like Lium/Chutes)
  - C_i = Carbon Intensity (gCO2/kWh) for verified location
  - σ_i = Signal Strength (verification confidence multiplier ∈ (0, 1])
"""

import os
import time
import json
import click
import logging
import bittensor as bt
from bittensor_wallet import Wallet
import threading
import sys
from typing import Dict, List, Tuple, Optional
import numpy as np

from location_verification import (
    verify_miner_location,
    VerificationTier,
    get_confidence_multiplier,
)
from carbon_intensity import get_carbon_intensity, get_default_carbon_intensity
from subnet_weights import get_max_subnet_weight

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

HEARTBEAT_TIMEOUT = 600  # seconds


def heartbeat_monitor(last_heartbeat, stop_event):
    """Monitor heartbeat and restart if validator stalls."""
    while not stop_event.is_set():
        time.sleep(5)
        if time.time() - last_heartbeat[0] > HEARTBEAT_TIMEOUT:
            logger.error("No heartbeat detected in the last 600 seconds. Restarting process.")
            logging.shutdown()
            os.execv(sys.executable, [sys.executable] + sys.argv)


def calculate_littlefoot_score(
    subnet_weight: float,
    carbon_intensity: float,
    signal_strength: float
) -> float:
    """
    Calculate Littlefoot efficiency score.
    
    Formula: S_i = W_i / (C_i * σ_i)
    
    Lower carbon intensity and higher verification confidence = higher score.
    
    Args:
        subnet_weight: W_i - Miner's weight on target subnet
        carbon_intensity: C_i - Grid carbon intensity (gCO2/kWh)
        signal_strength: σ_i - Verification confidence multiplier (0.0 to 1.0)
        
    Returns:
        Littlefoot score (higher = more efficient/cleaner)
    """
    if carbon_intensity <= 0 or signal_strength <= 0:
        return 0.0
    
    # Avoid division by zero
    denominator = carbon_intensity * signal_strength
    if denominator == 0:
        return 0.0
    
    score = subnet_weight / denominator
    return score


async def query_miner_verification_info(
    miner_hotkey: str,
    miner_uid: int,
    metagraph: bt.Metagraph
) -> Optional[Dict]:
    """
    Query miner for location verification information.
    
    In a real implementation, this would query the miner's endpoint.
    For MVP, we'll use chain commits or a simple query protocol.
    
    Args:
        miner_hotkey: Miner's hotkey
        miner_uid: Miner's UID
        metagraph: Current metagraph
        
    Returns:
        Dictionary with verification info, or None
    """
    # TODO: Implement actual miner query protocol
    # For now, return None (miners will need to commit this info on-chain)
    # In production, miners would expose an endpoint with their verification info
    return None


def get_miner_verification_from_commit(
    miner_hotkey: str,
    metagraph: bt.Metagraph
) -> Optional[Dict]:
    """
    Get miner verification info from chain commit.
    
    Miners commit their verification info on-chain (provider, API keys, etc.)
    """
    # TODO: Parse miner commits from metagraph
    # For MVP, return None (will be implemented based on commit format)
    return None


async def score_miners(
    metagraph: bt.Metagraph,
    subtensor: bt.Subtensor,
    target_netuids: List[int]
) -> Dict[int, float]:
    """
    Score all miners using Littlefoot scoring function.
    
    Args:
        metagraph: Current subnet metagraph
        subtensor: Subtensor instance
        target_netuids: List of target subnet netuids (e.g., [51, 64])
        
    Returns:
        Dictionary mapping UID to Littlefoot score
    """
    scores = {}
    
    for uid in range(metagraph.n):
        miner_hotkey = metagraph.hotkeys[uid]
        
        try:
            # 1. Get subnet weight (W_i)
            subnet_weight = get_max_subnet_weight(
                miner_hotkey, target_netuids, subtensor
            )
            
            if subnet_weight == 0:
                # Miner not active on target subnets, skip
                scores[uid] = 0.0
                continue
            
            # 2. Get verification info and location
            verification_info = get_miner_verification_from_commit(miner_hotkey, metagraph)
            if verification_info is None:
                # Try querying miner directly
                verification_info = await query_miner_verification_info(
                    miner_hotkey, uid, metagraph
                )
            
            if verification_info is None:
                # No verification info available
                logger.debug(f"Miner {uid} ({miner_hotkey[:8]}...): No verification info")
                scores[uid] = 0.0
                continue
            
            # 3. Verify location
            location, verification_tier = await verify_miner_location(verification_info)
            
            if location is None:
                # Location verification failed
                logger.debug(f"Miner {uid} ({miner_hotkey[:8]}...): Location verification failed")
                scores[uid] = 0.0
                continue
            
            # 4. Get carbon intensity (C_i)
            carbon_intensity = get_carbon_intensity(location)
            if carbon_intensity is None:
                # Use default if location not found
                carbon_intensity = get_default_carbon_intensity()
                logger.warning(
                    f"Miner {uid}: Location {location} not in carbon DB, using default {carbon_intensity}"
                )
            
            # 5. Get signal strength (σ_i)
            signal_strength = get_confidence_multiplier(verification_tier)
            
            # 6. Calculate Littlefoot score
            score = calculate_littlefoot_score(
                subnet_weight, carbon_intensity, signal_strength
            )
            
            scores[uid] = score
            
            logger.info(
                f"Miner {uid} ({miner_hotkey[:8]}...): "
                f"W={subnet_weight:.4f}, C={carbon_intensity:.1f}, σ={signal_strength:.2f}, "
                f"Score={score:.6f}, Location={location}, Tier={verification_tier.name}"
            )
            
        except Exception as e:
            logger.error(f"Error scoring miner {uid} ({miner_hotkey[:8]}...): {e}")
            scores[uid] = 0.0
    
    return scores


def normalize_weights(scores: Dict[int, float]) -> Tuple[List[int], List[float]]:
    """
    Normalize scores to weights for chain submission.
    
    Formula: Ŵ_i = S_i / Σ S_j
    
    Args:
        scores: Dictionary mapping UID to raw score
        
    Returns:
        Tuple of (uids, normalized_weights) ready for chain submission
    """
    uids = list(scores.keys())
    raw_scores = [scores[uid] for uid in uids]
    
    total_score = sum(raw_scores)
    if total_score == 0:
        # No valid scores, set equal weights
        logger.warning("No valid scores, setting equal weights")
        weights = [1.0 / len(uids)] * len(uids) if uids else []
    else:
        # Normalize
        weights = [score / total_score for score in raw_scores]
    
    return uids, weights


@click.command()
@click.option(
    "--network",
    default=lambda: os.getenv("NETWORK", "finney"),
    help="Network to connect to (finney, test, local)",
)
@click.option(
    "--netuid",
    type=int,
    default=lambda: int(os.getenv("NETUID", "1")),
    help="Subnet netuid",
)
@click.option(
    "--coldkey",
    default=lambda: os.getenv("WALLET_NAME", "default"),
    help="Wallet name",
)
@click.option(
    "--hotkey",
    default=lambda: os.getenv("HOTKEY_NAME", "default"),
    help="Hotkey name",
)
@click.option(
    "--lium-netuid",
    type=int,
    default=lambda: int(os.getenv("LIUM_NETUID", "51")),
    help="Lium subnet netuid",
)
@click.option(
    "--chutes-netuid",
    type=int,
    default=lambda: int(os.getenv("CHUTES_NETUID", "64")),
    help="Chutes subnet netuid",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
    default=lambda: os.getenv("LOG_LEVEL", "INFO"),
    help="Logging level",
)
def main(
    network: str,
    netuid: int,
    coldkey: str,
    hotkey: str,
    lium_netuid: int,
    chutes_netuid: int,
    log_level: str,
):
    """Run the Littlefoot subnet validator."""
    # Set log level
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    logger.info(
        f"Starting Littlefoot validator on network={network}, netuid={netuid}, "
        f"target_subnets=[{lium_netuid}, {chutes_netuid}]"
    )
    
    # Heartbeat setup
    last_heartbeat = [time.time()]
    stop_event = threading.Event()
    heartbeat_thread = threading.Thread(
        target=heartbeat_monitor, args=(last_heartbeat, stop_event), daemon=True
    )
    heartbeat_thread.start()
    
    target_netuids = [lium_netuid, chutes_netuid]
    
    try:
        # Initialize wallet, subtensor, and metagraph
        wallet = Wallet(name=coldkey, hotkey=hotkey)
        subtensor = bt.Subtensor(network=network)
        metagraph = bt.Metagraph(netuid=netuid, network=network)
        
        # Sync metagraph
        metagraph.sync(subtensor=subtensor)
        logger.info(f"Metagraph synced: {metagraph.n} neurons at block {metagraph.block}")
        
        # Get our UID
        my_hotkey = wallet.hotkey.ss58_address
        if my_hotkey not in metagraph.hotkeys:
            logger.error(f"Hotkey {my_hotkey} not registered on netuid {netuid}")
            stop_event.set()
            return
        my_uid = metagraph.hotkeys.index(my_hotkey)
        logger.info(f"Validator UID: {my_uid}")
        
        # Get tempo for this subnet
        tempo = subtensor.get_subnet_hyperparameters(netuid).tempo
        logger.info(f"Subnet tempo: {tempo} blocks")
        
        last_weight_block = 0
        
        # Main validator loop
        while True:
            try:
                # Sync metagraph
                metagraph.sync(subtensor=subtensor)
                current_block = subtensor.get_current_block()
                
                # Heartbeat: update the last heartbeat timestamp
                last_heartbeat[0] = time.time()
                
                # Check if we should set weights (once per tempo)
                blocks_since_last = current_block - last_weight_block
                if blocks_since_last >= tempo:
                    logger.info(f"Block {current_block}: Setting weights (tempo={tempo})")
                    
                    # Score all miners
                    import asyncio
                    scores = asyncio.run(score_miners(metagraph, subtensor, target_netuids))
                    
                    # Normalize scores to weights
                    uids, weights = normalize_weights(scores)
                    
                    if not uids:
                        logger.warning("No miners to weight, skipping weight setting")
                    else:
                        logger.info(
                            f"Setting weights for {len(uids)} miners "
                            f"(total score: {sum(scores.values()):.6f})"
                        )
                        
                        # Set weights on chain
                        success = subtensor.set_weights(
                            wallet=wallet,
                            netuid=netuid,
                            uids=uids,
                            weights=weights,
                            wait_for_inclusion=True,
                            wait_for_finalization=False,
                        )
                        
                        if success:
                            logger.info(f"Successfully set weights for {len(uids)} neurons")
                            last_weight_block = current_block
                        else:
                            logger.warning("Failed to set weights")
                else:
                    logger.debug(
                        f"Block {current_block}: Waiting for tempo "
                        f"({blocks_since_last}/{tempo} blocks)"
                    )
                
                # Sleep for ~1 block
                time.sleep(12)
                
            except KeyboardInterrupt:
                logger.info("Validator stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in validator loop: {e}", exc_info=True)
                time.sleep(12)
    finally:
        stop_event.set()
        heartbeat_thread.join(timeout=2)


if __name__ == "__main__":
    main()
