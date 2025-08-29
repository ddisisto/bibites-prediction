# Bibites Ecosystem Analysis System

## Project Overview
**Mission:** Natural language analysis of Bibites ecosystem dynamics, organism adaptation strategies, and survival prediction through adversarial gene vs neural analysis.

**Core Approach:** Hierarchical ecosystem analysis with specialized agents performing adversarial cross-validation of genetic and neural domains.

## Current Phase: Ecosystem Analysis & Adversarial Testing

**✅ Infrastructure Complete:**
- Python tooling for automated data extraction and validation
- Ecosystem reconnaissance framework (zones, species, population dynamics)
- Agent architecture for adversarial gene vs neural analysis
- 406-organism test ecosystem with 4 distinct zones and 7 species

**🎯 Current Focus:** 
- Adversarial analysis implementation (@gene-analyst vs @neural-analyst)
- Ecosystem context integration for survival prediction
- Cross-domain validation and synthesis

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
- **Source:** `Savefiles/` (symlinked Steam save directory)
- **Current Dataset:** `data/latest_ecosystem/` (3i1m6x-4.zip: 406 bibites, 7 species, 4 zones)
- **Tools Output:** `./tmp/` for intermediate analysis, structured output in `/analysis/`
- **Agent Specs:** `.claude/agents/` for coordination patterns and scope boundaries

## Analysis Tools

**See: [src/tools/README.md](src/tools/README.md) for complete tool inventory and usage patterns.**

### Core Tools
- **`extract_save.py`** - Automated save file processing (bibites, eggs, images, metadata)
- **`extract_data.py`** - Field extraction with dot notation (3x faster than jq)
- **`extract_metadata.py`** - Ecosystem zone configuration and settings analysis  
- **`validate_format.py`** - Data quality validation and format compliance

### Tool Development Protocol
**Never edit tools directly.** Always delegate to agents:

1. **Request Enhancement:** Specify exact requirements and test cases to @tools-engineer
2. **Agent Implementation:** @tools-engineer creates/modifies tools within strict functional scope
3. **Review & Test:** Validate agent output against real ecosystem data
4. **Git Integration:** Commit working tools with appropriate documentation

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

## Current Test Ecosystem

### Environment: 3i1m6x-4.zip (4-Zone Island System)
1. **Northern Island (sml):** Small plant pellets (0.251), lower biomass (8.0)
2. **Eastern Island (med):** Medium plant pellets (1.585), standard biomass (10.0)  
3. **Southern Island (big):** Large plant pellets (10.0), high biomass (10.0)
4. **Void (meat) Ring:** Carnivore habitat, meat pellets (0.259), low resources (fertility 3.2)

### Species Distribution (406 total organisms)
- **"loop" species:** 215 organisms (53% - dominant)
- **"ani" species:** 84 organisms (21% - major secondary)
- **5 rare species:** 107 organisms (26% - "creep", "eng", "plate", "dozer", "mm")

### Selected Test Specimens
1. **bibite_0.bb8** - "loop" (dominant species, oldest specimen)
2. **bibite_405.bb8** - "loop" (dominant species, youngest specimen)
3. **bibite_196.bb8** - "ani" (major secondary species)
4. **bibite_8.bb8** - "dozer" (ultra-rare: only 3 exist)
5. **bibite_11.bb8** - "plate" (distinct rare lineage)

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
- **`src/tools/README.md`** - Tool inventory, usage patterns, development protocol
- **`.claude/agents/`** - Agent specifications and coordination patterns
- **`data/latest_ecosystem/`** - Current analysis target (3i1m6x-4 ecosystem)
- **`./tmp/`** - Intermediate analysis outputs and extracted data

## Next Phase

**Ready for adversarial analysis implementation** on selected specimens with full ecosystem context integration.

---
*Natural language ecosystem analysis approach*  
*Updated: August 29, 2025*