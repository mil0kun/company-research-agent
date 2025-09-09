import logging
from typing import Dict, List, Optional, AsyncIterator

from langgraph.graph import StateGraph, END
from .classes import ResearchState
from .nodes import research, collector, curator, enricher, briefing, editor

logger = logging.getLogger(__name__)

class Graph:
    def __init__(
        self,
        target_customers: str,
        outreach_channels: str,
        business_type: Optional[str] = None,
        location: Optional[str] = None,
        websocket_manager = None,
        job_id: Optional[str] = None
    ):
        self.target_customers = target_customers
        self.outreach_channels = outreach_channels
        self.business_type = business_type
        self.location = location
        self.websocket_manager = websocket_manager
        self.job_id = job_id
        
        # Build the graph
        self.workflow = self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow for lead generation.
        """
        # Create the graph
        builder = StateGraph(ResearchState)
        
        # Add all nodes
        builder.add_node("research", research)
        builder.add_node("collector", collector)
        builder.add_node("curator", curator)
        builder.add_node("enricher", enricher)
        builder.add_node("briefing", briefing)
        builder.add_node("editor", editor)
        
        # Define the edges
        builder.add_edge("research", "collector")
        builder.add_edge("collector", "curator")
        builder.add_edge("curator", "enricher")
        builder.add_edge("enricher", "briefing")
        builder.add_edge("briefing", "editor")
        builder.add_edge("editor", END)
        
        # Set the entry point
        builder.set_entry_point("research")
        
        # Configure checkpoint options to ensure state is preserved
        graph_config = {"checkpoint_options": {"debug": True, "persist_raw": True}}
        
        # Compile the graph
        return builder.compile()
    
    async def run(self, thread: Dict) -> AsyncIterator[Dict]:
        """
        Run the lead generation workflow.
        """
        # Initialize the state with input parameters
        state = ResearchState({
            "target_customers": self.target_customers,
            "outreach_channels": self.outreach_channels,
            "business_type": self.business_type,
            "location": self.location,
            "websocket_manager": self.websocket_manager,
            "job_id": self.job_id,
            "documents": {}  # Initialize documents dictionary
        })
        
        print(f"Running graph with initial state keys: {list(state.keys())}")
        
        # Execute the graph - older version of langgraph
        # doesn't accept thread parameter
        async for s in self.workflow.astream(state):
            # Debug what's being passed
            print(f"Graph yielding state with keys: {list(s.keys())}")
            if "documents" in s:
                print(f"Documents in state: {len(s['documents'])}")
            else:
                print("No documents in yielded state")
                
            # Create a proper dictionary from the state to ensure all data is preserved
            if hasattr(s, "__dict__"):
                # If it's an object, convert to dict
                yield dict(s)
            else:
                # Otherwise just pass it through
                yield s
