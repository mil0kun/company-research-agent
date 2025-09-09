import logging
import os
import groq
from typing import Dict, List

from ..classes import ResearchState

logger = logging.getLogger(__name__)

async def briefing(state: Dict) -> Dict:
    """
    Briefing node that generates concise summaries for each lead category.
    """
    state = ResearchState(state)
    websocket_manager = state.get('websocket_manager')
    job_id = state.get('job_id')
    
    logger.info("Starting briefing phase")
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="briefing_started",
            message="Generating lead briefings for each category",
            result={
                "step": "Briefing",
                "status": "started"
            }
        )
    
    # Get enriched documents
    enriched_docs = state.get("enriched_docs", {})
    if not enriched_docs:
        logger.warning("No enriched documents found in state")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="briefing_warning",
                message="No enriched documents found to brief",
                result={
                    "step": "Briefing",
                    "status": "warning",
                    "warning": "No enriched documents found"
                }
            )
        return state
    
    # Initialize Groq client for briefing
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        logger.error("Missing GROQ_API_KEY for briefing")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="briefing_error",
                message="Missing API key for briefing",
                result={
                    "step": "Briefing",
                    "status": "error",
                    "error": "Missing GROQ_API_KEY"
                }
            )
        return state
    
    groq_client = groq.Client(api_key=groq_key)
    
    # Generate briefings for each analyst type
    briefings = {}
    
    # Map analyst types to human-readable names
    analyst_names = {
        "direct_leads_analyst": "Direct Leads",
        "partnership_analyst": "Potential Partners",
        "community_analyst": "Communities & Platforms",
        "events_analyst": "Events & Conferences",
        "influencer_analyst": "Influencers & Media"
    }
    
    # Get business context
    business_type = state.get("business_type", "Business")
    location = state.get("location", "")
    target_customers = state.get("target_customers", "")
    outreach_channels = state.get("outreach_channels", "")
    
    # Process each analyst type
    for analyst_type, docs in enriched_docs.items():
        if not docs:
            logger.warning(f"No documents found for analyst type: {analyst_type}")
            continue
        
        # Create a prompt for this analyst type
        category_name = analyst_names.get(analyst_type, analyst_type.replace("_", " ").title())
        
        # Combine all enriched content for this analyst type
        combined_content = ""
        for url, doc in docs.items():
            title = doc.get("title", "")
            enriched_content = doc.get("enriched_content", "")
            
            if title and enriched_content:
                combined_content += f"Source: {title}\n\n{enriched_content}\n\n---\n\n"
            elif enriched_content:
                combined_content += f"Source: {url}\n\n{enriched_content}\n\n---\n\n"
        
        if not combined_content:
            logger.warning(f"No content to generate briefing for {category_name}")
            continue
        
        # Generate a briefing for this category
        prompt = f"""Create a concise, actionable briefing about {category_name} for a {business_type} business in {location}.

Target Customers:
{target_customers}

Outreach Channels:
{outreach_channels}

Information from research:
{combined_content}

Your task is to compile this information into a clear, structured briefing that:
1. Starts with a brief overview of this lead category
2. Lists the specific leads found with their contact information
3. Provides concrete next steps or outreach strategies
4. Formats the information in clear Markdown with proper headings and bullet points

Focus on actionable information that can be used for lead generation. Be specific and practical.
"""
        
        try:
            response = groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a lead generation specialist creating concise, actionable briefings for business development."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=2048,
                stream=False
            )
            
            # Extract the briefing content
            briefing_content = response.choices[0].message.content if response.choices else ""
            
            if briefing_content:
                briefings[analyst_type] = {
                    "name": category_name,
                    "content": briefing_content
                }
                
                logger.info(f"Generated briefing for {category_name}")
                
                if websocket_manager and job_id:
                    await websocket_manager.send_status_update(
                        job_id=job_id,
                        status="briefing_progress",
                        message=f"Generated briefing for {category_name}",
                        result={
                            "step": "Briefing",
                            "status": "in_progress",
                            "category": category_name
                        }
                    )
            
        except Exception as e:
            logger.error(f"Error generating briefing for {category_name}: {e}")
    
    # Store briefings in state
    state["briefings"] = briefings
    
    # Count briefings
    total_briefings = len(briefings)
    logger.info(f"Generated {total_briefings} briefings")
    
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="briefing_completed",
            message=f"Generated {total_briefings} lead briefings",
            result={
                "step": "Briefing",
                "status": "completed",
                "total_briefings": total_briefings,
                "categories": list(briefings.keys())
            }
        )
    
    return state
