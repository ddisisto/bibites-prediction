#!/usr/bin/env python3
"""
extract_data.py - Extract specific fields from BB8 organism files.

Replaces manual jq commands with clean Python interface. Provides evolutionary tracking
and population analysis features for ecosystem monitoring.

Population tracking (uses genes.tag for quick species identification):
  python -m src.tools.extract_data --population-summary data/cycle_dir/bibites/
  python -m src.tools.extract_data --compare-populations data/cycle_A/bibites/ data/cycle_B/bibites/

Detailed analysis:
  python -m src.tools.extract_data --species-summary data/cycle_20250829205409/bibites/
  python -m src.tools.extract_data --compare-cycles data/cycle_A/bibites/ data/cycle_B/bibites/

Spatial ecosystem analysis:
  python -m src.tools.extract_data --spatial-analysis data/cycle_20250830003320/bibites/

Field extraction:
  python -m src.tools.extract_data --fields genes.genes.ColorR,genes.genes.ColorG data/bibites/bibite_18.bb8
  python -m src.tools.extract_data --fields genes.genes.AverageMutationNumber --batch data/bibites/

Features:
  - Quick population counts by species tag
  - Evolutionary trend analysis between cycles
  - Detailed species statistics (energy, age, colors)
  - Spatial distribution analysis across island zones
  - Flexible field extraction with batch processing
"""

import click
import orjson
from pathlib import Path
from typing import Optional, Tuple
from rich.console import Console

from ..core.parser import BB8ParseError
from .lib.field_extraction import process_single_file, process_batch_files, extract_species_field
from .lib.population_analysis import generate_species_summary
from .lib.spatial_analysis import generate_spatial_analysis
from .lib.comparison_tools import compare_cycle_directories, compare_specific_species
from .lib.output_formatters import display_table, display_json, display_csv, save_json_output

console = Console()

@click.command()
@click.argument('input_path', type=click.Path(path_type=Path), required=False)
@click.argument('cycle_b_path', type=click.Path(path_type=Path), required=False)
@click.option('--fields', '-f', 
              help='Comma-separated list of field paths (e.g., genes.genes.ColorR,genes.genes.ColorG)')
@click.option('--batch', '-b', is_flag=True, 
              help='Process all .bb8 files in directory')
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Output file (JSON format)')
@click.option('--format', type=click.Choice(['json', 'table', 'csv']), 
              default='table', help='Output format')
@click.option('--species-summary', is_flag=True,
              help='Generate species distribution summary for directory')
@click.option('--population-summary', is_flag=True,
              help='Quick species count for evolutionary tracking (alias for --species-summary)')
@click.option('--compare-cycles', is_flag=True,
              help='Compare species distributions between two cycle directories')
@click.option('--compare-populations', is_flag=True,
              help='Compare populations between two cycles (alias for --compare-cycles)')
@click.option('--spatial-analysis', is_flag=True,
              help='Generate spatial distribution analysis across island zones')
@click.option('--by-species', is_flag=True,
              help='Group population summary by sim-generated species ID instead of hereditary tags')
@click.option('--species-field', is_flag=True,
              help='Extract species ID field from organisms for species name mapping')
@click.option('--compare-species', nargs=2, type=int, metavar='SPECIES_A SPECIES_B',
              help='Compare two specific species by their sim-generated species ID')
def extract_data(input_path: Optional[Path], cycle_b_path: Optional[Path], fields: Optional[str], 
                batch: bool, output: Optional[Path], format: str, species_summary: bool, population_summary: bool, compare_cycles: bool, compare_populations: bool, spatial_analysis: bool, by_species: bool, species_field: bool, compare_species: Optional[Tuple[int, int]]):
    """Extract specific fields from BB8 organism files.
    
    Examples:
        # Extract specific fields from single file
        extract-data --fields genes.genes.ColorR,genes.genes.ColorG data/bibites/bibite_18.bb8
        
        # Quick species distribution analysis
        extract-data --species-summary data/cycle_20250829205409/bibites/
        extract-data --population-summary data/cycle_20250829205409/bibites/
        extract-data --population-summary --by-species data/cycle_20250829205409/bibites/
        
        # Extract species ID mapping
        extract-data --species-field data/cycle_20250829205409/bibites/
        
        # Compare two evolutionary cycles
        extract-data --compare-cycles data/cycle_A/bibites/ data/cycle_B/bibites/
        extract-data --compare-populations data/cycle_A/bibites/ data/cycle_B/bibites/
        
        # Compare specific species
        extract-data --compare-species 479 603 data/cycle_20250829205409/bibites/
        
        # Spatial ecosystem analysis across island zones
        extract-data --spatial-analysis data/cycle_20250830003320/bibites/
        
        # Batch extract fields from all files in directory
        extract-data --fields genes.genes.AverageMutationNumber --batch data/bibites/
    """
    
    # Handle different operation modes
    if species_summary or population_summary:
        if not input_path or not Path(input_path).exists():
            flag_name = "--population-summary" if population_summary else "--species-summary"
            console.print(f"[red]Error: input_path required for {flag_name}[/red]")
            return
        # Use quick mode for population-summary (both with and without by-species)
        quick_mode = population_summary
        generate_species_summary(Path(input_path), output, quick_mode=quick_mode, use_species_id=by_species)
        return
    
    if compare_cycles or compare_populations:
        if not input_path or not cycle_b_path or not Path(input_path).exists() or not Path(cycle_b_path).exists():
            flag_name = "--compare-populations" if compare_populations else "--compare-cycles"
            console.print(f"[red]Error: both input_path and cycle_b_path required for {flag_name}[/red]")
            return
        compare_cycle_directories(Path(input_path), Path(cycle_b_path), output)
        return
    
    if spatial_analysis:
        if not input_path or not Path(input_path).exists():
            console.print(f"[red]Error: input_path required for --spatial-analysis[/red]")
            return
        generate_spatial_analysis(Path(input_path), output)
        return
    
    if species_field:
        if not input_path or not Path(input_path).exists():
            console.print(f"[red]Error: input_path required for --species-field[/red]")
            return
        extract_species_field(Path(input_path), output)
        return
    
    if compare_species:
        if not input_path or not Path(input_path).exists():
            console.print(f"[red]Error: input_path required for --compare-species[/red]")
            return
        species_a, species_b = compare_species
        compare_specific_species(Path(input_path), species_a, species_b, output)
        return
    
    # Original field extraction logic
    if not fields:
        console.print("[red]Error: --fields required for field extraction mode[/red]")
        return
    
    if not input_path or not Path(input_path).exists():
        console.print("[red]Error: input_path required[/red]")
        return
    
    input_path = Path(input_path)
    field_paths = [f.strip() for f in fields.split(',')]
    
    if batch or input_path.is_dir():
        # Batch processing
        try:
            results, errors = process_batch_files(input_path, field_paths)
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            return
        
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
        # Single file processing
        try:
            extracted = process_single_file(input_path, field_paths)
            
            if format == 'json':
                console.print(orjson.dumps(extracted, option=orjson.OPT_INDENT_2).decode())
            else:
                # Simple key-value display
                for field_path, value in extracted.items():
                    console.print(f"{field_path}: {value}")
                    
        except BB8ParseError as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == '__main__':
    extract_data()