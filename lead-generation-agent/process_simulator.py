"""
Lead Generation Agent - Process Simulator

This script simulates the entire lead generation process from start to finish,
showing all prompts and responses at each step without making actual API calls.
"""

import os
import sys
import json
from datetime import datetime

# Function to display a step in the process with prompt and response
def display_step(step_number, step_name, system_prompt, user_prompt, response, max_length=None):
    print("\n" + "=" * 100)
    print(f"STEP {step_number}: {step_name}")
    print("=" * 100)
    
    print("SYSTEM PROMPT:")
    print("-" * 80)
    print(system_prompt)
    print("-" * 80 + "\n")
    
    print("USER PROMPT:")
    print("-" * 80)
    if max_length and len(user_prompt) > max_length:
        print(user_prompt[:max_length] + "...\n[Content truncated]")
    else:
        print(user_prompt)
    print("-" * 80 + "\n")
    
    print("RESPONSE:")
    print("-" * 80)
    if max_length and len(response) > max_length:
        print(response[:max_length] + "...\n[Content truncated]")
    else:
        print(response)
    print("-" * 80)

def main():
    print("\n\n" + "=" * 100)
    print("                LEAD GENERATION AGENT - FULL PROCESS SIMULATION")
    print("=" * 100 + "\n")

    # Get user input for business details
    print("Let's simulate the full lead generation process.")
    print("Please provide some business details to customize the simulation:\n")
    
    business_type = input("Business Type: ").strip() or "SaaS Inventory Management"
    location = input("Location: ").strip() or "Malaysia"
    
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
        target_customers = "Medium-sized Retail Chains (with multiple outlets and diverse product ranges)"
    
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
        outreach_channels = "Retail industry conferences, e-commerce platforms, logistics partners"

    print("\n\nSimulating the complete lead generation process...\n")
    
    current_year = datetime.now().year
    
    # STEP 1: DIRECT LEADS ANALYST QUERY GENERATION
    
    direct_leads_system = f"You are researching leads for a {business_type} business in {location}."
    
    direct_leads_prompt = f"""Researching potential leads on {datetime.now().strftime("%B %d, %Y")}.

As a Direct Leads Analyst, your task is to generate search queries that will help find specific businesses 
or individuals who could be potential direct customers for a {business_type} business in {location}.

Target Customers:
{target_customers}

Your search queries should:
- Focus on finding specific companies, organizations, or individuals who match the target customer profile
- Be designed to find lists, directories, or databases of potential clients
- Include location-specific terms to find local businesses or individuals
- Target current information (include {current_year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.

Important Guidelines:
- Focus on finding specific leads for a {business_type} business in {location}
- Target customers: {target_customers}
- Potential outreach channels: {outreach_channels}
- Make queries very brief and to the point
- Provide exactly 4 search queries (one per line), with no numbering or bullet points
- Each query should be specific and targeted to find actionable leads
- Include {location} and {current_year} in queries where relevant"""

    direct_leads_response = f"""medium-sized retail chains in Malaysia {current_year}
Malaysian retailers with multiple outlets inventory management needs
retail chains Malaysia POS integration inventory system
retail product management software buyers Malaysia {current_year}"""

    display_step(1, "DIRECT LEADS ANALYST QUERY GENERATION", direct_leads_system, direct_leads_prompt, direct_leads_response)
    
    # STEP 2: PARTNERSHIP ANALYST QUERY GENERATION
    
    partnership_system = f"You are researching leads for a {business_type} business in {location}."
    
    partnership_prompt = f"""Researching potential leads on {datetime.now().strftime("%B %d, %Y")}.

As a Partnership Analyst, your task is to identify potential business partners for a {business_type} 
business in {location} who can help reach {target_customers.split('\n')[0].lower() if '\n' in target_customers else target_customers.lower()}.

Generate search queries that will help find:
- Local businesses that complement {business_type} services
- Industry partners who work with similar customers
- Distribution channels or referral networks relevant to {business_type}
- Professional associations or groups in the {business_type} industry in {location}

Your search queries should be specific, include location terms, and target current information ({current_year} where relevant).

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points.

Important Guidelines:
- Focus on finding specific leads for a {business_type} business in {location}
- Target customers: {target_customers}
- Potential outreach channels: {outreach_channels}
- Make queries very brief and to the point
- Provide exactly 4 search queries (one per line), with no numbering or bullet points
- Each query should be specific and targeted to find actionable leads
- Include {location} and {current_year} in queries where relevant"""

    partnership_response = """retail POS system providers Malaysia partnerships
logistics software integration partners Malaysia
ecommerce platform providers Malaysia retail integration
Malaysia retail technology association members {current_year}"""

    display_step(2, "PARTNERSHIP ANALYST QUERY GENERATION", partnership_system, partnership_prompt, partnership_response)
    
    # STEP 3: DOCUMENT SEARCH RESULTS
    # Let's simulate some search results for one of the queries
    
    sample_search_results = [
        {
            "title": "Top 10 Retail Chains in Malaysia Using Advanced Inventory Solutions",
            "url": "https://example.com/malaysia-retail-chains",
            "content": """RetailTech Malaysia reports that several medium-sized retail chains have upgraded their inventory management systems in 2023. 
                        MegaMart Malaysia, with its 23 outlets across Kuala Lumpur and Selangor, implemented a new SaaS inventory system last quarter, 
                        resulting in 30% reduced stockouts. Their IT Director, Sarah Tan, can be reached at sarah.tan@megamart.my or +60 3-1234-5678. 
                        Another notable upgrade was at FamilyValue Stores (42 locations nationwide), which integrated their POS system with a 
                        cloud-based inventory solution. For partnership inquiries, contact their operations team at operations@familyvalue.com.my."""
        },
        {
            "title": "Malaysia Retail Association Technology Report 2023",
            "url": "https://example.com/malaysia-retail-report",
            "content": """The Malaysia Retail Chain Association (MRCA) published their annual technology adoption report. 
                        According to President Ahmad Rizal (president@mrca.org.my), 68% of member companies with 15+ outlets 
                        plan to upgrade their inventory management systems in the next 12 months. The report highlights 
                        challenges with existing systems including multi-location synchronization and supplier integration. 
                        MRCA will host their annual technology conference on September 15, 2024 at the Kuala Lumpur 
                        Convention Centre where retailers will meet technology providers."""
        }
    ]
    
    # STEP 4: DOCUMENT ENRICHMENT
    # Process one of the search results with the enrichment prompt
    
    enrichment_system = "You are a lead generation assistant that extracts contact information and relevant details from web content."
    
    enrichment_prompt = f"""Extract the most relevant information from this content about potential leads for a {business_type} business in {location}.

This content is from a direct_leads_analyst search.

Content:
{sample_search_results[0]["content"]}

Extract and format the following information:
1. Names of relevant companies, organizations, or individuals
2. Contact information (emails, phone numbers, websites)
3. Social media profiles or handles
4. Physical addresses if available
5. Brief description of why this is a good lead
6. Any other relevant details for lead generation

Format your response as structured information that can be easily parsed. Only include information that is actually present in the content.
"""

    enrichment_response = """Names: MegaMart Malaysia, FamilyValue Stores
Contact: sarah.tan@megamart.my, +60 3-1234-5678 (MegaMart), operations@familyvalue.com.my (FamilyValue)
Website: Not specified
Social Media: Not specified
Address: Multiple outlets across Kuala Lumpur and Selangor (MegaMart), 42 locations nationwide (FamilyValue)
Good Lead: MegaMart recently implemented a new SaaS inventory system and FamilyValue integrated their POS system with a cloud-based inventory solution - both are relevant to SaaS Inventory Management
Additional Details: MegaMart has 23 outlets, saw 30% reduced stockouts with new system; FamilyValue has 42 locations"""

    display_step(4, "DOCUMENT ENRICHMENT", enrichment_system, enrichment_prompt, enrichment_response)
    
    # STEP 5: BRIEFING GENERATION
    # Generate a briefing for the direct leads category
    
    briefing_system = "You are a lead generation specialist creating concise, actionable briefings for business development."
    
    # Combine multiple enriched documents
    combined_enriched_content = f"""Source: Top 10 Retail Chains in Malaysia Using Advanced Inventory Solutions

Names: MegaMart Malaysia, FamilyValue Stores
Contact: sarah.tan@megamart.my, +60 3-1234-5678 (MegaMart), operations@familyvalue.com.my (FamilyValue)
Website: Not specified
Social Media: Not specified
Address: Multiple outlets across Kuala Lumpur and Selangor (MegaMart), 42 locations nationwide (FamilyValue)
Good Lead: MegaMart recently implemented a new SaaS inventory system and FamilyValue integrated their POS system with a cloud-based inventory solution - both are relevant to SaaS Inventory Management
Additional Details: MegaMart has 23 outlets, saw 30% reduced stockouts with new system; FamilyValue has 42 locations

---

Source: Malaysia Retail Association Technology Report 2023

Names: Malaysia Retail Chain Association (MRCA), Ahmad Rizal (President)
Contact: president@mrca.org.my
Website: Not specified
Social Media: Not specified
Address: Not specified
Good Lead: 68% of MRCA member companies with 15+ outlets plan to upgrade inventory management systems in next 12 months
Additional Details: Annual technology conference on September 15, 2024 at Kuala Lumpur Convention Centre; report highlights challenges with multi-location synchronization and supplier integration
"""
    
    briefing_prompt = f"""Create a concise, actionable briefing about Direct Leads for a {business_type} business in {location}.

Target Customers:
{target_customers}

Outreach Channels:
{outreach_channels}

Information from research:
{combined_enriched_content}

Your task is to compile this information into a clear, structured briefing that:
1. Starts with a brief overview of this lead category
2. Lists the specific leads found with their contact information
3. Provides concrete next steps or outreach strategies
4. Formats the information in clear Markdown with proper headings and bullet points

Focus on actionable information that can be used for lead generation. Be specific and practical.
"""

    briefing_response = """# Direct Leads Summary

## Overview
We've identified several promising direct leads for your SaaS Inventory Management business in Malaysia. These potential clients are medium-sized retail chains with multiple outlets who have either recently implemented inventory solutions or are actively planning to upgrade their systems in the near future.

## Identified Leads

### MegaMart Malaysia
- **Contact**: Sarah Tan (IT Director), sarah.tan@megamart.my, +60 3-1234-5678
- **Scale**: 23 outlets across Kuala Lumpur and Selangor
- **Notes**: Recently implemented a new SaaS inventory system with reported 30% reduction in stockouts. Could be approached for either enhancement of current system or replacement if their solution isn't meeting all needs.

### FamilyValue Stores
- **Contact**: Operations Team, operations@familyvalue.com.my
- **Scale**: 42 locations nationwide
- **Notes**: Recently integrated their POS system with a cloud-based inventory solution. May be interested in advanced features or better integration capabilities.

### Malaysia Retail Chain Association (MRCA)
- **Contact**: Ahmad Rizal (President), president@mrca.org.my
- **Event**: Annual technology conference on September 15, 2024 at Kuala Lumpur Convention Centre
- **Opportunity**: 68% of member companies with 15+ outlets plan to upgrade their inventory management systems in the next 12 months
- **Pain Points**: Multi-location synchronization and supplier integration challenges

## Next Steps

### Immediate Actions (Next 30 Days)
1. **Contact MegaMart Malaysia**: Email Sarah Tan with a case study showing how your solution could further improve their inventory management beyond their recent 30% improvement
2. **Reach Out to FamilyValue Stores**: Contact their operations team to inquire about current challenges with their recent cloud integration
3. **Connect with MRCA President**: Email Ahmad Rizal requesting information about exhibiting at their September 15 technology conference

### Follow-up Strategy
1. Schedule demonstrations with interested parties within 2 weeks of initial contact
2. Prepare customized presentations addressing specific pain points (multi-location synchronization for chains, supplier integration)
3. Develop proposal templates tailored to retail chains at different stages (those looking to upgrade vs. those who recently implemented other solutions)

## Outreach Template
```
Subject: Enhancing Inventory Management for [Company]'s Multi-Location Operations

Dear [Name],

I recently learned about [Company]'s work with inventory management systems across your [X] locations. Our SaaS Inventory Management solution specifically addresses the challenges faced by multi-outlet retail chains in Malaysia, particularly around [specific pain point].

We've helped similar retailers achieve [specific result, e.g., "40% reduction in stockouts while reducing inventory costs by 15%"].

I'd welcome the opportunity to share how our solution might complement or enhance your current operations. Would you be available for a 20-minute call next week to discuss?

Best regards,
[Your Name]
```"""

    display_step(5, "BRIEFING GENERATION", briefing_system, briefing_prompt, briefing_response, max_length=2000)
    
    # STEP 6: FINAL REPORT COMPILATION
    
    final_report_system = "You are a professional business development consultant compiling a comprehensive lead generation report."
    
    # Combine multiple briefings
    combined_briefings = f"""## Direct Leads

{briefing_response}

## Potential Partners

# Potential Partners Summary

## Overview
We've identified several promising partnership opportunities for your SaaS Inventory Management business in Malaysia. These potential partners either provide complementary services to medium-sized retail chains or have established relationships with your target market.

## Identified Partners

### RetailTech Solutions Malaysia
- **Contact**: David Wong (Business Development), partnerships@retailtech.my, +60 3-8765-4321
- **Website**: www.retailtech.my
- **Notes**: Leading POS system provider in Malaysia with over 200 retail clients. Their POS systems lack advanced inventory management features, creating an integration opportunity.

### Malaysian E-Commerce Fulfillment Association
- **Contact**: contact@mefa.org.my
- **Event**: Quarterly networking sessions in Kuala Lumpur
- **Opportunity**: Their members handle fulfillment for many medium-sized retailers and often recommend technology solutions

## Next Steps
1. Reach out to RetailTech Solutions to discuss potential integration partnership
2. Apply for membership in the Malaysian E-Commerce Fulfillment Association
3. Prepare partnership proposal templates with different commission structures

## Events & Conferences

# Events & Conferences Summary

## Overview
We've identified several upcoming events where you can connect with potential clients and partners in the retail technology space in Malaysia.

## Key Events

### Malaysia Retail Chain Association Technology Conference
- **Date**: September 15, 2024
- **Location**: Kuala Lumpur Convention Centre
- **Opportunity**: Many medium-sized retail chains actively seeking inventory solutions will attend
- **Next Steps**: Apply for exhibitor space by July 30, 2024

### RetailEX ASEAN 2024
- **Date**: October 8-10, 2024
- **Location**: Bangkok (close to Malaysian market)
- **Opportunity**: Regional retail technology exhibition with strong Malaysian attendance

## Next Steps
1. Budget for and apply to exhibit at MRCA Technology Conference as top priority
2. Prepare demonstration materials specific to multi-location retail inventory challenges
3. Develop lead capture strategy for events
"""
    
    final_report_prompt = f"""Compile the following lead generation briefings into a comprehensive, well-structured report for a {business_type} business in {location}.

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

    final_report_response = """# Lead Generation Report: SaaS Inventory Management in Malaysia

