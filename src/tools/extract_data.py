#!/usr/bin/env python3
"""
extract_data.py - Extract specific fields from BB8 organism files.

Replaces manual jq commands with clean Python interface.
Usage examples:
  python extract_data.py --fields genes.genes.ColorR,genes.genes.ColorG data/bibites/bibite_18.bb8
  python extract_data.py --fields genes.genes.AverageMutationNumber --batch data/bibites/
"""

import click
import orjson
from pathlib import Path
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.progress import track
from rich.table import Table

from ..core.parser import load_bb8_file, extract_multiple_fields, BB8ParseError

console = Console()

@click.command()
@click.argument('input_path', type=click.Path(exists=True, path_type=Path))
@click.option('--fields', '-f', required=True, 
              help='Comma-separated list of field paths (e.g., genes.genes.ColorR,genes.genes.ColorG)')
@click.option('--batch', '-b', is_flag=True, 
              help='Process all .bb8 files in directory')
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Output file (JSON format)')
@click.option('--format', type=click.Choice(['json', 'table', 'csv']), 
              default='table', help='Output format')
def extract_data(input_path: Path, fields: str, batch: bool, output: Optional[Path], format: str):
    """Extract specific fields from BB8 organism files."""
    
    field_paths = [f.strip() for f in fields.split(',')]
    
    if batch or input_path.is_dir():
        # Batch processing
        bb8_files = list(input_path.glob('*.bb8'))
        if not bb8_files:
            console.print(f"[red]No .bb8 files found in {input_path}[/red]")
            return
        
        console.print(f"[blue]Processing {len(bb8_files)} files...[/blue]")
        
        results = []
        errors = []
        
        for file_path in track(bb8_files, description="Extracting data"):
            try:
                data = load_bb8_file(file_path)
                extracted = extract_multiple_fields(data, field_paths)
                extracted['_file'] = str(file_path.name)
                results.append(extracted)
                
            except BB8ParseError as e:
                errors.append(f"{file_path.name}: {e}")
        
        # Display results
        if format == 'table':
            _display_table(results, field_paths)
        elif format == 'json':
            _display_json(results)
        elif format == 'csv':
            _display_csv(results, field_paths)
        
        if errors:
            console.print(f"\n[red]Errors in {len(errors)} files:[/red]")
            for error in errors:
                console.print(f"  {error}")
        
        # Save output if requested
        if output:
            with open(output, 'wb') as f:
                f.write(orjson.dumps(results, option=orjson.OPT_INDENT_2))
            console.print(f"\n[green]Results saved to {output}[/green]")
    
    else:
        # Single file processing
        try:
            data = load_bb8_file(input_path)
            extracted = extract_multiple_fields(data, field_paths)
            
            if format == 'json':
                console.print(orjson.dumps(extracted, option=orjson.OPT_INDENT_2).decode())
            else:
                # Simple key-value display
                for field_path, value in extracted.items():
                    console.print(f"{field_path}: {value}")
                    
        except BB8ParseError as e:
            console.print(f"[red]Error: {e}[/red]")

def _display_table(results: List[Dict[str, Any]], field_paths: List[str]):
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

def _display_json(results: List[Dict[str, Any]]):
    """Display results as formatted JSON."""
    console.print(orjson.dumps(results, option=orjson.OPT_INDENT_2).decode())

def _display_csv(results: List[Dict[str, Any]], field_paths: List[str]):
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

if __name__ == '__main__':
    extract_data()