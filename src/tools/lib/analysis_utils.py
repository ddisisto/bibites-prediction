"""
Analysis utilities for ad-hoc analysis tools

Provides shared utilities extracted from ad-hoc analysis tools to eliminate code
duplication and standardize analysis patterns. This module leverages existing
infrastructure from field_extraction.py, population_analysis.py, and output_formatters.py.
"""

import json
import statistics
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union
from collections import defaultdict, Counter
from rich.console import Console
from rich.table import Table

console = Console()


def load_and_validate_organism_data(data_path: Union[str, Path]) -> List[Dict]:
    """Load organism data from JSON file and validate structure.
    
    This function standardizes how ad-hoc analysis tools load their data,
    typically from tmp/ directory JSON exports.
    
    Args:
        data_path: Path to JSON file containing organism data
        
    Returns:
        List of organism dictionaries with validated structure
        
    Raises:
        FileNotFoundError: If data file doesn't exist
        ValueError: If data structure is invalid
    """
    data_path = Path(data_path)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {data_path}: {e}")
    
    if not isinstance(data, list):
        raise ValueError(f"Expected list of organisms, got {type(data)}")
    
    if not data:
        raise ValueError("No organism data found")
    
    # Validate each organism has basic required structure
    for i, organism in enumerate(data):
        if not isinstance(organism, dict):
            raise ValueError(f"Organism {i} is not a dictionary")
        
        # Check for minimal required fields that most analysis tools expect
        required_base_fields = ['genes.tag', 'genes.speciesID']
        missing_fields = [field for field in required_base_fields if field not in organism]
        if missing_fields:
            console.print(f"[yellow]Warning: Organism {i} missing fields: {missing_fields}[/yellow]")
    
    console.print(f"[green]Loaded {len(data)} organisms from {data_path.name}[/green]")
    return data


def group_organisms_by_species(organisms: List[Dict], by_sim_id: bool = False) -> Dict[str, List[Dict]]:
    """Group organisms by species using either hereditary tag or sim-generated species ID.
    
    Standardizes the species grouping pattern used across multiple ad-hoc analysis tools.
    Leverages existing population_analysis.py patterns.
    
    Args:
        organisms: List of organism dictionaries
        by_sim_id: If True, use genes.speciesID; if False, use genes.tag
        
    Returns:
        Dictionary mapping species identifier to list of organisms
    """
    if by_sim_id:
        console.print(f"[blue]Grouping {len(organisms)} organisms by sim-generated species ID...[/blue]")
        species_field = 'genes.speciesID'
    else:
        console.print(f"[blue]Grouping {len(organisms)} organisms by hereditary tag...[/blue]")
        species_field = 'genes.tag'
    
    species_groups = defaultdict(list)
    
    for organism in organisms:
        species_id = organism.get(species_field, 'Unknown')
        species_groups[str(species_id)].append(organism)
    
    # Convert to regular dict and sort by population size
    result = dict(species_groups)
    sorted_species = sorted(result.keys(), key=lambda x: len(result[x]), reverse=True)
    
    console.print(f"[green]Found {len(sorted_species)} species groups[/green]")
    for species in sorted_species[:5]:  # Show top 5
        console.print(f"  {species}: {len(result[species])} organisms")
    if len(sorted_species) > 5:
        console.print(f"  ... and {len(sorted_species) - 5} more species")
    
    return result


def calculate_rankings(values: Dict[str, float], metric_name: str, higher_better: bool = True) -> List[Tuple[str, float, int]]:
    """Calculate rankings for species based on a metric value.
    
    Standardizes the ranking pattern used in multiple ad-hoc analysis tools.
    
    Args:
        values: Dictionary mapping species/organism ID to metric value
        metric_name: Human-readable name for the metric (for console output)
        higher_better: If True, higher values rank better; if False, lower values rank better
        
    Returns:
        List of tuples (species_id, value, rank) sorted by rank
    """
    if not values:
        return []
    
    # Sort by value
    sorted_items = sorted(values.items(), key=lambda x: x[1], reverse=higher_better)
    
    # Add rank information
    rankings = [(species_id, value, rank + 1) for rank, (species_id, value) in enumerate(sorted_items)]
    
    direction = "higher" if higher_better else "lower"
    console.print(f"[blue]Calculated {metric_name} rankings ({direction} is better)[/blue]")
    
    return rankings