**Generated on July 26, 2024**

## Executive Summary

This comprehensive lead generation report identifies key opportunities for your SaaS Inventory Management solution targeting medium-sized retail chains in Malaysia. Our research has uncovered:

- **5 Direct Client Leads**: Including MegaMart Malaysia and FamilyValue Stores, who have recently implemented inventory solutions but may benefit from enhancements
- **2 Strategic Partnership Opportunities**: Including RetailTech Solutions Malaysia, a POS provider with 200+ retail clients
- **2 High-Value Industry Events**: Including the MRCA Technology Conference on September 15, 2024, where 68% of attendees are actively seeking inventory management upgrades

The most immediately actionable opportunity is contacting Sarah Tan at MegaMart Malaysia, as they have already demonstrated interest in SaaS inventory solutions and have reported specific metrics (30% stockout reduction) that you can leverage in your outreach.

## Direct Leads

### Overview
We've identified several promising direct leads for your SaaS Inventory Management business in Malaysia. These potential clients are medium-sized retail chains with multiple outlets who have either recently implemented inventory solutions or are actively planning to upgrade their systems in the near future.

### Identified Leads

#### MegaMart Malaysia
- **Contact**: Sarah Tan (IT Director), sarah.tan@megamart.my, +60 3-1234-5678
- **Scale**: 23 outlets across Kuala Lumpur and Selangor
- **Notes**: Recently implemented a new SaaS inventory system with reported 30% reduction in stockouts. Could be approached for either enhancement of current system or replacement if their solution isn't meeting all needs.

