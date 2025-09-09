import asyncio
import logging
import os
from datetime import datetime
from typing import Any, Dict, List
import groq
from tavily import AsyncTavilyClient

from ...classes import ResearchState
from ...utils.references import clean_title

logger = logging.getLogger(__name__)

class BaseLeadResearcher:
    def __init__(self):
        tavily_key = os.getenv("TAVILY_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")

        if not tavily_key or not groq_key:
            raise ValueError("Missing API keys (TAVILY_API_KEY, GROQ_API_KEY)")
            
        self.tavily_client = AsyncTavilyClient(api_key=tavily_key)
        self.groq_client = groq.Client(api_key=groq_key)
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

            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are researching leads for a {business_type} business in {location}."
                    },
                    {
                        "role": "user",
                        "content": f"""Researching potential leads on {datetime.now().strftime("%B %d, %Y")}.
{self._format_query_prompt(prompt, business_type, location, target_customers, outreach_channels, current_year)}"""
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

            results = await self.tavily_client.search(
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

        # Prepare all search parameters upfront
        search_params = {
            "search_depth": "basic",
            "include_raw_content": False,
            "max_results": 5
        }

        if websocket_manager and job_id:
            await websocket_manager.send_status_update(
                job_id=job_id,
                status="search_started",
                message=f"Using Tavily to search for {len(queries)} queries",
                result={
                    "step": "Searching",
                    "total_queries": len(queries)
                }
            )
            
        # Create all API calls upfront
        search_tasks = [
            self.tavily_client.search(query, **search_params)
            for query in queries
        ]

        # Execute all API calls in parallel
        try:
            results = await asyncio.gather(*search_tasks)
        except Exception as e:
            logger.error(f"Error during parallel search execution: {e}")
            return {}

        # Process results
        merged_docs = {}
        for query, result in zip(queries, results):
            for item in result.get("results", []):
                if not item.get("content") or not item.get("url"):
                    continue
                    
                url = item.get("url")
                title = item.get("title", "")
                
                if title:
                    title = clean_title(title)
                    if title.lower() == url.lower() or not title.strip():
                        title = ""

                merged_docs[url] = {
                    "title": title,
                    "content": item.get("content", ""),
                    "query": query,
                    "url": url,
                    "source": "web_search",
                    "score": item.get("score", 0.0),
                    "analyst_type": self.analyst_type
                }

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

        return merged_docs
