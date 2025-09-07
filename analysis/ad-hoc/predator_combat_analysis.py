#!/usr/bin/env python3
"""
Combat effectiveness analysis for different predator lineages
"""
import json
import statistics
from collections import defaultdict

def analyze_combat_effectiveness():
    # Load combat data
    with open('tmp/combat_data.json', 'r') as f:
        combat_data = json.load(f)
    
    # Group by predator lineages
    lineage_combat = {
        'Pred': [],
        'Pred.lessgreen': [],
        'Greencreep': [],  # Surprising predators
        'Prey.Basic': [],  # Unexpected predators
        'Other': []
    }
    
    for organism in combat_data:
        tag = organism['genes.tag']
        species_id = organism['genes.speciesID']
        generation = organism['genes.gen']
        
        damage = organism.get('body.mouth.totalDamageDealt', 0.0) or 0.0
        kills = organism.get('body.mouth.totalMurders', 0) or 0
        bites = organism.get('body.mouth.bibitesBitten', 0) or 0
        murdered_area = organism.get('body.mouth.murderedArea', 0.0) or 0.0
        time_alive = organism.get('clock.timeAlive', 1.0) or 1.0  # Avoid division by zero
        
        combat_info = {
            'species_id': species_id,
            'generation': generation,
            'damage': damage,
            'kills': kills,
            'bites': bites,
            'murdered_area': murdered_area,
            'time_alive': time_alive,
            'damage_per_minute': (damage / time_alive) * 60,  # Damage rate
            'kill_efficiency': kills / max(damage, 1),  # Kills per damage
            'bite_accuracy': kills / max(bites, 1)  # Kill rate per bite
        }
        
        # Classify organism
        if tag == 'Pred':
            lineage_combat['Pred'].append(combat_info)
        elif tag == 'Pred.lessgreen':
            lineage_combat['Pred.lessgreen'].append(combat_info)
        elif tag == 'Greencreep':
            lineage_combat['Greencreep'].append(combat_info)
        elif tag == 'Prey.Basic':
            lineage_combat['Prey.Basic'].append(combat_info)
        else:
            lineage_combat['Other'].append(combat_info)
    
    print("⚔️  PREDATOR COMBAT EFFECTIVENESS ANALYSIS")
    print("=" * 80)
    
    # Find top performers overall
    all_combatants = []
    for lineage, organisms in lineage_combat.items():
        for org in organisms:
            org['lineage'] = lineage
            all_combatants.append(org)
    
    # Sort by total damage dealt
    top_damage_dealers = sorted(all_combatants, key=lambda x: x['damage'], reverse=True)[:10]
    
    print("\n🏆 TOP 10 DAMAGE DEALERS (All Lineages):")
    for i, combatant in enumerate(top_damage_dealers, 1):
        print(f"  {i:2d}. {combatant['lineage']} (Species {combatant['species_id']}, Gen {combatant['generation']})")
        print(f"      💥 {combatant['damage']:.1f} damage, {combatant['kills']} kills, {combatant['bites']} bites")
        print(f"      📈 {combatant['damage_per_minute']:.2f} dmg/min, {combatant['bite_accuracy']:.2f} kill/bite ratio")
    
    # Analyze each lineage
    print("\n" + "=" * 80)
    print("LINEAGE-BY-LINEAGE COMBAT ANALYSIS")
    print("=" * 80)
    
    for lineage, organisms in lineage_combat.items():
        if not organisms:
            continue
            
        # Filter active combatants (those with any combat activity)
        active_combatants = [o for o in organisms if o['damage'] > 0 or o['kills'] > 0 or o['bites'] > 0]
        total_organisms = len(organisms)
        active_count = len(active_combatants)
        
        if active_count == 0:
            print(f"\n🛡️  {lineage.upper()}: {total_organisms} organisms")
            print(f"      Status: PACIFIST - No combat activity detected")
            continue
        
        # Calculate statistics for active combatants
        damages = [o['damage'] for o in active_combatants]
        kills = [o['kills'] for o in active_combatants]
        bites = [o['bites'] for o in active_combatants]
        damage_rates = [o['damage_per_minute'] for o in active_combatants]
        
        total_damage = sum(damages)
        total_kills = sum(kills)
        total_bites = sum(bites)
        
        print(f"\n⚔️  {lineage.upper()}: {total_organisms} organisms ({active_count} combatants)")
        print(f"      Combat Participation: {(active_count/total_organisms)*100:.1f}%")
        print(f"      Total Stats: {total_damage:.1f} damage, {total_kills} kills, {total_bites} bites")
        
        if active_combatants:
            print(f"      Per-Combatant Avg: {statistics.mean(damages):.1f} dmg, {statistics.mean(kills):.1f} kills")
            print(f"      Damage Rate: {statistics.mean(damage_rates):.2f} ± {statistics.stdev(damage_rates) if len(damage_rates) > 1 else 0:.2f} dmg/min")
            
            # Find top performer in this lineage
            top_performer = max(active_combatants, key=lambda x: x['damage'])
            print(f"      Top Performer: Species {top_performer['species_id']} (Gen {top_performer['generation']})")
            print(f"        {top_performer['damage']:.1f} dmg, {top_performer['kills']} kills, {top_performer['damage_per_minute']:.2f} dmg/min")
    
    # Comparative analysis
    print("\n" + "=" * 80)
    print("COMPARATIVE LINEAGE EFFECTIVENESS")
    print("=" * 80)
    
    # Compare Pred vs Pred.lessgreen specifically
    pred_active = [o for o in lineage_combat['Pred'] if o['damage'] > 0 or o['kills'] > 0]
    predless_active = [o for o in lineage_combat['Pred.lessgreen'] if o['damage'] > 0 or o['kills'] > 0]
    
    if pred_active and predless_active:
        pred_avg_damage = statistics.mean([o['damage'] for o in pred_active])
        predless_avg_damage = statistics.mean([o['damage'] for o in predless_active])
        
        pred_participation = len(pred_active) / len(lineage_combat['Pred'])
        predless_participation = len(predless_active) / len(lineage_combat['Pred.lessgreen'])
        
        print(f"\n🎯 PRED vs PRED.LESSGREEN HEAD-TO-HEAD:")
        print(f"   Regular Pred:")
        print(f"     Combat Participation: {pred_participation:.1%}")
        print(f"     Avg Damage (active): {pred_avg_damage:.1f}")
        print(f"     Total Kills: {sum([o['kills'] for o in pred_active])}")
        
        print(f"   Pred.lessgreen:")
        print(f"     Combat Participation: {predless_participation:.1%}")
        print(f"     Avg Damage (active): {predless_avg_damage:.1f}")
        print(f"     Total Kills: {sum([o['kills'] for o in predless_active])}")
        
        if pred_avg_damage > predless_avg_damage:
            advantage = ((pred_avg_damage - predless_avg_damage) / predless_avg_damage) * 100
            print(f"   🏆 ADVANTAGE: Regular Pred (+{advantage:.1f}% damage)")
        else:
            advantage = ((predless_avg_damage - pred_avg_damage) / pred_avg_damage) * 100
            print(f"   🏆 ADVANTAGE: Pred.lessgreen (+{advantage:.1f}% damage)")
    
    # Surprising findings
    greencreep_active = [o for o in lineage_combat['Greencreep'] if o['damage'] > 0 or o['kills'] > 0]
    prey_active = [o for o in lineage_combat['Prey.Basic'] if o['damage'] > 0 or o['kills'] > 0]
    
    if greencreep_active:
        print(f"\n🚨 SURPRISE: GREENCREEP PREDATORS DETECTED!")
        print(f"     {len(greencreep_active)} Greencreep organisms showing predatory behavior")
        print(f"     Total damage: {sum([o['damage'] for o in greencreep_active]):.1f}")
        print(f"     Total kills: {sum([o['kills'] for o in greencreep_active])}")
    
    if prey_active:
        print(f"\n🚨 SURPRISE: PREY.BASIC PREDATORS DETECTED!")
        print(f"     {len(prey_active)} Prey.Basic organisms showing predatory behavior")
        print(f"     Total damage: {sum([o['damage'] for o in prey_active]):.1f}")
        print(f"     Total kills: {sum([o['kills'] for o in prey_active])}")
        print(f"     💡 These may be your 'kin-killing' organisms!")
    
    print(f"\n📊 ECOSYSTEM COMBAT SUMMARY:")
    total_active = sum(len([o for o in organisms if o['damage'] > 0 or o['kills'] > 0]) 
                      for organisms in lineage_combat.values())
    total_organisms = sum(len(organisms) for organisms in lineage_combat.values())
    
    print(f"     Total organisms: {total_organisms}")
    print(f"     Active combatants: {total_active} ({(total_active/total_organisms)*100:.1f}%)")
    print(f"     Combat intensity: {'HIGH' if total_active/total_organisms > 0.15 else 'MODERATE' if total_active/total_organisms > 0.05 else 'LOW'}")

if __name__ == "__main__":
    analyze_combat_effectiveness()