#### FamilyValue Stores
- **Contact**: Operations Team, operations@familyvalue.com.my
- **Scale**: 42 locations nationwide
- **Notes**: Recently integrated their POS system with a cloud-based inventory solution. May be interested in advanced features or better integration capabilities.

#### Malaysia Retail Chain Association (MRCA)
- **Contact**: Ahmad Rizal (President), president@mrca.org.my
- **Event**: Annual technology conference on September 15, 2024 at Kuala Lumpur Convention Centre
- **Opportunity**: 68% of member companies with 15+ outlets plan to upgrade their inventory management systems in the next 12 months
- **Pain Points**: Multi-location synchronization and supplier integration challenges

### Next Steps
1. **Contact MegaMart Malaysia**: Email Sarah Tan with a case study showing how your solution could further improve their inventory management beyond their recent 30% improvement
2. **Reach Out to FamilyValue Stores**: Contact their operations team to inquire about current challenges with their recent cloud integration
3. **Connect with MRCA President**: Email Ahmad Rizal requesting information about exhibiting at their September 15 technology conference

## Potential Partners

### Overview
We've identified several promising partnership opportunities for your SaaS Inventory Management business in Malaysia. These potential partners either provide complementary services to medium-sized retail chains or have established relationships with your target market.

### Identified Partners

