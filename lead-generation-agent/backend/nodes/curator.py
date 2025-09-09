import logging
from typing import Dict, List

from ..classes import ResearchState

logger = logging.getLogger(__name__)

async def curator(state: Dict) -> Dict:
    """
    Curator node that filters documents based on relevance.
    """
    state = ResearchState(state)
    websocket_manager = state.get('websocket_manager')
    job_id = state.get('job_id')
    
    logger.info("Starting curator phase")
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="curator_started",
            message="Curating lead research results by relevance",
            result={
                "step": "Curator",
                "status": "started"
            }
        )
    
    # Get organized documents
    organized_docs = state.get("organized_docs", {})
    if not organized_docs:
        logger.warning("No organized documents found in state")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="curator_warning",
                message="No organized documents found to curate",
                result={
                    "step": "Curator",
                    "status": "warning",
                    "warning": "No organized documents found"
                }
            )
        return state
    
    # Filter documents by Tavily score to get the most relevant ones
    score_threshold = 0.4  # Minimum relevance score
    curated_docs = {}
    
    for analyst_type, docs in organized_docs.items():
        # Sort docs by score in descending order
        sorted_docs = sorted(docs.items(), key=lambda x: x[1].get("score", 0), reverse=True)
        
        # Take top N documents with score above threshold
        top_docs = {}
        for url, doc in sorted_docs:
            if doc.get("score", 0) >= score_threshold and len(top_docs) < 5:
                top_docs[url] = doc
        
        # If we have at least one document above threshold, add to curated docs
        if top_docs:
            curated_docs[analyst_type] = top_docs
    
    # Store curated documents in state
    state["curated_docs"] = curated_docs
    
    # Count curated documents by analyst type
    counts = {analyst: len(docs) for analyst, docs in curated_docs.items()}
    total_curated = sum(counts.values())
    logger.info(f"Curated {total_curated} documents by relevance: {counts}")
    
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="curator_completed",
            message=f"Curated {total_curated} lead research results by relevance",
            result={
                "step": "Curator",
                "status": "completed",
                "total_curated": total_curated,
                "counts": counts
            }
        )
    
    return state
