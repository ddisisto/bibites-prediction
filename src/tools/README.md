# Bibites Analysis Tools

**Core Python utilities for automated Bibites ecosystem analysis. All tools use project-local conventions and consistent CLI patterns.**

## Tool Inventory

### Unified Analysis Tool

#### `bibites.py` - Zero Path Exposure Ecosystem Analysis ⭐ 
**THE unified command** that orchestrates all data access + analysis with transparent JIT extraction and caching. Users never see paths, autosave filenames, or internal structure.

```bash
# Quick ecosystem overview
python -m src.tools.bibites --latest --population --metadata

# Species evolution tracking
python -m src.tools.bibites --last 2 --compare --by-species

# Detailed spatial analysis with export
python -m src.tools.bibites --latest --species --spatial --output analysis.json

# Field extraction across population
python -m src.tools.bibites --latest --fields genes.genes.ColorR,neural.NeuronCount --batch

# Compare specific species by sim ID
python -m src.tools.bibites --latest --compare-species 479 603
```

**DESIGN PHILOSOPHY:**
- **Data Access Layer:** Hardcoded paths, automatic cache management
- **Analysis Layer:** All extract_*.py functionality in unified interface  
- **Zero Path Exposure:** User specifies WHAT data (--latest, --last N) not WHERE
- **Transparent Operation:** Automatic extraction, caching, and path resolution

**Replaces manual workflow:**
```bash
# OLD: Manual 3-step process
extract_save --latest
extract_data --population-summary data/autosave_20250831204442/bibites/
extract_metadata ~/.local/share/Steam/.../autosave_20250831204442.zip

# NEW: Single unified command
bibites --latest --population --metadata
```

### Individual Specialized Tools

### Data Extraction Tools

#### `extract_save.py` - Path-Agnostic Autosave Processing  
**Simplified autosave extraction** with hardcoded Steam paths and cache-transparent operation. No path management needed.
```bash
# Extract latest autosave (zero configuration required)
python -m src.tools.extract_save --latest

# Extract last N autosaves for longitudinal analysis
python -m src.tools.extract_save --last 3

# Extract specific autosave by name/pattern
python -m src.tools.extract_save --name autosave_20250831204442
python -m src.tools.extract_save --name 20250831204442  # partial match works

# Force re-extraction (override cache)
python -m src.tools.extract_save --latest --overwrite
```
**Features:** Cache-transparent (reuses extracted data), automatic Steam autosave detection, perfect filename correspondence  
**Outputs:** Organized `.bb8` files (bibites/, eggs/) + ecosystem images → `data/autosave_TIMESTAMP/`

#### `extract_data.py` - Field Extraction & Population Analysis
**Modular Python tool** for organism data extraction and evolutionary tracking. Refactored into specialized library modules for maintainability.
```bash
# Single organism analysis
python -m src.tools.extract_data --fields genes.tag,genes.genes.ColorR data/ecosystem/bibites/bibite_0.bb8

# Batch field extraction with table output
python -m src.tools.extract_data --fields genes.genes.AverageMutationNumber,clock.age --batch data/ecosystem/bibites/ --format table

# POPULATION TRACKING - Species distribution analysis
python -m src.tools.extract_data --population-summary data/cycle_dir/bibites/

# EVOLUTIONARY COMPARISON - Cross-cycle analysis
python -m src.tools.extract_data --compare-populations data/cycle_A/bibites/ data/cycle_B/bibites/

# SPATIAL ANALYSIS - Geographic zone distribution
python -m src.tools.extract_data --spatial-analysis data/cycle_dir/bibites/ --output ./tmp/spatial.json

# SPECIES ANALYSIS - Detailed species breakdowns (New!)
python -m src.tools.extract_data --species-summary data/cycle_dir/bibites/
```
**Modular Architecture:** 5 specialized lib modules (field_extraction, population_analysis, spatial_analysis, comparison_tools, output_formatters)
**Performance:** orjson parsing, rich output, 3x faster than manual jq commands

#### `extract_metadata.py` - Ecosystem Configuration
Reveals zone settings, environmental parameters, and world configuration from save files.
```bash
# Analyze ecosystem zones and settings
python -m src.tools.extract_metadata Savefiles/3i1m6x-4.zip

# Extract raw metadata files for inspection
python -m src.tools.extract_metadata --raw Savefiles/save.zip
```
**Reveals:** Zone names, resource types, fertility levels, pellet sizes, species data.

### Validation Tools

#### `validate_format.py` - Format Compliance
Validates .bb8 file structure and identifies format issues.
```bash
# Single file validation
python -m src.tools.validate_format data/ecosystem/bibites/bibite_0.bb8

# Batch validation with detailed analysis
python -m src.tools.validate_format --batch --detailed data/ecosystem/bibites/
```
**Checks:** Required fields, data types, neural network structure, genetic parameters.

## Project Conventions

### File System Patterns
- **`Savefiles/`** - Symlinked Bibites save directory (auto-finds latest non-auto saves)
- **`data/latest_ecosystem/`** - Current analysis target
- **`./tmp/`** - Project-local temporary files (not system `/tmp/`)
- **`.bb8` files** - Individual organism configurations (JSON format with UTF-8 BOM)

