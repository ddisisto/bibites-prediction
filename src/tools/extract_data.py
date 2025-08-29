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

Field extraction:
  python -m src.tools.extract_data --fields genes.genes.ColorR,genes.genes.ColorG data/bibites/bibite_18.bb8
  python -m src.tools.extract_data --fields genes.genes.AverageMutationNumber --batch data/bibites/

Features:
  - Quick population counts by species tag
  - Evolutionary trend analysis between cycles
  - Detailed species statistics (energy, age, colors)
  - Flexible field extraction with batch processing
"""

import click
import orjson
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console
from rich.progress import track
from rich.table import Table
from collections import Counter, defaultdict
import statistics

from ..core.parser import load_bb8_file, extract_multiple_fields, BB8ParseError

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
def extract_data(input_path: Optional[Path], cycle_b_path: Optional[Path], fields: Optional[str], 
                batch: bool, output: Optional[Path], format: str, species_summary: bool, population_summary: bool, compare_cycles: bool, compare_populations: bool):
    """Extract specific fields from BB8 organism files.
    
    Examples:
        # Extract specific fields from single file
        extract-data --fields genes.genes.ColorR,genes.genes.ColorG data/bibites/bibite_18.bb8
        
        # Quick species distribution analysis
        extract-data --species-summary data/cycle_20250829205409/bibites/
        extract-data --population-summary data/cycle_20250829205409/bibites/
        
        # Compare two evolutionary cycles
        extract-data --compare-cycles data/cycle_A/bibites/ data/cycle_B/bibites/
        extract-data --compare-populations data/cycle_A/bibites/ data/cycle_B/bibites/
        
        # Batch extract fields from all files in directory
        extract-data --fields genes.genes.AverageMutationNumber --batch data/bibites/
    """
    
    # Handle different operation modes
    if species_summary or population_summary:
        if not input_path or not Path(input_path).exists():
            flag_name = "--population-summary" if population_summary else "--species-summary"
            console.print(f"[red]Error: input_path required for {flag_name}[/red]")
            return
        # Use quick mode for population-summary
        quick_mode = population_summary
        _generate_species_summary(Path(input_path), output, quick_mode=quick_mode)
        return
    
    if compare_cycles or compare_populations:
        if not input_path or not cycle_b_path or not Path(input_path).exists() or not Path(cycle_b_path).exists():
            flag_name = "--compare-populations" if compare_populations else "--compare-cycles"
            console.print(f"[red]Error: both input_path and cycle_b_path required for {flag_name}[/red]")
            return
        _compare_cycle_directories(Path(input_path), Path(cycle_b_path), output)
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

def _generate_species_summary(input_path: Path, output: Optional[Path], quick_mode: bool = False):
    """Generate a species distribution summary for a directory of bibites."""
    
    if input_path.is_file():
        input_path = input_path.parent
    
    bb8_files = list(input_path.glob('*.bb8'))
    if not bb8_files:
        console.print(f"[red]No .bb8 files found in {input_path}[/red]")
        return
    
    # Quick mode for population tracking
    if quick_mode:
        _generate_quick_population_summary(bb8_files, output)
        return
        
    console.print(f"[blue]Analyzing {len(bb8_files)} organisms for species distribution...[/blue]")
    
    species_data = defaultdict(list)
    energy_data = []
    age_data = []
    errors = []
    
    # Key fields for species analysis
    species_fields = ['genes.tag', 'genes.genes.SpeciesID', 'energy', 'age', 'genes.genes.ColorR', 'genes.genes.ColorG', 'genes.genes.ColorB']
    
    for file_path in track(bb8_files, description="Analyzing organisms"):
        try:
            data = load_bb8_file(file_path)
            extracted = extract_multiple_fields(data, species_fields)
            
            # Prefer genes.tag, fall back to SpeciesID
            species_id = extracted.get('genes.tag') or extracted.get('genes.genes.SpeciesID', 'Unknown')
            energy = extracted.get('energy', 0)
            age = extracted.get('age', 0)
            color_r = extracted.get('genes.genes.ColorR', 0)
            color_g = extracted.get('genes.genes.ColorG', 0)
            color_b = extracted.get('genes.genes.ColorB', 0)
            
            species_data[species_id].append({
                'file': file_path.name,
                'energy': energy,
                'age': age,
                'color': (color_r, color_g, color_b)
            })
            
            if isinstance(energy, (int, float)):
                energy_data.append(energy)
            if isinstance(age, (int, float)):
                age_data.append(age)
                
        except BB8ParseError as e:
            errors.append(f"{file_path.name}: {e}")
    
    # Generate summary
    summary = {
        'total_organisms': len(bb8_files),
        'species_count': len(species_data),
        'species_distribution': {},
        'energy_stats': _calculate_stats(energy_data) if energy_data else None,
        'age_stats': _calculate_stats(age_data) if age_data else None,
        'errors': len(errors)
    }
    
    # Species distribution details
    for species_id, organisms in species_data.items():
        species_energies = [org['energy'] for org in organisms if isinstance(org['energy'], (int, float))]
        species_ages = [org['age'] for org in organisms if isinstance(org['age'], (int, float))]
        
        summary['species_distribution'][species_id] = {
            'count': len(organisms),
            'percentage': (len(organisms) / len(bb8_files)) * 100,
            'avg_energy': statistics.mean(species_energies) if species_energies else 0,
            'avg_age': statistics.mean(species_ages) if species_ages else 0,
            'dominant_color': _get_dominant_color([org['color'] for org in organisms])
        }
    
    # Display results
    console.print("\n[bold]Species Distribution Summary[/bold]")
    table = Table()
    table.add_column("Species ID", style="cyan")
    table.add_column("Count", style="green")
    table.add_column("Percentage", style="yellow")
    table.add_column("Avg Energy", style="blue")
    table.add_column("Avg Age", style="magenta")
    table.add_column("Color (R,G,B)", style="white")
    
    for species_id, stats in sorted(summary['species_distribution'].items(), 
                                  key=lambda x: x[1]['count'], reverse=True):
        color_str = f"({stats['dominant_color'][0]:.2f},{stats['dominant_color'][1]:.2f},{stats['dominant_color'][2]:.2f})"
        table.add_row(
            str(species_id),
            str(stats['count']),
            f"{stats['percentage']:.1f}%",
            f"{stats['avg_energy']:.1f}",
            f"{stats['avg_age']:.1f}",
            color_str
        )
    
    console.print(table)
    
    # Overall ecosystem stats
    if summary['energy_stats']:
        console.print(f"\n[bold]Ecosystem Energy:[/bold] Mean={summary['energy_stats']['mean']:.1f}, " +
                     f"Std={summary['energy_stats']['std']:.1f}, Range=[{summary['energy_stats']['min']:.1f}, {summary['energy_stats']['max']:.1f}]")
    
    if summary['age_stats']:
        console.print(f"[bold]Ecosystem Age:[/bold] Mean={summary['age_stats']['mean']:.1f}, " +
                     f"Std={summary['age_stats']['std']:.1f}, Range=[{summary['age_stats']['min']:.1f}, {summary['age_stats']['max']:.1f}]")
    
    if errors:
        console.print(f"\n[red]Errors in {len(errors)} files[/red]")
    
    # Save output if requested
    if output:
        with open(output, 'wb') as f:
            f.write(orjson.dumps(summary, option=orjson.OPT_INDENT_2))
        console.print(f"\n[green]Summary saved to {output}[/green]")

def _compare_cycle_directories(cycle_a_path: Path, cycle_b_path: Path, output: Optional[Path]):
    """Compare species distributions between two cycle directories."""
    
    console.print(f"[blue]Comparing cycles:[/blue]")
    console.print(f"  Cycle A: {cycle_a_path}")
    console.print(f"  Cycle B: {cycle_b_path}")
    
    # Get species data for both cycles
    species_a = _get_cycle_species_data(cycle_a_path, "A")
    species_b = _get_cycle_species_data(cycle_b_path, "B")
    
    if not species_a or not species_b:
        console.print("[red]Error: Could not load species data from one or both cycles[/red]")
        return
    
    # Compare species distributions
    all_species = set(species_a.keys()) | set(species_b.keys())
    
    comparison = {
        'cycle_a_total': sum(species_a.values()),
        'cycle_b_total': sum(species_b.values()),
        'species_changes': {},
        'new_species': [],
        'extinct_species': []
    }
    
    console.print("\n[bold]Species Population Changes[/bold]")
    table = Table()
    table.add_column("Species ID", style="cyan")
    table.add_column("Cycle A Count", style="green")
    table.add_column("Cycle B Count", style="blue")
    table.add_column("Change", style="yellow")
    table.add_column("% Change", style="magenta")
    table.add_column("Status", style="white")
    
    for species_id in sorted(all_species):
        count_a = species_a.get(species_id, 0)
        count_b = species_b.get(species_id, 0)
        change = count_b - count_a
        
        if count_a == 0 and count_b > 0:
            status = "NEW"
            percent_change = float('inf')
            percent_str = "∞"
            comparison['new_species'].append(species_id)
        elif count_a > 0 and count_b == 0:
            status = "EXTINCT"
            percent_change = -100.0
            percent_str = "-100%"
            comparison['extinct_species'].append(species_id)
        elif count_a > 0:
            percent_change = (change / count_a) * 100
            percent_str = f"{percent_change:+.1f}%"
            if percent_change > 20:
                status = "GROWING"
            elif percent_change < -20:
                status = "DECLINING"
            else:
                status = "STABLE"
        else:
            percent_change = 0.0
            percent_str = "0%"
            status = "STABLE"
        
        comparison['species_changes'][species_id] = {
            'cycle_a': count_a,
            'cycle_b': count_b,
            'change': change,
            'percent_change': percent_change,
            'status': status
        }
        
        # Color code the change
        change_style = "green" if change > 0 else "red" if change < 0 else "white"
        table.add_row(
            str(species_id),
            str(count_a),
            str(count_b),
            f"[{change_style}]{change:+d}[/{change_style}]",
            percent_str,
            status
        )
    
    console.print(table)
    
    # Summary statistics
    total_change = comparison['cycle_b_total'] - comparison['cycle_a_total']
    console.print(f"\n[bold]Population Summary:[/bold]")
    console.print(f"  Cycle A Total: {comparison['cycle_a_total']}")
    console.print(f"  Cycle B Total: {comparison['cycle_b_total']}")
    console.print(f"  Net Change: {total_change:+d}")
    console.print(f"  New Species: {len(comparison['new_species'])}")
    console.print(f"  Extinct Species: {len(comparison['extinct_species'])}")
    
    # Save output if requested
    if output:
        with open(output, 'wb') as f:
            f.write(orjson.dumps(comparison, option=orjson.OPT_INDENT_2))
        console.print(f"\n[green]Comparison saved to {output}[/green]")

def _get_cycle_species_data(cycle_path: Path, cycle_name: str) -> Dict[str, int]:
    """Extract species distribution from a cycle directory."""
    
    if cycle_path.is_file():
        cycle_path = cycle_path.parent
    
    bb8_files = list(cycle_path.glob('*.bb8'))
    if not bb8_files:
        console.print(f"[red]No .bb8 files found in {cycle_path} for cycle {cycle_name}[/red]")
        return {}
    
    species_counter = Counter()
    errors = 0
    
    for file_path in track(bb8_files, description=f"Loading cycle {cycle_name}"):
        try:
            data = load_bb8_file(file_path)
            # Try genes.tag first (for quick identification), then fall back to genes.genes.SpeciesID
            tag_extracted = extract_multiple_fields(data, ['genes.tag'])
            species_tag = tag_extracted.get('genes.tag')
            
            if species_tag:
                species_counter[species_tag] += 1
            else:
                # Fallback to SpeciesID if tag not available
                extracted = extract_multiple_fields(data, ['genes.genes.SpeciesID'])
                species_id = extracted.get('genes.genes.SpeciesID', 'Unknown')
                species_counter[species_id] += 1
                
        except BB8ParseError:
            errors += 1
    
    if errors > 0:
        console.print(f"[yellow]Warning: {errors} files failed to load in cycle {cycle_name}[/yellow]")
    
    return dict(species_counter)

def _calculate_stats(values: List[float]) -> Dict[str, float]:
    """Calculate basic statistics for a list of values."""
    if not values:
        return {}
    
    return {
        'mean': statistics.mean(values),
        'std': statistics.stdev(values) if len(values) > 1 else 0.0,
        'min': min(values),
        'max': max(values),
        'count': len(values)
    }

def _generate_quick_population_summary(bb8_files: List[Path], output: Optional[Path]):
    """Generate a quick population count table using genes.tag for species identification."""
    
    console.print(f"[blue]Counting {len(bb8_files)} organisms by species tag...[/blue]")
    
    species_counter = Counter()
    errors = 0
    
    for file_path in track(bb8_files, description="Counting species"):
        try:
            data = load_bb8_file(file_path)
            # Try genes.tag first (preferred for quick identification)
            tag_extracted = extract_multiple_fields(data, ['genes.tag'])
            species_tag = tag_extracted.get('genes.tag')
            
            if species_tag:
                species_counter[species_tag] += 1
            else:
                # Fallback to SpeciesID if tag not available  
                extracted = extract_multiple_fields(data, ['genes.genes.SpeciesID'])
                species_id = extracted.get('genes.genes.SpeciesID', 'Unknown')
                species_counter[species_id] += 1
                
        except BB8ParseError:
            errors += 1
    
    # Display quick table
    console.print("\n[bold]Population Summary[/bold]")
    table = Table()
    table.add_column("Species Tag", style="cyan")
    table.add_column("Count", style="green")
    table.add_column("Percentage", style="yellow")
    
    total_organisms = sum(species_counter.values())
    
    for species_tag, count in sorted(species_counter.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_organisms) * 100 if total_organisms > 0 else 0
        table.add_row(
            str(species_tag),
            str(count), 
            f"{percentage:.1f}%"
        )
    
    console.print(table)
    console.print(f"\n[bold]Total:[/bold] {total_organisms} organisms")
    
    if errors > 0:
        console.print(f"[red]Errors: {errors} files failed to load[/red]")
    
    # Save output if requested
    if output:
        summary_data = {
            'total_organisms': total_organisms,
            'species_counts': dict(species_counter),
            'errors': errors
        }
        with open(output, 'wb') as f:
            f.write(orjson.dumps(summary_data, option=orjson.OPT_INDENT_2))
        console.print(f"\n[green]Summary saved to {output}[/green]")

def _get_dominant_color(colors: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """Calculate the average dominant color from a list of RGB tuples."""
    if not colors:
        return (0.0, 0.0, 0.0)
    
    r_avg = statistics.mean([c[0] for c in colors if isinstance(c[0], (int, float))])
    g_avg = statistics.mean([c[1] for c in colors if isinstance(c[1], (int, float))])
    b_avg = statistics.mean([c[2] for c in colors if isinstance(c[2], (int, float))])
    
    return (r_avg, g_avg, b_avg)

if __name__ == '__main__':
    extract_data()