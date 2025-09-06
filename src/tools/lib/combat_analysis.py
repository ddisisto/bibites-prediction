"""
Combat effectiveness analysis module for Bibites ecosystem analysis.

Provides comprehensive combat analysis capabilities including size-relative combat metrics,
lineage-specific combat patterns, and combat vs reproductive correlation analysis.
Integrates the key algorithms from ad-hoc analysis tools into the unified library structure.

This module preserves the critical size-relative combat algorithm:
    size_adjusted_damage = damage / max(size, 0.01)  # Damage per unit size
    size_kill_ratio = kills / max(size, 0.01)  # Kills per unit size
    combat_fitness = size_adjusted_damage + (size_kill_ratio * 100)
"""

import statistics
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
from pathlib import Path

from .field_extraction import process_batch_files
from .analysis_utils import (
    load_and_validate_organism_data, group_organisms_by_species,
    filter_mature_organisms, find_top_performers, generate_insights,
    create_analysis_table, calculate_rankings
)
from .output_formatters import display_table, save_json_output
from rich.console import Console
from rich.table import Table

console = Console()


def calculate_combat_effectiveness(organisms: List[Dict], size_relative: bool = True) -> Dict:
    """Calculate comprehensive combat effectiveness metrics for organisms.
    
    This function implements the core size-relative combat algorithm that accounts
    for damage scaling with body size, providing true combat efficiency metrics.
    
    Args:
        organisms: List of organism dictionaries with combat data
        size_relative: If True, calculate size-adjusted combat metrics
        
    Returns:
        Dictionary containing combat analysis results including top performers,
        rankings, and ecosystem combat statistics
    """
    if not organisms:
        return {'error': 'No organisms provided for combat analysis'}
    
    console.print(f"[blue]Calculating combat effectiveness for {len(organisms)} organisms...[/blue]")
    
    # Separate organisms by combat activity level
    combat_data = {
        'all': [],
        'combatants': [],  # Have any combat activity
        'killers': [],     # Have successful kills
        'mature': []       # Size > 0.5 for meaningful analysis
    }
    
    for organism in organisms:
        # Extract combat metrics (CRITICAL FIELD MAPPINGS)
        damage = organism.get('body.mouth.totalDamageDealt', 0.0) or 0.0
        kills = organism.get('body.mouth.totalMurders', 0) or 0
        bites = organism.get('body.mouth.bibitesBitten', 0) or 0
        
        # Physical and temporal metrics
        size = organism.get('body.d2Size', 0.0) or 0.0
        eggs_laid = organism.get('body.eggLayer.nEggsLaid', 0) or 0
        time_alive = organism.get('clock.timeAlive', 1.0) or 1.0
        
        # Basic identifiers
        species_id = organism.get('genes.speciesID', 'Unknown')
        generation = organism.get('genes.gen', 0)
        tag = organism.get('genes.tag', 'Unknown')
        
        # CORE SIZE-RELATIVE COMBAT METRICS (PRESERVE EXACTLY)
        if size_relative:
            size_adjusted_damage = damage / max(size, 0.01)  # Damage per unit size
            size_kill_ratio = kills / max(size, 0.01)       # Kills per unit size
            combat_fitness = size_adjusted_damage + (size_kill_ratio * 100)
        else:
            size_adjusted_damage = damage
            size_kill_ratio = kills
            combat_fitness = damage + (kills * 100)
        
        # Additional effectiveness metrics
        damage_efficiency = damage / max(time_alive, 1.0) * 60  # Damage per minute
        bite_efficiency = kills / max(bites, 1) if bites > 0 else 0  # Kill rate per bite
        reproductive_rate = eggs_laid / (time_alive / 3600)  # Eggs per hour
        
        organism_combat_data = {
            'species_id': species_id,
            'generation': generation,
            'tag': tag,
            'damage': damage,
            'kills': kills,
            'bites': bites,
            'size': size,
            'eggs_laid': eggs_laid,
            'time_alive': time_alive,
            # Size-relative metrics (key innovation)
            'size_adjusted_damage': size_adjusted_damage,
            'size_kill_ratio': size_kill_ratio,
            'damage_efficiency': damage_efficiency,
            'bite_efficiency': bite_efficiency,
            'reproductive_rate': reproductive_rate,
            'combat_fitness': combat_fitness,  # Combined combat effectiveness score
            'total_fitness': eggs_laid + (kills * 5)  # Combined reproductive + combat
        }
        
        # Classify organism
        combat_data['all'].append(organism_combat_data)
        
        # Combat activity classification
        if damage > 0 or kills > 0 or bites > 0:
            combat_data['combatants'].append(organism_combat_data)
        
        # Successful killers
        if kills > 0:
            combat_data['killers'].append(organism_combat_data)
        
        # Mature organisms (size > 0.5 for meaningful analysis)
        if size > 0.5:
            combat_data['mature'].append(organism_combat_data)
    
    # Calculate ecosystem-wide statistics
    total_combatants = len(combat_data['combatants'])
    total_killers = len(combat_data['killers'])
    total_mature = len(combat_data['mature'])
    
    combat_participation = (total_combatants / len(organisms)) * 100
    kill_rate = (total_killers / len(organisms)) * 100
    maturity_rate = (total_mature / len(organisms)) * 100
    
    # Find top performers (focusing on mature combatants for meaningful results)
    mature_combatants = [org for org in combat_data['mature'] 
                        if org['damage'] > 0 or org['kills'] > 0 or org['bites'] > 0]
    
    top_damage_dealers = []
    top_killers = []
    top_combat_fitness = []
    
    if mature_combatants:
        # Top size-adjusted damage dealers
        top_damage_dealers = sorted(mature_combatants, 
                                   key=lambda x: x['size_adjusted_damage'], 
                                   reverse=True)[:8]
        
        # Top size-adjusted killers
        top_killers = sorted(mature_combatants, 
                            key=lambda x: x['size_kill_ratio'], 
                            reverse=True)[:8]
        
        # Top overall combat efficiency
        top_combat_fitness = sorted(mature_combatants, 
                                   key=lambda x: x['combat_fitness'], 
                                   reverse=True)[:5]
    
    # Generate ecosystem insights
    analysis_results = {
        'total_organisms': len(organisms),
        'total_combatants': total_combatants,
        'total_killers': total_killers,
        'total_mature': total_mature
    }
    insights = generate_insights(analysis_results, "combat")
    
    return {
        'summary': {
            'total_organisms': len(organisms),
            'combat_participation_rate': combat_participation,
            'kill_rate': kill_rate,
            'maturity_rate': maturity_rate,
            'total_combatants': total_combatants,
            'total_killers': total_killers,
            'mature_combatants': len(mature_combatants)
        },
        'top_performers': {
            'damage_dealers': top_damage_dealers,
            'killers': top_killers,
            'combat_fitness': top_combat_fitness
        },
        'combat_data': combat_data,
        'insights': insights,
        'size_relative': size_relative
    }