#### RetailTech Solutions Malaysia
- **Contact**: David Wong (Business Development), partnerships@retailtech.my, +60 3-8765-4321
- **Website**: www.retailtech.my
- **Notes**: Leading POS system provider in Malaysia with over 200 retail clients. Their POS systems lack advanced inventory management features, creating an integration opportunity.

#### Malaysian E-Commerce Fulfillment Association
- **Contact**: contact@mefa.org.my
- **Event**: Quarterly networking sessions in Kuala Lumpur
- **Opportunity**: Their members handle fulfillment for many medium-sized retailers and often recommend technology solutions

### Next Steps
1. Reach out to RetailTech Solutions to discuss potential integration partnership
2. Apply for membership in the Malaysian E-Commerce Fulfillment Association
3. Prepare partnership proposal templates with different commission structures

## Events & Conferences

### Overview
We've identified several upcoming events where you can connect with potential clients and partners in the retail technology space in Malaysia.

### Key Events

#### Malaysia Retail Chain Association Technology Conference
- **Date**: September 15, 2024
- **Location**: Kuala Lumpur Convention Centre
- **Opportunity**: Many medium-sized retail chains actively seeking inventory solutions will attend
- **Next Steps**: Apply for exhibitor space by July 30, 2024

#### RetailEX ASEAN 2024
- **Date**: October 8-10, 2024
- **Location**: Bangkok (close to Malaysian market)
- **Opportunity**: Regional retail technology exhibition with strong Malaysian attendance

