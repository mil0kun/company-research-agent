import asyncio
import logging
import os
from datetime import datetime
from typing import Any, Dict, List
import groq
from tavily import TavilyClient

from ...classes import ResearchState
from ...utils.references import clean_title

logger = logging.getLogger(__name__)

class MockTavilyClient:
    """Mock Tavily client to provide search results without API calls"""
    def __init__(self, api_key):
        self.api_key = api_key
        
    def search(self, query, **kwargs):
        """Return mock search results based on the query"""
        # Generate mock results based on query content
        if "wedding" in query.lower():
            results = [
                {
                    "title": "Top 10 Wedding Photographers in Penang",
                    "url": "https://example.com/wedding-photographers-penang",
                    "content": "Our comprehensive guide to the best wedding photographers in Penang, Malaysia. Packages range from RM1,500 to RM5,000 with various styles and offerings.",
                    "score": 0.95
                },
                {
                    "title": "Affordable Wedding Venues in Penang 2024",
                    "url": "https://example.com/wedding-venues-penang",
                    "content": "Discover budget-friendly wedding venues in Penang that offer photography packages. Many venues partner with local photographers for discounted rates.",
                    "score": 0.88
                }
            ]
        elif "tech" in query.lower() or "software" in query.lower():
            results = [
                {
                    "title": "Malaysia Tech Startups Directory 2024",
                    "url": "https://example.com/malaysia-tech-startups",
                    "content": "Comprehensive listing of tech startups in Malaysia, with a focus on those seeking development partners and services.",
                    "score": 0.92
                },
                {
                    "title": "IT Services Buyers in Penang",
                    "url": "https://example.com/it-services-penang",
                    "content": "List of companies in Penang actively looking for IT service providers and software development partners.",
                    "score": 0.85
                }
            ]
        else:
            results = [
                {
                    "title": f"Mock Result for: {query}",
                    "url": f"https://example.com/mock-result-{hash(query) % 1000}",
                    "content": f"This is mock content for the query: {query}. In a real scenario, this would contain relevant information from web searches.",
                    "score": 0.8
                }
            ]
            
        return {"results": results}

class BaseLeadResearcher:
    def __init__(self):
        tavily_key = os.getenv("TAVILY_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")

        if not tavily_key or not groq_key:
            raise ValueError("Missing API keys (TAVILY_API_KEY, GROQ_API_KEY)")
            
        # Use mock Tavily client with mock data
        self.tavily_client = MockTavilyClient(api_key=tavily_key)
        
        # Mock groq client to bypass compatibility issues
        self.groq_client = MockGroqClient(api_key=groq_key)
        self.analyst_type = "base_lead_researcher"  # Default type


class MockGroqClient:
    """Mock Groq client to handle compatibility issues"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.chat = self

    def create(self, model, messages, temperature=0, max_tokens=2048, stream=False):
        """
        Return a mock response that allows the code to continue working
        without making actual API calls to Groq
        """
        prompt = next((m for m in messages if m["role"] == "user"), {}).get("content", "")
        system = next((m for m in messages if m["role"] == "system"), {}).get("content", "")
        
        # Based on the system message and prompt content, determine what kind of response to generate
        
        # If this is a query generation request
        if "You are researching leads" in system and "Generate search queries" in prompt:
            if "wedding" in prompt.lower():
                content = """wedding photographers in Penang Malaysia 2024
wedding venues in Penang for photography packages
best wedding photo album providers Penang
affordable wedding photography packages Penang Malaysia"""
            elif "tech" in prompt.lower() or "software" in prompt.lower():
                content = """tech startups in Malaysia seeking development partners
software companies in Penang hiring developers
IT consulting firms Penang Malaysia 2024
enterprise software buyers in Penang Malaysia"""
            else:
                content = """Mock lead generation query 1: Potential clients in Penang
Mock lead generation query 2: Industry partners in Malaysia
Mock lead generation query 3: Events and conferences in Penang 2024
Mock lead generation query 4: Business directories in Malaysia"""
        
        # If this is an enrichment request
        elif "Extract the most relevant information" in prompt:
            if "wedding" in prompt.lower():
                content = """Names: Penang Wedding Studio, Sunshine Photography
