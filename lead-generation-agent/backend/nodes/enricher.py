import logging
import os
import groq
from typing import Dict, List
import asyncio

from ..classes import ResearchState

logger = logging.getLogger(__name__)

async def enricher(state: Dict) -> Dict:
    """
    Enricher node that extracts contact information and additional details from documents.
    """
    state = ResearchState(state)
    websocket_manager = state.get('websocket_manager')
    job_id = state.get('job_id')
    
    logger.info("Starting enricher phase")
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="enricher_started",
            message="Enriching lead research results with contact information",
            result={
                "step": "Enricher",
                "status": "started"
            }
        )
    
    # Get curated documents
    curated_docs = state.get("curated_docs", {})
    if not curated_docs:
        logger.warning("No curated documents found in state")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="enricher_warning",
                message="No curated documents found to enrich",
                result={
                    "step": "Enricher",
                    "status": "warning",
                    "warning": "No curated documents found"
                }
            )
        return state
    
    # Initialize Groq client for enrichment
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        logger.error("Missing GROQ_API_KEY for enrichment")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="enricher_error",
                message="Missing API key for enrichment",
                result={
                    "step": "Enricher",
                    "status": "error",
                    "error": "Missing GROQ_API_KEY"
                }
            )
        return state
    
    groq_client = groq.Client(api_key=groq_key)
    
    # Enrich documents by extracting contact information and additional details
    enriched_docs = {}
    enrichment_tasks = []
    
    for analyst_type, docs in curated_docs.items():
        enriched_docs[analyst_type] = {}
        
        # Process each document for this analyst type
        for url, doc in docs.items():
            # Create a task for each document enrichment
            task = enrich_document(
                groq_client=groq_client,
                doc=doc,
                analyst_type=analyst_type,
                business_type=state.get("business_type", ""),
                location=state.get("location", "")
            )
            enrichment_tasks.append((analyst_type, url, task))
    
    # Execute all enrichment tasks and collect results
    for analyst_type, url, task in enrichment_tasks:
        try:
            enriched_doc = await task
            enriched_docs[analyst_type][url] = enriched_doc
            
            # Update status periodically
            if websocket_manager and job_id:
                await websocket_manager.send_status_update(
                    job_id=job_id,
                    status="enricher_progress",
                    message=f"Enriched document: {enriched_doc.get('title', url)}",
                    result={
                        "step": "Enricher",
                        "status": "in_progress",
                        "url": url,
                        "analyst_type": analyst_type
                    }
                )
        except Exception as e:
            logger.error(f"Error enriching document {url}: {e}")
    
    # Store enriched documents in state
    state["enriched_docs"] = enriched_docs
    
    # Count enriched documents by analyst type
    counts = {analyst: len(docs) for analyst, docs in enriched_docs.items()}
    total_enriched = sum(counts.values())
    logger.info(f"Enriched {total_enriched} documents with contact information: {counts}")
    
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="enricher_completed",
            message=f"Enriched {total_enriched} lead research results with contact information",
            result={
                "step": "Enricher",
                "status": "completed",
                "total_enriched": total_enriched,
                "counts": counts
            }
        )
    
    return state

async def enrich_document(groq_client, doc, analyst_type, business_type, location):
    """
    Enrich a document with contact information and additional details.
    """
    content = doc.get("content", "")
    title = doc.get("title", "")
    url = doc.get("url", "")
    
    if not content:
        logger.warning(f"Empty content for document: {url}")
        return doc
    
    # Create enriched copy of the document
    enriched_doc = doc.copy()
    
    try:
        # Use Groq to extract contact information and additional details
        prompt = f"""Extract the most relevant information from this content about potential leads for a {business_type} business in {location}.

This content is from a {analyst_type} search.

Content:
{content}

Extract and format the following information:
1. Names of relevant companies, organizations, or individuals
2. Contact information (emails, phone numbers, websites)
3. Social media profiles or handles
4. Physical addresses if available
5. Brief description of why this is a good lead
6. Any other relevant details for lead generation

Format your response as structured information that can be easily parsed. Only include information that is actually present in the content.
"""

        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a lead generation assistant that extracts contact information and relevant details from web content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=1024,
            stream=False
        )
        
        # Extract the enriched content
        enriched_content = response.choices[0].message.content if response.choices else ""
        
        # Add the enriched content to the document
        enriched_doc["enriched_content"] = enriched_content
        enriched_doc["analyst_type"] = analyst_type
        
        return enriched_doc
        
    except Exception as e:
        logger.error(f"Error in document enrichment for {url}: {e}")
        enriched_doc["enrichment_error"] = str(e)
        return enriched_doc