### Next Steps
1. Budget for and apply to exhibit at MRCA Technology Conference as top priority
2. Prepare demonstration materials specific to multi-location retail inventory challenges
3. Develop lead capture strategy for events

## Prioritized Action Plan

### Immediate Actions (Next 14 Days)
1. **Contact Sarah Tan at MegaMart Malaysia** - Highest priority lead with demonstrated interest in SaaS inventory solutions
2. **Email Ahmad Rizal at MRCA** - Time-sensitive opportunity to secure exhibition space at September conference
3. **Reach out to RetailTech Solutions** - Partnership opportunity with greatest potential reach (200+ retail clients)

### Short-Term Actions (15-45 Days)
1. Follow up with FamilyValue Stores operations team
2. Apply for membership in Malaysian E-Commerce Fulfillment Association
3. Prepare customized presentations addressing specific pain points for retail chains
4. Develop marketing materials for MRCA Technology Conference

### Long-Term Strategy (45-90 Days)
1. Plan budget and resources for RetailEX ASEAN 2024 in October
2. Develop systematic approach to tracking relationships with all identified leads
3. Create case studies based on initial client successes
4. Refine partnership commission structures based on early results

## Outreach Templates

### For Direct Leads
```
Subject: Enhancing Inventory Management for [Company]'s Multi-Location Operations

Dear [Name],

I recently learned about [Company]'s work with inventory management systems across your [X] locations. Our SaaS Inventory Management solution specifically addresses the challenges faced by multi-outlet retail chains in Malaysia, particularly around [specific pain point].

We've helped similar retailers achieve [specific result, e.g., "40% reduction in stockouts while reducing inventory costs by 15%"].

I'd welcome the opportunity to share how our solution might complement or enhance your current operations. Would you be available for a 20-minute call next week to discuss?

Best regards,
[Your Name]
```

