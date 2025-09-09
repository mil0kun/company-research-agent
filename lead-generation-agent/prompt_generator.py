"""
Prompt Generator for Lead Generation Agent

This script provides a command-line interface to generate search prompts for lead generation
without executing the entire workflow. It allows the user to input business information
and see what prompts would be generated for different analyst types.
"""

import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from backend.nodes.researchers.base import BaseLeadResearcher, MockGroqClient

# Load environment variables
load_dotenv()

class DirectLeadResearcher(BaseLeadResearcher):
    """Direct leads researcher for generating queries about potential customers"""
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

class PartnershipResearcher(BaseLeadResearcher):
    """Partnership researcher for generating queries about potential business partners"""
    def __init__(self):
        super().__init__()
        self.analyst_type = "partnership_analyst"
    
    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""As a Partnership Analyst, your task is to generate search queries that will help find potential business 
partners for a {business_type} business in {location}.

Target Customers:
{target_customers}

Outreach Channels:
{outreach_channels}

Your search queries should:
- Focus on finding complementary businesses that serve a similar customer base
- Identify organizations that could refer clients or collaborate on joint offerings
- Look for industry associations or networks relevant to {business_type}
- Target current information (include {year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.
"""

class CommunityResearcher(BaseLeadResearcher):
    """Community researcher for generating queries about online communities and platforms"""
    def __init__(self):
        super().__init__()
        self.analyst_type = "community_analyst"
    
    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""As a Community Analyst, your task is to generate search queries that will help find online communities, 
forums, groups, and platforms where potential customers for a {business_type} business in {location} might gather.

Target Customers:
{target_customers}

Your search queries should:
- Focus on finding Facebook groups, Reddit communities, forums, and other online platforms
- Identify local community boards or discussion groups specific to {location}
- Look for industry-specific communities related to {business_type}
- Target current and active communities (include {year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.
"""

class EventsResearcher(BaseLeadResearcher):
    """Events researcher for generating queries about relevant events and conferences"""
    def __init__(self):
        super().__init__()
        self.analyst_type = "events_analyst"
    
    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""As an Events Analyst, your task is to generate search queries that will help find relevant events, 
conferences, trade shows, and meetups related to {business_type} in {location}.

Target Customers:
{target_customers}

Your search queries should:
- Focus on finding upcoming events where potential customers might attend
- Identify industry-specific conferences or trade shows in {location} or nearby areas
- Look for networking events that would attract your target audience
- Target current and upcoming events (include {year} and {year+1} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.
"""

class InfluencerResearcher(BaseLeadResearcher):
    """Influencer researcher for generating queries about industry influencers and media outlets"""
    def __init__(self):
        super().__init__()
        self.analyst_type = "influencer_analyst"
    
    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""As an Influencer Analyst, your task is to generate search queries that will help find relevant industry 
influencers, bloggers, journalists, and media outlets related to {business_type} in {location}.

Target Customers:
{target_customers}

Your search queries should:
- Focus on finding influential individuals with audiences that match your target customers
- Identify local media outlets, blogs, podcasts, or YouTube channels in {location}
- Look for industry-specific publications or thought leaders
- Target currently active influencers (include {year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.
"""

async def generate_prompts(business_info):
    """Generate prompts for all analyst types based on the provided business information"""
    # Initialize researchers
    researchers = {
        "Direct Leads": DirectLeadResearcher(),
        "Partnerships": PartnershipResearcher(),
        "Communities": CommunityResearcher(),
        "Events": EventsResearcher(),
        "Influencers": InfluencerResearcher()
    }
    
    # Create a state dictionary from the business info
    state = {
        "business_type": business_info["business_type"],
        "location": business_info["location"],
        "target_customers": business_info["target_customers"],
        "outreach_channels": business_info["outreach_channels"]
    }
    
    # Generate prompts for each researcher
    results = {}
    for name, researcher in researchers.items():
        prompt = f"Generate search queries to find {name.lower()}"
        queries = await researcher.generate_queries(state, prompt)
        results[name] = queries
    
    return results

def get_business_info():
    """Prompt the user for business information through the command line"""
    print("\n" + "="*80)
    print("LEAD GENERATION PROMPT GENERATOR".center(80))
    print("="*80 + "\n")
    
    business_info = {}
    
    print("Please provide information about your business to generate targeted search prompts:\n")
    
    business_info["business_type"] = input("What type of business are you running? (e.g., 'Wedding Photography'): ")
    business_info["location"] = input("What is your business location? (e.g., 'Penang, Malaysia'): ")
    
    print("\nDescribe your target customers (2-3 sentences). For example:")
    print("- Budget-conscious couples seeking professional quality within the RM1,500-RM3,000 range.")
    print("- Couples getting married in Penang or nearby states who prefer local vendors.")
    business_info["target_customers"] = input("\nYour target customers: ")
    
    print("\nDescribe your preferred outreach channels (2-3 sentences). For example:")
    print("- Wedding Planners and Coordinators based in Penang.")
    print("- Local wedding venues (hotels, event halls).")
    business_info["outreach_channels"] = input("\nYour outreach channels: ")
    
    return business_info

async def main():
    """Main entry point for the prompt generator script"""
    business_info = get_business_info()
    
    print("\nGenerating prompts based on your information...")
    print("This simulates what the lead generation agent would generate internally.\n")
    
    results = await generate_prompts(business_info)
    
    print("\n" + "="*80)
    print("GENERATED SEARCH QUERIES".center(80))
    print("="*80 + "\n")
    
    for category, queries in results.items():
        print(f"\n{category} Queries:".upper())
        print("-" * 40)
        for i, query in enumerate(queries, 1):
            print(f"{i}. {query}")
    
    print("\n" + "="*80)
    print("These queries would be used to search for leads in each category.".center(80))
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
