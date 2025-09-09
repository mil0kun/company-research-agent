import asyncio
import logging
from typing import Dict, List

from ..classes import ResearchState
from ..nodes.researchers import (
    DirectLeadsAnalyst,
    PartnershipAnalyst,
    CommunityAnalyst,
    EventsAnalyst,
    InfluencerAnalyst
)

logger = logging.getLogger(__name__)

async def research(state: Dict) -> Dict:
    """
    Research node that runs multiple researcher agents in parallel.
    """
    state = ResearchState(state)
    websocket_manager = state.get('websocket_manager')
    job_id = state.get('job_id')
    
    logger.info("Starting research phase")
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="research_started",
            message="Starting lead research with multiple analysts",
            result={
                "step": "Research",
                "status": "started"
            }
        )
    
    # Initialize all the research agents
    direct_analyst = DirectLeadsAnalyst()
    partnership_analyst = PartnershipAnalyst()
    community_analyst = CommunityAnalyst()
    events_analyst = EventsAnalyst()
    influencer_analyst = InfluencerAnalyst()
    
    # Default prompts for each analyst
    direct_prompt = "Generate search queries to find direct leads (potential customers)"
    partnership_prompt = "Generate search queries to find potential business partners"
    community_prompt = "Generate search queries to find online communities and platforms"
    events_prompt = "Generate search queries to find relevant events and conferences"
    influencer_prompt = "Generate search queries to find industry influencers and media outlets"
    
    # Generate queries for each analyst
    direct_queries_task = direct_analyst.generate_queries(state, direct_prompt)
    partnership_queries_task = partnership_analyst.generate_queries(state, partnership_prompt)
    community_queries_task = community_analyst.generate_queries(state, community_prompt)
    events_queries_task = events_analyst.generate_queries(state, events_prompt)
    influencer_queries_task = influencer_analyst.generate_queries(state, influencer_prompt)
    
    # Run query generation in parallel
    direct_queries, partnership_queries, community_queries, events_queries, influencer_queries = await asyncio.gather(
        direct_queries_task,
        partnership_queries_task,
        community_queries_task,
        events_queries_task,
        influencer_queries_task
    )
    
    # Store the queries in the state
    state["direct_queries"] = direct_queries
    state["partnership_queries"] = partnership_queries
    state["community_queries"] = community_queries
    state["events_queries"] = events_queries
    state["influencer_queries"] = influencer_queries
    
    # Execute searches for each analyst in parallel
    direct_docs_task = direct_analyst.search_documents(state, direct_queries)
    partnership_docs_task = partnership_analyst.search_documents(state, partnership_queries)
    community_docs_task = community_analyst.search_documents(state, community_queries)
    events_docs_task = events_analyst.search_documents(state, events_queries)
    influencer_docs_task = influencer_analyst.search_documents(state, influencer_queries)
    
    # Run document searches in parallel
    direct_docs, partnership_docs, community_docs, events_docs, influencer_docs = await asyncio.gather(
        direct_docs_task,
        partnership_docs_task,
        community_docs_task,
        events_docs_task,
        influencer_docs_task
    )
    
    # Add documents to state
    state.merge_docs(direct_docs)
    state.merge_docs(partnership_docs)
    state.merge_docs(community_docs)
    state.merge_docs(events_docs)
    state.merge_docs(influencer_docs)
    
    # Update state with researcher results
    total_docs = len(state.get_docs())
    logger.info(f"Research phase completed with {total_docs} total documents")
    
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="research_completed",
            message=f"Lead research completed with {total_docs} total documents",
            result={
                "step": "Research",
                "status": "completed",
                "total_documents": total_docs,
                "direct_leads_count": len(direct_docs),
                "partnership_count": len(partnership_docs),
                "community_count": len(community_docs),
                "events_count": len(events_docs),
                "influencer_count": len(influencer_docs)
            }
        )
    
    return state
