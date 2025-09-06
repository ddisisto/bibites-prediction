"""
Behavioral Analysis Module

Comprehensive behavioral analysis for Bibites organisms focusing on:
1. Pheromone emission and detection patterns (especially red pheromone danger signals)
2. Neural complexity metrics (brain architecture analysis)
3. Behavioral strategy classification

Preserves algorithms from existing ad-hoc analysis tools while providing
modular interface for integration into unified bibites analysis system.
"""

import statistics
from collections import defaultdict
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console
from rich.table import Table

from .analysis_utils import group_organisms_by_species

console = Console()


def calculate_basic_stats(values: List[float]) -> Dict[str, float]:
    """Calculate basic statistical measures for a list of values."""
    if not values:
        return {}
    
    return {
        'mean': statistics.mean(values),
        'stdev': statistics.stdev(values) if len(values) > 1 else 0.0,
        'min': min(values),
        'max': max(values),
        'median': statistics.median(values),
        'count': len(values)
    }


def analyze_pheromone_patterns(organisms: List[Dict], focus_color: str = "red") -> Dict:
    """
    Analyze pheromone emission and detection patterns across organisms.
    
    Focuses on red pheromone (PheroOut1/PheroSense1) patterns as these are
    critical danger signals in protectorate ecosystems. Preserves the core
    algorithm from pheromone_analysis.py.
    
    Args:
        organisms: List of organism dictionaries with neural data
        focus_color: Pheromone color to focus analysis on ("red", "green", "blue")
        
    Returns:
        Dict containing pheromone analysis results by species
    """
    # Map focus color to pheromone indices
    color_map = {
        "red": 1,
        "green": 2, 
        "blue": 3
    }
    
    if focus_color not in color_map:
        raise ValueError(f"Invalid focus_color '{focus_color}'. Must be one of: {list(color_map.keys())}")
    
    focus_idx = color_map[focus_color]
    
    species_pheromone = defaultdict(list)
    
    for organism in organisms:
        # Use species ID if available, fallback to tag
        species_key = organism.get('genes.speciesID', organism.get('genes.tag', 'unknown'))
        tag = organism.get('genes.tag', 'unknown')
        generation = organism.get('genes.gen', 0)
        
        # Extract pheromone-related nodes from neural data
        nodes = organism.get('brain.Nodes', [])
        
        pheromone_data = {
            'tag': tag,
            'generation': generation,
            'phero_out_1': 0.0,  # Red pheromone emission
            'phero_out_2': 0.0,  # Green pheromone emission
            'phero_out_3': 0.0,  # Blue pheromone emission
            'phero_sense_1': 0.0,  # Red pheromone detection
            'phero_sense_2': 0.0,  # Green pheromone detection  
            'phero_sense_3': 0.0,  # Blue pheromone detection
        }
        
        # Extract pheromone node values (preserving original algorithm)
        for node in nodes:
            desc = node.get('Desc', '')
            value = node.get('Value', 0.0)
            
            if desc == 'PhereOut1':  # Red pheromone output
                pheromone_data['phero_out_1'] = value
            elif desc == 'PhereOut2':  # Green pheromone output
                pheromone_data['phero_out_2'] = value
            elif desc == 'PhereOut3':  # Blue pheromone output
                pheromone_data['phero_out_3'] = value
            elif desc == 'PheroSense1':  # Red pheromone detection
                pheromone_data['phero_sense_1'] = value
            elif desc == 'PheroSense2':  # Green pheromone detection
                pheromone_data['phero_sense_2'] = value
            elif desc == 'PheroSense3':  # Blue pheromone detection
                pheromone_data['phero_sense_3'] = value
        
        species_pheromone[species_key].append(pheromone_data)
    
    # Analyze patterns by species (preserving core algorithm)
    analysis_results = {
        'focus_color': focus_color,
        'species_analysis': {},
        'emitters': [],
        'detectors': [],
        'summary_stats': {}
    }
    
    for species_key in sorted(species_pheromone.keys()):
        organisms_data = species_pheromone[species_key]
        tag = organisms_data[0]['tag']  # All should have same tag
        
        # Calculate emission/detection statistics for focus color
        focus_emissions = [o[f'phero_out_{focus_idx}'] for o in organisms_data]
        focus_detections = [o[f'phero_sense_{focus_idx}'] for o in organisms_data]
        generations = [o['generation'] for o in organisms_data]
        
        avg_emission = statistics.mean(focus_emissions)
        max_emission = max(focus_emissions)
        avg_detection = statistics.mean(focus_detections)
        
        species_stats = {
            'species_id': str(species_key),  # Ensure string key for JSON compatibility
            'tag': tag,
            'organism_count': len(organisms_data),
            'generation_range': (min(generations), max(generations)),
            'emission_stats': {
                'avg': avg_emission,
                'max': max_emission,
                'values': focus_emissions
            },
            'detection_stats': {
                'avg': avg_detection,
                'values': focus_detections
            }
        }
        
        analysis_results['species_analysis'][str(species_key)] = species_stats
        
        # Identify significant emitters (threshold from original algorithm)
        if max_emission > 0.1:
            analysis_results['emitters'].append({
                'species': str(species_key),  # Ensure string for JSON compatibility
                'tag': tag,
                'avg_emission': avg_emission,
                'max_emission': max_emission,
                'count': len(organisms_data)
            })
        
        # Identify significant detectors
        if avg_detection > 0.1:
            analysis_results['detectors'].append({
                'species': str(species_key),  # Ensure string for JSON compatibility
                'tag': tag,
                'avg_detection': avg_detection,
                'count': len(organisms_data)
            })
    
    # Calculate summary statistics
    all_emissions = [e for species_data in species_pheromone.values() 
                    for e in [o[f'phero_out_{focus_idx}'] for o in species_data]]
    all_detections = [d for species_data in species_pheromone.values() 
                     for d in [o[f'phero_sense_{focus_idx}'] for o in species_data]]
    
    analysis_results['summary_stats'] = {
        'total_organisms': len(organisms),
        'species_count': len(species_pheromone),
        'emission_distribution': calculate_basic_stats(all_emissions) if all_emissions else {},
        'detection_distribution': calculate_basic_stats(all_detections) if all_detections else {},
        'emitter_species_count': len(analysis_results['emitters']),
        'detector_species_count': len(analysis_results['detectors'])
    }
    
    return analysis_results


