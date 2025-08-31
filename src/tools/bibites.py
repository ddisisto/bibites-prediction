#!/usr/bin/env python3
"""
bibites.py - Unified Bibites ecosystem analysis tool with zero path exposure.

A single command that orchestrates data access + analysis with transparent JIT 
extraction and caching. Users never see paths, autosave filenames, or internal structure.

DESIGN PHILOSOPHY:
- Data Access Layer: Hardcoded paths, automatic cache management
- Analysis Layer: All extract_*.py functionality in unified interface  
- Zero Path Exposure: User specifies WHAT data (--latest, --last N) not WHERE
- Transparent Operation: Automatic extraction, caching, and path resolution

Usage Examples:
    # Quick ecosystem overview
    python -m src.tools.bibites --latest --population --metadata
    
    # Species evolution comparison
    python -m src.tools.bibites --last 2 --compare --by-species
    
    # Detailed analysis with export
    python -m src.tools.bibites --latest --species --spatial --output analysis.json
    
    # Field extraction examples  
    python -m src.tools.bibites --latest --fields genes.genes.ColorR,genes.genes.ColorG
    python -m src.tools.bibites --name 20250831 --fields genes.genes.AverageMutationNumber --batch
"""

import click
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
from rich.console import Console

# Import data access layer from extract_save.py
from .extract_save import (
    find_latest_autosave, find_last_n_autosaves, find_autosave_by_name,
    get_output_directory, is_directory_cached, extract_save_files,
    SaveExtractionError
)

# Import analysis modules from extract_data.py  
from .lib.field_extraction import process_single_file, process_batch_files, extract_species_field
from .lib.population_analysis import generate_species_summary
from .lib.spatial_analysis import generate_spatial_analysis
from .lib.comparison_tools import compare_cycle_directories, compare_specific_species
from .lib.output_formatters import display_table, display_json, display_csv, save_json_output

# Import metadata extraction from extract_metadata.py
from .extract_metadata import extract_metadata_from_save, display_metadata_results, MetadataExtractionError

# Import core parsing
from ..core.parser import BB8ParseError

console = Console()

class BibitesToolError(Exception):
    """Raised when bibites tool operation fails."""
    pass

def resolve_data_paths(latest: bool, last: Optional[int], name: Optional[str], 
                      overwrite: bool = False) -> List[Path]:
    """
    Resolve user data selection to extracted data paths.
    Transparently handles extraction and caching.
    
    Args:
        latest: Get latest autosave
        last: Get last N autosaves  
        name: Get autosave by name pattern
        overwrite: Force re-extraction even if cached
        
    Returns:
        List of data directory paths ready for analysis
        
    Raises:
        BibitesToolError: If data access fails
    """
    # Validate exactly one data selection option
    options_count = sum([latest, last is not None, name is not None])
    if options_count == 0:
        raise BibitesToolError("Must specify exactly one data selection: --latest, --last N, or --name PATTERN")
    elif options_count > 1:
        raise BibitesToolError("Cannot combine --latest, --last, and --name options")
    
    try:
        # Determine which autosave files to process
        if latest:
            zip_files = [find_latest_autosave()]
        elif last is not None:
            if last <= 0:
                raise BibitesToolError("--last must be a positive number")
            zip_files = find_last_n_autosaves(last)
            console.print(f"[blue]Found last {len(zip_files)} autosaves[/blue]")
        elif name is not None:
            zip_files = [find_autosave_by_name(name)]
        
    except SaveExtractionError as e:
        raise BibitesToolError(f"Data access failed: {e}")
    
    # Extract/cache data transparently
    output_paths = []
    extraction_needed = False
    
    for zip_file in zip_files:
        try:
            # Get output directory for this autosave
            output_dir = get_output_directory(zip_file)
            output_paths.append(output_dir)
            
            # Check cache first (unless overwrite requested)
            if not overwrite and is_directory_cached(output_dir):
                console.print(f"[cyan]Using cached data: {zip_file.name}[/cyan]")
                continue
            else:
                console.print(f"[green]Extracting: {zip_file.name}[/green]")
                stats = extract_save_files(zip_file, output_dir)
                extraction_needed = True
                
                if stats['errors']:
                    console.print(f"[yellow]Extraction completed with {len(stats['errors'])} errors[/yellow]")
                    
        except SaveExtractionError as e:
            raise BibitesToolError(f"Failed to extract {zip_file.name}: {e}")
    
    if extraction_needed:
        console.print("[green]Data extraction complete[/green]")
    
    return output_paths

