import logging
from typing import Dict, List

from .base import BaseLeadResearcher

logger = logging.getLogger(__name__)

class PartnershipAnalyst(BaseLeadResearcher):
    """
    Analyst focused on finding potential partners who serve the same audience.
    """
    def __init__(self):
        super().__init__()
        self.analyst_type = "partnership_analyst"
        
    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""As a Partnership Analyst, your task is to generate search queries that will help find potential 
business partners for a {business_type} business in {location} who serve the same target audience.

Who to Reach Out To:
{outreach_channels}

Your search queries should:
- Focus on finding complementary businesses who serve the same customer base
- Target businesses mentioned in the outreach channels list
- Look for established businesses that might be interested in partnerships
- Include location-specific terms to find local partners
- Target current information (include {year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.
"""
