import logging
from typing import Dict

from ..classes import ResearchState

logger = logging.getLogger(__name__)

async def collector(state: Dict) -> Dict:
    """
    Collector node that organizes the documents by analyst type.
    """
    state = ResearchState(state)
    websocket_manager = state.get('websocket_manager')
    job_id = state.get('job_id')
    
    logger.info("Starting collector phase")
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="collector_started",
            message="Organizing lead research results",
            result={
                "step": "Collector",
                "status": "started"
            }
        )
    
    # Get all documents and organize by analyst type
    all_docs = state.get_docs()
    if not all_docs:
        logger.warning("No documents found in state")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="collector_warning",
                message="No documents found to organize",
                result={
                    "step": "Collector",
                    "status": "warning",
                    "warning": "No documents found"
                }
            )
        return state
    
    # Organize documents by analyst type
    analyst_docs = {}
    for url, doc in all_docs.items():
        analyst_type = doc.get("analyst_type", "unknown")
        if analyst_type not in analyst_docs:
            analyst_docs[analyst_type] = {}
        analyst_docs[analyst_type][url] = doc
    
    # Store organized documents in state
    state["organized_docs"] = analyst_docs
    
    # Count documents by analyst type
    counts = {analyst: len(docs) for analyst, docs in analyst_docs.items()}
    logger.info(f"Documents organized by analyst type: {counts}")
    
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="collector_completed",
            message="Lead research results organized",
            result={
                "step": "Collector",
                "status": "completed",
                "counts": counts
            }
        )
    
    return state
