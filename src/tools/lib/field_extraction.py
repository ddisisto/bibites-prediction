"""
Core field extraction utilities for extract_data.py

Provides single-file and batch processing capabilities for extracting
specific fields from BB8 organism files with error handling and progress tracking.
"""

import orjson
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console
from rich.progress import track

from ...core.parser import load_bb8_file, extract_multiple_fields, BB8ParseError

console = Console()


def process_single_file(file_path: Path, field_paths: List[str]) -> Dict[str, Any]:
    """Extract fields from a single BB8 file."""
    try:
        data = load_bb8_file(file_path)
        return extract_multiple_fields(data, field_paths)
    except BB8ParseError as e:
        raise BB8ParseError(f"Error processing {file_path.name}: {e}")


def process_batch_files(directory_path: Path, field_paths: List[str]) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Extract fields from all BB8 files in a directory.
    
    Returns:
        Tuple of (results, errors) where results is list of extracted data
        and errors is list of error messages.
    """
    bb8_files = list(directory_path.glob('*.bb8'))
    if not bb8_files:
        raise ValueError(f"No .bb8 files found in {directory_path}")
    
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
    
    return results, errors


def extract_species_field(directory_path: Path, output: Optional[Path] = None) -> Dict[str, Any]:
    """Extract species ID field from organisms for species name mapping.
    
    This function is designed to extract species-related fields to create
    mappings between hereditary tags and sim-generated species names.
    """
    if directory_path.is_file():
        directory_path = directory_path.parent
    
    bb8_files = list(directory_path.glob('*.bb8'))
    if not bb8_files:
        console.print(f"[red]No .bb8 files found in {directory_path}[/red]")
        return {}
    
    console.print(f"[blue]Extracting species fields from {len(bb8_files)} organisms...[/blue]")
    
    # Fields related to species identification
    species_fields = ['genes.tag', 'genes.genes.SpeciesID', 'genes.speciesID']
    
    species_mapping = {}
    errors = []
    
    for file_path in track(bb8_files, description="Extracting species data"):
        try:
            data = load_bb8_file(file_path)
            extracted = extract_multiple_fields(data, species_fields)
            
            # Store the mapping for this organism
            species_mapping[file_path.name] = {
                'hereditary_tag': extracted.get('genes.tag'),
                'species_id_1': extracted.get('genes.genes.SpeciesID'),
                'species_id_2': extracted.get('genes.speciesID')
            }
            
        except BB8ParseError as e:
            errors.append(f"{file_path.name}: {e}")
    
    result = {
        'total_organisms': len(bb8_files),
        'species_mappings': species_mapping,
        'errors': len(errors)
    }
    
    # Display summary
    console.print(f"\n[bold]Species Field Extraction Summary:[/bold]")
    console.print(f"  Total organisms: {len(bb8_files)}")
    console.print(f"  Successful extractions: {len(species_mapping)}")
    if errors:
        console.print(f"  Errors: {len(errors)}")
    
    # Save output if requested
    if output:
        with open(output, 'wb') as f:
            f.write(orjson.dumps(result, option=orjson.OPT_INDENT_2))
        console.print(f"\n[green]Species mappings saved to {output}[/green]")
    
    return result