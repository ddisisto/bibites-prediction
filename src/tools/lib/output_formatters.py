"""
Output formatting utilities for extract_data.py

Provides consistent output formatting across different data types and formats.
Supports table, JSON, and CSV output modes with rich console formatting.
"""

import orjson
from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table

console = Console()


def display_table(results: List[Dict[str, Any]], field_paths: List[str]):
    """Display results as a formatted table."""
    table = Table()
    table.add_column("File", style="cyan")
    
    for field in field_paths:
        table.add_column(field, style="green")
    
    for result in results:
        row = [result.get('_file', '')]
        for field in field_paths:
            value = result.get(field)
            if value is None:
                row.append("[dim]None[/dim]")
            elif isinstance(value, float):
                row.append(f"{value:.6f}")
            else:
                row.append(str(value))
        table.add_row(*row)
    
    console.print(table)


def display_json(results: List[Dict[str, Any]]):
    """Display results as formatted JSON."""
    console.print(orjson.dumps(results, option=orjson.OPT_INDENT_2).decode())


def display_csv(results: List[Dict[str, Any]], field_paths: List[str]):
    """Display results as CSV format."""
    # Header
    header = ['file'] + field_paths
    console.print(','.join(header))
    
    # Data rows
    for result in results:
        row = [result.get('_file', '')]
        for field in field_paths:
            value = result.get(field)
            if value is None:
                row.append('')
            else:
                row.append(str(value))
        console.print(','.join(row))


def save_json_output(data: Any, output_path):
    """Save data as formatted JSON to file."""
    with open(output_path, 'wb') as f:
        f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))
    console.print(f"\n[green]Results saved to {output_path}[/green]")