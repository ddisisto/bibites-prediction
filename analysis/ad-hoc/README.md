# Ad-Hoc Analysis Scripts

**Purpose:** Proof-of-concept and validation scripts created during tool development process.

## Script Inventory

### Combat Analysis Scripts
- `size_relative_combat_analysis.py` - Size-relative combat effectiveness (key algorithm)
- `predator_combat_analysis.py` - Lineage-specific combat patterns
- `combat_reproduction_analysis.py` - Combat vs reproductive success correlations

### Behavioral Analysis Scripts  
- `neural_complexity_analysis.py` - Brain architecture complexity patterns
- `pheromone_analysis.py` - Red pheromone emission/detection analysis

### Ecosystem Analysis Scripts
- `quick_current_analysis.py` - Fast ecosystem overview
- `pred_lessgreen_analysis.py` - Specific lineage recovery analysis  
- `imposter_analysis.py` - Zone infiltration detection

## Development Process

These scripts follow the **ad-hoc POC → validation → integration** workflow:

1. **POC Phase:** Create standalone script to test analysis approach
2. **Validation Phase:** Validate against real ecosystem data
3. **Integration Phase:** Extract patterns into `src/tools/lib/` modules
4. **Archive Phase:** Keep original scripts for reference and regression testing

## Integration Status

- ✅ **Combat Analysis:** Integrated into `src/tools/lib/combat_analysis.py` (Issue #7)
- 🚧 **Behavioral Analysis:** In progress (Issue #8)
- ⏳ **Others:** Awaiting integration as needed

## Usage

These scripts work directly against extracted ecosystem data:

```bash
# Extract latest ecosystem first
python -m src.tools.bibites --latest

# Then run ad-hoc analysis
python analysis/ad-hoc/size_relative_combat_analysis.py
```

**Note:** Use integrated tools in `src/tools/bibites.py` for production analysis. These scripts are for development/validation reference.

---
*Organized: September 7, 2025*