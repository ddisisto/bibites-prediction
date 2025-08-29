#!/usr/bin/env python3
"""
BB8 file parser using orjson for high-performance JSON parsing.
Handles UTF-8 BOM and provides clean interface for Bibites organism data.
"""

import orjson
from pathlib import Path
from typing import Dict, Any, List, Optional
from rich.console import Console

console = Console()

class BB8ParseError(Exception):
    """Raised when BB8 file cannot be parsed."""
    pass

def load_bb8_file(file_path: Path) -> Dict[str, Any]:
    """
    Load and parse a .bb8 file with UTF-8 BOM handling.
    
    Args:
        file_path: Path to the .bb8 file
        
    Returns:
        Dict containing parsed JSON data
        
    Raises:
        BB8ParseError: If file cannot be parsed or doesn't exist
    """
    if not file_path.exists():
        raise BB8ParseError(f"File not found: {file_path}")
    
    try:
        # Read with UTF-8-BOM handling
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Parse with orjson (3x faster than stdlib json)
        data = orjson.loads(content.encode('utf-8'))
        
        return data
    
    except orjson.JSONDecodeError as e:
        raise BB8ParseError(f"Invalid JSON in {file_path}: {e}")
    except Exception as e:
        raise BB8ParseError(f"Error reading {file_path}: {e}")

def extract_field(data: Dict[str, Any], field_path: str) -> Any:
    """
    Extract a field from nested JSON data using dot notation.
    
    Args:
        data: Parsed JSON data
        field_path: Dot-separated path like "genes.ColorR" 
        
    Returns:
        Field value or None if not found
    """
    try:
        current = data
        for part in field_path.split('.'):
            current = current[part]
        return current
    except (KeyError, TypeError):
        return None

def extract_multiple_fields(data: Dict[str, Any], field_paths: List[str]) -> Dict[str, Any]:
    """
    Extract multiple fields from JSON data.
    
    Args:
        data: Parsed JSON data  
        field_paths: List of dot-separated field paths
        
    Returns:
        Dict mapping field paths to extracted values
    """
    result = {}
    for path in field_paths:
        result[path] = extract_field(data, path)
    return result

def validate_bb8_structure(data: Dict[str, Any]) -> bool:
    """
    Basic validation that data has expected BB8 structure.
    
    Args:
        data: Parsed JSON data
        
    Returns:
        True if structure is valid, False otherwise
    """
    required_top_level = ['transform', 'genes', 'brain', 'rb2d', 'body', 'clock']
    
    for field in required_top_level:
        if field not in data:
            console.print(f"[red]Missing required field: {field}[/red]")
            return False
    
    return True

if __name__ == "__main__":
    # Simple test
    test_file = Path("data/bibites/bibite_18.bb8")
    if test_file.exists():
        try:
            data = load_bb8_file(test_file)
            console.print(f"[green]Successfully parsed {test_file}[/green]")
            console.print(f"Top-level keys: {list(data.keys())}")
            
            # Test field extraction
            color_r = extract_field(data, "genes.ColorR")
            console.print(f"ColorR: {color_r}")
            
        except BB8ParseError as e:
            console.print(f"[red]Parse error: {e}[/red]")
    else:
        console.print(f"[yellow]Test file not found: {test_file}[/yellow]")