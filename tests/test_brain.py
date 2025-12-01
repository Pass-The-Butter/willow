"""Tests for the Brain class."""

import pytest
from src.brain import Brain


class TestBrain:
    """Test cases for the Brain class."""
    
    def test_init(self):
        """Test Brain initialization."""
        brain = Brain()
        assert len(brain) == 0
    
    def test_store_and_retrieve(self):
        """Test storing and retrieving knowledge."""
        brain = Brain()
        brain.store("greeting", "Hello, World!")
        assert brain.retrieve("greeting") == "Hello, World!"
    
    def test_retrieve_nonexistent(self):
        """Test retrieving non-existent knowledge returns None."""
        brain = Brain()
        assert brain.retrieve("nonexistent") is None
    
    def test_store_with_tags(self):
        """Test storing knowledge with tags."""
        brain = Brain()
        brain.store("policy1", "Work from home policy", tags=["hr", "policies"])
        assert brain.retrieve("policy1") == "Work from home policy"
        assert "policy1" in brain.search_by_tag("hr")
        assert "policy1" in brain.search_by_tag("policies")
    
    def test_search_by_tag_empty(self):
        """Test searching by non-existent tag returns empty list."""
        brain = Brain()
        assert brain.search_by_tag("nonexistent") == []
    
    def test_list_all_keys(self):
        """Test listing all knowledge keys."""
        brain = Brain()
        brain.store("key1", "value1")
        brain.store("key2", "value2")
        keys = brain.list_all_keys()
        assert "key1" in keys
        assert "key2" in keys
        assert len(keys) == 2
    
    def test_delete(self):
        """Test deleting knowledge."""
        brain = Brain()
        brain.store("key1", "value1", tags=["tag1"])
        assert brain.delete("key1") is True
        assert brain.retrieve("key1") is None
        assert "key1" not in brain.search_by_tag("tag1")
    
    def test_delete_nonexistent(self):
        """Test deleting non-existent knowledge returns False."""
        brain = Brain()
        assert brain.delete("nonexistent") is False
    
    def test_len(self):
        """Test length of brain."""
        brain = Brain()
        assert len(brain) == 0
        brain.store("key1", "value1")
        assert len(brain) == 1
        brain.store("key2", "value2")
        assert len(brain) == 2
    
    def test_store_empty_key_raises(self):
        """Test that storing with empty key raises ValueError."""
        brain = Brain()
        with pytest.raises(ValueError, match="Key cannot be empty"):
            brain.store("", "value")
    
    def test_store_empty_value_raises(self):
        """Test that storing with empty value raises ValueError."""
        brain = Brain()
        with pytest.raises(ValueError, match="Value cannot be empty"):
            brain.store("key", "")
    
    def test_overwrite_existing(self):
        """Test that storing with existing key overwrites."""
        brain = Brain()
        brain.store("key1", "value1")
        brain.store("key1", "value2")
        assert brain.retrieve("key1") == "value2"
    
    def test_delete_cleans_up_empty_tags(self):
        """Test that deleting knowledge cleans up empty tag sets."""
        brain = Brain()
        brain.store("key1", "value1", tags=["unique-tag"])
        assert "key1" in brain.search_by_tag("unique-tag")
        brain.delete("key1")
        # After deletion, the empty tag set should be cleaned up
        assert brain.search_by_tag("unique-tag") == []