def analyze_predator_combat_patterns(organisms: List[Dict], lineage_filter: str = None) -> Dict:
    """Analyze combat patterns specific to predator lineages.
    
    Provides lineage-specific combat analysis with focus on predator effectiveness
    and inter-lineage comparisons.
    
    Args:
        organisms: List of organism dictionaries
        lineage_filter: Optional specific lineage to focus on (e.g., 'Pred', 'Pred.lessgreen')
        
    Returns:
        Dictionary containing lineage-specific combat analysis
    """
    if not organisms:
        return {'error': 'No organisms provided for lineage analysis'}
    
    console.print(f"[blue]Analyzing predator combat patterns for {len(organisms)} organisms...[/blue]")
    if lineage_filter:
        console.print(f"[blue]Filtering for lineage: {lineage_filter}[/blue]")
    
    # Group organisms by lineage (using hereditary tag)
    lineage_groups = group_organisms_by_species(organisms, by_sim_id=False)
    
    # Define primary combat lineages
    combat_lineages = ['Pred', 'Pred.lessgreen', 'Greencreep', 'Prey.Basic']
    
    lineage_combat_data = {}
    
    for lineage in combat_lineages:
        if lineage_filter and lineage != lineage_filter:
            continue
            
        if lineage not in lineage_groups:
            continue
        
        lineage_organisms = lineage_groups[lineage]
        active_combatants = []
        
        # Calculate combat metrics for this lineage
        for organism in lineage_organisms:
            damage = organism.get('body.mouth.totalDamageDealt', 0.0) or 0.0
            kills = organism.get('body.mouth.totalMurders', 0) or 0
            bites = organism.get('body.mouth.bibitesBitten', 0) or 0
            size = organism.get('body.d2Size', 0.0) or 0.0
            time_alive = organism.get('clock.timeAlive', 1.0) or 1.0
            
            # Only include organisms with combat activity
            if damage > 0 or kills > 0 or bites > 0:
                combat_info = {
                    'species_id': organism.get('genes.speciesID', 'Unknown'),
                    'generation': organism.get('genes.gen', 0),
                    'damage': damage,
                    'kills': kills,
                    'bites': bites,
                    'size': size,
                    'damage_per_minute': (damage / time_alive) * 60,
                    'kill_efficiency': kills / max(damage, 1),
                    'bite_accuracy': kills / max(bites, 1) if bites > 0 else 0,
                    'size_adjusted_damage': damage / max(size, 0.01),
                    'lineage': lineage
                }
                active_combatants.append(combat_info)
        
        if not active_combatants:
            lineage_combat_data[lineage] = {
                'total_population': len(lineage_organisms),
                'active_combatants': 0,
                'status': 'PACIFIST',
                'combat_participation': 0.0
            }
            continue
        
        # Calculate lineage statistics
        damages = [c['damage'] for c in active_combatants]
        kills = [c['kills'] for c in active_combatants]
        damage_rates = [c['damage_per_minute'] for c in active_combatants]
        size_damages = [c['size_adjusted_damage'] for c in active_combatants]
        
        total_damage = sum(damages)
        total_kills = sum(kills)
        combat_participation = (len(active_combatants) / len(lineage_organisms)) * 100
        
        # Find top performer in this lineage
        top_performer = max(active_combatants, key=lambda x: x['damage'])
        
        lineage_combat_data[lineage] = {
            'total_population': len(lineage_organisms),
            'active_combatants': len(active_combatants),
            'combat_participation': combat_participation,
            'total_damage': total_damage,
            'total_kills': total_kills,
            'avg_damage': statistics.mean(damages),
            'avg_kills': statistics.mean(kills),
            'avg_damage_rate': statistics.mean(damage_rates),
            'avg_size_adjusted_damage': statistics.mean(size_damages),
            'damage_rate_std': statistics.stdev(damage_rates) if len(damage_rates) > 1 else 0,
            'top_performer': top_performer,
            'status': 'ACTIVE_COMBAT'
        }
    
    # Comparative analysis between Pred and Pred.lessgreen
    comparison = {}
    if 'Pred' in lineage_combat_data and 'Pred.lessgreen' in lineage_combat_data:
        pred_data = lineage_combat_data['Pred']
        predless_data = lineage_combat_data['Pred.lessgreen']
        
        if pred_data['status'] == 'ACTIVE_COMBAT' and predless_data['status'] == 'ACTIVE_COMBAT':
            if pred_data['avg_damage'] > predless_data['avg_damage']:
                advantage = ((pred_data['avg_damage'] - predless_data['avg_damage']) / 
                           predless_data['avg_damage']) * 100
                comparison = {'winner': 'Pred', 'advantage_percent': advantage, 'metric': 'damage'}
            else:
                advantage = ((predless_data['avg_damage'] - pred_data['avg_damage']) / 
                           pred_data['avg_damage']) * 100
                comparison = {'winner': 'Pred.lessgreen', 'advantage_percent': advantage, 'metric': 'damage'}
    
    # Check for surprising predators (Greencreep, Prey.Basic showing combat behavior)
    surprising_predators = {}
    for lineage in ['Greencreep', 'Prey.Basic']:
        if lineage in lineage_combat_data and lineage_combat_data[lineage]['status'] == 'ACTIVE_COMBAT':
            surprising_predators[lineage] = lineage_combat_data[lineage]
    
    return {
        'lineage_analysis': lineage_combat_data,
        'pred_comparison': comparison,
        'surprising_predators': surprising_predators,
        'lineage_filter': lineage_filter
    }


