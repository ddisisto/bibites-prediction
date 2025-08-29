# Bibites Analysis Tools

**Core Python utilities for automated Bibites ecosystem analysis. All tools use project-local conventions and consistent CLI patterns.**

## Tool Inventory

### Data Extraction Tools

#### `extract_save.py` - Save File Processing  
Extracts all content from Bibites save .zip files with automatic organization.
```bash
# Extract latest save file
python -m src.tools.extract_save Savefiles/latest.zip data/ecosystem_name/

# AUTO-EXTRACT LATEST AUTOSAVE (New!)
python -m src.tools.extract_save --latest-autosave data/

# Create timestamped cycle directory for evolution tracking
python -m src.tools.extract_save --latest-autosave --cycle-name data/

# Batch process multiple saves
python -m src.tools.extract_save --batch Savefiles/ data/batch_output/
```
**Outputs:** Organized `.bb8` files (bibites/, eggs/) + ecosystem images + metadata

#### `extract_data.py` - Field Extraction
Extracts specific data fields from .bb8 organism files using dot notation.
```bash
# Single organism analysis
python -m src.tools.extract_data --fields genes.tag,genes.genes.ColorR data/ecosystem/bibites/bibite_0.bb8

# Batch field extraction with table output
python -m src.tools.extract_data --fields genes.genes.AverageMutationNumber,clock.age --batch data/ecosystem/bibites/ --format table

# POPULATION TRACKING (New!)
python -m src.tools.extract_data --population-summary data/cycle_dir/bibites/

# EVOLUTIONARY COMPARISON (New!)
python -m src.tools.extract_data --compare-populations data/cycle_A/bibites/ data/cycle_B/bibites/
```
**Supports:** JSON, CSV, table output formats. 3x faster than manual jq commands.

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

### Complete Ecosystem Analysis Workflow
```bash
# 1. Extract latest save
python -m src.tools.extract_save Savefiles/$(ls -t Savefiles/*.zip | head -1 | grep -v auto) data/current/

# 2. Understand ecosystem structure
python -m src.tools.extract_metadata Savefiles/latest.zip

# 3. Analyze species distribution
python -m src.tools.extract_data --fields genes.tag,clock.age --batch data/current/bibites/ --format table

# 4. Validate data quality
python -m src.tools.validate_format --batch data/current/bibites/
```

### Representative Specimen Selection
```bash
# Extract key genetic features for species clustering
python -m src.tools.extract_data --fields genes.tag,genes.genes.AverageMutationNumber,genes.genes.SizeRatio --batch data/current/bibites/ --output ./tmp/species_analysis.json

# Validate selected specimens for analysis
python -m src.tools.validate_format --detailed data/current/bibites/bibite_0.bb8 data/current/bibites/bibite_405.bb8
```

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

## Integration with Analysis Agents

### For Ecosystem Analysis Agents
- **@ecosystem-scout:** Use `extract_metadata.py` + `extract_data.py --batch` for population overview
- **@gene-analyst:** Use `extract_data.py` with genetic field paths for WAG analysis  
- **@neural-analyst:** Use `extract_data.py` with brain field paths for circuit analysis
- **@synthesis-judge:** Access all extracted data for cross-domain validation

### Data Flow Pattern
1. **Extract** ecosystem with appropriate tool
2. **Validate** data quality and completeness  
3. **Analyze** with domain-specific agents using extracted data
4. **Integrate** findings through synthesis agents
5. **Document** results in appropriate `/analysis/` subdirectories

---
*Tools designed for natural language ecosystem analysis workflow*
*Updated: August 29, 2025*