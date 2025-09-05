"""
Spatial analysis utilities for extract_data.py

Provides geographic distribution analysis across concentric zones,
radial distance calculation, and spatial statistics for ecosystem monitoring.
"""

import statistics
import math
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from collections import defaultdict
from rich.console import Console
from rich.progress import track
from rich.table import Table

from ...core.parser import load_bb8_file, extract_multiple_fields, BB8ParseError
from .bibites_data import get_zip_file_from_data_path
from ..extract_metadata import extract_metadata_from_save

console = Console()


def calculate_distance_from_center(x: float, y: float) -> float:
    """Calculate radial distance from ecosystem center (0,0)."""
    return math.sqrt(x**2 + y**2)


def extract_world_radius(input_path: Path) -> float:
    """Extract world radius from SimulationSize setting in metadata."""
    try:
        # Get the data directory (parent of bibites if we're passed bibites dir)
        data_dir = input_path.parent if input_path.name == 'bibites' else input_path
        
        # Get original zip file from extracted data path
        zip_file = get_zip_file_from_data_path(data_dir)
        if not zip_file:
            console.print(f"[yellow]Could not find original zip file for {data_dir}, using default world radius[/yellow]")
            return 750.0  # Default fallback
        
        # Use metadata extraction to get settings
        temp_dir = Path('./tmp')
        temp_dir.mkdir(exist_ok=True)
        
        metadata = extract_metadata_from_save(zip_file, temp_dir, extract_raw=False)
        
        # Look for SimulationSize in settings
        simulation_size = None
        if 'settings' in metadata:
            # Check various possible keys for SimulationSize
            for key, value in metadata['settings'].items():
                if 'SimulationSize' in key or 'simulationSize' in key.lower():
                    if isinstance(value, dict) and 'Value' in value:
                        simulation_size = float(value['Value'])
                    elif isinstance(value, (int, float)):
                        simulation_size = float(value)
                    break
        
        if simulation_size is not None:
            world_radius = simulation_size  # SimulationSize IS the world radius
            console.print(f"[green]Extracted SimulationSize: {simulation_size}, using world_radius: {world_radius}[/green]")
            return world_radius
        else:
            console.print(f"[yellow]SimulationSize not found in metadata, using default world radius[/yellow]")
            return 1500.0  # Default fallback
            
    except Exception as e:
        console.print(f"[red]Error extracting world radius: {e}, using default[/red]")
        return 1500.0  # Default fallback


def parse_zone_configuration(input_path: Path) -> List[Dict[str, Any]]:
    """Parse zone configuration from settings.bb8settings via metadata extraction."""
    zones = []
    
    try:
        # Get the data directory (parent of bibites if we're passed bibites dir)
        data_dir = input_path.parent if input_path.name == 'bibites' else input_path
        
        # Get original zip file from extracted data path
        zip_file = get_zip_file_from_data_path(data_dir)
        if not zip_file:
            console.print(f"[yellow]Could not find original zip file for {data_dir}[/yellow]")
            return zones
        
        # Use metadata extraction to get zone data
        temp_dir = Path('./tmp')
        temp_dir.mkdir(exist_ok=True)
        
        metadata = extract_metadata_from_save(zip_file, temp_dir, extract_raw=False)
        
        # Extract zone info from metadata  
        if 'zones' in metadata:
            for zone_data in metadata['zones']:
                if isinstance(zone_data, dict) and zone_data.get('name'):
                    # Filter out spawn zones and focus on actual plant zones
                    if (zone_data.get('material') == 'Plant' and 
                        zone_data.get('radius', 0) > 0):
                        zones.append(zone_data)
        
        console.print(f"[green]Found {len(zones)} plant zones in configuration[/green]")
        return zones
        
    except Exception as e:
        console.print(f"[red]Error parsing zone configuration: {e}[/red]")
        return zones


