"""
bibites_analysis.py - Analysis orchestration for bibites ecosystem analysis.

Orchestrates all analysis operations by delegating to existing extract_data.py modules:
- Population and species analysis
- Spatial distribution analysis  
- Cross-cycle comparison analysis
- Field extraction and species comparison
- Metadata analysis coordination

This module provides high-level analysis runners that coordinate the existing 
specialized analysis modules.
"""

from pathlib import Path
from typing import Optional, List, Tuple
from rich.console import Console

# Import analysis modules from extract_data.py  
from .field_extraction import process_batch_files, extract_species_field
from .population_analysis import generate_species_summary
from .spatial_analysis import generate_spatial_analysis
from .comparison_tools import compare_cycle_directories, compare_specific_species
from .combat_analysis import run_combat_analysis_from_directory
from .behavioral_analysis import (
    analyze_pheromone_patterns, calculate_neural_complexity, 
    classify_behavioral_strategies, display_behavioral_analysis_results
)
from .output_formatters import display_table, display_json, display_csv, save_json_output

# Import metadata extraction from extract_metadata.py
from ..extract_metadata import extract_metadata_from_save, display_metadata_results, MetadataExtractionError

# Import data access functions
from .bibites_data import get_zip_file_from_data_path, BibitesDataError

console = Console()

class BibitesAnalysisError(Exception):
    """Raised when analysis operation fails."""
    pass

def run_population_analysis(data_paths: List[Path], output: Optional[Path], 
                           by_species: bool, quick_mode: bool = True) -> None:
    """Run population/species summary analysis."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Population analysis requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    generate_species_summary(bibites_dir, output, quick_mode=quick_mode, use_species_id=by_species)

def run_spatial_analysis(data_paths: List[Path], output: Optional[Path]) -> None:
    """Run spatial distribution analysis."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Spatial analysis requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    generate_spatial_analysis(bibites_dir, output)

def run_comparison_analysis(data_paths: List[Path], output: Optional[Path]) -> None:
    """Run population comparison between cycles."""
    if len(data_paths) != 2:
        raise BibitesAnalysisError("Comparison analysis requires exactly two datasets (use --last 2)")
    
    # Order matters: newer first, older second for proper comparison direction
    bibites_dir_a = data_paths[0] / 'bibites'  # More recent
    bibites_dir_b = data_paths[1] / 'bibites'  # Older
    
    if not bibites_dir_a.exists():
        raise BibitesAnalysisError(f"First dataset bibites directory not found: {bibites_dir_a}")
    if not bibites_dir_b.exists():
        raise BibitesAnalysisError(f"Second dataset bibites directory not found: {bibites_dir_b}")
    
    compare_cycle_directories(bibites_dir_a, bibites_dir_b, output)

def run_metadata_analysis(data_paths: List[Path], output_dir: Optional[Path] = None) -> None:
    """Run ecosystem metadata analysis."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Metadata analysis requires exactly one dataset (use --latest or --name)")
    
    try:
        # Find the original zip file from the data path
        zip_file = get_zip_file_from_data_path(data_paths[0])
        
        temp_dir = output_dir if output_dir else Path('./tmp')
        temp_dir.mkdir(exist_ok=True)
        
        metadata = extract_metadata_from_save(zip_file, temp_dir, extract_raw=False)
        display_metadata_results(metadata)
        
    except (BibitesDataError, MetadataExtractionError) as e:
        raise BibitesAnalysisError(f"Metadata extraction failed: {e}")

def run_field_extraction(data_paths: List[Path], fields: str, batch: bool, 
                        output: Optional[Path], format: str) -> None:
    """Run field extraction analysis."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Field extraction requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    field_paths = [f.strip() for f in fields.split(',')]
    
    if batch:
        # Batch processing
        try:
            results, errors = process_batch_files(bibites_dir, field_paths)
        except ValueError as e:
            raise BibitesAnalysisError(f"Field extraction failed: {e}")
        
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
        raise BibitesAnalysisError("Single file field extraction not supported in unified tool. Use --batch for directory processing.")

def run_species_field_extraction(data_paths: List[Path], output: Optional[Path]) -> None:
    """Extract species ID fields for species name mapping."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Species field extraction requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    extract_species_field(bibites_dir, output)

def run_species_comparison(data_paths: List[Path], species_a: int, species_b: int, 
                          output: Optional[Path]) -> None:
    """Compare two specific species by their sim-generated species ID."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Species comparison requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    compare_specific_species(bibites_dir, species_a, species_b, output)