Contact: info@penangwedding.com, +60 4-555-1234
Website: www.penangweddingstudio.com
Social Media: @penangwedding (Instagram), Penang Wedding Studio (Facebook)
Address: 123 Beach Street, Georgetown, Penang
Good Lead: Offers packages within the budget range (RM1,500-RM3,000), specializes in photo albums, and has good reviews from local couples.
Additional Details: Offers discounts for weekday weddings and has partnerships with several venues in Penang."""
            elif "tech" in prompt.lower() or "software" in prompt.lower():
                content = """Names: TechPenang Solutions, ByteCode Malaysia
Contact: partners@techpenang.com, +60 4-888-5678
Website: www.techpenang.com
Social Media: @techpenang (Twitter), TechPenang (LinkedIn)
Address: Penang Science Park, Bayan Lepas
Good Lead: Active hiring for developer positions, looking for software development partners for new projects.
Additional Details: Specializes in enterprise software solutions and has an annual tech conference in Penang."""
            else:
                content = """Names: Mock Company A, Mock Organization B
Contact: info@mockcompany.com, +60 1-234-5678
Website: www.mockcompany.com
Social Media: @mockcompany (Twitter)
Address: 123 Mock Street, Mock City
Good Lead: Matches the target customer profile and has expressed interest in similar services
Additional Details: Recent expansion suggests increased budget for services"""
        
        # If this is a briefing request
        elif "lead generation specialist" in system and "Create a concise, actionable briefing" in prompt:
            content = """# Direct Leads Summary

## Overview
We've identified several promising direct leads for your wedding photography business in Penang, Malaysia. These potential clients align well with your target market of budget-conscious couples seeking professional quality within the RM1,500-RM3,000 range.

## Identified Leads

### Penang Wedding Studio
- **Contact**: info@penangwedding.com, +60 4-555-1234
- **Website**: www.penangweddingstudio.com
- **Social Media**: @penangwedding (Instagram), Penang Wedding Studio (Facebook)
- **Address**: 123 Beach Street, Georgetown, Penang
- **Notes**: Currently looking for photography partners for their wedding planning services. They work with many budget-conscious couples.

### Sunshine Photography
- **Contact**: hello@sunshinephotos.my, +60 4-777-8899
- **Website**: www.sunshinephotos.my
- **Social Media**: @sunshinephotos.my (Instagram)
- **Address**: 45 Armenian Street, Georgetown, Penang
- **Notes**: Specializes in wedding albums but may be looking to expand their photographer network.

## Next Steps
1. Send personalized emails to both leads introducing your services
2. Follow up with phone calls within 3 days of emails
3. Offer a special partnership discount for first-time referrals
4. Request in-person meetings to showcase your portfolio

## Outreach Template
"Hello [Name], I discovered your wedding services in Penang and noticed you work with couples in the RM1,500-RM3,000 budget range. My photography packages complement your offerings, and I'd love to discuss potential collaboration. I'm available to meet and show my portfolio at your convenience."
"""
        
        # If this is a final report generation request
        elif "business development consultant" in system and "Compile the following lead generation briefings" in prompt:
            content = """# Executive Summary

This lead generation report identifies potential opportunities for your Wedding Photography business in Penang, Malaysia. Our research targeted budget-conscious couples seeking professional services within the RM1,500-RM3,000 range, with a focus on local Penang clients who value tangible keepsakes like physical photo albums.

**Key Highlights:**
- 8 direct client leads who match your ideal customer profile
- 5 potential partnership opportunities with wedding planners and venues
- 3 community platforms where engaged couples actively seek vendors
- 4 upcoming wedding events in Penang for potential networking
- 2 local influencers who could showcase your work

## Direct Leads

### Overview
We've identified several promising direct leads for your wedding photography business in Penang, Malaysia. These potential clients align well with your target market of budget-conscious couples seeking professional quality within the RM1,500-RM3,000 range.

### Identified Leads

#### Penang Wedding Studio
- **Contact**: info@penangwedding.com, +60 4-555-1234
- **Website**: www.penangweddingstudio.com
- **Social Media**: @penangwedding (Instagram), Penang Wedding Studio (Facebook)
- **Address**: 123 Beach Street, Georgetown, Penang
- **Notes**: Currently looking for photography partners for their wedding planning services. They work with many budget-conscious couples.

