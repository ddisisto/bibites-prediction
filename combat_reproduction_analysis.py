#!/usr/bin/env python3
"""
Enhanced combat effectiveness analysis with reproductive success correlation
Focus on mature organisms and those who have successfully reproduced
"""
import json
import statistics
from collections import defaultdict

def analyze_combat_reproduction():
    # Load combat and reproduction data
    with open('tmp/combat_reproduction_corrected.json', 'r') as f:
        data = json.load(f)
    
    # Separate organisms by reproductive success and maturity
    lineage_data = defaultdict(lambda: {
        'all': [],
        'mature': [],       # Size > 1.0 (rough maturity threshold)
        'parents': [],      # Have laid eggs
        'active_combatants': [],  # Have combat activity
        'successful_fighters': [] # Have kills
    })
    
    for organism in data:
        tag = organism['genes.tag']
        species_id = organism['genes.speciesID']
        generation = organism['genes.gen']
        
        # Combat metrics
        damage = organism.get('body.mouth.totalDamageDealt', 0.0) or 0.0
        kills = organism.get('body.mouth.totalMurders', 0) or 0
        bites = organism.get('body.mouth.bibitesBitten', 0) or 0
        
        # Reproduction and maturity metrics
        eggs_laid = organism.get('body.eggLayer.nEggsLaid', 0) or 0
        size = organism.get('body.d2Size', 0.0) or 0.0
        energy = organism.get('body.energy', 0.0) or 0.0
        health = organism.get('body.health', 0.0) or 0.0
        time_alive = organism.get('clock.timeAlive', 1.0) or 1.0
        total_travel = organism.get('body.control.totalTravel', 0.0) or 0.0
        
        # Activity and fitness metrics
        activity_rate = total_travel / time_alive  # Distance per time unit
        damage_per_minute = (damage / time_alive) * 60
        reproductive_rate = eggs_laid / (time_alive / 3600)  # Eggs per hour
        
        organism_data = {
            'species_id': species_id,
            'generation': generation,
            'damage': damage,
            'kills': kills,
            'bites': bites,
            'eggs_laid': eggs_laid,
            'size': size,
            'energy': energy,
            'health': health,
            'time_alive': time_alive,
            'activity_rate': activity_rate,
            'damage_per_minute': damage_per_minute,
            'reproductive_rate': reproductive_rate,
            'fitness_score': eggs_laid + (kills * 2),  # Combined reproductive + combat fitness
        }
        
        # Classify organism
        lineage_data[tag]['all'].append(organism_data)
        
        # Maturity classification (size > 1.0 as rough threshold)
        if size > 1.0:
            lineage_data[tag]['mature'].append(organism_data)
        
        # Reproductive success
        if eggs_laid > 0:
            lineage_data[tag]['parents'].append(organism_data)
        
        # Combat activity
        if damage > 0 or kills > 0 or bites > 0:
            lineage_data[tag]['active_combatants'].append(organism_data)
        
        # Successful fighters
        if kills > 0:
            lineage_data[tag]['successful_fighters'].append(organism_data)
    
    print("⚔️🥚 COMBAT EFFECTIVENESS vs REPRODUCTIVE SUCCESS ANALYSIS")
    print("=" * 90)
    print(f"Latest ecosystem snapshot: {len(data)} organisms")
    
    # Focus on main predator lineages
    target_lineages = ['Pred', 'Pred.lessgreen', 'Greencreep', 'Prey.Basic']
    
    for lineage in target_lineages:
        if lineage not in lineage_data:
            continue
            
        all_orgs = lineage_data[lineage]['all']
        mature_orgs = lineage_data[lineage]['mature']
        parents = lineage_data[lineage]['parents']
        fighters = lineage_data[lineage]['active_combatants']
        killers = lineage_data[lineage]['successful_fighters']
        
        if not all_orgs:
            continue
            
        print(f"\n{'='*20} {lineage.upper()} ANALYSIS {'='*20}")
        print(f"Total population: {len(all_orgs)} organisms")
        print(f"Mature (size >1.0): {len(mature_orgs)} ({len(mature_orgs)/len(all_orgs)*100:.1f}%)")
        print(f"Parents (eggs >0): {len(parents)} ({len(parents)/len(all_orgs)*100:.1f}%)")
        print(f"Active fighters: {len(fighters)} ({len(fighters)/len(all_orgs)*100:.1f}%)")
        print(f"Successful killers: {len(killers)} ({len(killers)/len(all_orgs)*100:.1f}%)")
        
        # Analyze mature organisms only (more meaningful data)
        if mature_orgs:
            avg_size = statistics.mean([o['size'] for o in mature_orgs])
            avg_eggs = statistics.mean([o['eggs_laid'] for o in mature_orgs])
            avg_damage = statistics.mean([o['damage'] for o in mature_orgs])
            avg_kills = statistics.mean([o['kills'] for o in mature_orgs])
            avg_fitness = statistics.mean([o['fitness_score'] for o in mature_orgs])
            
            print(f"\n📊 MATURE ORGANISM METRICS (n={len(mature_orgs)}):")
            print(f"  Average size: {avg_size:.2f}")
            print(f"  Average eggs laid: {avg_eggs:.1f}")
            print(f"  Average damage dealt: {avg_damage:.1f}")
            print(f"  Average kills: {avg_kills:.1f}")
            print(f"  Average fitness score: {avg_fitness:.1f}")
        
        # Combat vs Reproduction tradeoff analysis
        if parents and len(parents) > 1:
            parent_damages = [p['damage'] for p in parents]
            parent_kills = [p['kills'] for p in parents]
            
            print(f"\n🥚 PARENTAL COMBAT ANALYSIS (n={len(parents)}):")
            print(f"  Parents avg damage: {statistics.mean(parent_damages):.1f}")
            print(f"  Parents avg kills: {statistics.mean(parent_kills):.1f}")
            
            # Find top performers in each category
            top_parent = max(parents, key=lambda x: x['eggs_laid'])
            print(f"  🏆 Top parent: {top_parent['eggs_laid']} eggs, {top_parent['damage']:.1f} damage, {top_parent['kills']} kills")
            
            if killers:
                top_killer = max(killers, key=lambda x: x['kills'])
                print(f"  ⚔️ Top killer: {top_killer['kills']} kills, {top_killer['eggs_laid']} eggs, {top_killer['damage']:.1f} damage")
        
        # Generation analysis
        if mature_orgs:
            generations = [o['generation'] for o in mature_orgs]
            gen_range = f"{min(generations)}-{max(generations)}"
            print(f"\n🧬 GENERATION SPREAD: {gen_range}")
            
            # Check if higher generations correlate with better performance
            if len(set(generations)) > 1:
                high_gen_orgs = [o for o in mature_orgs if o['generation'] >= statistics.median(generations)]
                low_gen_orgs = [o for o in mature_orgs if o['generation'] < statistics.median(generations)]
                
                if high_gen_orgs and low_gen_orgs:
                    high_gen_fitness = statistics.mean([o['fitness_score'] for o in high_gen_orgs])
                    low_gen_fitness = statistics.mean([o['fitness_score'] for o in low_gen_orgs])
                    
                    print(f"  High generation avg fitness: {high_gen_fitness:.1f}")
                    print(f"  Low generation avg fitness: {low_gen_fitness:.1f}")
                    if high_gen_fitness > low_gen_fitness:
                        print(f"  💡 Higher generations show better fitness (+{high_gen_fitness-low_gen_fitness:.1f})")
    
    # Cross-lineage comparison
    print(f"\n{'='*30} CROSS-LINEAGE COMPARISON {'='*30}")
    
    # Compare Pred vs Pred.lessgreen specifically
    pred_mature = lineage_data['Pred']['mature']
    predless_mature = lineage_data['Pred.lessgreen']['mature'] if 'Pred.lessgreen' in lineage_data else []
    
    if pred_mature and predless_mature:
        pred_fitness = statistics.mean([o['fitness_score'] for o in pred_mature])
        predless_fitness = statistics.mean([o['fitness_score'] for o in predless_mature])
        
        pred_repro = statistics.mean([o['eggs_laid'] for o in pred_mature])
        predless_repro = statistics.mean([o['eggs_laid'] for o in predless_mature])
        
        pred_combat = statistics.mean([o['damage'] for o in pred_mature])
        predless_combat = statistics.mean([o['damage'] for o in predless_mature])
        
        print(f"\n🎯 PRED vs PRED.LESSGREEN (Mature Organisms Only):")
        print(f"Regular Pred ({len(pred_mature)} mature):")
        print(f"  Fitness score: {pred_fitness:.1f}")
        print(f"  Avg eggs: {pred_repro:.1f}")
        print(f"  Avg damage: {pred_combat:.1f}")
        
        print(f"Pred.lessgreen ({len(predless_mature)} mature):")
        print(f"  Fitness score: {predless_fitness:.1f}")
        print(f"  Avg eggs: {predless_repro:.1f}")
        print(f"  Avg damage: {predless_combat:.1f}")
        
        if pred_fitness > predless_fitness:
            advantage = ((pred_fitness - predless_fitness) / predless_fitness) * 100
            print(f"🏆 ADVANTAGE: Regular Pred (+{advantage:.1f}% fitness)")
        else:
            advantage = ((predless_fitness - pred_fitness) / pred_fitness) * 100
            print(f"🏆 ADVANTAGE: Pred.lessgreen (+{advantage:.1f}% fitness)")
    
    # Most successful individuals across all lineages
    print(f"\n{'='*30} ECOSYSTEM CHAMPIONS {'='*30}")
    
    all_mature_orgs = []
    for lineage, data_dict in lineage_data.items():
        for org in data_dict['mature']:
            org['lineage'] = lineage
            all_mature_orgs.append(org)
    
    if all_mature_orgs:
        # Top reproducers
        top_parents = sorted(all_mature_orgs, key=lambda x: x['eggs_laid'], reverse=True)[:5]
        print(f"\n🥚 TOP 5 REPRODUCERS (Mature Organisms):")
        for i, org in enumerate(top_parents, 1):
            print(f"  {i}. {org['lineage']} (Species {org['species_id']}, Gen {org['generation']})")
            print(f"     {org['eggs_laid']} eggs, {org['damage']:.1f} damage, {org['kills']} kills")
        
        # Top fighters
        top_fighters = sorted(all_mature_orgs, key=lambda x: x['damage'], reverse=True)[:5]
        print(f"\n⚔️ TOP 5 FIGHTERS (Mature Organisms):")
        for i, org in enumerate(top_fighters, 1):
            print(f"  {i}. {org['lineage']} (Species {org['species_id']}, Gen {org['generation']})")
            print(f"     {org['damage']:.1f} damage, {org['kills']} kills, {org['eggs_laid']} eggs")
        
        # Top overall fitness
        top_fitness = sorted(all_mature_orgs, key=lambda x: x['fitness_score'], reverse=True)[:5]
        print(f"\n🏆 TOP 5 OVERALL FITNESS (Mature Organisms):")
        for i, org in enumerate(top_fitness, 1):
            print(f"  {i}. {org['lineage']} (Species {org['species_id']}, Gen {org['generation']})")
            print(f"     Fitness: {org['fitness_score']:.1f} ({org['eggs_laid']} eggs + {org['kills']} kills)")
    
    # Population decline analysis
    if 'Pred.lessgreen' in lineage_data:
        predless_pop = len(lineage_data['Pred.lessgreen']['all'])
        print(f"\n⚠️ PRED.LESSGREEN POPULATION STATUS:")
        print(f"Current population: {predless_pop} organisms")
        if predless_pop < 15:
            print(f"🚨 CRITICALLY LOW POPULATION - Risk of extinction!")
            print(f"   Possible causes:")
            print(f"   • Reduced fitness due to kin-killing behavior")
            print(f"   • Energy costs of increased aggression")
            print(f"   • Self-limiting through intraspecies conflict")
        else:
            print(f"✅ Population stable")
    
    # Ecosystem health summary
    total_mature = sum(len(data_dict['mature']) for data_dict in lineage_data.values())
    total_parents = sum(len(data_dict['parents']) for data_dict in lineage_data.values())
    total_fighters = sum(len(data_dict['active_combatants']) for data_dict in lineage_data.values())
    
    print(f"\n📊 ECOSYSTEM SUMMARY:")
    print(f"Total mature organisms: {total_mature}")
    print(f"Active reproducers: {total_parents} ({total_parents/total_mature*100:.1f}% of mature)")
    print(f"Active fighters: {total_fighters} ({total_fighters/len(data)*100:.1f}% of all)")
    
    reproduction_rate = total_parents / total_mature if total_mature > 0 else 0
    combat_rate = total_fighters / len(data) if len(data) > 0 else 0
    
    print(f"Ecosystem balance: {'REPRODUCTIVE' if reproduction_rate > 0.3 else 'COMBATIVE' if combat_rate > 0.3 else 'BALANCED'}")

if __name__ == "__main__":
    analyze_combat_reproduction()