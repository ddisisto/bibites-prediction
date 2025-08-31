"""
Comparison utilities for extract_data.py

Provides cycle-to-cycle species comparison, species-specific analysis,
and population change tracking for evolutionary monitoring.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from rich.console import Console
from rich.table import Table

from .population_analysis import get_cycle_species_data
from ...core.parser import load_bb8_file, extract_multiple_fields, BB8ParseError

console = Console()


def compare_cycle_directories(cycle_a_path: Path, cycle_b_path: Path, output: Optional[Path]):
    """Compare species distributions between two cycle directories."""
    
    console.print(f"[blue]Comparing cycles:[/blue]")
    console.print(f"  Cycle A: {cycle_a_path}")
    console.print(f"  Cycle B: {cycle_b_path}")
    
    # Get species data for both cycles
    species_a = get_cycle_species_data(cycle_a_path, "A")
    species_b = get_cycle_species_data(cycle_b_path, "B")
    
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
        import orjson
        with open(output, 'wb') as f:
            f.write(orjson.dumps(comparison, option=orjson.OPT_INDENT_2))
        console.print(f"\n[green]Comparison saved to {output}[/green]")


def compare_specific_species(directory_path: Path, species_a: int, species_b: int, output: Optional[Path]):
    """Compare two specific species by their sim-generated species ID.
    
    This function provides detailed comparison between two species within
    the same ecosystem, analyzing their characteristics and distributions.
    """
    if directory_path.is_file():
        directory_path = directory_path.parent
    
    bb8_files = list(directory_path.glob('*.bb8'))
    if not bb8_files:
        console.print(f"[red]No .bb8 files found in {directory_path}[/red]")
        return
    
    console.print(f"[blue]Comparing species {species_a} vs {species_b} from {len(bb8_files)} organisms...[/blue]")
    
    # Fields for detailed species comparison
    comparison_fields = [
        'genes.genes.SpeciesID', 'genes.speciesID', 'genes.tag',
        'energy', 'age', 'rb2d.px', 'rb2d.py',
        'genes.genes.ColorR', 'genes.genes.ColorG', 'genes.genes.ColorB',
        'genes.genes.AverageMutationNumber'
    ]
    
    species_a_data = []
    species_b_data = []
    errors = []
    
    from rich.progress import track
    for file_path in track(bb8_files, description="Analyzing species"):
        try:
            data = load_bb8_file(file_path)
            extracted = extract_multiple_fields(data, comparison_fields)
            
            # Check if this organism matches either target species
            species_id_1 = extracted.get('genes.genes.SpeciesID')
            species_id_2 = extracted.get('genes.speciesID')
            
            # Match either species ID field
            if species_id_1 == species_a or species_id_2 == species_a:
                extracted['_file'] = file_path.name
                species_a_data.append(extracted)
            elif species_id_1 == species_b or species_id_2 == species_b:
                extracted['_file'] = file_path.name
                species_b_data.append(extracted)
                
        except BB8ParseError as e:
            errors.append(f"{file_path.name}: {e}")
    
    # Generate comparison summary
    comparison_result = {
        'species_a': {
            'id': species_a,
            'count': len(species_a_data),
            'organisms': species_a_data
        },
        'species_b': {
            'id': species_b,
            'count': len(species_b_data),
            'organisms': species_b_data
        },
        'total_searched': len(bb8_files),
        'errors': len(errors)
    }
    
    # Display results
    console.print(f"\n[bold]Species Comparison Results:[/bold]")
    console.print(f"  Species {species_a}: {len(species_a_data)} organisms found")
    console.print(f"  Species {species_b}: {len(species_b_data)} organisms found")
    console.print(f"  Total organisms searched: {len(bb8_files)}")
    
    if len(species_a_data) == 0 and len(species_b_data) == 0:
        console.print(f"[yellow]Warning: No organisms found for either species {species_a} or {species_b}[/yellow]")
        return
    
    # Calculate and display basic statistics for each species
    if species_a_data:
        console.print(f"\n[bold]Species {species_a} Statistics:[/bold]")
        _display_species_stats(species_a_data, species_a)
    
    if species_b_data:
        console.print(f"\n[bold]Species {species_b} Statistics:[/bold]")
        _display_species_stats(species_b_data, species_b)
    
    if errors:
        console.print(f"\n[red]Errors in {len(errors)} files[/red]")
    
    # Save detailed results if requested
    if output:
        import orjson
        with open(output, 'wb') as f:
            f.write(orjson.dumps(comparison_result, option=orjson.OPT_INDENT_2))
        console.print(f"\n[green]Species comparison saved to {output}[/green]")


def _display_species_stats(species_data: list, species_id: int):
    """Display basic statistics for a species dataset."""
    import statistics
    
    if not species_data:
        return
    
    # Extract numeric fields for statistics
    energies = [org.get('energy') for org in species_data if isinstance(org.get('energy'), (int, float))]
    ages = [org.get('age') for org in species_data if isinstance(org.get('age'), (int, float))]
    x_positions = [org.get('rb2d.px') for org in species_data if isinstance(org.get('rb2d.px'), (int, float))]
    y_positions = [org.get('rb2d.py') for org in species_data if isinstance(org.get('rb2d.py'), (int, float))]
    
    console.print(f"  Count: {len(species_data)}")
    
    if energies:
        console.print(f"  Energy: Mean={statistics.mean(energies):.1f}, Range=[{min(energies):.1f}, {max(energies):.1f}]")
    
    if ages:
        console.print(f"  Age: Mean={statistics.mean(ages):.1f}, Range=[{min(ages):.1f}, {max(ages):.1f}]")
    
    if x_positions and y_positions:
        console.print(f"  Position: Center=({statistics.mean(x_positions):.0f}, {statistics.mean(y_positions):.0f})")
    
    # Show dominant hereditary tag
    tags = [org.get('genes.tag') for org in species_data if org.get('genes.tag')]
    if tags:
        from collections import Counter
        tag_counts = Counter(tags)
        dominant_tag = tag_counts.most_common(1)[0]
        console.print(f"  Dominant Tag: {dominant_tag[0]} ({dominant_tag[1]} organisms)")