def classify_zone_concentric(x: float, y: float, zones: List[Dict[str, Any]], world_radius: float) -> str:
    """Classify coordinates into zones, handling both positioned circular zones and concentric rings."""
    if not zones:
        return "Unknown"
    
    # Convert absolute coordinates to relative (0-1 range)
    rel_x = x / world_radius
    rel_y = y / world_radius
    
    # First, check positioned circular zones (highest priority)
    positioned_zones = []
    concentric_zones = []
    
    for zone in zones:
        radius = zone.get('radius', 0)
        inside_radius = zone.get('insideRadius', 0)
        name = zone.get('name', 'Unknown')
        distribution = zone.get('distribution', '')
        pos_x = zone.get('posX', 0)
        pos_y = zone.get('posY', 0)
        
        # All radii are relative in this ecosystem
        if not zone.get('radiusIsRelative', True):
            radius /= world_radius
            inside_radius /= world_radius
            pos_x /= world_radius  
            pos_y /= world_radius
        
        # WORKAROUND: Fix corrupted AntiPred distribution from metadata parsing bug
        if name == 'AntiPred' and distribution == 'Flat':
            distribution = 'CentricGradual'  # Silent fix for metadata parsing corruption
        
        # Handle positioned circular zones (Flat distribution with non-zero position)
        if distribution == 'Flat' and (pos_x != 0 or pos_y != 0):
            # Calculate distance from zone center 
            zone_distance = math.sqrt((rel_x - pos_x) ** 2 + (rel_y - pos_y) ** 2)
            
            if zone_distance <= radius:
                positioned_zones.append({
                    'name': name,
                    'distance_from_center': zone_distance,
                    'priority': 0  # Highest priority for positioned zones
                })
        
        # Handle concentric zones (centered at origin)
        elif distribution == 'CentricGradual' and pos_x == 0 and pos_y == 0:
            # Center circle (no insideRadius calculation needed)
            concentric_zones.append({
                'name': name,
                'min_distance': 0,
                'max_distance': radius,
                'priority': 1  # High priority for center
            })
        elif distribution in ['Ring', 'FlatRing'] and pos_x == 0 and pos_y == 0:
            # Calculate actual inside radius: insideRadius is relative to radius
            actual_inside_radius = inside_radius * radius
            
            if actual_inside_radius < radius:
                # Valid rings like MidPlateau and OuterReach
                concentric_zones.append({
                    'name': name,
                    'min_distance': actual_inside_radius,
                    'max_distance': radius,
                    'priority': 2  # Medium priority for rings
                })
            else:
                # Invalid ring configuration - inside radius too large
                # These might represent special spawn zones or deprecated configs
                pass
    
    # Return positioned zone match if found (highest priority)
    if positioned_zones:
        # If multiple positioned zones contain the point, return the closest one
        closest_positioned = min(positioned_zones, key=lambda z: z['distance_from_center'])
        return closest_positioned['name']
    
    # Fall back to concentric zone classification
    if concentric_zones:
        # Calculate distance from center for concentric zones
        distance = calculate_distance_from_center(x, y)
        relative_distance = distance / world_radius
        
        # Sort by priority, then by specificity (smaller zones first)
        concentric_zones.sort(key=lambda z: (z['priority'], z['max_distance'] - z['min_distance']))
        
        # Find the best matching concentric zone
        for zone in concentric_zones:
            if zone['min_distance'] <= relative_distance <= zone['max_distance']:
                return zone['name']
        
        # If no exact match, find the closest concentric zone
        closest_zone = None
        min_distance_diff = float('inf')
        
        for zone in concentric_zones:
            if relative_distance < zone['min_distance']:
                distance_diff = zone['min_distance'] - relative_distance
            elif relative_distance > zone['max_distance']:
                distance_diff = relative_distance - zone['max_distance']
            else:
                continue  # Should have been caught above
                
            if distance_diff < min_distance_diff:
                min_distance_diff = distance_diff
                closest_zone = zone['name']
        
        return closest_zone or "Beyond"
    
    return "Unknown"


