# Bibites Ecosystem Analysis System

## Project Overview
**Mission:** Natural language analysis of Bibites ecosystem dynamics, organism adaptation strategies, and survival prediction through adversarial gene vs neural analysis.

**Core Approach:** Hierarchical ecosystem analysis with specialized agents performing adversarial cross-validation of genetic and neural domains.

## Current Phase: Evolutionary Tracking & Speciation Analysis

**✅ Infrastructure Complete:**
- Python tooling for automated autosave processing and evolutionary tracking
- Ecosystem reconnaissance framework with spatial analysis capabilities (concentric zones)
- Cross-pollination and bulk retag functionality for controlled experiments
- Fixed spatial analysis for accurate zone classification and organism distribution
- Optimized population management (~40-50 organisms per species for efficient simulation)

**🎯 Current Focus:** 
- Multiple protectorate zone ecosystem analysis (pred exp 3.3.2)
- Concentric zone evolutionary pressure studies
- Bulk taxonomy standardization and prey differentiation
- Carnivore kin identification in safe harbor zones
- Red pheromone behavioral evolution tracking

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
- **Current Dataset:** `pred exp 3.3.2` (Multiple protectorate zones, population-optimized ecosystem)
- **Tools Output:** `./tmp/` for intermediate analysis, `evolution/` for cycle tracking
- **RW Functionality:** Cross-pollination and bulk retag for controlled evolutionary experiments
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
- **Bulk retag:** `bibites --retag --find-tag OLD --replace-tag NEW --apply`
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

## Development Team Architecture (September 2025)

### Active Development Team
**Current 4-member ecosystem optimized for evolutionary tracking and analysis:**

1. **User (Daniel)**
   - Strategic decisions and requirements validation
   - Domain expertise and biological interpretation oversight
   - Final validation of analysis outputs and methodology

2. **Main Context (Primary Analysis)**
   - Complex ecosystem analysis and behavioral interpretation
   - Natural language reasoning for biological insights
   - Coordination between user requirements and tool outputs
   - All interpretive analysis work (behavioral, evolutionary, ecological)

3. **@tools-engineer**
   - Python tooling ecosystem maintenance and enhancement
   - Data extraction, processing, and formatting utilities
   - Strict scope: Data in → Data out, zero biological interpretation
   - Repository workspace: src/ directory ownership

4. **@process-manager**  
   - Repository hygiene and documentation synchronization
   - Development workflow coordination and process gates
   - Meta-documentation maintenance and agent definition updates

### Analysis Framework (Supersedes Adversarial Architecture)
**Primary Context Analytical Reasoning:**
- Ecosystem dynamics analysis with zone-aware context
- Behavioral pattern interpretation from neural and genetic data
- Species-level evolutionary tracking and speciation analysis
- Cross-domain insights integrating genetic, neural, and environmental factors

### Coordination Patterns
- **Primary Context Analysis:** All complex reasoning, biological interpretation, and ecosystem insights
- **Tool Integration:** @tools-engineer provides data extraction utilities, main context performs analysis
- **Process Gates:** @process-manager ensures documentation sync and workflow hygiene  
- **User Validation:** Daniel provides strategic guidance and final methodology validation
- **Git Workflow:** Clean commits with proper attribution and scope boundaries

## Current Ecosystem: Multiple Protectorate Concentric Zones (3.3.2)

### Environment: Concentric Zone Configuration  
1. **AntiPred Zone (0-24%):** Central sanctuary with red-pheromone emitters + color selection towers
2. **KillingField (24-30%):** Dangerous transition zone with selective pressure
3. **FootHills (46-57%):** Mid-range habitat with moderate resource density  
4. **MidPlateau (57-80%):** Secondary population hub with balanced resources
5. **OuterReach (80-100%):** Outer zone with carnivore safe harbors + meat production

### Current Species & Population Optimization
- **Population Target:** ~40-50 individuals per species for efficient 2x+ simulation speed
- **Multiple Protectorates:** Each zone supports red-pheromone emitting species with genetic color selection
- **Carnivore Safe Harbors:** Meat production zones for predator kin identification learning
- **Stable Implementation:** Multiple protectorate system confirmed stable and functional

### Evolutionary Drivers & Selective Pressures
- **Red Pheromone Communication:** Danger signaling between protected and non-protected species
- **Color Selection Towers:** Genetic color-based selection across different zones
- **Spatial Segregation:** Clear zone preferences preventing unwanted species mixing
- **Kin Identification Learning:** Carnivore safe harbors enable behavioral improvement
- **Population Balance:** Optimized organism counts maintain ecosystem stability

### Key Research Areas
1. **Multiple Protectorate Analysis:** How different zones drive unique evolutionary pressures
2. **Red Pheromone Evolution:** Behavioral adaptation to danger signal communication
3. **Kin Identification:** Carnivore learning effectiveness in safe harbor zones
4. **Population Optimization:** Maintaining species diversity within simulation efficiency constraints
5. **Taxonomy Standardization:** Bulk retag functionality for clearer ecological function naming

## Development Workflow

### Analysis Workflow (Current Approach)
1. **Data Extraction** - @tools-engineer provides data access via unified bibites tool
2. **Primary Analysis** - Main context performs ecosystem analysis, species profiling, and behavioral interpretation
3. **Tool Enhancement** - @tools-engineer implements new data processing capabilities as needed  
4. **Process Validation** - @process-manager ensures workflow hygiene and documentation sync
5. **User Validation** - Daniel provides strategic guidance and methodology validation

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