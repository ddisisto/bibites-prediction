# Bibites Ecosystem Analysis System

## Project Overview
**Mission:** Natural language analysis of Bibites ecosystem dynamics, organism adaptation strategies, and survival prediction through adversarial gene vs neural analysis.

**Core Approach:** Hierarchical ecosystem analysis with specialized agents performing adversarial cross-validation of genetic and neural domains.

## Current Phase: Evolutionary Tracking & Speciation Analysis

**✅ Infrastructure Complete:**
- Python tooling for automated autosave processing and evolutionary tracking
- Ecosystem reconnaissance framework with spatial analysis capabilities
- Validated prediction-observation methodology (4/6 prediction accuracy achieved)
- Optimized 3-lineage ecosystem (<500 organisms for 2x+ simulation speed)

**🎯 Current Focus:** 
- Geographic speciation tracking in isolated herbivore populations
- Tag/species mapping for lineage divergence analysis  
- Plate species biomass and divergence studies (South vs East islands)
- Individual organism analysis beyond hereditary tags

## Architecture Decisions

### Technical Stack
- **Language:** Python 3.13 with virtual environment (.venv)
- **JSON Processing:** orjson (3x faster than stdlib) + msgspec validation
- **CLI Framework:** click + rich for consistent tool interfaces
- **Data Storage:** Project-local patterns (./tmp/, Savefiles/ symlink)

### Analysis Architecture
- **Natural Language Analysis** - Domain expertise through specialized agents
- **Adversarial Validation** - Gene vs neural blind prediction challenges  
- **Ecosystem Context** - Zone-aware analysis with environmental parameters
- **Hierarchical Coordination** - @ecosystem-scout → @specimen-curator → specialists

### Data Architecture  
- **Source:** `Savefiles/Autosaves/` (automated 10-minute cycle extraction)
- **Current Dataset:** `data/cycle_20250831115522/` (403 organisms, 3 lineages, optimized ecosystem)
- **Tools Output:** `./tmp/` for intermediate analysis, `evolution/` for cycle tracking
- **Agent Specs:** `.claude/agents/` for coordination patterns and scope boundaries

## Analysis Tools

### Unified Interface
**Primary tool:** `python -m src.tools.bibites` - Zero path exposure, transparent cache validation

**MANDATORY: Always check help first**
```bash
python -m src.tools.bibites --help
```

**Tool Usage Patterns for Agents:**
- **ALWAYS run `--help` first** - Never assume command structure
- **NEVER use Bash commands like `find`, `grep`, `cat`** - Use project tools instead
- **Data selection:** `bibites --latest`, `bibites --name PATTERN`, `bibites --list` 
- **Analysis operations:** `bibites --population`, `bibites --spatial`, `bibites --metadata`
- **Field extraction:** `bibites --fields FIELD_LIST --batch`
- **Cross-pollination:** `bibites --inject-fittest --source X --target Y`
- **File access:** Use Read, Glob, Grep tools from Claude Code environment

**Complete Tool Reference:** @src/tools/README.md

### Tool Development Protocol
**Never edit tools directly.** Always delegate to @tools-engineer:

1. **Specify Requirements:** Exact test cases, expected behavior, compatibility needs
2. **Proper Tool Usage:** Agent must use project's unified interface, not external commands
3. **Agent Implementation:** @tools-engineer creates/modifies within strict functional scope  
4. **Validation & Test:** Test agent output against real ecosystem data
5. **Documentation:** Update tool docs and this CLAUDE.md with new capabilities

### Tool Issue Protocol
**STOP immediately if tools don't work as expected:**
- Document the specific failure or unexpected behavior
- Discuss resolution options before continuing
- Never work around broken tools - fix them properly
- This prevents compounding issues and maintains system reliability

## Agent Ecosystem

### Hierarchical Analysis Agents (5-6 total)
- **@ecosystem-scout:** Population analysis, zone identification, specimen selection context
- **@specimen-curator:** Strategic organism selection across ecological niches
- **@gene-analyst:** Genetic domain specialist (WAG systems, mutation patterns, physical traits)
- **@neural-analyst:** Neural domain specialist (circuit topology, synaptic patterns, behavior prediction)  
- **@synthesis-judge:** Cross-domain validation, prediction accuracy assessment, integration

