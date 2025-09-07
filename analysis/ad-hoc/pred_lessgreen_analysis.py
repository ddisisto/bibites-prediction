#!/usr/bin/env python3
"""
Analysis of the new Pred.lessgreen lineage - color genetics and evolution patterns
"""
import json
import statistics
from collections import defaultdict

def analyze_pred_lessgreen():
    # Load the latest color data
    with open('tmp/latest_color_data.json', 'r') as f:
        color_data = json.load(f)
    
    # Separate species for analysis
    pred_lessgreen = []
    pred_regular = []
    greencreep = []
    
    for organism in color_data:
        tag = organism['genes.tag']
        if tag == 'Pred.lessgreen':
            pred_lessgreen.append(organism)
        elif tag == 'Pred':
            pred_regular.append(organism)
        elif tag == 'Greencreep':
            greencreep.append(organism)
    
    print("🎯 PRED.LESSGREEN LINEAGE ANALYSIS")
    print("=" * 70)
    print(f"Population: {len(pred_lessgreen)} organisms (Species ID: {pred_lessgreen[0]['genes.speciesID']})")
    
    # Color analysis
    red_values = [o['genes.genes.ColorR'] for o in pred_lessgreen]
    green_values = [o['genes.genes.ColorG'] for o in pred_lessgreen]
    blue_values = [o['genes.genes.ColorB'] for o in pred_lessgreen]
    generations = [o['genes.gen'] for o in pred_lessgreen]
    
    print(f"\nGeneration Range: {min(generations)} - {max(generations)}")
    print(f"Color Profile:")
    print(f"  🔴 Red:   {statistics.mean(red_values):.3f} (range: {min(red_values):.3f} - {max(red_values):.3f})")
    print(f"  🟢 Green: {statistics.mean(green_values):.3f} (range: {min(green_values):.3f} - {max(green_values):.3f})")
    print(f"  🔵 Blue:  {statistics.mean(blue_values):.3f} (range: {min(blue_values):.3f} - {max(blue_values):.3f})")
    
    # Compare to regular Pred
    pred_red = [o['genes.genes.ColorR'] for o in pred_regular]
    pred_green = [o['genes.genes.ColorG'] for o in pred_regular]
    pred_blue = [o['genes.genes.ColorB'] for o in pred_regular]
    
    print(f"\nCOMPARISON TO REGULAR PRED ({len(pred_regular)} organisms):")
    print(f"  Pred Regular Green: {statistics.mean(pred_green):.3f}")
    print(f"  Pred.lessgreen Green: {statistics.mean(green_values):.3f}")
    print(f"  💡 Green Reduction: {statistics.mean(pred_green) - statistics.mean(green_values):.3f}")
    
    # Compare to Greencreep
    gc_green = [o['genes.genes.ColorG'] for o in greencreep]
    print(f"\n  Greencreep Green: {statistics.mean(gc_green):.3f}")
    print(f"  💡 Differentiation from Greencreep: {abs(statistics.mean(green_values) - statistics.mean(gc_green)):.3f}")
    
    # Color phenotype assessment
    avg_color = (statistics.mean(red_values), statistics.mean(green_values), statistics.mean(blue_values))
    print(f"\n🎨 PHENOTYPE ASSESSMENT:")
    print(f"  Average RGB: ({avg_color[0]:.3f}, {avg_color[1]:.3f}, {avg_color[2]:.3f})")
    
    if avg_color[0] > 0.5 and avg_color[1] > 0.5 and avg_color[2] > 0.5:
        print(f"  Phenotype: 🤍 GREYISH/NEUTRAL (reduced green advantage)")
    elif avg_color[1] > max(avg_color[0], avg_color[2]):
        print(f"  Phenotype: 🟢 GREEN-DOMINANT (still has green advantage)")
    elif avg_color[0] > avg_color[1]:
        print(f"  Phenotype: 🔴 RED-SHIFTED (potential kin-killing mode)")
    else:
        print(f"  Phenotype: 🔵 BLUE-SHIFTED")
    
    # Evolution tracking
    gen_color_map = defaultdict(list)
    for organism in pred_lessgreen:
        gen = organism['genes.gen']
        gen_color_map[gen].append((
            organism['genes.genes.ColorR'],
            organism['genes.genes.ColorG'], 
            organism['genes.genes.ColorB']
        ))
    
    print(f"\n📈 GENERATIONAL EVOLUTION:")
    for gen in sorted(gen_color_map.keys()):
        colors = gen_color_map[gen]
        avg_r = statistics.mean([c[0] for c in colors])
        avg_g = statistics.mean([c[1] for c in colors])
        avg_b = statistics.mean([c[2] for c in colors])
        print(f"  Gen {gen:2d}: R={avg_r:.3f}, G={avg_g:.3f}, B={avg_b:.3f} ({len(colors)} organisms)")
    
    # Survival assessment
    print(f"\n⚔️ SURVIVAL ASSESSMENT:")
    print(f"  Population: {len(pred_lessgreen)} organisms (15.5% of ecosystem)")
    if len(pred_lessgreen) > 10:
        print(f"  Status: 🟢 THRIVING - Population above critical mass")
        print(f"  Prediction: Likely to establish as permanent lineage")
    elif len(pred_lessgreen) > 5:
        print(f"  Status: 🟡 STRUGGLING - Marginal population")
        print(f"  Prediction: Evolution pressure will determine survival")
    else:
        print(f"  Status: 🔴 ENDANGERED - Critical population")
        print(f"  Prediction: High extinction risk")
    
    # Strategic implications
    print(f"\n🧠 STRATEGIC IMPLICATIONS:")
    green_diff = statistics.mean(pred_green) - statistics.mean(green_values)
    if green_diff > 0.3:
        print(f"  • SIGNIFICANT green reduction achieved ({green_diff:.3f})")
        print(f"  • May break convergent green evolution pattern")
        print(f"  • Potential for kin-killing if green detection damaged")
    elif green_diff > 0.1:
        print(f"  • MODERATE green reduction ({green_diff:.3f})")
        print(f"  • May provide selective advantage in green-saturated ecosystem")
    else:
        print(f"  • MINIMAL green reduction ({green_diff:.3f})")
        print(f"  • May not break existing convergent evolution patterns")

if __name__ == "__main__":
    analyze_pred_lessgreen()