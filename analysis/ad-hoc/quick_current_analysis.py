#!/usr/bin/env python3
"""
Quick analysis of current ecosystem state
"""
import json
import statistics
from collections import defaultdict

def quick_analysis():
    with open('tmp/current_ecosystem.json', 'r') as f:
        data = json.load(f)
    
    # Group by lineage
    lineages = defaultdict(list)
    for org in data:
        tag = org['genes.tag']
        lineages[tag].append({
            'damage': org.get('body.mouth.totalDamageDealt', 0) or 0,
            'kills': org.get('body.mouth.totalMurders', 0) or 0,
            'eggs': org.get('body.eggLayer.nEggsLaid', 0) or 0,
            'size': org.get('body.d2Size', 0) or 0,
            'generation': org.get('genes.gen', 0) or 0,
            'species': org.get('genes.speciesID', 0) or 0
        })
    
    print("🚀 CURRENT ECOSYSTEM ANALYSIS")
    print("=" * 60)
    
    for tag, orgs in lineages.items():
        if tag not in ['Pred', 'Pred.lessgreen', 'Greencreep']:
            continue
            
        print(f"\n{tag.upper()}: {len(orgs)} organisms")
        
        # Combat stats
        combatants = [o for o in orgs if o['damage'] > 0 or o['kills'] > 0]
        if combatants:
            avg_damage = statistics.mean([c['damage'] for c in combatants])
            total_kills = sum([c['kills'] for c in combatants])
            combat_rate = len(combatants) / len(orgs) * 100
            print(f"  Combat: {len(combatants)} active ({combat_rate:.1f}%)")
            print(f"  Avg damage: {avg_damage:.1f}, Total kills: {total_kills}")
        
        # Size-relative efficiency for mature organisms
        mature = [o for o in orgs if o['size'] > 0.3]
        if mature:
            avg_size = statistics.mean([m['size'] for m in mature])
            mature_combatants = [m for m in mature if m['damage'] > 0]
            if mature_combatants:
                size_eff = [c['damage'] / max(c['size'], 0.01) for c in mature_combatants]
                avg_efficiency = statistics.mean(size_eff)
                print(f"  Size efficiency: {avg_efficiency:.1f} dmg/size")
        
        # Reproductive success
        parents = [o for o in orgs if o['eggs'] > 0]
        if parents:
            total_eggs = sum([p['eggs'] for p in parents])
            print(f"  Reproduction: {len(parents)} parents, {total_eggs} total eggs")
        
        # Generation spread
        gens = [o['generation'] for o in orgs]
        if gens:
            print(f"  Generations: {min(gens)}-{max(gens)}")
    
    # Top performers
    all_orgs = []
    for tag, orgs in lineages.items():
        for org in orgs:
            org['tag'] = tag
            all_orgs.append(org)
    
    # Top damage dealers (size-adjusted)
    combatants = [o for o in all_orgs if o['damage'] > 0 and o['size'] > 0.1]
    if combatants:
        for c in combatants:
            c['size_eff'] = c['damage'] / c['size']
        
        top_eff = sorted(combatants, key=lambda x: x['size_eff'], reverse=True)[:5]
        print(f"\n🏆 TOP 5 EFFICIENCY CHAMPIONS:")
        for i, org in enumerate(top_eff, 1):
            print(f"  {i}. {org['tag']} (Gen {org['generation']})")
            print(f"     {org['size_eff']:.1f} dmg/size, {org['damage']:.1f} dmg, {org['kills']} kills")

if __name__ == "__main__":
    quick_analysis()