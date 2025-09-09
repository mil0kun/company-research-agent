"""
Real Groq API Lead Researcher Script

This script makes a real API call to Groq to generate research queries
based on user input about their business.
"""

import os
import sys
import asyncio
from datetime import datetime
import json
from typing import Dict, List

# Function to display a prompt with formatting
def display_prompt_and_response(analyst_type, system_prompt, user_prompt, response):
    print("\n" + "=" * 100)
    print(f"ANALYST TYPE: {analyst_type.upper()}")
    print("=" * 100)
    
    print("SYSTEM PROMPT:")
    print("-" * 80)
    print(system_prompt)
    print("-" * 80 + "\n")
    
    print("USER PROMPT:")
    print("-" * 80)
    print(user_prompt)
    print("-" * 80 + "\n")
    
    print("GROQ API RESPONSE:")
    print("-" * 80)
    print(response)
    print("-" * 80)

# Format query prompt based on analyst type
def format_query_prompt(analyst_type, prompt, business_type, location, target_customers, outreach_channels, year):
    base_prompt = f"""{prompt}

Important Guidelines:
- Focus on finding specific leads for a {business_type} business in {location}
- Target customers: {target_customers}
- Potential outreach channels: {outreach_channels}
- Make queries very brief and to the point
- Provide exactly 4 search queries (one per line), with no numbering or bullet points
- Each query should be specific and targeted to find actionable leads
- Include {location} and {year} in queries where relevant"""
    
    return base_prompt

# Generate prompt based on analyst type
def get_analyst_prompt(analyst_type, business_type, location, target_customers):
    current_year = datetime.now().year
    
    if analyst_type == "direct_leads_analyst":
        return f"""As a Direct Leads Analyst, your task is to generate search queries that will help find specific businesses 
or individuals who could be potential direct customers for a {business_type} business in {location}.

Target Customers:
{target_customers}

Your search queries should:
- Focus on finding specific companies, organizations, or individuals who match the target customer profile
- Be designed to find lists, directories, or databases of potential clients
- Include location-specific terms to find local businesses or individuals
- Target current information (include {current_year} where relevant)
- Be very specific and actionable

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""
    
    elif analyst_type == "partnership_analyst":
        return f"""As a Partnership Analyst, your task is to identify potential business partners for a {business_type} 
business in {location} who can help reach {target_customers.split('\n')[0].lower() if '\n' in target_customers else target_customers.lower()}.

Generate search queries that will help find:
- Local businesses that complement {business_type} services
- Industry partners who work with similar customers
- Distribution channels or referral networks relevant to {business_type}
- Professional associations or groups in the {business_type} industry in {location}

Your search queries should be specific, include location terms, and target current information ({current_year} where relevant).

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""
    
    elif analyst_type == "community_analyst":
        return f"""As a Community Analyst for a {business_type} business in {location}, your task is to find 
online and offline communities where {target_customers.split('\n')[0].lower() if '\n' in target_customers else target_customers.lower()} might gather.

Generate search queries that will help find:
- Online forums, Facebook groups, and social media communities
- Local community events or meetups
- Industry-specific discussion boards and platforms
- Specialized communities related to {business_type} in {location}

Your search queries should be specific, include relevant location terms, and target current information.

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""
    
    elif analyst_type == "events_analyst":
        return f"""As an Events Analyst for a {business_type} business in {location}, your task is to find 
relevant events, exhibitions, and conferences where you can connect with {target_customers.split('\n')[0].lower() if '\n' in target_customers else target_customers.lower()}.

Generate search queries that will help find:
- Industry expos, fairs, and exhibitions in {location} and nearby areas in {current_year}
- Networking events related to {business_type}
- Local community events that attract your target customers
- Industry conferences and conventions in {location}

Your search queries should be specific, include relevant location terms, and focus on upcoming events.

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""
    
    elif analyst_type == "influencer_analyst":
        return f"""As an Influencer Analyst for a {business_type} business in {location}, your task is to identify 
key influencers, bloggers, and media channels that reach {target_customers.split('\n')[0].lower() if '\n' in target_customers else target_customers.lower()}.

Generate search queries that will help find:
- Industry bloggers and influencers based in {location}
- Social media accounts focused on {business_type} in {location}
- Popular publications and media outlets covering {business_type}
- Local personalities and thought leaders in the {business_type} industry

Your search queries should be specific, include relevant location terms, and target current influencers.

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""
    
    else:
        return f"""As a Lead Researcher for a {business_type} business in {location}, your task is to generate search queries 
that will help find potential leads and opportunities.

Target Customers:
{target_customers}

