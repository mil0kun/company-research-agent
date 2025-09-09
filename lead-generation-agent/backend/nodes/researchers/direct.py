import logging
from typing import Dict, List

from .base import BaseLeadResearcher

logger = logging.getLogger(__name__)

class DirectLeadsAnalyst(BaseLeadResearcher):
    """
    Analyst focused on finding specific companies or individuals that are potential direct customers.
    """
    def __init__(self):
        super().__init__()
        self.analyst_type = "direct_leads_analyst"

    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""As a Direct Leads Analyst, your task is to generate search queries that will help find specific businesses 
or individuals who could be potential direct customers for a {business_type} business in {location}.

Target Customers:
{target_customers}

Your search queries should:
- Focus on finding specific companies, organizations, or individuals who match the target customer profile
- Be designed to find lists, directories, or databases of potential clients
- Include location-specific terms to find local businesses or individuals
- Target current information (include {year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.
"""