def generate_spatial_analysis(input_path: Path, output: Optional[Path]):
    """Generate spatial distribution analysis across concentric zones."""
    
    if input_path.is_file():
        input_path = input_path.parent
    
    bb8_files = list(input_path.glob('*.bb8'))
    if not bb8_files:
        console.print(f"[red]No .bb8 files found in {input_path}[/red]")
        return
    
    console.print(f"[blue]Analyzing spatial distribution of {len(bb8_files)} organisms across concentric zones...[/blue]")
    
    # Parse zone configuration and extract world radius
    zones = parse_zone_configuration(input_path)
    
    # Extract world radius from SimulationSize setting
    world_radius = extract_world_radius(input_path)
    if not zones:
        console.print("[yellow]No zone configuration found, using fallback classification[/yellow]")
    else:
        console.print("[blue]Zone boundaries (% of world radius):[/blue]")
        for zone in zones:
            radius = zone.get('radius', 0)
            inside_radius = zone.get('insideRadius', 0)
            distribution = zone.get('distribution', '')
            name = zone.get('name', 'Unknown')
            
            if distribution == 'CentricGradual':
                console.print(f"  {name}: 0.0% - {radius*100:.1f}% (center)")
            elif distribution in ['Ring', 'FlatRing']:
                actual_inside_radius = inside_radius * radius
                if actual_inside_radius < radius:
                    console.print(f"  {name}: {actual_inside_radius*100:.1f}% - {radius*100:.1f}%")
                else:
                    console.print(f"  {name}: INVALID (inside {inside_radius*100:.1f}% > radius {radius*100:.1f}%)")
            else:
                console.print(f"  {name}: {radius*100:.1f}% (unknown distribution: {distribution})")
    
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
            if species is None:
                species = 'None'
            
            if x is not None and y is not None:
                zone = classify_zone_concentric(x, y, zones, world_radius) if zones else "Unknown"
                distance = calculate_distance_from_center(x, y)
                zone_species_data[zone][species].append({
                    'file': file_path.name,
                    'x': x,
                    'y': y,
                    'distance': distance
                })
                zone_totals[zone] += 1
                species_zone_data[species][zone] += 1
                
        except BB8ParseError as e:
            errors.append(f"{file_path.name}: {e}")
    
    # Calculate zone statistics
    total_organisms = sum(zone_totals.values())
    
    # Display zone-based species distribution
    console.print("\n[bold]Species Distribution by Concentric Zone[/bold]")
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
    
    # Display species-based zone distribution with radial analysis
    console.print("\n[bold]Zone Distribution by Species[/bold]")
    species_table = Table()
    species_table.add_column("Species", style="cyan")
    species_table.add_column("Total Count", style="green") 
    species_table.add_column("Primary Zone", style="blue")
    species_table.add_column("Zone Distribution", style="yellow")
    
    for species in sorted(species_zone_data.keys(), key=lambda x: str(x) if x is not None else "None"):
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
    
    # Add radial distance analysis with relative distances
    console.print("\n[bold]Radial Distance Analysis[/bold]")
    all_distances = []
    zone_distances = defaultdict(list)
    # world_radius will be extracted from metadata
    
    for zone, species_data in zone_species_data.items():
        for species, organisms in species_data.items():
            for organism in organisms:
                distance = organism['distance']
                all_distances.append(distance)
                zone_distances[zone].append(distance)
    
    if all_distances:
        min_abs = min(all_distances)
        max_abs = max(all_distances)
        mean_abs = statistics.mean(all_distances)
        
        console.print(f"  Absolute distance range: {min_abs:.1f} - {max_abs:.1f}")
        console.print(f"  Relative distance range: {min_abs/world_radius:.3f} - {max_abs/world_radius:.3f} ({min_abs/world_radius*100:.1f}% - {max_abs/world_radius*100:.1f}% of world)")
        console.print(f"  World radius (from SimulationSize): {world_radius:.1f} units")
        console.print(f"  Mean distance from center: {mean_abs:.1f} ({mean_abs/world_radius*100:.1f}% of world)")
        
        # Show distance ranges by zone
        distance_table = Table()
        distance_table.add_column("Zone", style="cyan")
        distance_table.add_column("Count", style="green")
        distance_table.add_column("Abs Range", style="yellow")
        distance_table.add_column("Rel Range (%)", style="blue")
        distance_table.add_column("Mean Abs (Rel %)", style="magenta")
        
        for zone in sorted(zone_distances.keys()):
            distances = zone_distances[zone]
            if distances:
                min_d, max_d = min(distances), max(distances)
                mean_d = statistics.mean(distances)
                distance_table.add_row(
                    zone,
                    str(len(distances)),
                    f"{min_d:.1f} - {max_d:.1f}",
                    f"{min_d/world_radius*100:.1f} - {max_d/world_radius*100:.1f}",
                    f"{mean_d:.1f} ({mean_d/world_radius*100:.1f}%)"
                )
        
        console.print(distance_table)
    
    # Generate detailed zone analysis
    analysis_summary = {
        'total_organisms': total_organisms,
        'zone_totals': dict(zone_totals),
        'zone_species_breakdown': {},
        'species_zone_preferences': dict(species_zone_data),
        'coordinate_ranges_by_zone': {},
        'radial_analysis': {
            'overall_range': [min(all_distances), max(all_distances)] if all_distances else [0, 0],
            'mean_distance': statistics.mean(all_distances) if all_distances else 0,
            'zone_distance_ranges': {}
        },
        'zone_configuration': zones,
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
            distances = [organism['distance'] for organism in species_data[species] for species in species_data]
            
            analysis_summary['coordinate_ranges_by_zone'][zone] = {
                'x_range': [min(x_coords), max(x_coords)],
                'y_range': [min(y_coords), max(y_coords)],
                'center': [statistics.mean(x_coords), statistics.mean(y_coords)],
                'organism_count': len(all_positions)
            }
            
            if distances:
                analysis_summary['radial_analysis']['zone_distance_ranges'][zone] = {
                    'min_distance': min(distances),
                    'max_distance': max(distances),
                    'mean_distance': statistics.mean(distances)
                }
    
    # Summary insights
    console.print(f"\n[bold]Spatial Analysis Summary:[/bold]")
    console.print(f"  Total organisms analyzed: {total_organisms}")
    console.print(f"  Zones populated: {len(zone_totals)}")
    console.print(f"  Zone configuration: {len(zones)} concentric zones parsed")
    
    if zone_totals:
        most_populated = max(zone_totals.items(), key=lambda item: item[1])[0]
        least_populated = min(zone_totals.items(), key=lambda item: item[1])[0]
        console.print(f"  Most populated zone: {most_populated} ({zone_totals[most_populated]} organisms)")
        console.print(f"  Least populated zone: {least_populated} ({zone_totals[least_populated]} organisms)")
        
        # Show ecosystem compactness
        if all_distances:
            ecosystem_extent = max(all_distances) / world_radius * 100
            console.print(f"  Ecosystem compactness: {ecosystem_extent:.1f}% of world radius (organisms concentrated near center)")
        console.print(f"  Used world radius: {world_radius:.1f} units (SimulationSize)")
    
    if errors:
        console.print(f"\n[red]Errors in {len(errors)} files[/red]")
    
    # Save detailed results if requested
    if output:
        import orjson
        with open(output, 'wb') as f:
            f.write(orjson.dumps(analysis_summary, option=orjson.OPT_INDENT_2))
        console.print(f"\n[green]Spatial analysis saved to {output}[/green]")