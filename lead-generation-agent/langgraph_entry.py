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
    
    # Print the state before running
    initial_state = {
        "target_customers": input.get("target_customers", ""),
        "outreach_channels": input.get("outreach_channels", ""),
        "business_type": input.get("business_type", ""),
        "location": input.get("location", ""),
        "documents": {}  # Initialize documents dictionary
    }
    print(f"\nInitial state: {list(initial_state.keys())}")
    
    # Execute the graph and yield states
    async for state in graph.run(thread={}):
        # Explicitly ensure documents are passed along
        print(f"\nState keys from graph: {list(state.keys())}")
        if isinstance(state, dict) and "documents" not in state and hasattr(state, "get_docs"):
            docs = state.get_docs()
            if docs:
                print(f"Found {len(docs)} documents in get_docs() but not in state keys")
                state["documents"] = docs
                
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
        print("\n=== Starting Test Run with Input ===")
        print(f"Business Type: {test_input['business_type']}")
        print(f"Location: {test_input['location']}")
        print("Target Customers: ", test_input['target_customers'][:50] + "...")
        print("Outreach Channels: ", test_input['outreach_channels'][:50] + "...")
        print("\n=== Running Workflow ===")
        
        async for state in main(test_input):
            print(f"\n>>> State update: {list(state.keys())}")
            
            # Print query information if available
            if 'direct_queries' in state:
                print(f"Direct Queries: {state['direct_queries']}")
            if 'partnership_queries' in state:
                print(f"Partnership Queries: {state['partnership_queries']}")
                
            # Print document counts
            docs = state.get("documents", {})
            print(f"Documents count: {len(docs)}")
            if docs:
                print(f"First document URL: {list(docs.keys())[0] if docs else 'None'}")
            
            # Print organized documents if available
            org_docs = state.get("organized_docs", {})
            if org_docs:
                print(f"Organized docs types: {list(org_docs.keys())}")
                for analyst_type, docs in org_docs.items():
                    print(f"  {analyst_type}: {len(docs)} docs")
            
            # Print curated docs if available
            curated_docs = state.get("curated_docs", {})
            if curated_docs:
                print(f"Curated docs types: {list(curated_docs.keys())}")
        
        # Final report is in the last state
        print("\n=== Final Report ===")
        print(state.get("report") or state.get("editor", {}).get("report", "No report generated"))
    
    # Execute the test
    asyncio.run(run_test())
