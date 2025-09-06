# Speciation Analysis: Auto-Generated Species within Hereditary Tags

**Date**: September 6, 2025  
**Save**: `autosave_20250906041556` (254 organisms)  
**Analysis**: Genetic drift patterns within ecosystem tags using game's auto-assigned species IDs

## Executive Summary

The game's auto-speciation system has generated **13 distinct species** across the 7 hereditary tags, revealing active genetic drift and subspeciation within established lineages. Most significant speciation is occurring in **Greencreep** (6 species) and **Pred** (6 species) - the two competing lineages experiencing the strongest selection pressures.

## Species Breakdown by Hereditary Tag

### Greencreep (96 organisms → 6 species)
| Species ID | Count | % of Tag | Generation Range | Notes |
|------------|-------|----------|------------------|-------|
| **2836** | 35 | 36.5% | Gen 114-118 | **Dominant lineage** |
| **2849** | 25 | 26.0% | Gen 114-117 | Major competing lineage |
| **2884** | 12 | 12.5% | Gen 115-116 | Moderate specialization |
| **2862** | 10 | 10.4% | Gen 114-115 | Earlier generation branch |
| **2878** | 8 | 8.3% | Gen 117-118 | **Latest generation specialist** |
| **2896** | 6 | 6.3% | Gen 115-116 | Minor specialized branch |

**Analysis**: Massive ongoing speciation with 6 distinct lineages! Species 2836 and 2849 are the major competing branches, while 2878 represents the newest evolution (Gen 117-118).

### Pred (57 organisms → 6 species)
| Species ID | Count | % of Tag | Generation Range | Notes |
|------------|-------|----------|------------------|-------|
| **2872** | 31 | 54.4% | Gen 53-57 | **Dominant predator lineage** |
| **2885** | 8 | 14.0% | Gen 73-75 | **Advanced generation branch** |
| **2867** | 7 | 12.3% | Gen 52-53 | Earlier competing lineage |
| **2802** | 5 | 8.8% | Gen 43-45 | **Ancestral species** (lower gens) |
| **2890** | 3 | 5.3% | Gen 73 | High-gen specialist |
| **2822** | 3 | 5.3% | Gen 72-73 | High-gen specialist |

**Analysis**: Clear evolutionary stratification! Species 2885, 2890, 2822 represent **advanced evolution** (Gen 72-75) while 2802 maintains the **ancestral baseline** (Gen 43-45).

### Protected Species (Stable/Minimal Speciation)

#### Herb.Prot.Magenta (37 organisms → 1 species)
- **Species 2783**: 37 organisms (100%), Gen 42-45
- **Analysis**: **Perfect lineage stability** - the baseline protectorate species maintains complete genetic unity.

#### Herb.Prot.Yellow (22 organisms → 1 species)  
- **Species 2810**: 22 organisms (100%), Gen 3-5
- **Analysis**: Recent derived species from Magenta baseline, **no speciation yet**.

#### Herb.Prot.Cyan (15 organisms → 1 species)
- **Species 2779**: 15 organisms (100%), Gen 7-8  
- **Analysis**: Young derived species, **genetically stable**.

### Spawned Prey (No Evolution)
#### Prey.Basic (17 organisms → 1 species)
- **Species 1956**: 17 organisms (100%), Gen 0-1
- **Analysis**: Environment-spawned, minimal evolution as expected.

#### Prey.Deathwatch (10 organisms → 1 species)  
- **Species 2572**: 10 organisms (100%), Gen 0
- **Analysis**: Environment-spawned, **no evolution**.

## Key Speciation Patterns

### 1. **Selection Pressure Drives Speciation**
**High pressure lineages**:
- **Greencreep**: 6 species (competing with predators)
- **Pred**: 6 species (adapting hunting strategies)

**Protected lineages**: 
- **All protectorates**: 1 species each (stable sanctuary environments)

### 2. **Generation-Based Evolutionary Stratification**
**Pred lineage shows clear generational clustering**:
- **Ancestral**: Species 2802 (Gen 43-45) - 5 organisms
- **Mainstream**: Species 2872 (Gen 53-57) - 31 organisms  
- **Advanced**: Species 2885 (Gen 73-75) - 8 organisms

### 3. **Magenta as Evolutionary Baseline**
As noted by user, **Herb.Prot.Magenta** (Species 2783) serves as baseline:
- **Generation range**: 42-45 (oldest established lineage)
- **Perfect stability**: No subspeciation despite age
- **Derived species**: Yellow (2810) and Cyan (2779) branched from this baseline

### 4. **Rapid vs Stable Evolution**
**Rapid speciation zones**:
- OuterReach/MidPlateau: High predator-prey interaction
- Multiple competing species within single tags

**Stable evolution zones**:
- Protected sanctuaries: Single species per tag
- Environmental spawning: No evolution (as designed)

## Genetic Analysis Implications

### Next Research Directions
1. **Compare genetic makeup** of dominant vs minor species within each tag
2. **Analyze neural architecture** differences between Species 2872 vs 2885 (Pred)
3. **Study resource utilization** patterns across Greencreep subspecies
4. **Track generational advancement** - are higher generation species outcompeting lower ones?

### Specific Comparisons for Genetic Analysis
**High-value comparisons**:
- **Pred 2802 vs 2885**: Ancestral (Gen 43-45) vs Advanced (Gen 73-75)
- **Greencreep 2836 vs 2849**: Dominant competing lineages (35 vs 25 organisms)  
- **Protectorate baseline**: Magenta 2783 vs derived Yellow 2810/Cyan 2779

## Research Questions

### Evolutionary Trajectories
1. **Are advanced generations replacing ancestral ones?** (Pred 2885 vs 2802)
2. **What drives Greencreep subspeciation?** (6 species from single tag)
3. **Do genetic differences correlate with spatial distribution?** (species per zone analysis)
4. **Is speciation accelerating or stabilizing?** (generation trends)

### Adaptive Strategies  
1. **Hunting specialization**: Different Pred species targeting different prey types?
2. **Resource partitioning**: Greencreep subspecies avoiding competition through niche specialization?
3. **Color-blind evolution**: Which Pred species developing pheromone-based hunting first?

---

**Methodology**: Game auto-assigned species IDs (`genes.speciesID`) analyzed across 254 organisms  
**Tools**: `python -m src.tools.bibites --latest --fields genes.speciesID,genes.tag,genes.gen`  
**Next**: Comparative genetic analysis of key subspecies for evolutionary insights

*🤖 Generated with [Claude Code](https://claude.ai/code)*