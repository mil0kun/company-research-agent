import json
import os
from typing import AsyncIterator, Dict

from backend.graph import Graph
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def main(input: Dict) -> AsyncIterator[Dict]:
    """
    Main entry point for the lead generation graph when used in LangGraph.
    """
    # Initialize the graph with input parameters
    graph = Graph(
        target_customers=input.get("target_customers", ""),
        outreach_channels=input.get("outreach_channels", ""),
        business_type=input.get("business_type", ""),
        location=input.get("location", "")
    )
    
    # Execute the graph and yield states
    async for state in graph.run(thread={}):
        yield state

if __name__ == "__main__":
    import asyncio
    
    # Test input for local development
    test_input = {
        "target_customers": """Budget-conscious couples seeking professional quality within the RM1,500-RM3,000 range.
Couples getting married in Penang or nearby states who prefer local vendors.
Value-seeking couples who prioritize tangible keepsakes, like a physical photo album.""",
        "outreach_channels": """Wedding Planners and Coordinators based in Penang.
Local wedding venues (hotels, event halls).
Online wedding directories and Facebook groups for Malaysian couples.
Bridal boutiques and makeup artists in Penang for cross-promotion.
Organizers of wedding expos in Penang and Kuala Lumpur.""",
        "business_type": "Wedding Photography",
        "location": "Penang, Malaysia"
    }
    
    # Run the graph with test input
    async def run_test():
        async for state in main(test_input):
            print(f"State update: {list(state.keys())}")
        
        # Final report is in the last state
        print("\nFinal report:")
        print(state.get("report") or state.get("editor", {}).get("report", "No report generated"))
    
    # Execute the test
    asyncio.run(run_test())
