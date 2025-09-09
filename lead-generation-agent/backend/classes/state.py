import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class ResearchState(dict):
    """
    State container for the lead generation process.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the state with a default fallback.
        """
        return super().get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the state.
        """
        self[key] = value
        
    def update_nested(self, key: str, value: Dict[str, Any]) -> None:
        """
        Update a nested dictionary in the state.
        """
        if key not in self:
            self[key] = {}
        if isinstance(self[key], dict) and isinstance(value, dict):
            self[key].update(value)
        else:
            self[key] = value
            
    def add_to_list(self, key: str, value: Any) -> None:
        """
        Add a value to a list in the state.
        """
        if key not in self:
            self[key] = []
        if isinstance(self[key], list):
            self[key].append(value)
        else:
            self[key] = [value]
            
    def get_docs(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all documents from the state.
        """
        return self.get("documents", {})
    
    def get_doc_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get a document by URL.
        """
        return self.get_docs().get(url)
    
    def add_doc(self, url: str, doc: Dict[str, Any]) -> None:
        """
        Add a document to the state.
        """
        if "documents" not in self:
            self["documents"] = {}
        self["documents"][url] = doc
        
    def merge_docs(self, docs: Dict[str, Dict[str, Any]]) -> None:
        """
        Merge documents into the state.
        """
        if "documents" not in self:
            self["documents"] = {}
        self["documents"].update(docs)
        
    def get_all_analyst_docs(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Get all documents grouped by analyst type.
        """
        analyst_docs = {}
        for url, doc in self.get_docs().items():
            analyst_type = doc.get("analyst_type", "unknown")
            if analyst_type not in analyst_docs:
                analyst_docs[analyst_type] = {}
            analyst_docs[analyst_type][url] = doc
        return analyst_docs