def calculate_neural_complexity(organisms: List[Dict]) -> Dict:
    """
    Calculate neural complexity metrics for organisms.
    
    Preserves the core algorithm from neural_complexity_analysis.py that
    calculates nodes, synapses, and complexity ratios by species.
    
    Args:
        organisms: List of organism dictionaries with neural data
        
    Returns:
        Dict containing neural complexity analysis by species
    """
    species_neural = defaultdict(list)
    
    for organism in organisms:
        # Use species ID if available, fallback to tag
        species_key = organism.get('genes.speciesID', organism.get('genes.tag', 'unknown'))
        tag = organism.get('genes.tag', 'unknown')
        generation = organism.get('genes.gen', 0)
        
        # Count nodes and synapses (preserving original algorithm)
        nodes = organism.get('brain.Nodes', [])
        synapses = organism.get('brain.Synapses', [])
        
        node_count = len(nodes) if nodes else 0
        synapse_count = len(synapses) if synapses else 0
        
        species_neural[species_key].append({
            'tag': tag,
            'generation': generation,
            'node_count': node_count,
            'synapse_count': synapse_count,
            'complexity_ratio': synapse_count / max(node_count, 1)  # Avoid division by zero
        })
    
    # Analyze by species (preserving core algorithm)
    analysis_results = {
        'species_analysis': {},
        'complexity_rankings': [],
        'summary_stats': {}
    }
    
    for species_key in sorted(species_neural.keys()):
        organisms_data = species_neural[species_key]
        tag = organisms_data[0]['tag']  # All should have same tag
        
        node_counts = [o['node_count'] for o in organisms_data]
        synapse_counts = [o['synapse_count'] for o in organisms_data]
        complexity_ratios = [o['complexity_ratio'] for o in organisms_data]
        generations = [o['generation'] for o in organisms_data]
        
        # Calculate statistics (preserving original format)
        species_stats = {
            'species_id': str(species_key),  # Ensure string key for JSON compatibility
            'tag': tag,
            'organism_count': len(organisms_data),
            'generation_range': (min(generations), max(generations)),
            'nodes': {
                'mean': statistics.mean(node_counts),
                'stdev': statistics.stdev(node_counts) if len(node_counts) > 1 else 0,
                'values': node_counts
            },
            'synapses': {
                'mean': statistics.mean(synapse_counts),
                'stdev': statistics.stdev(synapse_counts) if len(synapse_counts) > 1 else 0,
                'values': synapse_counts
            },
            'complexity': {
                'mean': statistics.mean(complexity_ratios),
                'stdev': statistics.stdev(complexity_ratios) if len(complexity_ratios) > 1 else 0,
                'values': complexity_ratios
            }
        }
        
        analysis_results['species_analysis'][str(species_key)] = species_stats
        
        # Add to complexity rankings
        analysis_results['complexity_rankings'].append({
            'species': str(species_key),  # Ensure string for JSON compatibility
            'tag': tag,
            'avg_complexity': species_stats['complexity']['mean'],
            'avg_nodes': species_stats['nodes']['mean'],
            'avg_synapses': species_stats['synapses']['mean'],
            'count': len(organisms_data)
        })
    
    # Sort rankings by complexity ratio
    analysis_results['complexity_rankings'].sort(key=lambda x: x['avg_complexity'], reverse=True)
    
    # Calculate ecosystem-wide summary
    all_nodes = [n for species_data in species_neural.values() 
                for n in [o['node_count'] for o in species_data]]
    all_synapses = [s for species_data in species_neural.values() 
                   for s in [o['synapse_count'] for o in species_data]]
    all_complexity = [c for species_data in species_neural.values() 
                     for c in [o['complexity_ratio'] for o in species_data]]
    
    analysis_results['summary_stats'] = {
        'total_organisms': len(organisms),
        'species_count': len(species_neural),
        'nodes_distribution': calculate_basic_stats(all_nodes) if all_nodes else {},
        'synapses_distribution': calculate_basic_stats(all_synapses) if all_synapses else {},
        'complexity_distribution': calculate_basic_stats(all_complexity) if all_complexity else {}
    }
    
    return analysis_results


