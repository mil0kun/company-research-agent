import logging
from typing import Dict, List

from .base import BaseLeadResearcher

logger = logging.getLogger(__name__)

class InfluencerAnalyst(BaseLeadResearcher):
    """
    Analyst focused on finding key individuals or media outlets that influence the target audience.
    """
    def __init__(self):
        super().__init__()
        self.analyst_type = "influencer_analyst"
        
    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""As an Influencer Analyst, your task is to generate search queries that will help find key individuals,
influencers, bloggers, and media outlets that influence the target audience for a {business_type} business in {location}.

Target Customers:
{target_customers}

Your search queries should:
- Focus on finding industry-specific influencers, bloggers, and content creators
- Target local influencers in {location} when possible
- Look for media outlets, magazines, or publications that cover the industry
- Find popular social media accounts that potential customers follow
- Target current information (include {year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.
"""