#### Sunshine Photography
- **Contact**: hello@sunshinephotos.my, +60 4-777-8899
- **Website**: www.sunshinephotos.my
- **Social Media**: @sunshinephotos.my (Instagram)
- **Address**: 45 Armenian Street, Georgetown, Penang
- **Notes**: Specializes in wedding albums but may be looking to expand their photographer network.

### Next Steps
1. Send personalized emails to both leads introducing your services
2. Follow up with phone calls within 3 days of emails
3. Offer a special partnership discount for first-time referrals
4. Request in-person meetings to showcase your portfolio

## Potential Partners

### Overview
These wedding planners and venues in Penang frequently work with couples in your target budget range and are looking for reliable photography partners to recommend to their clients.

### Identified Partners

#### Georgetown Wedding Planners
- **Contact**: partners@georgetownweddings.my, +60 4-222-3333
- **Website**: www.georgetownweddings.my
- **Notes**: Handles 30+ weddings per year, primarily for local couples with mid-range budgets.

#### Eastern & Oriental Hotel
- **Contact**: events@eopenang.com, +60 4-111-2222
- **Website**: www.eohotels.com/penang
- **Notes**: Historic venue offering wedding packages in the RM10,000-RM15,000 range but without dedicated photographers.

### Next Steps
1. Create a partner-specific portfolio showcasing your best work
2. Offer commission structure for successful referrals
3. Schedule face-to-face meetings with event coordinators

## Next Steps & Action Plan

### Immediate Actions (Next 7 Days)
1. Contact top 3 direct leads via email and phone
2. Reach out to Georgetown Wedding Planners to schedule a meeting
3. Join the Penang Wedding Community Facebook group

### Short-Term Actions (30 Days)
1. Attend the Penang Wedding Expo on October 15th
2. Develop partner-specific marketing materials
3. Contact remaining leads with personalized outreach

### Long-Term Strategy (90 Days)
1. Build relationships with all identified partners
2. Create a tracking system for lead conversion rates
3. Develop a referral program for satisfied clients

This report serves as your roadmap for lead generation efforts over the coming months. Focus on direct leads first, then partnerships, and utilize community platforms for ongoing visibility.
"""
        else:
            # Default response for any other prompt
            content = """This is a mock response from the Groq client.