### Adversarial Framework
**Gene ↔ Neural Blind Predictions:**
- @gene-analyst predicts neural complexity from genetic parameters alone
- @neural-analyst predicts genetic investments from brain structure alone
- @synthesis-judge evaluates predictions against actual organism data
- Ecosystem context provides survival validation for all predictions

### Coordination Patterns
- **Sequential handoffs:** Ecosystem → Selection → Adversarial → Synthesis
- **Context preservation:** Each layer provides environmental/survival context to next
- **Git workflow:** Agent outputs → human review → commit → iteration
- **Scope boundaries:** Strict domain limitations prevent agent drift

## Current Ecosystem: Optimized 3-Lineage System

### Environment: Balanced Zone Configuration
1. **Northern Island:** Small plant pellets, **creep species isolation** (100% endemic)
2. **Eastern Island:** Medium plant pellets, **plate species concentration** (79% of plate population)  
3. **Southern Island:** Large plant pellets, **plate biomass specialization** (bigger, older individuals)
4. **Central/Western + Void:** Carnivore corridors for **loop species mobility**

### Species Distribution (403 total organisms)
- **"loop" species:** 215 organisms (53.3% - mobile carnivores, all zones)
- **"plate" species:** 98 organisms (24.3% - herbivores, East/South specialization)
- **"creep" species:** 90 organisms (22.3% - herbivores, Northern isolation)

### Geographic Isolation & Speciation
- **Perfect Herbivore Isolation:** Each island maintains distinct herbivore population
- **Carnivore Mobility:** Loop species crosses vast expanses between islands
- **Divergent Evolution:** Plate species showing East vs South adaptation patterns
  - **Eastern plates:** Higher density, medium pellet specialization
  - **Southern plates:** Lower density, larger biomass, big pellet adaptation

### Key Research Areas
1. **Tag vs Species Mapping:** Current hereditary tags useful for lineage tracking but need refinement for subspecies analysis
2. **Biomass Studies:** Southern plate individuals significantly larger/older despite lower population counts
3. **Speciation Events:** Regular divergence occurring in all 3 lineages across geographic areas
4. **Population Optimization:** <500 total organisms maintaining 2x+ simulation speed

## Development Workflow

### Analysis Phase Pipeline
1. **Ecosystem Reconnaissance** - @ecosystem-scout analyzes population and zones
2. **Specimen Curation** - @specimen-curator selects representative organisms  
3. **Adversarial Analysis** - Gene/neural specialists make blind predictions
4. **Cross Validation** - @synthesis-judge evaluates prediction accuracy
5. **Insight Integration** - Document findings for ecosystem survival prediction

### Git Workflow
- **Agent delegation:** Specify requirements, let agents implement
- **Human validation:** Test agent outputs, review quality
- **Clean commits:** Agent attribution, clear scope boundaries
- **Iterative refinement:** Build on validated agent deliverables

### Context Management
- **Phase documents:** This CLAUDE.md for overall coordination
- **Analysis tracking:** ANALYSIS.md for current ecosystem analysis phase  
- **Agent specifications:** `.claude/agents/` for coordination patterns
- **Tool documentation:** `src/tools/README.md` for utility references

## Success Criteria

### Ecosystem Analysis
- **Zone characterization:** Complete environmental parameter mapping
- **Species profiling:** Genetic and neural signatures of all major lineages
- **Survival prediction:** Ecosystem-contextualized organism compatibility models
- **Cross-domain validation:** Gene vs neural prediction accuracy assessment

### System Validation
- **Tool effectiveness:** Eliminate manual data processing workflows
- **Agent coordination:** Successful multi-agent adversarial analysis
- **Context integration:** Ecosystem survival factors inform all predictions
- **Knowledge synthesis:** Actionable insights for organism engineering

## Key Files & Documentation

- **`ANALYSIS.md`** - Current ecosystem analysis phase context and progress
- **`analysis/SPECIES_DIVERGENCE_REPORT.md`** - Geographic subspeciation and biomass specialization analysis
- **`src/tools/README.md`** - Tool inventory, usage patterns, development protocol
- **`evolution/`** - Cycle tracking and prediction validation archives
- **`data/cycle_20250831115522/`** - Current optimized 3-lineage ecosystem
- **`./tmp/`** - Intermediate analysis outputs and spatial data

## Next Phase

**Geographic speciation tracking** with focus on plate biomass divergence, loop mobility patterns, and creep endemic evolution in Northern island isolation.

---
*Natural language ecosystem analysis approach*  
*Updated: August 29, 2025*