def combat_reproductive_correlation(organisms: List[Dict]) -> Dict:
    """Analyze correlation between combat effectiveness and reproductive success.
    
    Examines the tradeoffs and synergies between fighting ability and breeding success
    across different maturity levels and species.
    
    Args:
        organisms: List of organism dictionaries
        
    Returns:
        Dictionary containing combat vs reproduction correlation analysis
    """
    if not organisms:
        return {'error': 'No organisms provided for correlation analysis'}
    
    console.print(f"[blue]Analyzing combat vs reproductive correlation for {len(organisms)} organisms...[/blue]")
    
    # Group organisms by reproductive and combat status
    analysis_groups = {
        'all': [],
        'mature': [],       # Size > 1.0 for meaningful reproductive analysis
        'parents': [],      # Have laid eggs
        'fighters': [],     # Have combat activity  
        'killers': []       # Have successful kills
    }
    
    for organism in organisms:
        # Extract all relevant metrics
        damage = organism.get('body.mouth.totalDamageDealt', 0.0) or 0.0
        kills = organism.get('body.mouth.totalMurders', 0) or 0
        bites = organism.get('body.mouth.bibitesBitten', 0) or 0
        eggs_laid = organism.get('body.eggLayer.nEggsLaid', 0) or 0
        size = organism.get('body.d2Size', 0.0) or 0.0
        time_alive = organism.get('clock.timeAlive', 1.0) or 1.0
        energy = organism.get('body.energy', 0.0) or 0.0
        health = organism.get('body.health', 0.0) or 0.0
        
        # Calculate composite metrics
        reproductive_rate = eggs_laid / (time_alive / 3600)  # Eggs per hour
        damage_per_minute = (damage / time_alive) * 60
        fitness_score = eggs_laid + (kills * 2)  # Combined reproductive + combat fitness
        
        organism_data = {
            'species_id': organism.get('genes.speciesID', 'Unknown'),
            'tag': organism.get('genes.tag', 'Unknown'),
            'generation': organism.get('genes.gen', 0),
            'damage': damage,
            'kills': kills,
            'bites': bites,
            'eggs_laid': eggs_laid,
            'size': size,
            'energy': energy,
            'health': health,
            'time_alive': time_alive,
            'reproductive_rate': reproductive_rate,
            'damage_per_minute': damage_per_minute,
            'fitness_score': fitness_score
        }
        
        # Classify organism
        analysis_groups['all'].append(organism_data)
        
        # Maturity classification (size > 1.0)
        if size > 1.0:
            analysis_groups['mature'].append(organism_data)
        
        # Reproductive success
        if eggs_laid > 0:
            analysis_groups['parents'].append(organism_data)
        
        # Combat activity
        if damage > 0 or kills > 0 or bites > 0:
            analysis_groups['fighters'].append(organism_data)
        
        # Successful killers
        if kills > 0:
            analysis_groups['killers'].append(organism_data)
    
    # Analyze correlations in mature organisms only
    mature_organisms = analysis_groups['mature']
    correlations = {}
    
    if len(mature_organisms) > 1:
        # Combat vs reproduction tradeoff analysis
        mature_parents = [org for org in mature_organisms if org['eggs_laid'] > 0]
        mature_fighters = [org for org in mature_organisms if org['damage'] > 0 or org['kills'] > 0]
        
        if mature_parents:
            parent_avg_damage = statistics.mean([p['damage'] for p in mature_parents])
            parent_avg_kills = statistics.mean([p['kills'] for p in mature_parents])
            
            correlations['parental_combat'] = {
                'sample_size': len(mature_parents),
                'avg_damage': parent_avg_damage,
                'avg_kills': parent_avg_kills
            }
            
            # Find top performers in each category
            top_parent = max(mature_parents, key=lambda x: x['eggs_laid'])
            correlations['top_parent'] = top_parent
        
        if mature_fighters:
            fighter_avg_eggs = statistics.mean([f['eggs_laid'] for f in mature_fighters])
            correlations['fighter_reproduction'] = {
                'sample_size': len(mature_fighters),
                'avg_eggs': fighter_avg_eggs
            }
        
        # Generation analysis for evolutionary trends
        if mature_organisms:
            generations = [org['generation'] for org in mature_organisms]
            if len(set(generations)) > 1:
                median_gen = statistics.median(generations)
                high_gen_orgs = [org for org in mature_organisms if org['generation'] >= median_gen]
                low_gen_orgs = [org for org in mature_organisms if org['generation'] < median_gen]
                
                if high_gen_orgs and low_gen_orgs:
                    high_gen_fitness = statistics.mean([org['fitness_score'] for org in high_gen_orgs])
                    low_gen_fitness = statistics.mean([org['fitness_score'] for org in low_gen_orgs])
                    
                    correlations['generational_fitness'] = {
                        'high_gen_fitness': high_gen_fitness,
                        'low_gen_fitness': low_gen_fitness,
                        'improvement': high_gen_fitness > low_gen_fitness,
                        'improvement_percent': ((high_gen_fitness - low_gen_fitness) / low_gen_fitness * 100) 
                                             if low_gen_fitness > 0 else 0
                    }
    
    # Find ecosystem champions across categories
    champions = {}
    if mature_organisms:
        # Top reproducers
        champions['top_reproducers'] = sorted(mature_organisms, 
                                            key=lambda x: x['eggs_laid'], 
                                            reverse=True)[:5]
        
        # Top fighters  
        champions['top_fighters'] = sorted(mature_organisms, 
                                         key=lambda x: x['damage'], 
                                         reverse=True)[:5]
        
        # Top overall fitness
        champions['top_fitness'] = sorted(mature_organisms, 
                                        key=lambda x: x['fitness_score'], 
                                        reverse=True)[:5]
    
    # Population health metrics
    total_mature = len(analysis_groups['mature'])
    total_parents = len(analysis_groups['parents'])
    total_fighters = len(analysis_groups['fighters'])
    
    population_health = {
        'total_mature': total_mature,
        'reproduction_rate': (total_parents / total_mature * 100) if total_mature > 0 else 0,
        'combat_rate': (total_fighters / len(organisms) * 100) if organisms else 0,
        'ecosystem_balance': 'REPRODUCTIVE' if (total_parents / total_mature) > 0.3 else 
                            'COMBATIVE' if (total_fighters / len(organisms)) > 0.3 else 'BALANCED'
    }
    
    return {
        'analysis_groups': analysis_groups,
        'correlations': correlations,
        'champions': champions,
        'population_health': population_health
    }


