# Experiment 3: Tag Standardization Specification

## Objective
Implement bulk tag modification to standardize ecosystem taxonomy with clear ecological function + reproductive status naming.

## Current Tag Issues (Experiment 3)
```
"L1 l1"              → 111 organisms (messy, unclear)
"Greencreep"         → 61 organisms (okay, but inconsistent) 
"Magentadeath three" → 42 organisms (messy version number)
"Deathwatch"         → 16 organisms (unclear function)
"bait-basic"         → 16 organisms (unclear vs other bait types)
```

## Proposed Standardization
```
Current Tag           → New Tag         | Rationale
"L1 l1"              → "Pred.Evolved"  | Reproductive predator lineage
"Greencreep"         → "Herb.Green"    | Green-selected herbivore (reproductive)
"Magentadeath three" → "Herb.Protected"| Sanctuary-dwelling herbivore (reproductive) 
"Deathwatch"         → "Prey.Static"   | Environment-spawned, non-reproductive
"bait-basic"         → "Prey.Static"   | Environment-spawned, non-reproductive
```

## Standardized Taxonomy Pattern
**Format**: `{EcoRole}.{Status/Trait}`

**EcoRoles:**
- **Pred**: Predator/carnivore lineages  
- **Herb**: Herbivore/plant-eating lineages
- **Prey**: Non-reproductive, environment-managed food sources

**Status/Traits:**
- **Evolved**: Self-reproducing, evolving lineage
- **Static**: Environment-spawned, non-reproducing (like bait/deathwatch)
- **Green**: Color-selected (green advantageous in outer zones)
- **Protected**: Sanctuary-dwelling (AntiPred zone specialists)

## Expected Outcomes
- **Clear ecological function** at a glance
- **Reproductive status** immediately visible  
- **Consistent naming** across all experiments
- **Analysis-friendly** for automated processing

## Test Case
**Source**: Current experiment autosave  
**Expected**: Clean standardized tags maintaining all organism functionality  
**Validation**: Visual confirmation in game UI + spatial analysis verification

---
*Implementation target for tools-engineer review & development*