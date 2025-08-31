"""
Population analysis utilities for extract_data.py

Provides species distribution analysis, population summaries, and statistical
calculations for ecosystem monitoring and evolutionary tracking.
"""

import statistics
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from collections import Counter, defaultdict
from rich.console import Console
from rich.progress import track
from rich.table import Table

from ...core.parser import load_bb8_file, extract_multiple_fields, BB8ParseError

console = Console()


def calculate_stats(values: List[float]) -> Dict[str, float]:
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


def get_dominant_color(colors: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """Calculate the average dominant color from a list of RGB tuples."""
    if not colors:
        return (0.0, 0.0, 0.0)
    
    r_avg = statistics.mean([c[0] for c in colors if isinstance(c[0], (int, float))])
    g_avg = statistics.mean([c[1] for c in colors if isinstance(c[1], (int, float))])
    b_avg = statistics.mean([c[2] for c in colors if isinstance(c[2], (int, float))])
    
    return (r_avg, g_avg, b_avg)


def get_cycle_species_data(cycle_path: Path, cycle_name: str) -> Dict[str, int]:
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


def generate_quick_population_summary(bb8_files: List[Path], output: Optional[Path], use_species_id: bool = False):
    """Generate a quick population count table using genes.tag or species ID for species identification."""
    
    if use_species_id:
        console.print(f"[blue]Analyzing {len(bb8_files)} organisms by species within hereditary tags...[/blue]")
        
        # Collect both tag and species ID for breakdown analysis
        tag_species_breakdown = defaultdict(lambda: defaultdict(int))
        errors = 0
        
        for file_path in track(bb8_files, description="Analyzing species breakdown"):
            try:
                data = load_bb8_file(file_path)
                extracted = extract_multiple_fields(data, ['genes.tag', 'genes.speciesID'])
                
                tag = extracted.get('genes.tag', 'Unknown')
                species_id = extracted.get('genes.speciesID', 'Unknown')
                
                tag_species_breakdown[tag][species_id] += 1
                
            except BB8ParseError:
                errors += 1
        
        # Display breakdown table
        console.print("\n[bold]Population Summary (By Species)[/bold]")
        table = Table()
        table.add_column("Tag", style="cyan") 
        table.add_column("Count", style="green")
        table.add_column("Percentage", style="yellow")
        table.add_column("Species Breakdown", style="white", max_width=60)
        
        total_organisms = sum(sum(species_counts.values()) for species_counts in tag_species_breakdown.values())
        
        for tag in sorted(tag_species_breakdown.keys()):
            species_counts = tag_species_breakdown[tag]
            tag_total = sum(species_counts.values())
            tag_percentage = (tag_total / total_organisms) * 100 if total_organisms > 0 else 0
            
            # Create species breakdown string
            breakdown_parts = []
            for species_id, count in sorted(species_counts.items(), key=lambda x: x[1], reverse=True):
                species_pct = (count / tag_total) * 100 if tag_total > 0 else 0
                breakdown_parts.append(f"species_{species_id}: {count} ({species_pct:.1f}%)")
            
            breakdown_str = ", ".join(breakdown_parts)
            
            table.add_row(
                str(tag),
                str(tag_total),
                f"{tag_percentage:.1f}%",
                breakdown_str
            )
        
        console.print(table)
        console.print(f"\n[bold]Total:[/bold] {total_organisms} organisms")
        
        if errors > 0:
            console.print(f"[red]Errors: {errors} files failed to load[/red]")
        
        # Save output if requested
        if output:
            summary_data = {
                'total_organisms': total_organisms,
                'tag_species_breakdown': {tag: dict(species_counts) for tag, species_counts in tag_species_breakdown.items()},
                'errors': errors
            }
            with open(output, 'wb') as f:
                import orjson
                f.write(orjson.dumps(summary_data, option=orjson.OPT_INDENT_2))
            console.print(f"\n[green]Summary saved to {output}[/green]")
        
    else:
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
                    extracted = extract_multiple_fields(data, ['genes.speciesID'])
                    species_id = extracted.get('genes.speciesID', 'Unknown')
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
                import orjson
                f.write(orjson.dumps(summary_data, option=orjson.OPT_INDENT_2))
            console.print(f"\n[green]Summary saved to {output}[/green]")


def generate_species_summary(input_path: Path, output: Optional[Path], quick_mode: bool = False, use_species_id: bool = False):
    """Generate a species distribution summary for a directory of bibites."""
    
    if input_path.is_file():
        input_path = input_path.parent
    
    bb8_files = list(input_path.glob('*.bb8'))
    if not bb8_files:
        console.print(f"[red]No .bb8 files found in {input_path}[/red]")
        return
    
    # Quick mode for population tracking
    if quick_mode:
        generate_quick_population_summary(bb8_files, output, use_species_id)
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
        'energy_stats': calculate_stats(energy_data) if energy_data else None,
        'age_stats': calculate_stats(age_data) if age_data else None,
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
            'dominant_color': get_dominant_color([org['color'] for org in organisms])
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
        import orjson
        with open(output, 'wb') as f:
            f.write(orjson.dumps(summary, option=orjson.OPT_INDENT_2))
        console.print(f"\n[green]Summary saved to {output}[/green]")