def run_combat_analysis_from_directory(bibites_dir: Path, 
                                     lineage_filter: str = None,
                                     size_relative: bool = True,
                                     output: Optional[Path] = None) -> Dict:
    """Run comprehensive combat analysis on a bibites directory.
    
    Main entry point for combat analysis that handles data loading and coordinates
    all combat analysis functions.
    
    Args:
        bibites_dir: Path to directory containing .bb8 files
        lineage_filter: Optional specific lineage to focus on
        size_relative: Whether to use size-relative combat metrics
        output: Optional output file for results
        
    Returns:
        Dictionary containing complete combat analysis results
    """
    console.print(f"[green]Starting combat analysis of {bibites_dir}...[/green]")
    
    # Extract combat-relevant fields
    combat_fields = [
        'genes.tag', 'genes.speciesID', 'genes.gen',
        'body.mouth.totalDamageDealt', 'body.mouth.totalMurders', 'body.mouth.bibitesBitten',
        'body.d2Size', 'body.eggLayer.nEggsLaid', 'body.energy', 'body.health',
        'clock.timeAlive', 'body.control.totalTravel'
    ]
    
    try:
        results, errors = process_batch_files(bibites_dir, combat_fields)
        
        if errors:
            console.print(f"[yellow]Warning: {len(errors)} files had extraction errors[/yellow]")
        
        if not results:
            raise ValueError("No organism data extracted for combat analysis")
        
        # Run all combat analysis functions
        combat_effectiveness = calculate_combat_effectiveness(results, size_relative=size_relative)
        predator_patterns = analyze_predator_combat_patterns(results, lineage_filter=lineage_filter)
        reproductive_correlation = combat_reproductive_correlation(results)
        
        # Combine all results
        complete_analysis = {
            'meta': {
                'analysis_type': 'combat_effectiveness',
                'bibites_directory': str(bibites_dir),
                'organism_count': len(results),
                'size_relative': size_relative,
                'lineage_filter': lineage_filter
            },
            'combat_effectiveness': combat_effectiveness,
            'predator_patterns': predator_patterns,
            'reproductive_correlation': reproductive_correlation,
            'errors': errors
        }
        
        # Save output if requested
        if output:
            save_json_output(complete_analysis, output)
            console.print(f"[green]Combat analysis results saved to {output}[/green]")
        
        return complete_analysis
        
    except Exception as e:
        console.print(f"[red]Combat analysis failed: {e}[/red]")
        raise