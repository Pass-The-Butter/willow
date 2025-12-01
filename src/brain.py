"""
Core brain module for Willow.

This module provides the main interface for storing and retrieving
company knowledge.
"""

from typing import Optional


class Brain:
    """
    The Company Brain - a simple knowledge management system.
    
    Stores and retrieves company knowledge using key-value pairs
    with optional tagging for organization.
    """
    
    def __init__(self):
        """Initialize an empty brain."""
        self._knowledge = {}
        self._tags = {}
    
    def store(self, key: str, value: str, tags: Optional[list] = None) -> None:
        """
        Store a piece of knowledge in the brain.
        
        Args:
            key: A unique identifier for the knowledge.
            value: The knowledge content to store.
            tags: Optional list of tags for categorization.
        """
        if not key:
            raise ValueError("Key cannot be empty")
        if not value:
            raise ValueError("Value cannot be empty")
            
        self._knowledge[key] = value
        
        if tags:
            for tag in tags:
                if tag not in self._tags:
                    self._tags[tag] = set()
                self._tags[tag].add(key)
    
    def retrieve(self, key: str) -> Optional[str]:
        """
        Retrieve a piece of knowledge by its key.
        
        Args:
            key: The identifier of the knowledge to retrieve.
            
        Returns:
            The knowledge content if found, None otherwise.
        """
        return self._knowledge.get(key)
    
    def search_by_tag(self, tag: str) -> list:
        """
        Find all knowledge entries with a specific tag.
        
        Args:
            tag: The tag to search for.
            
        Returns:
            A list of keys that have the specified tag.
        """
        return list(self._tags.get(tag, set()))
    
    def list_all_keys(self) -> list:
        """
        List all knowledge keys in the brain.
        
        Returns:
            A list of all knowledge keys.
        """
        return list(self._knowledge.keys())
    
    def delete(self, key: str) -> bool:
        """
        Delete a piece of knowledge from the brain.
        
        Args:
            key: The identifier of the knowledge to delete.
            
        Returns:
            True if the knowledge was deleted, False if it didn't exist.
        """
        if key in self._knowledge:
            del self._knowledge[key]
            # Remove from all tags
            for tag in self._tags:
                self._tags[tag].discard(key)
            return True
        return False
    
    def __len__(self) -> int:
        """Return the number of knowledge entries in the brain."""
        return len(self._knowledge)