def classify_behavioral_strategies(organisms: List[Dict]) -> Dict:
    """
    Classify organisms into behavioral strategy categories based on 
    neural architecture and pheromone patterns.
    
    Combines pheromone and neural complexity analysis to identify
    behavioral archetypes across the ecosystem.
    
    Args:
        organisms: List of organism dictionaries with complete data
        
    Returns:
        Dict containing behavioral strategy classification
    """
    # Get pheromone and neural analysis
    pheromone_analysis = analyze_pheromone_patterns(organisms, focus_color="red")
    neural_analysis = calculate_neural_complexity(organisms)
    
    strategies = {
        'communicators': [],      # High pheromone emission/detection
        'complex_thinkers': [],   # High neural complexity
        'simple_survivors': [],   # Low complexity, low communication
        'specialists': [],        # High in one domain, low in another
        'generalists': []         # Moderate in multiple domains
    }
    
    # Classify each species by combining analyses
    for species_key in pheromone_analysis['species_analysis']:
        phero_data = pheromone_analysis['species_analysis'][species_key]
        neural_data = neural_analysis['species_analysis'].get(species_key, {})
        
        if not neural_data:
            continue
            
        # Extract key metrics
        max_emission = phero_data['emission_stats']['max']
        avg_detection = phero_data['detection_stats']['avg']
        avg_complexity = neural_data['complexity']['mean']
        avg_nodes = neural_data['nodes']['mean']
        
        # Classification logic
        is_high_communicator = max_emission > 0.1 or avg_detection > 0.1
        is_complex_brain = avg_complexity > 2.0 or avg_nodes > 20
        
        species_profile = {
            'species': species_key,
            'tag': phero_data['tag'],
            'count': phero_data['organism_count'],
            'communication_score': max(max_emission, avg_detection),
            'complexity_score': avg_complexity,
            'node_count': avg_nodes,
            'classification_factors': {
                'high_communicator': is_high_communicator,
                'complex_brain': is_complex_brain,
                'max_emission': max_emission,
                'avg_detection': avg_detection,
                'complexity_ratio': avg_complexity
            }
        }
        
        # Assign to behavioral strategy category
        if is_high_communicator and is_complex_brain:
            strategies['generalists'].append(species_profile)
        elif is_high_communicator and not is_complex_brain:
            strategies['communicators'].append(species_profile)
        elif not is_high_communicator and is_complex_brain:
            strategies['complex_thinkers'].append(species_profile)
        elif max_emission > 0.05 or avg_detection > 0.05 or avg_complexity > 1.5:
            strategies['specialists'].append(species_profile)
        else:
            strategies['simple_survivors'].append(species_profile)
    
    # Add strategy summaries
    strategy_summary = {}
    for strategy_name, species_list in strategies.items():
        strategy_summary[strategy_name] = {
            'count': len(species_list),
            'species': [s['species'] for s in species_list],
            'avg_communication': statistics.mean([s['communication_score'] for s in species_list]) if species_list else 0,
            'avg_complexity': statistics.mean([s['complexity_score'] for s in species_list]) if species_list else 0
        }
    
    return {
        'strategies': strategies,
        'strategy_summary': strategy_summary,
        'total_species': len(pheromone_analysis['species_analysis']),
        'classification_criteria': {
            'high_communication_threshold': 0.1,
            'complex_brain_threshold': 2.0,
            'node_count_threshold': 20
        }
    }


