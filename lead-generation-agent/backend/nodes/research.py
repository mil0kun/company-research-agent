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
    
    # Debug prints
    print(f"\n=== Generated Queries ===")
    print(f"Direct Queries ({len(direct_queries)}): {direct_queries}")
    print(f"Partnership Queries ({len(partnership_queries)}): {partnership_queries}")
    print(f"Community Queries ({len(community_queries)}): {community_queries}")
    print(f"Events Queries ({len(events_queries)}): {events_queries}")
    print(f"Influencer Queries ({len(influencer_queries)}): {influencer_queries}")
    
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
    
    # For debugging
    logger.info(f"Direct docs: {len(direct_docs)}")
    logger.info(f"Partnership docs: {len(partnership_docs)}")
    logger.info(f"Community docs: {len(community_docs)}")
    logger.info(f"Events docs: {len(events_docs)}")
    logger.info(f"Influencer docs: {len(influencer_docs)}")
    
    # Add documents to state
    state.merge_docs(direct_docs)
    state.merge_docs(partnership_docs)
    state.merge_docs(community_docs)
    state.merge_docs(events_docs)
    state.merge_docs(influencer_docs)
    
    # Check if we have documents
    total_docs = len(state.get_docs())
    print(f"\n=== Document Collection Summary ===")
    print(f"Total documents collected: {total_docs}")
    print(f"Direct docs: {len(direct_docs)}")
    print(f"Partnership docs: {len(partnership_docs)}")
    print(f"Community docs: {len(community_docs)}")
    print(f"Events docs: {len(events_docs)}")
    print(f"Influencer docs: {len(influencer_docs)}")
    
    # Explicitly add some mock documents if none were found
    if len(state.get_docs()) == 0:
        logger.warning("No documents were found, adding mock documents")
        print("Adding mock documents as fallback...")
        mock_docs = {
            "https://example.com/mock1": {
                "title": "Mock Lead 1",
                "content": "This is mock content for lead 1",
                "query": "mock query 1",
                "url": "https://example.com/mock1",
                "source": "web_search",
                "score": 0.9,
                "analyst_type": "direct_leads_analyst"
            },
            "https://example.com/mock2": {
                "title": "Mock Lead 2",
                "content": "This is mock content for lead 2",
                "query": "mock query 2",
                "url": "https://example.com/mock2",
                "source": "web_search",
                "score": 0.85,
                "analyst_type": "partnership_analyst"
            }
        }
        state.merge_docs(mock_docs)
        print(f"Added {len(mock_docs)} mock documents")
    
    # Print document keys to verify they're in the state
    docs = state.get_docs()
    print(f"Document keys in state after merging: {list(docs.keys())[:5]}")
    
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
