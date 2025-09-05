# Post-Compact Testing Plan: Fixed Retag Functionality

## Objective
Test the fixed retag functionality with meaningful prey tag differentiation for behavioral nudge studies.

## Immediate Testing Protocol

### Phase 1: Simple Retag Test (Validation)
```bash
# Verify save generation works without game crashes
python -m src.tools.bibites --retag --name "pred exp 3" --find-tag "bait-basic" --replace-tag "Prey.Basic" --apply --output "test_save_validation"
```

**Expected**: Generated save loads successfully in Bibites game UI (no NullReferenceException)

### Phase 2: Meaningful Prey Differentiation
```bash
# Distinguished prey types for behavioral nudge analysis
python -m src.tools.bibites --retag --name "pred exp 3" --find-tag "bait-basic" --replace-tag "Prey.Basic" --apply --output "prey_differentiated"

python -m src.tools.bibites --retag --name "prey_differentiated" --find-tag "Deathwatch" --replace-tag "Prey.Deathwatch" --apply --output "prey_standardized"
```

**Purpose**: 
- **Prey.Basic**: Environment-spawned basic prey for general predation
- **Prey.Deathwatch**: Environment-spawned specialized prey with different behavioral triggers
- Both remain non-reproductive but serve distinct ecological niches for predator selection studies

## Research Context
**From CONCEPTION.md section 3.2.4**: User is studying predator behavioral selection with different prey types as environmental nudges. The distinction between basic vs deathwatch prey remains meaningful for:
- Predator preference analysis
- Behavioral trigger studies  
- Environmental nudge effectiveness
- Selection pressure differentiation

## Success Criteria
1. **Save Compatibility**: Generated saves load in game without errors
2. **Tag Accuracy**: Organisms properly retagged as intended
3. **Functional Preservation**: All organisms retain ecological function
4. **Ready for Analysis**: Spatial analysis shows proper tag distribution

## Next Phase Research
**After Testing Complete**:
- Study separate roles of Prey.Basic vs Prey.Deathwatch in predator selection
- Analyze behavioral nudge effectiveness across prey types
- Examine predator preference patterns in multi-prey environments
- Document findings for systematic predator behavioral analysis

---
*All systems ready for post-compact retag testing with fixed metadata inclusion*