def display_behavioral_analysis_results(results_dict: Dict, analysis_type: str) -> None:
    """
    Display behavioral analysis results in rich formatted tables.
    
    Args:
        results_dict: Results from behavioral analysis functions
        analysis_type: Type of analysis ("pheromone", "neural", "strategy")
    """
    if analysis_type == "pheromone":
        _display_pheromone_results(results_dict)
    elif analysis_type == "neural":
        _display_neural_results(results_dict)
    elif analysis_type == "strategy":
        _display_strategy_results(results_dict)
    else:
        console.print(f"[red]Unknown analysis type: {analysis_type}[/red]")


def _display_pheromone_results(results: Dict) -> None:
    """Display pheromone analysis results."""
    console.print(f"\n[bold blue]🔴 {results['focus_color'].upper()} PHEROMONE ANALYSIS[/bold blue]")
    console.print("=" * 80)
    
    # Species breakdown table
    table = Table(title="Species Pheromone Patterns")
    table.add_column("Species ID", style="cyan")
    table.add_column("Tag", style="green")
    table.add_column("Count", justify="right")
    table.add_column("Avg Emission", justify="right")
    table.add_column("Max Emission", justify="right")
    table.add_column("Avg Detection", justify="right")
    table.add_column("Status")
    
    for species_data in results['species_analysis'].values():
        avg_emission = species_data['emission_stats']['avg']
        max_emission = species_data['emission_stats']['max']
        avg_detection = species_data['detection_stats']['avg']
        
        status = "Normal"
        if max_emission > 0.1:
            status = "[red]EMITTER[/red]"
        elif avg_detection > 0.1:
            status = "[yellow]DETECTOR[/yellow]"
        
        table.add_row(
            str(species_data['species_id']),
            species_data['tag'],
            str(species_data['organism_count']),
            f"{avg_emission:.3f}",
            f"{max_emission:.3f}",
            f"{avg_detection:.3f}",
            status
        )
    
    console.print(table)
    
    # Summary
    summary = results['summary_stats']
    console.print(f"\n[bold]Summary:[/bold] {summary['total_organisms']} organisms, {summary['species_count']} species")
    console.print(f"Emitter species: {summary['emitter_species_count']}, Detector species: {summary['detector_species_count']}")


