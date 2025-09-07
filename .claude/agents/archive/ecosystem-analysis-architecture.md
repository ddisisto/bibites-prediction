# Bibites Ecosystem Analysis Agent Architecture

## Core Agent Domains

### 1. @organism-analyst
**Domain:** `/organisms/` - Individual organism analysis and characterization
**Git Branch:** `analysis/organisms`

**Key Responsibilities:**
- Parse and analyze individual .bb8 files for genetic/neural patterns
- Create standardized organism profiles for survival prediction
- Extract survival-relevant features (aggression, diet, reproduction rate)
- Classify organisms into behavioral archetypes

**First Implementation Tasks:**
- Create organism analysis template
- Analyze first 5 organisms (bibite_000-004) 
- Establish feature extraction pipeline

### 2. @species-tracker  
**Domain:** `/species/` - Lineage tracking and evolutionary analysis
**Git Branch:** `analysis/species`

**Key Responsibilities:**
- Track organism lineages from speciesData.json
- Analyze evolutionary adaptation patterns
- Identify successful species strategies in Daniel's stable worlds
- Build species compatibility matrices

**First Implementation Tasks:**
- Parse speciesData.json structure
- Create lineage visualization
- Identify top-performing species lineages

### 3. @ecosystem-analyst
**Domain:** `/ecosystem/` - Population dynamics and ecosystem-level insights  
**Git Branch:** `analysis/ecosystem`

**Key Responsibilities:**
- Analyze population-level dynamics from validation-1.zip
- Model ecosystem carrying capacity and niche structures
- Predict organism compatibility with established ecosystems
- Generate ecosystem integration strategies

**First Implementation Tasks:**
- Map ecosystem population dynamics
- Identify ecosystem niches and carrying capacity
- Create compatibility prediction framework

### 4. @tools-engineer
**Domain:** `/tools/` - Analysis utilities and standardized workflows
**Git Branch:** `tools/utilities`

**Key Responsibilities:**
- Build extract-save.sh for zip file processing
- Create analyze-organism.sh for standardized profiling
- Implement jq-based feature extraction utilities
- Maintain tool documentation and validation

**First Implementation Tasks:**
- Create extract-save.sh script
- Build jq feature extraction utilities
- Establish tool testing framework

### 5. @insights-synthesizer
**Domain:** `/insights/` - High-level pattern discovery
**Git Branch:** `insights/synthesis`

**Key Responsibilities:**
- Synthesize findings across all analysis domains
- Generate ecosystem survival predictions
- Create organism engineering recommendations
- Build decision frameworks for ecosystem integration

**First Implementation Tasks:**
- Create insight aggregation templates
- Generate initial cross-domain patterns
- Establish prediction validation framework

## Proposed Implementation Order

**Phase 1:** @tools-engineer (Foundation)
**Phase 2:** @organism-analyst (Core Analysis)  
**Phase 3:** @ecosystem-analyst (Context)
**Phase 4:** @insights-synthesizer (Synthesis)
**Phase 5:** @species-tracker (Evolutionary)

## Integration Pattern

Each agent creates concrete outputs in their filesystem domain that we can review together, iterate on, and commit to git. No ephemeral-only work.

---
*Created: August 29, 2025*
*Status: Architecture proposal - needs Daniel review*