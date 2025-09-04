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
from typing import Optional, Tuple
from rich.console import Console

# Import modular components
from .lib.bibites_data import resolve_data_paths, display_save_listing, BibitesDataError
from .lib.bibites_analysis import (
    run_population_analysis, run_spatial_analysis, run_comparison_analysis,
    run_metadata_analysis, run_field_extraction, run_species_field_extraction,
    run_species_comparison, BibitesAnalysisError
)
from .lib.bibites_crosspolinate import run_inject_fittest, BibitesCrossPollinateError

# Import core parsing for error handling
from ..core.parser import BB8ParseError
from .extract_save import SaveExtractionError
from .extract_metadata import MetadataExtractionError

console = Console()

class BibitesToolError(Exception):
    """Raised when bibites tool operation fails."""
    pass


@click.command()
# Data Selection Options
@click.option('--latest', is_flag=True,
              help='Use the latest autosave')
@click.option('--last', type=int, metavar='N',
              help='Use the last N autosaves')
@click.option('--name', type=str, metavar='PATTERN',
              help='Use save by name or partial name match (searches both autosaves and manual saves)')
@click.option('--list', '-l', is_flag=True,
              help='List all available saves with metadata (default if no other options)')

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

# Cross-Pollination Options
@click.option('--inject-fittest', is_flag=True,
              help='Inject fittest bibites from source save into target save')
@click.option('--source', type=str, metavar='SAVE_NAME',
              help='Source save name pattern for cross-pollination')
@click.option('--target', type=str, metavar='SAVE_NAME', 
              help='Target save name pattern for cross-pollination')
@click.option('--count', type=int, default=3,
              help='Number of fittest bibites to inject (default: 3)')

# Output Options
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Output file (JSON format) or custom save name for cross-pollination')
@click.option('--format', type=click.Choice(['json', 'table', 'csv']), 
              default='table', help='Output format')
@click.option('--overwrite', is_flag=True,
              help='Force re-extraction even if data is cached')

def bibites(latest: bool, last: Optional[int], name: Optional[str], list: bool,
           population_summary: bool, species_summary: bool, spatial_analysis: bool,
           compare_populations: bool, metadata: bool,
           by_species: bool, species_field: bool, compare_species: Optional[Tuple[int, int]],
           fields: Optional[str], batch: bool,
           inject_fittest: bool, source: Optional[str], target: Optional[str], count: int,
           output: Optional[Path], format: str, overwrite: bool):
    """Unified Bibites ecosystem analysis tool with zero path exposure.
    
    A single command for all data access and analysis operations. Automatically handles
    save discovery (autosaves and manual saves), extraction, caching, and analysis.
    
    DATA SELECTION:
        --latest                Use latest autosave
        --last N                Use last N autosaves 
        --name PATTERN          Use save matching pattern (autosaves and manual saves)
        --list                  List available saves (default if no options given)
    
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
    
    CROSS-POLLINATION:
        --inject-fittest        Inject fittest bibites from source into target save
        --source SAVE_NAME      Source save name pattern
        --target SAVE_NAME      Target save name pattern  
        --count N               Number of fittest bibites to inject (default: 3)
    
    OUTPUT OPTIONS:
        --format [table|json|csv]  Output format
        --output FILE/NAME        Save JSON results to file or custom save name
        --overwrite               Force re-extraction
    
    EXAMPLES:
        # List all available saves (default behavior)
        bibites
        bibites --list
        
        # Quick ecosystem overview
        bibites --latest --population --metadata
        
        # Work with manual saves
        bibites --name "pred train br" --population --metadata
        
        # Species evolution tracking  
        bibites --last 2 --compare --by-species
        
        # Detailed spatial analysis with export
        bibites --latest --species --spatial --output analysis.json
        
        # Field extraction across population
        bibites --latest --fields genes.genes.ColorR,neural.NeuronCount --batch
        
        # Compare specific species by sim ID
        bibites --latest --compare-species 479 603
        
        # Cross-pollination examples
        bibites --inject-fittest --source "pred train br" --target "pred train br - pre-herbivore staging"
        bibites --inject-fittest --source "pred train br" --target "pred train br - pre-herbivore staging" --count 5 --output "pred train br - staged"
    """
    
    try:
        # Handle cross-pollination mode
        if inject_fittest:
            if not source or not target:
                console.print("[red]Error: --inject-fittest requires both --source and --target options[/red]")
                raise click.Abort()
            
            if count <= 0:
                console.print("[red]Error: --count must be a positive number[/red]")
                raise click.Abort()
            
            console.print(f"[bold cyan]Cross-Pollination Mode[/bold cyan]")
            console.print(f"[blue]Injecting top {count} fittest bibites from '{source}' into '{target}'[/blue]\n")
            
            # Convert output Path to string if provided
            output_name = str(output.stem) if output else None
            
            run_inject_fittest(source, target, count, output_name)
            return
        
        # Check if user wants listing (explicit --list or no data selection options)
        data_selection_count = sum([latest, last is not None, name is not None])
        
        if list or data_selection_count == 0:
            display_save_listing()
            return
        
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
        
    except (BibitesDataError, BibitesAnalysisError, BibitesCrossPollinateError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
    except (BB8ParseError, SaveExtractionError, MetadataExtractionError) as e:
        console.print(f"[red]Analysis failed: {e}[/red]")
        raise click.Abort()

if __name__ == '__main__':
    bibites()