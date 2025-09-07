# Bibites Ecosystem Analysis System

**Natural language analysis of evolutionary ecosystems through adversarial gene vs neural architecture prediction.**

## Overview

This project analyzes complex evolutionary ecosystems from [The Bibites](https://leocaussan.itch.io/the-bibites) artificial life simulator, focusing on:

- **Evolutionary tracking** across species and subspeciation events
- **Combat effectiveness** with size-relative damage calculations
- **Behavioral analysis** of pheromone communication and neural complexity
- **Spatial ecosystem dynamics** across territorial zones
- **Survival prediction** through cross-domain validation

## Key Features

### Unified Analysis Tools
```bash
# Complete ecosystem analysis
python -m src.tools.bibites --latest --population --combat --species

# Combat effectiveness with size-relative calculations
python -m src.tools.bibites --latest --combat --lineage Pred.lessgreen

# Species-level evolutionary tracking
python -m src.tools.bibites --latest --species --spatial --by-species
```

### Real Ecosystem Insights
- **Size-relative combat analysis**: Damage effectiveness scaled by organism body size
- **Active speciation tracking**: 13+ distinct species across 7 hereditary lineages
- **Zone-based evolution**: Geographic isolation driving subspeciation
- **Predator-prey dynamics**: Multi-lineage apex predator competition

## Technical Approach

### Agent-Coordinated Analysis
- **@tools-engineer**: Python tooling ecosystem maintenance
- **@process-manager**: Development workflow and repository hygiene
- Systematic tool integration from ad-hoc analysis to production workflows

### Analysis Architecture
```
Ecosystem Data → Field Extraction → Species Grouping → Cross-Domain Analysis → Strategic Insights
```

## Quick Start

### Prerequisites
- Python 3.13+ with virtual environment
- The Bibites simulator (for generating ecosystem data)

### Installation
```bash
git clone https://github.com/yourusername/bibites-prediction
cd bibites-prediction
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Basic Usage
```bash
# Extract and analyze latest ecosystem
python -m src.tools.bibites --latest --population

# Combat analysis with rankings  
python -m src.tools.bibites --latest --combat

# Export analysis results
python -m src.tools.bibites --latest --population --species --output analysis.json
```

## Analysis Capabilities

### Combat Analysis
- Size-relative damage effectiveness calculations
- Kill-to-damage ratios with strategic insights
- Lineage-specific predator performance metrics
- Combat vs reproductive success correlations

### Evolutionary Tracking
- Species emergence and divergence detection
- Geographic subspeciation analysis
- Population dynamics across territorial zones
- Genetic drift and adaptation patterns

### Behavioral Analysis
- Neural network complexity scoring
- Pheromone emission and detection patterns
- Zone infiltration and sanctuary violations
- Behavioral strategy classification

## Project Structure

```
src/tools/           # Core analysis tooling
├── bibites.py       # Unified analysis interface
├── lib/             # Modular analysis libraries
└── README.md        # Tool documentation

analysis/
├── experiment_3/    # Current ecosystem analysis results
└── ad-hoc/         # Development and validation scripts

.claude/agents/      # Agent coordination definitions
```

## Current Research

### Experiment 3.3.2: Multiple Protectorate Ecosystem
- **Population**: 300+ organisms across 7+ species lineages
- **Environment**: Concentric territorial zones with selective pressures
- **Key Finding**: Pred.lessgreen recovery from near-extinction to apex predator status
- **Active Research**: Red pheromone avoidance evolution and kin identification

## Contributing

This project uses an agent-coordinated development workflow with systematic validation gates. See `.claude/agents/` for coordination patterns.

## License

[Your chosen license]

## Acknowledgments

- [The Bibites](https://leocaussan.itch.io/the-bibites) by Leo Caussan
- Artificial life simulation community
- Claude Code development environment