import logging
from typing import Dict, List

from .base import BaseLeadResearcher

logger = logging.getLogger(__name__)

class EventsAnalyst(BaseLeadResearcher):
    """
    Analyst focused on finding relevant events, conferences, or trade shows.
    """
    def __init__(self):
        super().__init__()
        self.analyst_type = "events_analyst"
        
    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""As an Events Analyst, your task is to generate search queries that will help find relevant events, 
conferences, trade shows, and expos for a {business_type} business in {location}.

Who to Reach Out To:
{outreach_channels}

Your search queries should:
- Focus on finding upcoming industry events, expos, trade shows, and conferences
- Target events in {location} or nearby areas
- Look for events mentioned in the outreach channels
- Include the current or upcoming year ({year} or {year+1})
- Find event organizers and their contact information
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.
"""
