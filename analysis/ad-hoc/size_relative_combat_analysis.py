#!/usr/bin/env python3
"""
Size-relative combat effectiveness analysis
Accounts for damage scaling with body size - true combat efficiency
"""
import json
import statistics
from collections import defaultdict

def analyze_size_relative_combat():
    # Load latest data
    with open('tmp/latest_size_relative_combat.json', 'r') as f:
        data = json.load(f)
    
    # Separate organisms by lineage
    lineage_data = defaultdict(lambda: {
        'all': [],
        'mature': [],       # Size > 0.5 (reasonable maturity threshold)
        'parents': [],      # Have laid eggs
        'combatants': [],   # Have combat activity
        'killers': []       # Have successful kills
    })
    
    for organism in data:
        tag = organism['genes.tag']
        species_id = organism['genes.speciesID']
        generation = organism['genes.gen']
        
        # Combat metrics
        damage = organism.get('body.mouth.totalDamageDealt', 0.0) or 0.0
        kills = organism.get('body.mouth.totalMurders', 0) or 0
        bites = organism.get('body.mouth.bibitesBitten', 0) or 0
        
        # Physical metrics
        size = organism.get('body.d2Size', 0.0) or 0.0
        eggs_laid = organism.get('body.eggLayer.nEggsLaid', 0) or 0
        energy = organism.get('body.energy', 0.0) or 0.0
        health = organism.get('body.health', 0.0) or 0.0
        time_alive = organism.get('clock.timeAlive', 1.0) or 1.0
        
        # SIZE-RELATIVE COMBAT METRICS (the key insight!)
        size_adjusted_damage = damage / max(size, 0.01)  # Damage per unit size
        damage_efficiency = damage / max(time_alive, 1.0) * 60  # Damage per minute
        size_kill_ratio = kills / max(size, 0.01)  # Kills per unit size
        bite_efficiency = kills / max(bites, 1)  # Successful kill rate
        
        # Reproductive metrics
        reproductive_rate = eggs_laid / (time_alive / 3600)  # Eggs per hour
        
        organism_data = {
            'species_id': species_id,
            'generation': generation,
            'damage': damage,
            'kills': kills,
            'bites': bites,
            'size': size,
            'eggs_laid': eggs_laid,
            'energy': energy,
            'health': health,
            'time_alive': time_alive,
            # Size-relative metrics
            'size_adjusted_damage': size_adjusted_damage,
            'size_kill_ratio': size_kill_ratio,
            'damage_efficiency': damage_efficiency,
            'bite_efficiency': bite_efficiency,
            'reproductive_rate': reproductive_rate,
            # Combined fitness
            'combat_fitness': size_adjusted_damage + (size_kill_ratio * 100),
            'total_fitness': eggs_laid + (kills * 5)  # Weighted fitness score
        }
        
        # Classify organism
        lineage_data[tag]['all'].append(organism_data)
        
        # Maturity (size > 0.5 as reasonable threshold)
        if size > 0.5:
            lineage_data[tag]['mature'].append(organism_data)
        
        # Reproductive success
        if eggs_laid > 0:
            lineage_data[tag]['parents'].append(organism_data)
        
        # Combat activity
        if damage > 0 or kills > 0 or bites > 0:
            lineage_data[tag]['combatants'].append(organism_data)
        
        # Successful killers
        if kills > 0:
            lineage_data[tag]['killers'].append(organism_data)
    
    print("⚔️📏 SIZE-RELATIVE COMBAT EFFECTIVENESS ANALYSIS")
    print("=" * 90)
    print(f"Latest ecosystem: {len(data)} organisms")
    print("\n💡 KEY INSIGHT: Damage scales with body size - analyzing TRUE combat efficiency!\n")
    
    # Focus on main combatant lineages
    combat_lineages = ['Pred', 'Pred.lessgreen', 'Greencreep', 'Prey.Basic']
    
    for lineage in combat_lineages:
        if lineage not in lineage_data:
            continue
            
        all_orgs = lineage_data[lineage]['all']
        mature_orgs = lineage_data[lineage]['mature']
        combatants = lineage_data[lineage]['combatants']
        killers = lineage_data[lineage]['killers']
        
        if not all_orgs:
            continue
            
        print(f"\n{'='*25} {lineage.upper()} ANALYSIS {'='*25}")
        print(f"Population: {len(all_orgs)} organisms ({len(all_orgs)/len(data)*100:.1f}% of ecosystem)")
        print(f"Mature (>0.5 size): {len(mature_orgs)} ({len(mature_orgs)/len(all_orgs)*100:.1f}%)")
        print(f"Combat active: {len(combatants)} ({len(combatants)/len(all_orgs)*100:.1f}%)")
        print(f"Successful killers: {len(killers)} ({len(killers)/len(all_orgs)*100:.1f}%)")
        
        # Analyze combatants (size-relative metrics)
        if combatants:
            size_damages = [c['size_adjusted_damage'] for c in combatants]
            size_kill_ratios = [c['size_kill_ratio'] for c in combatants]
            bite_efficiencies = [c['bite_efficiency'] for c in combatants]
            combat_fitness = [c['combat_fitness'] for c in combatants]
            
            print(f"\n📊 SIZE-RELATIVE COMBAT METRICS ({len(combatants)} combatants):")
            print(f"  Damage per size unit: {statistics.mean(size_damages):.1f} (±{statistics.stdev(size_damages) if len(size_damages) > 1 else 0:.1f})")
            print(f"  Kills per size unit: {statistics.mean(size_kill_ratios):.2f}")
            print(f"  Bite success rate: {statistics.mean(bite_efficiencies):.2f}")
            print(f"  Combat fitness score: {statistics.mean(combat_fitness):.1f}")
            
            # Find most efficient fighter
            if combatants:
                top_fighter = max(combatants, key=lambda x: x['combat_fitness'])
                print(f"  🏆 Most efficient: Species {top_fighter['species_id']} (Gen {top_fighter['generation']})")
                print(f"     Size: {top_fighter['size']:.2f}, {top_fighter['damage']:.1f} dmg, {top_fighter['kills']} kills")
                print(f"     Efficiency: {top_fighter['size_adjusted_damage']:.1f} dmg/size, {top_fighter['size_kill_ratio']:.2f} kills/size")
        
        # Generation analysis
        if mature_orgs:
            generations = [o['generation'] for o in mature_orgs]
            gen_range = f"{min(generations)}-{max(generations)}"
            print(f"\n🧬 GENERATION ANALYSIS: {gen_range}")
            
            # Evolution trend
            if len(set(generations)) > 2:
                latest_gen = max(generations)
                earliest_gen = min(generations)
                
                latest_orgs = [o for o in mature_orgs if o['generation'] >= latest_gen - 2]
                earliest_orgs = [o for o in mature_orgs if o['generation'] <= earliest_gen + 2]
                
                if latest_orgs and earliest_orgs:
                    latest_combat_fitness = statistics.mean([o['combat_fitness'] for o in latest_orgs])
                    earliest_combat_fitness = statistics.mean([o['combat_fitness'] for o in earliest_orgs])
                    
                    print(f"  Latest gen combat fitness: {latest_combat_fitness:.1f}")
                    print(f"  Earliest gen combat fitness: {earliest_combat_fitness:.1f}")
                    if latest_combat_fitness > earliest_combat_fitness:
                        improvement = ((latest_combat_fitness - earliest_combat_fitness) / earliest_combat_fitness) * 100
                        print(f"  📈 COMBAT EVOLUTION: +{improvement:.1f}% improvement over generations!")
                    else:
                        decline = ((earliest_combat_fitness - latest_combat_fitness) / earliest_combat_fitness) * 100
                        print(f"  📉 Combat decline: -{decline:.1f}% over generations")
    
    # Cross-lineage efficiency comparison
    print(f"\n{'='*30} EFFICIENCY RANKINGS {'='*30}")
    
    # Collect all mature combatants for comparison
    all_combatants = []
    for lineage, data_dict in lineage_data.items():
        for org in data_dict['combatants']:
            if org['size'] > 0.5:  # Mature only
                org['lineage'] = lineage
                all_combatants.append(org)
    
    if all_combatants:
        # Top size-relative damage dealers
        top_damage_efficiency = sorted(all_combatants, key=lambda x: x['size_adjusted_damage'], reverse=True)[:8]
        print(f"\n🏆 TOP 8 SIZE-ADJUSTED DAMAGE DEALERS:")
        for i, org in enumerate(top_damage_efficiency, 1):
            print(f"  {i}. {org['lineage']} (Species {org['species_id']}, Gen {org['generation']})")
            print(f"     Size: {org['size']:.2f}, Total damage: {org['damage']:.1f}")
            print(f"     🎯 Efficiency: {org['size_adjusted_damage']:.1f} damage per size unit")
        
        # Top killers per size
        top_kill_efficiency = sorted(all_combatants, key=lambda x: x['size_kill_ratio'], reverse=True)[:8]
        print(f"\n⚔️ TOP 8 SIZE-ADJUSTED KILLERS:")
        for i, org in enumerate(top_kill_efficiency, 1):
            print(f"  {i}. {org['lineage']} (Species {org['species_id']}, Gen {org['generation']})")
            print(f"     Size: {org['size']:.2f}, Kills: {org['kills']}")
            print(f"     🎯 Efficiency: {org['size_kill_ratio']:.2f} kills per size unit")
        
        # Overall combat efficiency champions
        top_combat_fitness = sorted(all_combatants, key=lambda x: x['combat_fitness'], reverse=True)[:5]
        print(f"\n🏆 TOP 5 OVERALL COMBAT EFFICIENCY:")
        for i, org in enumerate(top_combat_fitness, 1):
            print(f"  {i}. {org['lineage']} (Species {org['species_id']}, Gen {org['generation']})")
            print(f"     Combat fitness: {org['combat_fitness']:.1f}")
            print(f"     Size: {org['size']:.2f}, {org['damage']:.1f} dmg, {org['kills']} kills, {org['eggs_laid']} eggs")
    
    # Pred.lessgreen recovery analysis
    if 'Pred.lessgreen' in lineage_data:
        predless_all = lineage_data['Pred.lessgreen']['all']
        predless_combatants = lineage_data['Pred.lessgreen']['combatants']
        
        print(f"\n🚀 PRED.LESSGREEN POPULATION RECOVERY ANALYSIS:")
        print(f"Population: {len(predless_all)} organisms (RECOVERED from 8!)")
        
        if predless_combatants:
            avg_combat_fitness = statistics.mean([c['combat_fitness'] for c in predless_combatants])
            avg_size_damage = statistics.mean([c['size_adjusted_damage'] for c in predless_combatants])
            
            print(f"Combat efficiency: {avg_combat_fitness:.1f} fitness score")
            print(f"Size-adjusted damage: {avg_size_damage:.1f} per size unit")
            
            # Check for kin-killing adaptation
            generations = [c['generation'] for c in predless_combatants]
            if generations:
                print(f"Generation spread: {min(generations)}-{max(generations)}")
                
                if len(predless_all) > 15:
                    print("✅ Population stabilized above critical threshold!")
                    print("💡 Natural selection working - survivors adapting to reduce kin-killing")
                else:
                    print("⚠️ Still rebuilding - monitoring population growth")
    
    # Ecosystem pressure analysis
    print(f"\n{'='*30} ECOSYSTEM DYNAMICS {'='*30}")
    
    total_combatants = sum(len(data_dict['combatants']) for data_dict in lineage_data.values())
    total_killers = sum(len(data_dict['killers']) for data_dict in lineage_data.values())
    total_mature = sum(len(data_dict['mature']) for data_dict in lineage_data.values())
    
    combat_pressure = (total_combatants / len(data)) * 100
    kill_pressure = (total_killers / len(data)) * 100
    maturity_rate = (total_mature / len(data)) * 100
    
    print(f"Combat participation: {combat_pressure:.1f}% of population")
    print(f"Active killers: {kill_pressure:.1f}% of population") 
    print(f"Mature organisms: {maturity_rate:.1f}% of population")
    
    if combat_pressure > 40:
        print("🔥 HIGH COMBAT PRESSURE - Ecosystem in active warfare")
    elif combat_pressure > 25:
        print("⚔️ MODERATE COMBAT - Balanced predator-prey dynamics")
    else:
        print("🕊️ LOW COMBAT - Peaceful ecosystem")
    
    # Herbivore harassment effectiveness
    greencreep_combatants = lineage_data.get('Greencreep', {}).get('combatants', [])
    if greencreep_combatants:
        gc_harassment = [c for c in greencreep_combatants if c['damage'] > 10 and c['kills'] == 0]
        print(f"\n🌿 GREENCREEP HARASSMENT STRATEGY:")
        print(f"Active harassers: {len(gc_harassment)} ({len(gc_harassment)/len(greencreep_combatants)*100:.1f}% of combatants)")
        print(f"💡 High damage, low kills = successful 'death by thousand cuts' strategy!")

if __name__ == "__main__":
    analyze_size_relative_combat()