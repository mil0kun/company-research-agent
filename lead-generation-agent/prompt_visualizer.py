"""
Prompt Visualizer for Lead Generation Agent

This script shows all the prompts used in the lead generation process,
from the initial research queries to the final report generation.
"""

import os
import sys
import json
from datetime import datetime

# Function to display a prompt with formatting
def display_prompt(title, role, content, max_length=None):
    print("\n" + "=" * 80)
    print(f"## {title}")
    print("=" * 80)
    print(f"Role: {role}")
    print("-" * 80)
    
    if max_length and len(content) > max_length:
        print(content[:max_length] + "...\n[Content truncated]")
    else:
        print(content)
    print("=" * 80 + "\n")

def main():
    print("\n\n" + "=" * 100)
    print("                       LEAD GENERATION AGENT - PROMPT VISUALIZER")
    print("=" * 100 + "\n")

    # Get user input for business details
    print("Let's visualize the prompts for a sample lead generation process.")
    print("Please provide some business details to customize the prompts:\n")
    
    business_type = input("Business Type: ").strip() or "Wedding Photography"
    location = input("Location: ").strip() or "Penang, Malaysia"
    
    print("\nNow, please describe your target customers (press Enter twice when done):")
    target_customers = ""
    while True:
        line = input()
        if not line and target_customers:  # Empty line after some content means we're done
            break
        if target_customers:
            target_customers += "\n"
        target_customers += line
    
    if not target_customers:
        target_customers = "Young couples looking for budget-friendly photography services"
    
    print("\nPotential outreach channels (press Enter twice when done):")
    outreach_channels = ""
    while True:
        line = input()
        if not line and outreach_channels:  # Empty line after some content means we're done
            break
        if outreach_channels:
            outreach_channels += "\n"
        outreach_channels += line
    
    if not outreach_channels:
        outreach_channels = "Wedding planners, social media, wedding venues"

    print("\n\nGenerating visualization of all prompts used in the lead generation process...\n")
    
    # 1. INITIAL RESEARCH PROMPTS
    
    # Direct Leads Analyst Prompt
    direct_leads_prompt = f"""As a Direct Leads Analyst, your task is to generate search queries that will help find specific businesses 
or individuals who could be potential direct customers for a {business_type} business in {location}.

Target Customers:
{target_customers}

Your search queries should:
- Focus on finding specific companies, organizations, or individuals who match the target customer profile
- Be designed to find lists, directories, or databases of potential clients
- Include location-specific terms to find local businesses or individuals
- Target current information (include {datetime.now().year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""

    display_prompt("1. DIRECT LEADS ANALYST PROMPT", "System: You are researching leads for a business", direct_leads_prompt)

    # Partnership Analyst Prompt
    partnership_prompt = f"""As a Partnership Analyst, your task is to identify potential business partners for a {business_type} 
business in {location} who can help reach {target_customers.split('\n')[0].lower() if '\n' in target_customers else target_customers.lower()}.

Generate search queries that will help find:
- Local businesses that complement {business_type} services
- Industry partners who work with similar customers
- Distribution channels or referral networks relevant to {business_type}
- Professional associations or groups in the {business_type} industry in {location}

Your search queries should be specific, include location terms, and target current information ({datetime.now().year} where relevant).

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""

    display_prompt("2. PARTNERSHIP ANALYST PROMPT", "System: You are researching leads for a business", partnership_prompt)

    # Community Analyst Prompt
    community_prompt = f"""As a Community Analyst for a {business_type} business in {location}, your task is to find 
online and offline communities where {target_customers.split('\n')[0].lower() if '\n' in target_customers else target_customers.lower()} might gather.

Generate search queries that will help find:
- Online forums, Facebook groups, and social media communities
- Local community events or meetups
- Industry-specific discussion boards and platforms
- Specialized communities related to {business_type} in {location}

Your search queries should be specific, include relevant location terms, and target current information.

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""

    display_prompt("3. COMMUNITY ANALYST PROMPT", "System: You are researching leads for a business", community_prompt)

    # Events Analyst Prompt
    events_prompt = f"""As an Events Analyst for a {business_type} business in {location}, your task is to find 
relevant events, exhibitions, and conferences where you can connect with {target_customers.split('\n')[0].lower() if '\n' in target_customers else target_customers.lower()}.

Generate search queries that will help find:
- Industry expos, fairs, and exhibitions in {location} and nearby areas in {datetime.now().year}
- Networking events related to {business_type}
- Local community events that attract your target customers
- Industry conferences and conventions in {location}

Your search queries should be specific, include relevant location terms, and focus on upcoming events.

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""

    display_prompt("4. EVENTS ANALYST PROMPT", "System: You are researching leads for a business", events_prompt)

    # Influencer Analyst Prompt
    influencer_prompt = f"""As an Influencer Analyst for a {business_type} business in {location}, your task is to identify 
key influencers, bloggers, and media channels that reach {target_customers.split('\n')[0].lower() if '\n' in target_customers else target_customers.lower()}.

Generate search queries that will help find:
- Industry bloggers and influencers based in {location}
- Social media accounts focused on {business_type} in {location}
- Popular publications and media outlets covering {business_type}
- Local personalities and thought leaders in the {business_type} industry

Your search queries should be specific, include relevant location terms, and target current influencers.

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""

    display_prompt("5. INFLUENCER ANALYST PROMPT", "System: You are researching leads for a business", influencer_prompt)

    # 2. DOCUMENT ENRICHMENT PROMPT
    
    # Create a sample search result
    sample_content = f"""ABC Wedding Studio is one of the top photographers in {location} for couples on a budget. 
