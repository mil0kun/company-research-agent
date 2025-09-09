import logging
from typing import Dict, List

from .base import BaseLeadResearcher

logger = logging.getLogger(__name__)

class CommunityAnalyst(BaseLeadResearcher):
    """
    Analyst focused on finding online communities, forums, and platforms where the target audience is active.
    """
    def __init__(self):
        super().__init__()
        self.analyst_type = "community_analyst"
        
    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""As a Community Analyst, your task is to generate search queries that will help find online communities, 
forums, social media groups, and platforms where the target audience for a {business_type} business in {location} is active.

Target Customers:
{target_customers}

Who to Reach Out To:
{outreach_channels}

Your search queries should:
- Focus on finding Facebook groups, Reddit communities, forums, or online directories
- Target platforms specific to {location} or the region
- Look for active online communities where potential customers gather
- Find online directories or listings that are industry-specific
- Target current information (include {year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.
"""
