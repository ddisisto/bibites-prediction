"""
Spatial analysis utilities for extract_data.py

Provides geographic distribution analysis across island zones,
coordinate classification, and spatial statistics for ecosystem monitoring.
"""

import statistics
from pathlib import Path
from typing import Dict, Any, Optional
from collections import defaultdict
from rich.console import Console
from rich.progress import track
from rich.table import Table

from ...core.parser import load_bb8_file, extract_multiple_fields, BB8ParseError

console = Console()


def classify_zone(x: float, y: float) -> str:
    """Classify coordinates into island zones based on the 4-zone ecosystem layout."""
    # Based on coordinate analysis from cycle_20250830003320
    # Northern Island (small): Y > 5000
    # Eastern Island (medium): X > 7000 and -5000 <= Y <= 5000  
    # Southern Island (big): Y < -5000
    # Void (meat ring): extreme coordinates beyond typical landmasses
    # Central/Western: remaining coordinates
    
    # Check for void zone (extreme coordinates)
    if abs(x) > 14000 or abs(y) > 14000:
        return "Void"
    
    # Northern Island 
    if y > 5000:
        return "Northern Island"
    
    # Southern Island
    elif y < -5000:
        return "Southern Island"
    
    # Eastern Island
    elif x > 7000:
        return "Eastern Island"
    
    # Central/Western area
    else:
        return "Central/Western"


def generate_spatial_analysis(input_path: Path, output: Optional[Path]):
    """Generate spatial distribution analysis across island zones."""
    
    if input_path.is_file():
        input_path = input_path.parent
    
    bb8_files = list(input_path.glob('*.bb8'))
    if not bb8_files:
        console.print(f"[red]No .bb8 files found in {input_path}[/red]")
        return
    
    console.print(f"[blue]Analyzing spatial distribution of {len(bb8_files)} organisms across island zones...[/blue]")
    
    zone_species_data = defaultdict(lambda: defaultdict(list))
    zone_totals = defaultdict(int)
    species_zone_data = defaultdict(lambda: defaultdict(int))
    position_fields = ['rb2d.px', 'rb2d.py', 'genes.tag']
    errors = []
    
    for file_path in track(bb8_files, description="Analyzing positions"):
        try:
            data = load_bb8_file(file_path)
            extracted = extract_multiple_fields(data, position_fields)
            
            x = extracted.get('rb2d.px')
            y = extracted.get('rb2d.py') 
            species = extracted.get('genes.tag', 'unknown')
            
            if x is not None and y is not None:
                zone = classify_zone(x, y)
                zone_species_data[zone][species].append({
                    'file': file_path.name,
                    'x': x,
                    'y': y
                })
                zone_totals[zone] += 1
                species_zone_data[species][zone] += 1
                
        except BB8ParseError as e:
            errors.append(f"{file_path.name}: {e}")
    
    # Calculate zone statistics
    total_organisms = sum(zone_totals.values())
    
    # Display zone-based species distribution
    console.print("\n[bold]Species Distribution by Island Zone[/bold]")
    zone_table = Table()
    zone_table.add_column("Zone", style="cyan")
    zone_table.add_column("Total Count", style="green")
    zone_table.add_column("% of Population", style="yellow")
    zone_table.add_column("Dominant Species", style="blue")
    zone_table.add_column("Species Count", style="magenta")
    
    for zone in sorted(zone_totals.keys()):
        count = zone_totals[zone]
        percentage = (count / total_organisms * 100) if total_organisms > 0 else 0
        
        # Find dominant species in this zone
        species_counts = {species: len(organisms) for species, organisms in zone_species_data[zone].items()}
        if species_counts:
            # Fix the type error by using max with proper key function
            dominant_species = max(species_counts.items(), key=lambda item: item[1])[0]
            dominant_count = species_counts[dominant_species] 
            species_summary = f"{dominant_species} ({dominant_count})"
        else:
            species_summary = "None"
        
        zone_table.add_row(
            zone,
            str(count),
            f"{percentage:.1f}%",
            species_summary,
            str(len(zone_species_data[zone]))
        )
    
    console.print(zone_table)
    
    # Display species-based zone distribution  
    console.print("\n[bold]Zone Distribution by Species[/bold]")
    species_table = Table()
    species_table.add_column("Species", style="cyan")
    species_table.add_column("Total Count", style="green") 
    species_table.add_column("Primary Zone", style="blue")
    species_table.add_column("Zone Distribution", style="yellow")
    
    for species in sorted(species_zone_data.keys()):
        total_count = sum(species_zone_data[species].values())
        
        # Find primary zone for this species
        if species_zone_data[species]:
            # Fix the type error by using max with proper key function
            primary_zone = max(species_zone_data[species].items(), key=lambda item: item[1])[0]
            primary_count = species_zone_data[species][primary_zone]
        else:
            primary_zone = "None"
            primary_count = 0
        
        # Zone distribution summary
        zone_dist = []
        for zone in sorted(species_zone_data[species].keys()):
            count = species_zone_data[species][zone]
            pct = (count / total_count * 100) if total_count > 0 else 0
            zone_dist.append(f"{zone}: {count} ({pct:.0f}%)")
        
        species_table.add_row(
            species,
            str(total_count),
            f"{primary_zone} ({primary_count})",
            "; ".join(zone_dist)
        )
    
    console.print(species_table)
    
    # Generate detailed zone analysis
    analysis_summary = {
        'total_organisms': total_organisms,
        'zone_totals': dict(zone_totals),
        'zone_species_breakdown': {},
        'species_zone_preferences': dict(species_zone_data),
        'coordinate_ranges_by_zone': {},
        'errors': len(errors)
    }
    
    # Calculate coordinate ranges for each zone
    for zone, species_data in zone_species_data.items():
        all_positions = []
        species_breakdown = {}
        
        for species, organisms in species_data.items():
            positions = [(org['x'], org['y']) for org in organisms]
            all_positions.extend(positions)
            species_breakdown[species] = len(organisms)
        
        analysis_summary['zone_species_breakdown'][zone] = species_breakdown
        
        if all_positions:
            x_coords = [pos[0] for pos in all_positions]
            y_coords = [pos[1] for pos in all_positions]
            analysis_summary['coordinate_ranges_by_zone'][zone] = {
                'x_range': [min(x_coords), max(x_coords)],
                'y_range': [min(y_coords), max(y_coords)],
                'center': [statistics.mean(x_coords), statistics.mean(y_coords)],
                'organism_count': len(all_positions)
            }
    
    # Summary insights
    console.print(f"\n[bold]Spatial Analysis Summary:[/bold]")
    console.print(f"  Total organisms analyzed: {total_organisms}")
    console.print(f"  Zones populated: {len(zone_totals)}")
    
    if zone_totals:
        # Fix the type error by using max with proper key function
        most_populated = max(zone_totals.items(), key=lambda item: item[1])[0]
        least_populated = min(zone_totals.items(), key=lambda item: item[1])[0]
        console.print(f"  Most populated zone: {most_populated} ({zone_totals[most_populated]} organisms)")
        console.print(f"  Least populated zone: {least_populated} ({zone_totals[least_populated]} organisms)")
    
    if errors:
        console.print(f"\n[red]Errors in {len(errors)} files[/red]")
    
    # Save detailed results if requested
    if output:
        import orjson
        with open(output, 'wb') as f:
            f.write(orjson.dumps(analysis_summary, option=orjson.OPT_INDENT_2))
        console.print(f"\n[green]Spatial analysis saved to {output}[/green]")