"""
bibites_analysis.py - Analysis orchestration for bibites ecosystem analysis.

Orchestrates all analysis operations by delegating to existing extract_data.py modules:
- Population and species analysis
- Spatial distribution analysis  
- Cross-cycle comparison analysis
- Field extraction and species comparison
- Metadata analysis coordination

This module provides high-level analysis runners that coordinate the existing 
specialized analysis modules.
"""

from pathlib import Path
from typing import Optional, List, Tuple
from rich.console import Console

# Import analysis modules from extract_data.py  
from .field_extraction import process_batch_files, extract_species_field
from .population_analysis import generate_species_summary
from .spatial_analysis import generate_spatial_analysis
from .comparison_tools import compare_cycle_directories, compare_specific_species
from .output_formatters import display_table, display_json, display_csv, save_json_output

# Import metadata extraction from extract_metadata.py
from ..extract_metadata import extract_metadata_from_save, display_metadata_results, MetadataExtractionError

# Import data access functions
from .bibites_data import get_zip_file_from_data_path, BibitesDataError

console = Console()

class BibitesAnalysisError(Exception):
    """Raised when analysis operation fails."""
    pass

def run_population_analysis(data_paths: List[Path], output: Optional[Path], 
                           by_species: bool, quick_mode: bool = True) -> None:
    """Run population/species summary analysis."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Population analysis requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    generate_species_summary(bibites_dir, output, quick_mode=quick_mode, use_species_id=by_species)

def run_spatial_analysis(data_paths: List[Path], output: Optional[Path]) -> None:
    """Run spatial distribution analysis."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Spatial analysis requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    generate_spatial_analysis(bibites_dir, output)

def run_comparison_analysis(data_paths: List[Path], output: Optional[Path]) -> None:
    """Run population comparison between cycles."""
    if len(data_paths) != 2:
        raise BibitesAnalysisError("Comparison analysis requires exactly two datasets (use --last 2)")
    
    # Order matters: newer first, older second for proper comparison direction
    bibites_dir_a = data_paths[0] / 'bibites'  # More recent
    bibites_dir_b = data_paths[1] / 'bibites'  # Older
    
    if not bibites_dir_a.exists():
        raise BibitesAnalysisError(f"First dataset bibites directory not found: {bibites_dir_a}")
    if not bibites_dir_b.exists():
        raise BibitesAnalysisError(f"Second dataset bibites directory not found: {bibites_dir_b}")
    
    compare_cycle_directories(bibites_dir_a, bibites_dir_b, output)

def run_metadata_analysis(data_paths: List[Path], output_dir: Optional[Path] = None) -> None:
    """Run ecosystem metadata analysis."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Metadata analysis requires exactly one dataset (use --latest or --name)")
    
    try:
        # Find the original zip file from the data path
        zip_file = get_zip_file_from_data_path(data_paths[0])
        
        temp_dir = output_dir if output_dir else Path('./tmp')
        temp_dir.mkdir(exist_ok=True)
        
        metadata = extract_metadata_from_save(zip_file, temp_dir, extract_raw=False)
        display_metadata_results(metadata)
        
    except (BibitesDataError, MetadataExtractionError) as e:
        raise BibitesAnalysisError(f"Metadata extraction failed: {e}")

def run_field_extraction(data_paths: List[Path], fields: str, batch: bool, 
                        output: Optional[Path], format: str) -> None:
    """Run field extraction analysis."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Field extraction requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    field_paths = [f.strip() for f in fields.split(',')]
    
    if batch:
        # Batch processing
        try:
            results, errors = process_batch_files(bibites_dir, field_paths)
        except ValueError as e:
            raise BibitesAnalysisError(f"Field extraction failed: {e}")
        
        # Display results
        if format == 'table':
            display_table(results, field_paths)
        elif format == 'json':
            display_json(results)
        elif format == 'csv':
            display_csv(results, field_paths)
        
        if errors:
            console.print(f"\n[red]Errors in {len(errors)} files:[/red]")
            for error in errors:
                console.print(f"  {error}")
        
        # Save output if requested
        if output:
            save_json_output(results, output)
    else:
        raise BibitesAnalysisError("Single file field extraction not supported in unified tool. Use --batch for directory processing.")

def run_species_field_extraction(data_paths: List[Path], output: Optional[Path]) -> None:
    """Extract species ID fields for species name mapping."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Species field extraction requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    extract_species_field(bibites_dir, output)

def run_species_comparison(data_paths: List[Path], species_a: int, species_b: int, 
                          output: Optional[Path]) -> None:
    """Compare two specific species by their sim-generated species ID."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Species comparison requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    compare_specific_species(bibites_dir, species_a, species_b, output)