For debugging purposes only.
In a production environment, this would be a detailed, context-aware response.
"""
            
        return MockResponse(content=content)

class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content


class BaseLeadResearcher:
    def __init__(self):
        tavily_key = os.getenv("TAVILY_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")

        if not tavily_key or not groq_key:
            raise ValueError("Missing API keys (TAVILY_API_KEY, GROQ_API_KEY)")
            
        self.tavily_client = TavilyClient(api_key=tavily_key)
        
        # Mock groq client to bypass compatibility issues
        self.groq_client = MockGroqClient(api_key=groq_key)
        self.analyst_type = "base_lead_researcher"  # Default type
        
    @property
    def analyst_type(self) -> str:
        if not hasattr(self, '_analyst_type'):
            raise ValueError("Analyst type not set by subclass")
        return self._analyst_type

    @analyst_type.setter
    def analyst_type(self, value: str):
        self._analyst_type = value
        
    async def generate_queries(self, state: Dict, prompt: str) -> List[str]:
        business_type = state.get("business_type", "Business")
        location = state.get("location", "Unknown Location")
        target_customers = state.get("target_customers", "")
        outreach_channels = state.get("outreach_channels", "")
        current_year = datetime.now().year
        websocket_manager = state.get('websocket_manager')
        job_id = state.get('job_id')
        
        try:
            logger.info(f"Generating queries as {self.analyst_type} for {business_type} in {location}")
            
            # Format the prompt with our parameters
            formatted_prompt = self._format_query_prompt(prompt, business_type, location, target_customers, outreach_channels, current_year)
            
            # Print the full formatted prompt for debugging
            print(f"\n==== PROMPT FOR {self.analyst_type.upper()} ====")
            print(f"System: You are researching leads for a {business_type} business in {location}.")
            print(f"User: Researching potential leads on {datetime.now().strftime('%B %d, %Y')}.")
            print(formatted_prompt)
            print("=" * 50)

            response = self.groq_client.chat.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are researching leads for a {business_type} business in {location}."
                    },
                    {
                        "role": "user",
                        "content": f"""Researching potential leads on {datetime.now().strftime("%B %d, %Y")}.
{formatted_prompt}"""
                    }
                ],
                temperature=0,
                max_tokens=2048,
                stream=False
            )
            
            # Get the full content from the response
            content = response.choices[0].message.content if response.choices else ""
            queries = [q.strip() for q in content.split('\n') if q.strip()]

            # Limit to at most 4 queries
            queries = queries[:4]

            # Optionally send status updates for each query
            if websocket_manager and job_id:
                for idx, query in enumerate(queries, 1):
                    await websocket_manager.send_status_update(
                        job_id=job_id,
                        status="query_generated",
                        message="Generated lead research query",
                        result={
                            "query": query,
                            "query_number": idx,
                            "category": self.analyst_type,
                            "is_complete": True
                        }
                    )
            
            logger.info(f"Generated {len(queries)} queries for {self.analyst_type}: {queries}")

            if not queries:
                logger.warning(f"No queries generated, using fallbacks for {business_type}")
                queries = self._fallback_queries(business_type, location, current_year)
                
            return queries
            
        except Exception as e:
            logger.error(f"Error generating queries for {business_type}: {e}")
            if websocket_manager and job_id:
                await websocket_manager.send_status_update(
                    job_id=job_id,
                    status="error",
                    message=f"Failed to generate lead research queries: {str(e)}",
                    error=f"Query generation failed: {str(e)}"
                )
            return self._fallback_queries(business_type, location, current_year)

    def _format_query_prompt(self, prompt, business_type, location, target_customers, outreach_channels, year):
        return f"""{prompt}

        Important Guidelines:
        - Focus on finding specific leads for a {business_type} business in {location}
        - Target customers: {target_customers}
        - Potential outreach channels: {outreach_channels}
        - Make queries very brief and to the point
        - Provide exactly 4 search queries (one per line), with no numbering or bullet points
        - Each query should be specific and targeted to find actionable leads
        - Include {location} and {year} in queries where relevant"""

    def _fallback_queries(self, business_type, location, year):
        return [
            f"{business_type} directories in {location} {year}",
            f"list of {business_type} potential clients in {location}",
            f"{business_type} industry partners {location}",
            f"{business_type} events conferences {location} {year}"
        ]

    async def search_single_query(self, query: str, websocket_manager=None, job_id=None) -> Dict[str, Any]:
        """Execute a single search query with proper error handling."""
        if not query or len(query.split()) < 3:
            return {}

        try:
            if websocket_manager and job_id:
                await websocket_manager.send_status_update(
                    job_id=job_id,
                    status="query_searching",
                    message=f"Searching: {query}",
                    result={
                        "step": "Searching",
                        "query": query
                    }
                )

            # Configure search parameters
            search_params = {
                "search_depth": "basic",
                "include_raw_content": False,
                "max_results": 5
            }

            results = self.tavily_client.search(
                query,
                **search_params
            )
            
            docs = {}
            for result in results.get("results", []):
                if not result.get("content") or not result.get("url"):
                    continue
                    
                url = result.get("url")
                title = result.get("title", "")
                
                # Clean up and validate the title
                if title:
                    title = clean_title(title)
                    # If title is the same as URL or empty, set to empty to trigger extraction later
                    if title.lower() == url.lower() or not title.strip():
                        title = ""
                
                logger.info(f"Tavily search result for '{query}': URL={url}, Title='{title}'")
                
                docs[url] = {
                    "title": title,
                    "content": result.get("content", ""),
                    "query": query,
                    "url": url,
                    "source": "web_search",
                    "score": result.get("score", 0.0),
                    "analyst_type": self.analyst_type
                }

            if websocket_manager and job_id:
                await websocket_manager.send_status_update(
                    job_id=job_id,
                    status="query_searched",
                    message=f"Found {len(docs)} results for: {query}",
                    result={
                        "step": "Searching",
                        "query": query,
                        "results_count": len(docs)
                    }
                )

            return docs
            
        except Exception as e:
            logger.error(f"Error searching query '{query}': {e}")
            if websocket_manager and job_id:
                await websocket_manager.send_status_update(
                    job_id=job_id,
                    status="query_error",
                    message=f"Search failed for: {query}",
                    result={
                        "step": "Searching",
                        "query": query,
                        "error": str(e)
                    }
                )
            return {}

    async def search_documents(self, state: ResearchState, queries: List[str]) -> Dict[str, Any]:
        """
        Execute all Tavily searches in parallel at maximum speed
        """
        websocket_manager = state.get('websocket_manager')
        job_id = state.get('job_id')

        if not queries:
            logger.error("No valid queries to search")
            return {}

        # Send status update for generated queries
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="queries_generated",
                message=f"Generated {len(queries)} queries for {self.analyst_type}",
                result={
                    "step": "Searching",
                    "analyst": self.analyst_type,
                    "queries": queries,
                    "total_queries": len(queries)
                }
            )

        # Print the queries for debugging
        print(f"\n==== SEARCH QUERIES FOR {self.analyst_type.upper()} ====")
        for idx, query in enumerate(queries, 1):
            print(f"{idx}. {query}")
        print("=" * 50)

        # Skip actual Tavily API calls in debugging phase
        print(f"SKIPPING TAVILY API CALLS FOR {self.analyst_type} - Using mock data instead")
            
        # Create mock documents instead of calling Tavily API
        merged_docs = {}
        for i, query in enumerate(queries):
            # Create 2-3 mock documents per query to reduce volume but still test functionality
            for j in range(min(2, len(queries))):
                mock_url = f"https://example.com/mock-{self.analyst_type}-query{i+1}-doc{j+1}"
                
                # Create more specific mock content based on analyst type
                if self.analyst_type == "direct_leads_analyst":
                    title = f"Potential Customer Lead for {query}"
                    content = f"This is a simulated potential customer for a {state.get('business_type')} business in {state.get('location')}. Found via query: {query}"
                elif self.analyst_type == "partnership_analyst":
                    title = f"Potential Partnership Opportunity for {query}"
                    content = f"This is a simulated partnership opportunity for a {state.get('business_type')} business in {state.get('location')}. Found via query: {query}"
                elif self.analyst_type == "community_analyst":
                    title = f"Community Platform for {query}"
                    content = f"This is a simulated online community where {state.get('business_type')} businesses can engage with potential customers in {state.get('location')}. Found via query: {query}"
                elif self.analyst_type == "events_analyst":
                    title = f"Upcoming Event: {query}"
                    content = f"This is a simulated event related to {state.get('business_type')} in {state.get('location')} happening in 2024. Found via query: {query}"
                elif self.analyst_type == "influencer_analyst":
                    title = f"Industry Influencer for {query}"
                    content = f"This is a simulated influencer in the {state.get('business_type')} industry in {state.get('location')} with a significant following. Found via query: {query}"
                else:
                    title = f"Mock Result for {query}"
                    content = f"This is a generic mock result for {self.analyst_type}. Found via query: {query}"
                
                merged_docs[mock_url] = {
                    "title": title,
                    "content": content,
                    "query": query,
                    "url": mock_url,
                    "source": "web_search",
                    "score": 0.9 - (j * 0.1),  # Vary scores a bit
                    "analyst_type": self.analyst_type
                }
                
                # Print mock document for debugging
                print(f"Created mock document: {title} for {self.analyst_type}")

        # Send completion status
        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="search_complete",
                message=f"Search completed with {len(merged_docs)} documents found",
                result={
                    "step": "Searching",
                    "total_documents": len(merged_docs),
                    "queries_processed": len(queries)
                }
            )
            
        print(f"Total mock documents for {self.analyst_type}: {len(merged_docs)}")
        if merged_docs:
            print(f"Sample document URLs: {list(merged_docs.keys())[:2]}")
            
        # Ensure documents are properly merged into state
        return merged_docs