### For Potential Partners
```
Subject: Partnership Opportunity: Complementary Solutions for Retail Clients

Dear [Name],

I've been following [Partner Company]'s work in the Malaysian retail technology space and believe there may be a valuable partnership opportunity between our companies.

Our SaaS Inventory Management solution complements your [POS/fulfillment/etc.] offering by addressing the specific challenges of multi-location inventory synchronization and supplier integration that many medium-sized retail chains face.

I'd like to explore how we might work together to provide more comprehensive solutions to your retail clients. Would you be available for a brief discussion next week?

Best regards,
[Your Name]
```

This report provides a roadmap for your lead generation efforts over the next 90 days, with specific contacts, opportunities, and action items prioritized for maximum impact. The research indicates strong market potential for your SaaS Inventory Management solution among medium-sized retail chains in Malaysia, particularly those struggling with multi-location synchronization and supplier integration challenges."""

    display_step(6, "FINAL REPORT COMPILATION", final_report_system, final_report_prompt, final_report_response, max_length=3000)
    
    # Completion message
    print("\n" + "=" * 100)
    print("                            END OF PROCESS SIMULATION")
    print("=" * 100)
    print("\nThis simulation shows the complete flow of the lead generation agent process:")
    print("1. Initial research queries generation for direct leads")
    print("2. Initial research queries generation for partnerships")
    print("3. (Implied) Web searches using these queries")
    print("4. Document enrichment to extract contact information and relevant details")
    print("5. Creation of actionable briefings for each lead category")
    print("6. Final compilation into a comprehensive lead generation report")
    print("\nIn a real execution, the system would perform these steps automatically,")
    print("collecting actual web search results and producing a customized report")
    print("based on real data about your target market.")
    print("=" * 100 + "\n")

if __name__ == "__main__":
    main()
