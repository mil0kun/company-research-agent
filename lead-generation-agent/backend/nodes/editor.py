import logging
import os
import groq
from typing import Dict
from datetime import datetime

from ..classes import ResearchState

logger = logging.getLogger(__name__)

async def editor(state: Dict) -> Dict:
    """
    Editor node that compiles all briefings into a single, well-structured lead generation report.
    """
    state = ResearchState(state)
    websocket_manager = state.get('websocket_manager')
    job_id = state.get('job_id')
    
    logger.info("Starting editor phase")
    if websocket_manager and job_id:
        await websocket_manager.send_status_update(
            job_id=job_id,
            status="editor_started",
            message="Compiling final lead generation report",
            result={
                "step": "Editor",
                "status": "started"
            }
        )
    
    # Get briefings
    briefings = state.get("briefings", {})
    if not briefings:
        logger.warning("No briefings found in state")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="editor_warning",
                message="No briefings found to compile",
                result={
                    "step": "Editor",
                    "status": "warning",
                    "warning": "No briefings found"
                }
            )
        return state
    
    # Initialize Groq client for report compilation
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        logger.error("Missing GROQ_API_KEY for report compilation")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="editor_error",
                message="Missing API key for report compilation",
                result={
                    "step": "Editor",
                    "status": "error",
                    "error": "Missing GROQ_API_KEY"
                }
            )
        return state
    
    # Use mock Groq client
    from ..nodes.researchers.base import MockGroqClient
    groq_client = MockGroqClient(api_key=groq_key)
    
    # Get business context
    business_type = state.get("business_type", "Business")
    location = state.get("location", "")
    target_customers = state.get("target_customers", "")
    outreach_channels = state.get("outreach_channels", "")
    
    # Prepare briefing content
    combined_briefings = ""
    for analyst_type, briefing in briefings.items():
        name = briefing.get("name", analyst_type.replace("_", " ").title())
        content = briefing.get("content", "")
        if content:
            combined_briefings += f"## {name}\n\n{content}\n\n"
    
    if not combined_briefings:
        logger.error("No briefing content to compile")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="editor_error",
                message="No briefing content to compile",
                result={
                    "step": "Editor",
                    "status": "error",
                    "error": "No briefing content"
                }
            )
        return state
    
    # Generate the final report
    prompt = f"""Compile the following lead generation briefings into a comprehensive, well-structured report for a {business_type} business in {location}.

Target Customers:
{target_customers}

Outreach Channels:
{outreach_channels}

Briefings:
{combined_briefings}

Your task is to:
1. Create a professional, executive-summary style introduction that explains the purpose and scope of this lead generation report
2. Organize the briefings in a logical order, maintaining their content but improving the formatting and flow
3. Add an executive summary at the beginning that highlights the most promising leads across all categories
4. Add a "Next Steps" section at the end with a prioritized action plan
5. Format everything in clean, professional Markdown with consistent headings, bullet points, and styling

Make sure the report is action-oriented, with clear recommendations for follow-up on the most promising leads.
"""

    # Print the report generation prompt for debugging
    print(f"\n==== FINAL REPORT GENERATION PROMPT ====")
    print("System: You are a professional business development consultant compiling a comprehensive lead generation report.")
    print(f"User prompt (truncated to first 300 chars): {prompt[:300]}...")
    print("=" * 50)
    
    try:
        response = groq_client.chat.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a professional business development consultant compiling a comprehensive lead generation report."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=4096,
            stream=False
        )
        
        # Extract the report content
        report_content = response.choices[0].message.content if response.choices else ""
        
        if not report_content:
            logger.error("Failed to generate report content")
            if websocket_manager and job_id:
                await websocket_manager.send_status_update(
                    job_id=job_id,
                    status="editor_error",
                    message="Failed to generate report content",
                    result={
                        "step": "Editor",
                        "status": "error",
                        "error": "No report content generated"
                    }
                )
            return state
        
        # Add title and date
        current_date = datetime.now().strftime("%B %d, %Y")
        report_title = f"# Lead Generation Report: {business_type} in {location}\n\n**Generated on {current_date}**\n\n"
        final_report = report_title + report_content
        
        # Store the final report in state
        state["report"] = final_report
        
        logger.info(f"Generated final lead generation report ({len(final_report)} characters)")
        
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="editor_completed",
                message="Compiled final lead generation report",
                result={
                    "step": "Editor",
                    "status": "completed",
                    "report_length": len(final_report)
                }
            )
        
    except Exception as e:
        logger.error(f"Error compiling final report: {e}")
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="editor_error",
                message=f"Error compiling final report: {str(e)}",
                result={
                    "step": "Editor",
                    "status": "error",
                    "error": str(e)
                }
            )
    
    return state