def create_analysis_table(data: Dict[str, Dict[str, Any]], title: str, columns: List[str]) -> Table:
    """Create a standardized Rich table for analysis results.
    
    Uses the same styling patterns as existing output_formatters.py but with
    flexibility for different data structures common in ad-hoc analysis tools.
    
    Args:
        data: Dictionary mapping row identifier to row data dictionary
        title: Table title
        columns: List of column names to display from row data
        
    Returns:
        Rich Table object ready for console.print()
    """
    table = Table(title=title)
    
    # Add identifier column
    table.add_column("ID", style="cyan")
    
    # Add data columns
    for column in columns:
        table.add_column(column, style="green")
    
    # Sort rows by first numeric column if available, otherwise alphabetically
    try:
        numeric_col = next(col for col in columns 
                          if any(isinstance(row_data.get(col), (int, float)) 
                               for row_data in data.values()))
        sorted_rows = sorted(data.items(), 
                           key=lambda x: x[1].get(numeric_col, 0), 
                           reverse=True)
    except StopIteration:
        sorted_rows = sorted(data.items())
    
    # Add rows
    for row_id, row_data in sorted_rows:
        row_values = [str(row_id)]
        for column in columns:
            value = row_data.get(column)
            if value is None:
                row_values.append("[dim]None[/dim]")
            elif isinstance(value, float):
                row_values.append(f"{value:.2f}")
            else:
                row_values.append(str(value))
        
        table.add_row(*row_values)
    
    return table


def generate_insights(analysis_results: Dict[str, Any], context: str) -> List[str]:
    """Generate standardized insights from analysis results.
    
    Provides the insight generation pattern common across ad-hoc analysis tools,
    with context-aware messaging similar to the existing tools.
    
    Args:
        analysis_results: Dictionary containing analysis metrics and results
        context: Context string for insight generation (e.g., "combat", "reproduction")
        
    Returns:
        List of insight strings ready for console output
    """
    insights = []
    
    # Population insights
    if 'total_organisms' in analysis_results:
        total = analysis_results['total_organisms']
        insights.append(f"📊 Ecosystem contains {total} organisms")
        
        if total < 50:
            insights.append("⚠️  Population below optimal simulation threshold")
        elif total > 500:
            insights.append("🐌 Large population may slow simulation performance")
        else:
            insights.append("✅ Population size optimal for analysis and simulation speed")
    
    # Species diversity insights
    if 'species_count' in analysis_results:
        species_count = analysis_results['species_count']
        insights.append(f"🧬 Found {species_count} distinct species")
        
        if species_count < 3:
            insights.append("⚠️  Low species diversity - ecosystem may be unstable")
        elif species_count > 10:
            insights.append("🌟 High species diversity indicates active speciation")
    
    # Context-specific insights
    if context == "combat":
        if 'total_combatants' in analysis_results:
            combatants = analysis_results['total_combatants']
            total = analysis_results.get('total_organisms', 1)
            combat_rate = (combatants / total) * 100
            
            if combat_rate > 40:
                insights.append("🔥 High combat pressure - ecosystem in active warfare")
            elif combat_rate > 25:
                insights.append("⚔️  Moderate combat - balanced predator-prey dynamics")
            else:
                insights.append("🕊️  Low combat - peaceful ecosystem")
    
    elif context == "reproduction":
        if 'total_parents' in analysis_results:
            parents = analysis_results['total_parents']
            total = analysis_results.get('total_organisms', 1)
            repro_rate = (parents / total) * 100
            
            if repro_rate > 30:
                insights.append("🥚 High reproductive activity - population growth phase")
            elif repro_rate < 10:
                insights.append("⚠️  Low reproductive activity - population may decline")
            else:
                insights.append("📈 Balanced reproductive activity")
    
    elif context == "evolution":
        if 'generation_range' in analysis_results:
            gen_range = analysis_results['generation_range']
            insights.append(f"🧬 Generation spread: {gen_range}")
            
            if isinstance(gen_range, tuple) and len(gen_range) == 2:
                min_gen, max_gen = gen_range
                if max_gen - min_gen > 50:
                    insights.append("📈 Long evolutionary history - mature ecosystem")
                elif max_gen - min_gen < 10:
                    insights.append("🆕 Recent speciation event or population bottleneck")
    
    # Performance insights
    if 'top_performers' in analysis_results:
        performers = analysis_results['top_performers']
        if performers:
            top_species = performers[0].get('species', 'Unknown')
            insights.append(f"🏆 Top performer: {top_species}")
    
    # Warning insights for population health
    if 'critical_populations' in analysis_results:
        critical = analysis_results['critical_populations']
        if critical:
            for species in critical:
                insights.append(f"🚨 {species} at critically low population - extinction risk")
    
    return insights