def _display_neural_results(results: Dict) -> None:
    """Display neural complexity analysis results."""
    console.print(f"\n[bold blue]🧠 NEURAL COMPLEXITY ANALYSIS[/bold blue]")
    console.print("=" * 80)
    
    # Complexity rankings table
    table = Table(title="Neural Complexity Rankings")
    table.add_column("Rank", justify="right")
    table.add_column("Species ID", style="cyan") 
    table.add_column("Tag", style="green")
    table.add_column("Count", justify="right")
    table.add_column("Avg Nodes", justify="right")
    table.add_column("Avg Synapses", justify="right")
    table.add_column("Complexity Ratio", justify="right")
    
    for i, species in enumerate(results['complexity_rankings'], 1):
        table.add_row(
            str(i),
            str(species['species']),
            species['tag'],
            str(species['count']),
            f"{species['avg_nodes']:.1f}",
            f"{species['avg_synapses']:.1f}",
            f"{species['avg_complexity']:.2f}"
        )
    
    console.print(table)
    
    # Summary statistics
    summary = results['summary_stats']
    console.print(f"\n[bold]Summary:[/bold] {summary['total_organisms']} organisms, {summary['species_count']} species")
    if summary['complexity_distribution']:
        dist = summary['complexity_distribution']
        console.print(f"Complexity distribution: {dist['mean']:.2f} ± {dist['stdev']:.2f} (range: {dist['min']:.2f}-{dist['max']:.2f})")


def _display_strategy_results(results: Dict) -> None:
    """Display behavioral strategy classification results."""
    console.print(f"\n[bold blue]🎭 BEHAVIORAL STRATEGY CLASSIFICATION[/bold blue]")
    console.print("=" * 80)
    
    # Strategy summary
    for strategy_name, summary in results['strategy_summary'].items():
        if summary['count'] > 0:
            console.print(f"\n[bold]{strategy_name.replace('_', ' ').title()}:[/bold] {summary['count']} species")
            console.print(f"  Avg Communication: {summary['avg_communication']:.3f}")
            console.print(f"  Avg Complexity: {summary['avg_complexity']:.2f}")
            console.print(f"  Species: {', '.join(map(str, summary['species']))}")
    
    # Detailed species table
    table = Table(title="Species Behavioral Classification")
    table.add_column("Species ID", style="cyan")
    table.add_column("Tag", style="green") 
    table.add_column("Strategy", style="yellow")
    table.add_column("Communication", justify="right")
    table.add_column("Complexity", justify="right")
    table.add_column("Nodes", justify="right")
    
    all_species = []
    for strategy_name, species_list in results['strategies'].items():
        for species in species_list:
            all_species.append((strategy_name, species))
    
    # Sort by communication score + complexity score for interesting insights
    all_species.sort(key=lambda x: x[1]['communication_score'] + x[1]['complexity_score'], reverse=True)
    
    for strategy_name, species in all_species:
        table.add_row(
            str(species['species']),
            species['tag'],
            strategy_name.replace('_', ' ').title(),
            f"{species['communication_score']:.3f}",
            f"{species['complexity_score']:.2f}",
            f"{species['node_count']:.1f}"
        )
    
    console.print(table)
    
    console.print(f"\n[bold]Classification Criteria:[/bold]")
    criteria = results['classification_criteria']
    console.print(f"  High Communication Threshold: {criteria['high_communication_threshold']}")
    console.print(f"  Complex Brain Threshold: {criteria['complex_brain_threshold']}")
    console.print(f"  Node Count Threshold: {criteria['node_count_threshold']}")