def run_population_analysis(data_paths: List[Path], output: Optional[Path], 
                           by_species: bool, quick_mode: bool = True) -> None:
    """Run population/species summary analysis."""
    if len(data_paths) != 1:
        raise BibitesToolError("Population analysis requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesToolError(f"Bibites directory not found: {bibites_dir}")
    
    generate_species_summary(bibites_dir, output, quick_mode=quick_mode, use_species_id=by_species)

def run_spatial_analysis(data_paths: List[Path], output: Optional[Path]) -> None:
    """Run spatial distribution analysis."""
    if len(data_paths) != 1:
        raise BibitesToolError("Spatial analysis requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesToolError(f"Bibites directory not found: {bibites_dir}")
    
    generate_spatial_analysis(bibites_dir, output)

def run_comparison_analysis(data_paths: List[Path], output: Optional[Path]) -> None:
    """Run population comparison between cycles."""
    if len(data_paths) != 2:
        raise BibitesToolError("Comparison analysis requires exactly two datasets (use --last 2)")
    
    # Order matters: newer first, older second for proper comparison direction
    bibites_dir_a = data_paths[0] / 'bibites'  # More recent
    bibites_dir_b = data_paths[1] / 'bibites'  # Older
    
    if not bibites_dir_a.exists():
        raise BibitesToolError(f"First dataset bibites directory not found: {bibites_dir_a}")
    if not bibites_dir_b.exists():
        raise BibitesToolError(f"Second dataset bibites directory not found: {bibites_dir_b}")
    
    compare_cycle_directories(bibites_dir_a, bibites_dir_b, output)

def run_metadata_analysis(data_paths: List[Path], output_dir: Optional[Path] = None) -> None:
    """Run ecosystem metadata analysis."""
    if len(data_paths) != 1:
        raise BibitesToolError("Metadata analysis requires exactly one dataset (use --latest or --name)")
    
    # Find the original zip file from the data path
    # data_paths[0] should be like data/autosave_20250831115522/
    data_path = data_paths[0]
    autosave_name = data_path.name
    
    # Reconstruct zip path - this is a bit hacky but works with current structure
    from .extract_save import get_all_autosaves
    try:
        all_saves = get_all_autosaves()
        zip_file = None
        for save in all_saves:
            if save.stem == autosave_name:
                zip_file = save
                break
        
        if zip_file is None:
            raise BibitesToolError(f"Could not find source zip for dataset: {autosave_name}")
        
        temp_dir = output_dir if output_dir else Path('./tmp')
        temp_dir.mkdir(exist_ok=True)
        
        metadata = extract_metadata_from_save(zip_file, temp_dir, extract_raw=False)
        display_metadata_results(metadata)
        
    except (SaveExtractionError, MetadataExtractionError) as e:
        raise BibitesToolError(f"Metadata extraction failed: {e}")

def run_field_extraction(data_paths: List[Path], fields: str, batch: bool, 
                        output: Optional[Path], format: str) -> None:
    """Run field extraction analysis."""
    if len(data_paths) != 1:
        raise BibitesToolError("Field extraction requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesToolError(f"Bibites directory not found: {bibites_dir}")
    
    field_paths = [f.strip() for f in fields.split(',')]
    
    if batch:
        # Batch processing
        try:
            results, errors = process_batch_files(bibites_dir, field_paths)
        except ValueError as e:
            raise BibitesToolError(f"Field extraction failed: {e}")
        
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
        raise BibitesToolError("Single file field extraction not supported in unified tool. Use --batch for directory processing.")

def run_species_field_extraction(data_paths: List[Path], output: Optional[Path]) -> None:
    """Extract species ID fields for species name mapping."""
    if len(data_paths) != 1:
        raise BibitesToolError("Species field extraction requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesToolError(f"Bibites directory not found: {bibites_dir}")
    
    extract_species_field(bibites_dir, output)

def run_species_comparison(data_paths: List[Path], species_a: int, species_b: int, 
                          output: Optional[Path]) -> None:
    """Compare two specific species by their sim-generated species ID."""
    if len(data_paths) != 1:
        raise BibitesToolError("Species comparison requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesToolError(f"Bibites directory not found: {bibites_dir}")
    
    compare_specific_species(bibites_dir, species_a, species_b, output)

@click.command()
# Data Selection Options (exactly one required)
@click.option('--latest', is_flag=True,
              help='Use the latest autosave')
@click.option('--last', type=int, metavar='N',
              help='Use the last N autosaves')
@click.option('--name', type=str, metavar='PATTERN',
              help='Use autosave by name or partial name match')

# Analysis Options (choose one or more)
@click.option('--population-summary', '--population', is_flag=True,
              help='Generate population summary (quick species counts)')
@click.option('--species-summary', '--species', is_flag=True,
              help='Generate detailed species analysis')
@click.option('--spatial-analysis', '--spatial', is_flag=True,
              help='Generate spatial distribution analysis across zones')
@click.option('--compare-populations', '--compare', is_flag=True,
              help='Compare populations between cycles (requires --last 2)')
@click.option('--metadata', '--config', is_flag=True,
              help='Extract ecosystem metadata and zone configuration')

# Species Analysis Options
@click.option('--by-species', is_flag=True,
              help='Group analysis by sim-generated species ID instead of hereditary tags')
@click.option('--species-field', is_flag=True,
              help='Extract species ID field for species name mapping')
@click.option('--compare-species', nargs=2, type=int, metavar='SPECIES_A SPECIES_B',
              help='Compare two specific species by their sim-generated species ID')

# Field Extraction Options
@click.option('--fields', '-f', 
              help='Extract specific fields (comma-separated, e.g. genes.genes.ColorR,genes.genes.ColorG)')
@click.option('--batch', '-b', is_flag=True, 
              help='Process all files when extracting fields (default for unified tool)')

# Output Options
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Output file (JSON format)')
@click.option('--format', type=click.Choice(['json', 'table', 'csv']), 
              default='table', help='Output format')
@click.option('--overwrite', is_flag=True,
              help='Force re-extraction even if data is cached')

def bibites(latest: bool, last: Optional[int], name: Optional[str],
           population_summary: bool, species_summary: bool, spatial_analysis: bool,
           compare_populations: bool, metadata: bool,
           by_species: bool, species_field: bool, compare_species: Optional[Tuple[int, int]],
           fields: Optional[str], batch: bool,
           output: Optional[Path], format: str, overwrite: bool):
    """Unified Bibites ecosystem analysis tool with zero path exposure.
    
    A single command for all data access and analysis operations. Automatically handles
    autosave discovery, extraction, caching, and analysis with no path management required.
    
    DATA SELECTION (exactly one required):
        --latest                Use latest autosave
        --last N                Use last N autosaves 
        --name PATTERN          Use autosave matching name pattern
    
    ANALYSIS OPTIONS (choose one or more):
        --population            Quick species population counts
        --species               Detailed species statistics 
        --spatial               Spatial distribution analysis
        --compare               Compare populations between cycles
        --metadata              Extract ecosystem configuration
        
    SPECIES ANALYSIS:
        --by-species            Use sim-generated species IDs instead of tags
        --species-field         Extract species ID mapping
        --compare-species A B   Compare specific species by ID
        
    FIELD EXTRACTION:
        --fields FIELD_LIST     Extract specific organism fields
        --batch                 Process all files (automatic in unified tool)
    
    OUTPUT OPTIONS:
        --format [table|json|csv]  Output format
        --output FILE             Save JSON results to file
        --overwrite               Force re-extraction
    
    EXAMPLES:
        # Quick ecosystem overview
        bibites --latest --population --metadata
        
        # Species evolution tracking  
        bibites --last 2 --compare --by-species
        
        # Detailed spatial analysis with export
        bibites --latest --species --spatial --output analysis.json
        
        # Field extraction across population
        bibites --latest --fields genes.genes.ColorR,neural.NeuronCount --batch
        
        # Compare specific species by sim ID
        bibites --latest --compare-species 479 603
    """
    
    try:
        # Resolve data paths transparently
        console.print("[blue]Resolving data access...[/blue]")
        data_paths = resolve_data_paths(latest, last, name, overwrite)
        
        # Track which analyses were requested
        analysis_count = sum([
            population_summary, species_summary, spatial_analysis, 
            compare_populations, metadata, species_field,
            compare_species is not None, fields is not None
        ])
        
        if analysis_count == 0:
            console.print("[yellow]No analysis requested. Use --help to see available options.[/yellow]")
            console.print("[blue]Available data paths:[/blue]")
            for path in data_paths:
                console.print(f"  {path.resolve()}")
            return
        
        console.print(f"[green]Running {analysis_count} analysis operation(s)...[/green]\n")
        
        # Run requested analyses
        if population_summary:
            console.print("[bold cyan]Population Summary Analysis[/bold cyan]")
            run_population_analysis(data_paths, output, by_species, quick_mode=True)
            console.print()
        
        if species_summary:
            console.print("[bold cyan]Species Summary Analysis[/bold cyan]")
            run_population_analysis(data_paths, output, by_species, quick_mode=False)
            console.print()
        
        if spatial_analysis:
            console.print("[bold cyan]Spatial Distribution Analysis[/bold cyan]")
            run_spatial_analysis(data_paths, output)
            console.print()
        
        if compare_populations:
            console.print("[bold cyan]Population Comparison Analysis[/bold cyan]")
            run_comparison_analysis(data_paths, output)
            console.print()
        
        if metadata:
            console.print("[bold cyan]Ecosystem Metadata Analysis[/bold cyan]")
            run_metadata_analysis(data_paths, output.parent if output else None)
            console.print()
        
        if species_field:
            console.print("[bold cyan]Species Field Extraction[/bold cyan]")
            run_species_field_extraction(data_paths, output)
            console.print()
        
        if compare_species:
            console.print("[bold cyan]Species Comparison Analysis[/bold cyan]")
            species_a, species_b = compare_species
            run_species_comparison(data_paths, species_a, species_b, output)
            console.print()
        
        if fields:
            console.print("[bold cyan]Field Extraction Analysis[/bold cyan]")
            run_field_extraction(data_paths, fields, batch=True, output=output, format=format)
            console.print()
        
        console.print("[bold green]Analysis complete![/bold green]")
        
    except BibitesToolError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
    except (BB8ParseError, SaveExtractionError, MetadataExtractionError) as e:
        console.print(f"[red]Analysis failed: {e}[/red]")
        raise click.Abort()

if __name__ == '__main__':
    bibites()