### CLI Patterns
- **Rich output** - Progress bars, colored tables, structured display
- **Consistent flags** - `--batch` for multi-file, `--format` for output type, `--help` everywhere
- **Error handling** - Graceful failures with helpful error messages
- **Performance** - orjson parsing (3x faster than stdlib json)

## Usage Examples

### Complete Ecosystem Analysis with Unified Tool ⭐
```bash
# Single command ecosystem analysis (replaces 3-4 separate commands)
python -m src.tools.bibites --latest --population --species --metadata --spatial --output analysis.json

# Evolution tracking across cycles
python -m src.tools.bibites --last 3 --compare 

# Species-level speciation analysis
python -m src.tools.bibites --latest --species --by-species --spatial

# Targeted field analysis
python -m src.tools.bibites --latest --fields genes.genes.AverageMutationNumber,clock.age --batch --format csv
```

### Legacy Individual Tool Workflow
```bash
# 1. Extract latest autosave (no paths needed)
python -m src.tools.extract_save --latest

# 2. Analyze species distribution immediately  
python -m src.tools.extract_data --population-summary data/autosave_TIMESTAMP/bibites/

# 3. Understand ecosystem structure
python -m src.tools.extract_metadata ~/.local/share/Steam/.../autosave_TIMESTAMP.zip

# 4. Validate data quality
python -m src.tools.validate_format --batch data/autosave_TIMESTAMP/bibites/
```

### Representative Specimen Selection
```bash
# Extract key genetic features for species clustering
python -m src.tools.extract_data --fields genes.tag,genes.genes.AverageMutationNumber,genes.genes.SizeRatio --batch data/autosave_TIMESTAMP/bibites/ --output ./tmp/species_analysis.json

# Validate selected specimens for analysis
python -m src.tools.validate_format --detailed data/autosave_TIMESTAMP/bibites/bibite_0.bb8 data/autosave_TIMESTAMP/bibites/bibite_405.bb8
```

### Longitudinal Analysis with Cache-Transparent Operation
```bash
# Extract last 5 autosaves for temporal analysis (cache-transparent)
python -m src.tools.extract_save --last 5

# Compare population changes across extracted cycles
python -m src.tools.extract_data --compare-populations \
  data/autosave_20250830/bibites/ \
  data/autosave_20250831/bibites/

# Batch analyze all extracted autosaves for species tracking
for dir in data/autosave_*/; do
  echo "Analyzing $(basename $dir)..."
  python -m src.tools.extract_data --population-summary ${dir}bibites/
done
```
**Benefits:** Zero path management, automatic cache reuse, perfect for evolutionary tracking workflows

## Tool Development & Updates

### Getting Tools Modified
**DO NOT edit tool files directly.** Use agent delegation for all tool improvements:

```
Request: @tools-engineer - Enhance extract_data.py to support neural network field extraction
Scope: Add --neural-fields flag for brain.Nodes, brain.Synapses extraction  
Test: Validate against data/current/bibites/bibite_0.bb8
```

**Agent reviews and validates:** Code changes, tests functionality, maintains consistency
**You review and commit:** Agent outputs, ensuring quality and integration

### Tool Extension Patterns
- **New extractors:** Follow `extract_*.py` naming, use click + rich CLI patterns
- **New validators:** Follow `validate_*.py` naming, support batch processing
- **Integration:** Update this README.md via @tools-engineer when adding tools
- **Testing:** Always test against real ecosystem data before committing

## Integration with Development Team

### Development Team Integration
- **Main Context Analysis:** Use tools for data extraction, perform all interpretive analysis in primary context
- **@tools-engineer:** Maintain and enhance modular lib/ structure, implement new data processing capabilities
- **@process-manager:** Ensure tool development follows project conventions and documentation standards

### Data Flow Pattern
1. **Extract** ecosystem data with appropriate tool
2. **Validate** data quality and completeness using validation tools
3. **Analyze** ecosystem dynamics, species behavior, and evolutionary patterns in primary context
4. **Enhance** tools as needed through @tools-engineer delegation for new data processing requirements
5. **Document** results and insights in appropriate `/analysis/` subdirectories

## Modular Architecture Details

### Library Structure (`src/tools/lib/`)
The modular refactor creates focused, single-responsibility modules:

- **`field_extraction.py`** - Core BB8 file processing, single/batch extraction, species field mapping
- **`population_analysis.py`** - Species distribution, statistics, population summaries  
- **`spatial_analysis.py`** - Geographic zone classification, spatial distribution analysis
- **`comparison_tools.py`** - Cycle comparisons, species-to-species analysis  
- **`output_formatters.py`** - Table, JSON, CSV output with consistent rich formatting

### Extension Points
Ready for species name integration:
- Species ID mapping infrastructure in place
- Clear separation between hereditary tags and sim-generated species
- Modular structure supports easy feature addition without code disruption

---
*Tools designed for evolutionary tracking and speciation analysis workflow*
*Updated: August 31, 2025*