They offer packages starting from 1,500 MYR for 4 hours of coverage and a digital album. 
You can contact them at info@abcweddingstudio.com or call +60 4-123-4567. 
Their Instagram account @abcweddingstudio has over 5,000 followers, and they're located at 
123 Beach Street, Georgetown. They've been featured in several local wedding magazines for their 
affordable yet professional services."""

    enrichment_prompt = f"""Extract the most relevant information from this content about potential leads for a {business_type} business in {location}.

This content is from a direct_leads_analyst search.

Content:
{sample_content}

Extract and format the following information:
1. Names of relevant companies, organizations, or individuals
2. Contact information (emails, phone numbers, websites)
3. Social media profiles or handles
4. Physical addresses if available
5. Brief description of why this is a good lead
6. Any other relevant details for lead generation

Format your response as structured information that can be easily parsed. Only include information that is actually present in the content.
"""

    display_prompt("6. DOCUMENT ENRICHMENT PROMPT", "System: You are a lead generation assistant that extracts contact information and relevant details from web content", enrichment_prompt)

    # 3. BRIEFING GENERATION PROMPT
    
    # Create sample enriched content
    sample_enriched_content = """Names: ABC Wedding Studio
Contact: info@abcweddingstudio.com, +60 4-123-4567
Website: Not specified
Social Media: @abcweddingstudio (Instagram)
Address: 123 Beach Street, Georgetown
Good Lead: Offers affordable packages (starting from 1,500 MYR) which fits the budget-friendly requirement
Additional Details: Featured in local wedding magazines, offers 4 hours of coverage and digital albums"""

    briefing_prompt = f"""Create a concise, actionable briefing about Direct Leads for a {business_type} business in {location}.

Target Customers:
{target_customers}

Outreach Channels:
{outreach_channels}

Information from research:
Source: Top Wedding Photographers in Penang

{sample_enriched_content}

---

Your task is to compile this information into a clear, structured briefing that:
1. Starts with a brief overview of this lead category
2. Lists the specific leads found with their contact information
3. Provides concrete next steps or outreach strategies
4. Formats the information in clear Markdown with proper headings and bullet points

Focus on actionable information that can be used for lead generation. Be specific and practical.
"""

    display_prompt("7. BRIEFING GENERATION PROMPT", "System: You are a lead generation specialist creating concise, actionable briefings for business development", briefing_prompt)

    # 4. FINAL REPORT COMPILATION PROMPT
    
    # Create sample briefing content
    sample_briefing = """# Direct Leads Summary

## Overview
We've identified several promising direct leads for your wedding photography business in Penang, Malaysia. These potential clients align well with your target market of budget-conscious couples seeking professional quality within the 1,500-3,000 MYR range.

## Identified Leads

### ABC Wedding Studio
- **Contact**: info@abcweddingstudio.com, +60 4-123-4567
- **Social Media**: @abcweddingstudio (Instagram)
- **Address**: 123 Beach Street, Georgetown, Penang
- **Notes**: Offers affordable packages starting from 1,500 MYR, featured in local wedding magazines

## Next Steps
1. Send personalized emails introducing your services
2. Follow up with phone calls within 3 days of emails
3. Offer a special partnership discount for first-time referrals
4. Request in-person meetings to showcase your portfolio

## Outreach Template
"Hello [Name], I discovered your wedding services in Penang and noticed you work with couples in the budget range I specialize in. My photography packages may complement your offerings, and I'd love to discuss potential collaboration. I'm available to meet and show my portfolio at your convenience."
"""

    final_report_prompt = f"""Compile the following lead generation briefings into a comprehensive, well-structured report for a {business_type} business in {location}.

Target Customers:
{target_customers}

Outreach Channels:
{outreach_channels}

Briefings:
## Direct Leads

{sample_briefing}

## Potential Partners

[Sample content for partners briefing would appear here]

Your task is to:
1. Create a professional, executive-summary style introduction that explains the purpose and scope of this lead generation report
2. Organize the briefings in a logical order, maintaining their content but improving the formatting and flow
3. Add an executive summary at the beginning that highlights the most promising leads across all categories
4. Add a "Next Steps" section at the end with a prioritized action plan
5. Format everything in clean, professional Markdown with consistent headings, bullet points, and styling

Make sure the report is action-oriented, with clear recommendations for follow-up on the most promising leads.
"""

    display_prompt("8. FINAL REPORT COMPILATION PROMPT", "System: You are a professional business development consultant compiling a comprehensive lead generation report", final_report_prompt, max_length=1500)

    # Completion message
    print("\n" + "=" * 100)
    print("                            END OF PROMPT VISUALIZATION")
    print("=" * 100)
    print("\nThese prompts show the complete flow of the lead generation agent process:")
    print("1-5. Initial research queries generation for various analyst types")
    print("6. Document enrichment to extract contact information and relevant details")
    print("7. Creation of actionable briefings for each lead category")
    print("8. Final compilation into a comprehensive lead generation report")
    print("\nThe actual system would execute these in sequence, with each stage building on the results of the previous ones.")
    print("=" * 100 + "\n")

if __name__ == "__main__":
    main()
