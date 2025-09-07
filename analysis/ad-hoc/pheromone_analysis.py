#!/usr/bin/env python3
"""
Pheromone emission and detection analysis across species
Focuses on red pheromone (PheroOut1/PheroSense1) patterns
"""
import json
import statistics
from collections import defaultdict

def analyze_pheromone_data():
    # Load the neural data
    with open('tmp/pheromone_neural_data.json', 'r') as f:
        neural_data = json.load(f)
    
    species_pheromone = defaultdict(list)
    
    for organism in neural_data:
        species_id = organism['genes.speciesID']
        tag = organism['genes.tag']
        generation = organism['genes.gen']
        
        # Extract pheromone-related nodes
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
        
        # Find pheromone nodes
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
        
        species_pheromone[species_id].append(pheromone_data)
    
    # Analyze by species
    print("🔴 RED PHEROMONE EMISSION & DETECTION ANALYSIS")
    print("=" * 80)
    
    red_emitters = []
    red_detectors = []
    
    for species_id in sorted(species_pheromone.keys()):
        organisms = species_pheromone[species_id]
        tag = organisms[0]['tag']  # All should have same tag
        
        red_emissions = [o['phero_out_1'] for o in organisms]
        red_detections = [o['phero_sense_1'] for o in organisms]
        green_emissions = [o['phero_out_2'] for o in organisms]
        blue_emissions = [o['phero_out_3'] for o in organisms]
        
        generations = [o['generation'] for o in organisms]
        
        avg_red_emission = statistics.mean(red_emissions)
        avg_red_detection = statistics.mean(red_detections)
        max_red_emission = max(red_emissions)
        
        print(f"\nSpecies {species_id} ({tag}) - {len(organisms)} organisms, Gen {min(generations)}-{max(generations)}")
        print(f"  🔴 Red Emission:  Avg {avg_red_emission:.3f}, Max {max_red_emission:.3f}")
        print(f"  🔴 Red Detection: Avg {avg_red_detection:.3f}")
        
        if max_red_emission > 0.1:  # Significant red pheromone emission
            red_emitters.append({
                'species': species_id,
                'tag': tag,
                'avg_emission': avg_red_emission,
                'max_emission': max_red_emission,
                'count': len(organisms)
            })
            print(f"  ⚠️  RED PHEROMONE EMITTER DETECTED!")
        
        if avg_red_detection > 0.1:  # Significant red pheromone detection
            red_detectors.append({
                'species': species_id,
                'tag': tag,
                'avg_detection': avg_red_detection,
                'count': len(organisms)
            })
            print(f"  👁️  Red pheromone detector")
        
        # Show other pheromones for comparison
        if statistics.mean(green_emissions) > 0.01:
            print(f"  🟢 Green Emission: Avg {statistics.mean(green_emissions):.3f}")
        if statistics.mean(blue_emissions) > 0.01:
            print(f"  🔵 Blue Emission:  Avg {statistics.mean(blue_emissions):.3f}")
    
    # Summary analysis
    print("\n" + "=" * 80)
    print("SUMMARY: RED PHEROMONE CONTAMINATION ANALYSIS")
    print("=" * 80)
    
    if red_emitters:
        print(f"\n⚠️  RED PHEROMONE EMITTERS FOUND: {len(red_emitters)} species")
        for emitter in sorted(red_emitters, key=lambda x: x['max_emission'], reverse=True):
            print(f"  • Species {emitter['species']} ({emitter['tag']}): "
                  f"{emitter['max_emission']:.3f} max emission, {emitter['count']} organisms")
    else:
        print("\n✅ NO SIGNIFICANT RED PHEROMONE EMISSION DETECTED")
    
    if red_detectors:
        print(f"\n👁️  RED PHEROMONE DETECTORS: {len(red_detectors)} species")
        for detector in sorted(red_detectors, key=lambda x: x['avg_detection'], reverse=True):
            print(f"  • Species {detector['species']} ({detector['tag']}): "
                  f"{detector['avg_detection']:.3f} avg detection, {detector['count']} organisms")
    
    # Strategic recommendations
    print("\n" + "=" * 80)
    print("STRATEGIC RECOMMENDATIONS")
    print("=" * 80)
    
    if red_emitters:
        print("\n🎯 DIRECT INTERVENTION NEEDED:")
        print("  • Red pheromone emission detected in ecosystem")
        print("  • Manual savefile engineering required (similar to color tower approach)")
        print("  • Target species for PheroOut1 neuron suppression:")
        
        for emitter in red_emitters:
            if emitter['tag'] in ['Greencreep', 'Pred']:
                print(f"    - {emitter['tag']} Species {emitter['species']}: {emitter['count']} organisms")
        
        print("\n💡 ENGINEERING APPROACHES:")
        print("  1. PheroOut1 baseActivation → negative value (suppress red emission)")
        print("  2. Sever synaptic connections to PheroOut1 neurons")
        print("  3. Add inhibitory synapses targeting PheroOut1")
        print("  4. Implement 'red pheromone tower' - automatic suppression like color selection")
    else:
        print("\n✅ NO DIRECT INTERVENTION REQUIRED")
        print("  • No significant red pheromone emission detected")
        print("  • Current ecosystem already achieving red pheromone avoidance")

if __name__ == "__main__":
    analyze_pheromone_data()