def calculate_species_statistics(species_groups: Dict[str, List[Dict]], metrics: List[str]) -> Dict[str, Dict[str, float]]:
    """Calculate statistical summaries for each species across specified metrics.
    
    Standardizes the statistical calculation pattern used in ad-hoc analysis tools.
    Leverages existing calculate_stats function from population_analysis.py patterns.
    
    Args:
        species_groups: Dictionary from group_organisms_by_species()
        metrics: List of field names to calculate statistics for
        
    Returns:
        Dictionary mapping species to statistics dictionary
    """
    from .population_analysis import calculate_stats  # Use existing infrastructure
    
    species_stats = {}
    
    for species_id, organisms in species_groups.items():
        species_stats[species_id] = {}
        
        for metric in metrics:
            # Extract numeric values for this metric
            values = []
            for organism in organisms:
                value = organism.get(metric)
                if isinstance(value, (int, float)):
                    values.append(float(value))
            
            if values:
                stats = calculate_stats(values)
                species_stats[species_id][metric] = stats
            else:
                species_stats[species_id][metric] = {'count': 0, 'mean': 0.0}
    
    return species_stats


def filter_mature_organisms(organisms: List[Dict], size_threshold: float = 0.5) -> List[Dict]:
    """Filter organisms to only include mature specimens above size threshold.
    
    Standardizes the maturity filtering pattern used across multiple ad-hoc analysis tools.
    
    Args:
        organisms: List of organism dictionaries
        size_threshold: Minimum size to consider organism mature
        
    Returns:
        List of mature organisms
    """
    mature_organisms = []
    
    for organism in organisms:
        size = organism.get('body.d2Size', 0.0) or 0.0
        if size >= size_threshold:
            mature_organisms.append(organism)
    
    console.print(f"[blue]Filtered to {len(mature_organisms)} mature organisms (size ≥ {size_threshold})[/blue]")
    return mature_organisms


def find_top_performers(organisms: List[Dict], metric_field: str, count: int = 5, higher_better: bool = True) -> List[Dict]:
    """Find top performing organisms based on a specific metric.
    
    Standardizes the top performer identification pattern used in ad-hoc analysis tools.
    
    Args:
        organisms: List of organism dictionaries
        metric_field: Field name to rank by
        count: Number of top performers to return
        higher_better: If True, higher values are better
        
    Returns:
        List of top performing organisms
    """
    # Filter organisms that have the metric
    valid_organisms = [org for org in organisms if metric_field in org and org[metric_field] is not None]
    
    if not valid_organisms:
        console.print(f"[yellow]Warning: No organisms found with metric '{metric_field}'[/yellow]")
        return []
    
    # Sort by metric
    sorted_organisms = sorted(valid_organisms, 
                            key=lambda x: x[metric_field], 
                            reverse=higher_better)
    
    top_performers = sorted_organisms[:count]
    
    direction = "highest" if higher_better else "lowest"
    console.print(f"[green]Found {len(top_performers)} top performers by {metric_field} ({direction} values)[/green]")
    
    return top_performers