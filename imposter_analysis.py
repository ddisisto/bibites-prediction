#!/usr/bin/env python3
"""
Find and analyze the imposter organisms in protectorate zones
"""
import json
import math

def analyze_imposters():
    # Load latest organism data
    from subprocess import run, PIPE
    
    # Get full organism data
    result = run([
        'python', '-m', 'src.tools.bibites', '--latest', 
        '--fields', 'genes.genes.ColorR,genes.genes.ColorG,genes.genes.ColorB,genes.tag,genes.speciesID,genes.gen,clock.age,physicals.posX,physicals.posY',
        '--batch', '--format', 'json'
    ], capture_output=True, text=True, cwd='.')
    
    organisms = json.loads(result.stdout)
    
    # World parameters (from spatial analysis)
    world_radius = 1500.0
    
    # Zone boundaries (circular positioned zones from metadata)
    protectorate_zones = {
        'MagentaProtectorate': {'center': (-450, 0), 'radius': 340},  # Estimated positions
        'CyanProtectorate': {'center': (225, 390), 'radius': 340},
        'YellowProtectorate': {'center': (225, -390), 'radius': 340}
    }
    
    # Find organisms in each zone
    zone_populations = {
        'MagentaProtectorate': [],
        'CyanProtectorate': [], 
        'YellowProtectorate': [],
        'Other': []
    }
    
    for org in organisms:
        pos_x = org.get('physicals.posX', 0)
        pos_y = org.get('physicals.posY', 0)
        
        # Check which protectorate zone this organism is in
        in_zone = None
        for zone_name, zone_info in protectorate_zones.items():
            center_x, center_y = zone_info['center']
            radius = zone_info['radius']
            
            distance = math.sqrt((pos_x - center_x)**2 + (pos_y - center_y)**2)
            if distance <= radius:
                in_zone = zone_name
                break
        
        if in_zone:
            zone_populations[in_zone].append(org)
        else:
            zone_populations['Other'].append(org)
    
    print("🥷 IMPOSTER ANALYSIS: Finding Non-Protected Species in Sanctuary Zones")
    print("=" * 80)
    
    # Analyze each protectorate zone
    for zone_name in ['MagentaProtectorate', 'CyanProtectorate', 'YellowProtectorate']:
        organisms_in_zone = zone_populations[zone_name]
        if not organisms_in_zone:
            continue
            
        print(f"\n🛡️  {zone_name.upper()}: {len(organisms_in_zone)} organisms")
        
        # Group by species
        species_count = {}
        imposters = []
        
        for org in organisms_in_zone:
            tag = org['genes.tag']
            species_count[tag] = species_count.get(tag, 0) + 1
            
            # Check if this is an imposter (wrong species for zone)
            expected_species = f"Herb.Prot.{zone_name.replace('Protectorate', '')}"
            if tag != expected_species:
                imposters.append(org)
        
        # Display species breakdown
        for species, count in sorted(species_count.items()):
            expected = f"Herb.Prot.{zone_name.replace('Protectorate', '')}"
            if species == expected:
                print(f"  ✅ {species}: {count} organisms (legitimate)")
            else:
                print(f"  🚨 {species}: {count} organisms (IMPOSTER!)")
        
        # Analyze imposters in detail
        if imposters:
            print(f"\n  📊 IMPOSTER DETAILS:")
            for i, imp in enumerate(imposters):
                print(f"    Imposter {i+1}:")
                print(f"      Species: {imp['genes.tag']} (ID: {imp['genes.speciesID']})")
                print(f"      Generation: {imp['genes.gen']}, Age: {imp.get('clock.age', 'unknown')}")
                print(f"      Color: RGB({imp['genes.genes.ColorR']:.3f}, {imp['genes.genes.ColorG']:.3f}, {imp['genes.genes.ColorB']:.3f})")
                print(f"      Position: ({imp['physicals.posX']:.1f}, {imp['physicals.posY']:.1f})")
                
                # Check if color might be providing camouflage
                if zone_name == 'MagentaProtectorate':
                    red = imp['genes.genes.ColorR']
                    blue = imp['genes.genes.ColorB']
                    if red > 0.5 and blue > 0.5:
                        print(f"      💡 Potential magenta mimicry: High red ({red:.3f}) + blue ({blue:.3f})")
    
    print(f"\n🧬 EVOLUTIONARY IMPLICATIONS:")
    total_imposters = sum(len([o for o in zone_populations[z] if not o['genes.tag'].startswith('Herb.Prot.')]) 
                         for z in ['MagentaProtectorate', 'CyanProtectorate', 'YellowProtectorate'])
    
    if total_imposters > 0:
        print(f"  • {total_imposters} imposters found across sanctuary zones")
        print(f"  • Selection pressure: Tower protection without color requirements")
        print(f"  • Evolutionary advantage: Safety without genetic constraints")
        print(f"  • Potential outcome: Sanctuary zone exploitation by non-target species")
        print(f"  • 'Life finds a way' - organisms exploiting loopholes in ecosystem design")
    else:
        print(f"  • No imposters detected - protectorate zones functioning as designed")

if __name__ == "__main__":
    analyze_imposters()