Generate exactly 4 search queries, each on a new line, with no numbering or bullet points."""

async def generate_queries_with_real_groq(analyst_type, business_type, location, target_customers, outreach_channels):
    """Generate queries using the real Groq API"""
    # Read the environment files to look for API key
    # If your .env file is in a different location, adjust this path
    env_file_path = os.path.join(os.getcwd(), '.env')
    groq_key = None
    
    # Try to read from .env file
    if os.path.exists(env_file_path):
        print(f"Found .env file at {env_file_path}")
        try:
            with open(env_file_path, 'r') as f:
                for line in f:
                    if line.strip().startswith('GROQ_API_KEY='):
                        groq_key = line.strip().split('=', 1)[1].strip()
                        # Remove quotes if present
                        if groq_key.startswith('"') and groq_key.endswith('"'):
                            groq_key = groq_key[1:-1]
                        elif groq_key.startswith("'") and groq_key.endswith("'"):
                            groq_key = groq_key[1:-1]
                        print("Found GROQ_API_KEY in .env file")
                        break
        except Exception as e:
            print(f"Error reading .env file: {e}")
    
    # If not found in .env, check environment variables
    if not groq_key:
        groq_key = os.getenv("GROQ_API_KEY")
    
    # If still not found, ask the user for the API key
    if not groq_key:
        print("Could not find GROQ_API_KEY in environment variables or .env file")
        groq_key = input("Please enter your Groq API key: ").strip()
        
    if not groq_key:
        print("ERROR: No Groq API key provided")
        return None
        
    # Get the appropriate prompt for this analyst type
    prompt = get_analyst_prompt(analyst_type, business_type, location, target_customers)
    
    # Format the prompt with parameters
    current_year = datetime.now().year
    formatted_prompt = format_query_prompt(
        analyst_type, prompt, business_type, location, 
        target_customers, outreach_channels, current_year
    )
        
    # Make the API call using requests directly instead of the groq client
    import requests
    
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }
    
    # System prompt
    system_prompt = f"You are researching leads for a {business_type} business in {location}."
    
    # User prompt
    user_prompt = f"""Researching potential leads on {datetime.now().strftime("%B %d, %Y")}.
{formatted_prompt}"""
        
    # Make the API call using requests directly instead of the groq client
    import requests
    
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }
    
    # System prompt
    system_prompt = f"You are researching leads for a {business_type} business in {location}."
    
    # User prompt
    user_prompt = f"""Researching potential leads on {datetime.now().strftime("%B %d, %Y")}.
{formatted_prompt}"""

    # Request payload
    payload = {
        "model": "groq/compound",  # Using groq/compound as requested
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0,
        "max_tokens": 2048
    }
    
    try:
        # Make the API call
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions", 
            headers=headers, 
            json=payload
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Display the prompt and response
            display_prompt_and_response(analyst_type, system_prompt, user_prompt, content)
            
            return content
        else:
            print(f"Error calling Groq API: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return None
    
    # Initialize real Groq client
    groq_client = groq.Client(api_key=groq_key)
    
    # Get the appropriate prompt for this analyst type
    prompt = get_analyst_prompt(analyst_type, business_type, location, target_customers)
    
    # Format the prompt with parameters
    current_year = datetime.now().year
    formatted_prompt = format_query_prompt(
        analyst_type, prompt, business_type, location, 
        target_customers, outreach_channels, current_year
    )
    
    # System prompt
    system_prompt = f"You are researching leads for a {business_type} business in {location}."
    
    # User prompt
    user_prompt = f"""Researching potential leads on {datetime.now().strftime("%B %d, %Y")}.
{formatted_prompt}"""
    
    try:
        # Make the actual API call to Groq
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0,
            max_tokens=2048
        )
        
        # Extract and return the content
        content = response.choices[0].message.content if response.choices else ""
        
        # Display the prompt and response
        display_prompt_and_response(analyst_type, system_prompt, user_prompt, content)
        
        return content
        
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return None

async def main():
    print("\n\n" + "=" * 100)
    print("                REAL GROQ API LEAD RESEARCHER")
    print("=" * 100 + "\n")

    # Get user input for business details
    print("Please provide business details to generate research queries using the real Groq API:\n")
    
    business_type = input("Business Type: ").strip() or "Digital Marketing Agency"
    location = input("Location: ").strip() or "Singapore"
    
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
        target_customers = "E-commerce businesses\nStartups seeking growth\nLocal SMEs with limited marketing budgets"
    
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
        outreach_channels = "Business networking events, industry conferences, referral partnerships"

    print("\n\nCalling Groq API to generate research queries...\n")
    
    # List of analyst types to generate queries for
    analyst_types = [
        "direct_leads_analyst",
        "partnership_analyst",
        "community_analyst",
        "events_analyst",
        "influencer_analyst"
    ]
    
    # Generate queries for each analyst type
    for analyst_type in analyst_types:
        result = await generate_queries_with_real_groq(
            analyst_type, 
            business_type, 
            location, 
            target_customers, 
            outreach_channels
        )
        
        if not result:
            print(f"Failed to generate queries for {analyst_type}")
    
    # Completion message
    print("\n" + "=" * 100)
    print("                 GROQ API QUERY GENERATION COMPLETE")
    print("=" * 100)
    print("\nThese queries would be used in a real execution to search for leads and opportunities.")
    print("The full process would continue with:")
    print("1. Web searches using these queries")
    print("2. Document enrichment to extract contact information")
    print("3. Creation of actionable briefings for each lead category")
    print("4. Final compilation into a comprehensive lead generation report")
    print("=" * 100 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
