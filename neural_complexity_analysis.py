#!/usr/bin/env python3
"""
Neural complexity analysis for species comparison
"""
import json
import statistics
from collections import defaultdict

def analyze_neural_data():
    # Load the neural data from our bibites command
    with open('tmp/neural_data.json', 'r') as f:
        neural_data = json.load(f)
    
    species_neural = defaultdict(list)
    
    for organism in neural_data:
        species_id = organism['genes.speciesID']
        tag = organism['genes.tag']
        generation = organism['genes.gen']
        
        # Count nodes and synapses
        nodes = organism.get('brain.Nodes', [])
        synapses = organism.get('brain.Synapses', [])
        
        node_count = len(nodes) if nodes else 0
        synapse_count = len(synapses) if synapses else 0
        
        species_neural[species_id].append({
            'tag': tag,
            'generation': generation,
            'node_count': node_count,
            'synapse_count': synapse_count,
            'complexity_ratio': synapse_count / max(node_count, 1)  # Avoid division by zero
        })
    
    # Analyze by species
    print("Neural Complexity Analysis by Species")
    print("=" * 60)
    
    for species_id in sorted(species_neural.keys()):
        organisms = species_neural[species_id]
        tag = organisms[0]['tag']  # All should have same tag
        
        node_counts = [o['node_count'] for o in organisms]
        synapse_counts = [o['synapse_count'] for o in organisms]
        complexity_ratios = [o['complexity_ratio'] for o in organisms]
        generations = [o['generation'] for o in organisms]
        
        print(f"\nSpecies {species_id} ({tag}) - {len(organisms)} organisms")
        print(f"  Generations: {min(generations)}-{max(generations)}")
        print(f"  Nodes: {statistics.mean(node_counts):.1f} ± {statistics.stdev(node_counts) if len(node_counts) > 1 else 0:.1f}")
        print(f"  Synapses: {statistics.mean(synapse_counts):.1f} ± {statistics.stdev(synapse_counts) if len(synapse_counts) > 1 else 0:.1f}")
        print(f"  Complexity (synapses/nodes): {statistics.mean(complexity_ratios):.2f} ± {statistics.stdev(complexity_ratios) if len(complexity_ratios) > 1 else 0:.2f}")

if __name__ == "__main__":
    analyze_neural_data()