def run_combat_analysis(data_paths: List[Path], lineage: Optional[str], 
                       size_relative: bool, output: Optional[Path]) -> None:
    """Run comprehensive combat effectiveness analysis."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Combat analysis requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    try:
        results = run_combat_analysis_from_directory(
            bibites_dir, 
            lineage_filter=lineage,
            size_relative=size_relative,
            output=output
        )
        
        # Display key results to console
        if results and 'combat_effectiveness' in results:
            combat_data = results['combat_effectiveness']
            summary = combat_data.get('summary', {})
            
            console.print(f"\n[green]⚔️ COMBAT EFFECTIVENESS ANALYSIS[/green]")
            console.print(f"📊 Total organisms: {summary.get('total_organisms', 0)}")
            console.print(f"⚔️ Active combatants: {summary.get('total_combatants', 0)} ({summary.get('combat_participation_rate', 0):.1f}%)")
            console.print(f"💀 Successful killers: {summary.get('total_killers', 0)} ({summary.get('kill_rate', 0):.1f}%)")
            console.print(f"🧬 Mature organisms: {summary.get('mature_combatants', 0)}")
            
            # Show insights
            insights = combat_data.get('insights', [])
            if insights:
                console.print(f"\n[blue]💡 KEY INSIGHTS:[/blue]")
                for insight in insights[:5]:  # Limit to top 5 insights
                    console.print(f"  {insight}")
            
            # Show top performers
            top_performers = combat_data.get('top_performers', {})
            if top_performers.get('combat_fitness'):
                console.print(f"\n[yellow]🏆 TOP COMBAT PERFORMERS:[/yellow]")
                for i, performer in enumerate(top_performers['combat_fitness'][:3], 1):
                    console.print(f"  {i}. {performer['tag']} (Species {performer['species_id']}, Gen {performer['generation']})")
                    console.print(f"     Combat fitness: {performer['combat_fitness']:.1f}, Size: {performer['size']:.2f}")
                    console.print(f"     {performer['damage']:.1f} damage, {performer['kills']} kills, {performer['eggs_laid']} eggs")
        
    except Exception as e:
        raise BibitesAnalysisError(f"Combat analysis failed: {e}")


def run_behavioral_analysis(data_paths: List[Path], pheromone_focus: str, 
                           neural_complexity_only: bool, by_species: bool, 
                           output: Optional[Path]) -> None:
    """Run comprehensive behavioral analysis including pheromone patterns and neural complexity."""
    if len(data_paths) != 1:
        raise BibitesAnalysisError("Behavioral analysis requires exactly one dataset (use --latest or --name)")
    
    bibites_dir = data_paths[0] / 'bibites'
    if not bibites_dir.exists():
        raise BibitesAnalysisError(f"Bibites directory not found: {bibites_dir}")
    
    try:
        # Extract the organism data with neural and genetic information
        console.print("[blue]Extracting behavioral data from organisms...[/blue]")
        
        # We need specific fields for behavioral analysis
        behavioral_fields = [
            'genes.speciesID', 'genes.tag', 'genes.gen',
            'brain.Nodes', 'brain.Synapses', 'brain.InputNodes', 'brain.OutputNodes'
        ]
        
        organisms_data, errors = process_batch_files(
            directory_path=bibites_dir,
            field_paths=behavioral_fields
        )
        
        if errors:
            console.print(f"[yellow]Warning: {len(errors)} files had parsing errors[/yellow]")
            
        if not organisms_data:
            console.print("[red]No organism data found for behavioral analysis[/red]")
            return
        
        console.print(f"[green]Loaded {len(organisms_data)} organisms for behavioral analysis[/green]")
        
        # Initialize results dictionary
        analysis_results = {}
        
        # Run neural complexity analysis (always included)
        console.print("\n[blue]Analyzing neural complexity patterns...[/blue]")
        neural_results = calculate_neural_complexity(organisms_data)
        analysis_results['neural_complexity'] = neural_results
        display_behavioral_analysis_results(neural_results, "neural")
        
        # Run pheromone analysis (unless neural-only mode)
        if not neural_complexity_only:
            console.print(f"\n[blue]Analyzing {pheromone_focus} pheromone patterns...[/blue]")
            pheromone_results = analyze_pheromone_patterns(organisms_data, focus_color=pheromone_focus)
            analysis_results['pheromone_patterns'] = pheromone_results
            display_behavioral_analysis_results(pheromone_results, "pheromone")
            
            # Run behavioral strategy classification (combines both analyses)
            console.print(f"\n[blue]Classifying behavioral strategies...[/blue]")
            strategy_results = classify_behavioral_strategies(organisms_data)
            analysis_results['behavioral_strategies'] = strategy_results
            display_behavioral_analysis_results(strategy_results, "strategy")
        
        # Save results to output file if requested
        if output:
            console.print(f"\n[blue]Saving behavioral analysis results to {output}[/blue]")
            save_json_output(analysis_results, output)
            
        # Summary insights
        console.print(f"\n[bold green]Behavioral Analysis Summary:[/bold green]")
        total_species = neural_results['summary_stats']['species_count']
        total_organisms = neural_results['summary_stats']['total_organisms']
        console.print(f"  • Analyzed {total_organisms} organisms across {total_species} species")
        
        if neural_results['complexity_rankings']:
            top_complex = neural_results['complexity_rankings'][0]
            console.print(f"  • Most complex species: {top_complex['tag']} (complexity ratio: {top_complex['avg_complexity']:.2f})")
        
        if not neural_complexity_only and 'pheromone_patterns' in analysis_results:
            phero_summary = analysis_results['pheromone_patterns']['summary_stats']
            emitter_count = phero_summary['emitter_species_count']
            detector_count = phero_summary['detector_species_count']
            console.print(f"  • {pheromone_focus.capitalize()} pheromone: {emitter_count} emitter species, {detector_count} detector species")
            
            if 'behavioral_strategies' in analysis_results:
                strategy_summary = analysis_results['behavioral_strategies']['strategy_summary']
                for strategy_name, info in strategy_summary.items():
                    if info['count'] > 0:
                        console.print(f"  • {strategy_name.replace('_', ' ').title()}: {info['count']} species")
        
    except Exception as e:
        raise BibitesAnalysisError(f"Behavioral analysis failed: {e}")