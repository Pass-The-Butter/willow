# Willow - the Company Brain

A knowledge management system for storing and retrieving company information.

## Overview

Willow is a simple yet powerful tool for managing company knowledge. It allows you to store, retrieve, and organize information using tags for easy categorization.

## Features

- **Store Knowledge**: Save company information with unique keys
- **Tag Organization**: Categorize knowledge using tags for easy retrieval
- **Search by Tag**: Find all related knowledge by searching tags
- **Simple API**: Clean and intuitive Python interface

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from src.brain import Brain

# Create a new brain instance
brain = Brain()

# Store knowledge with tags
brain.store("remote-policy", "Employees can work remotely up to 3 days per week.", tags=["hr", "policies"])
brain.store("vacation-days", "All employees receive 20 vacation days per year.", tags=["hr", "benefits"])

# Retrieve specific knowledge
policy = brain.retrieve("remote-policy")
print(policy)  # "Employees can work remotely up to 3 days per week."

# Search by tag
hr_items = brain.search_by_tag("hr")
print(hr_items)  # ["remote-policy", "vacation-days"]
```

## Running Tests

```bash
pytest
```

## License

MIT License
