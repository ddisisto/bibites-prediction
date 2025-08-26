# The Bibites: Game Mechanics Research

## Executive Summary

The Bibites is an artificial life simulation that uses NEAT-based neural network evolution to create emergent behaviors in digital organisms called "Bibites." This research documents the core mechanics, survival systems, and behavioral patterns that present prediction opportunities for our system.

## Core Game Mechanics

### 1. Neural Network-Based Control System

**NEAT Algorithm Implementation:**
- Uses NeuroEvolution of Augmenting Topologies (NEAT) to evolve neural network brains
- Starts with simple topologies and adds complexity through evolution
- Each Bibite has a unique brain with evolved connections and weights
- Supports both topology and weight evolution simultaneously

**Neural Network Structure:**
- **Input Neurons:** Sense internal state and environment
  - Energy levels (EnergyRatio, LifeRatio)
  - Proximity detection (BibiteCloseness, PlantCloseness, MeatCloseness)
  - Population counts (NBibites, NPlants, NMeats)
  - Pheromone detection (angle, heading, concentration)
  - Time awareness (Tic, Minute, TimeAlive)
  - Color genes of nearby organisms

- **Output Neurons:** Control behaviors and actions
  - Movement (Accelerate, Rotate)
  - Social behaviors (Herding, Grab)
  - Reproduction (EggProduction, Want2Lay)
  - Feeding (Want2Eat, Digestion)
  - Healing and growth
  - Pheromone production
  - Attack tendencies

- **Activation Functions:** TanH, Sigmoid, and ReLu for signal processing

### 2. Energy System (Closed Loop)

**Energy Forms:**
- Biomass (environmental energy pool)
- Body Points (structural energy)
- Health (vitality energy)
- Energy Reserves (stored energy)
- Eggs (reproductive energy)
- Plant Pellets (primary food source)
- Meat Pellets (secondary food source)

**Energy Flow:**
- Most actions consume energy
- Energy transfers between forms with inefficiencies
- Waste energy returns to environment as Biomass
- Plant pellets are most abundant, leading to herbivory prevalence

### 3. Aging and Lifespan Mechanics

**Aging System:**
- Each Bibite has an age and aging threshold (Aging Start)
- Beyond threshold, aging factor calculates penalties
- **Strength Reduction:** Exponential decrease in attack/eating ability
- **Metabolism Increase:** Higher energy requirements for survival
- Natural death prevents indefinite survival

## Survival and Success Factors

### 1. Primary Survival Requirements

**Energy Management:**
- Successful feeding on plant/meat pellets
- Efficient energy conversion and storage
- Balanced energy expenditure vs. intake

**Reproduction Threshold:**
- Must reach maturity (size-based, not age-based)
- Requires ≥50% health to reproduce
- Need sufficient energy for egg development

**Environmental Navigation:**
- Effective movement and foraging behaviors
- Avoidance of threats and hostile organisms
- Adaptation to local environmental conditions

### 2. Emergent Behavioral Patterns

**Successful Strategies:**
- **Herbivory:** Focus on abundant plant pellets
- **Herding:** Group movement for protection/efficiency
- **Altruism:** Species-beneficial behaviors over individual gain
- **Pheromone Trail Following:** Communication-based foraging
- **Territory Establishment:** Food stockpiling behaviors

**Problematic Behaviors:**
- **Cannibalism:** Killing own species members
- **Grey Goo:** Aggressive fast-reproduction strategy
- **Pheromone Manipulation:** Deceptive signaling tactics

### 3. Environmental Adaptation

**Zone-Based Mechanics (v0.6.0+):**
- Different pellet types per zone
- Variable pellet sizes and fertility
- Zone-specific movement patterns
- Adaptation pressure varies by region

**Biomass Density Effects:**
- Determines environmental fertility (E/u²)
- Affects pellet spawn rates and distribution
- Influences population carrying capacity

## Communication and Social Systems

### Pheromone System

**Three-Channel Communication:**
- Red, Green, and Blue pheromone channels
- Concentration gradients detectable by specialized neurons
- Enables complex social behaviors and coordination

**Communication Behaviors:**
- **Trail Following:** Hunting and foraging coordination
- **Threat Signaling:** Warning system for predators
- **Autocrine Signaling:** Self-communication for memory/state
- **Deception:** False signal generation for competitive advantage

## Reproduction and Evolution Mechanics

### Egg Production System

**Reproduction Requirements:**
- Maturity based on size, not age
- Health threshold (≥50%) required
- Gradual egg production with energy investment
- Clutch laying capability (multiple eggs)

**Genetic Inheritance:**
- Asexual reproduction with potential mutations
- Parent genes inherited with mutation events
- Poisson distribution governs mutation frequency
- Gaussian distribution determines mutation magnitude

### Mutation Mechanics

**Dual-Gene System:**
- **Mutation Chance:** Average mutations per generation (Poisson λ)
- **Mutation Variance:** Magnitude of changes (Gaussian distribution)
- Random gene selection for mutation events
- No bias toward beneficial mutations

**Evolutionary Pressure:**
- Natural selection as primary optimization force
- Energy competition drives adaptation
- Reproductive success determines genetic propagation

## Internal Organ System (v0.6.0+)

**Organ Competition:**
- Multiple organs compete for internal space
- Size trade-offs affect functionality
- **Stomach:** Food storage and digestion capacity (supported by StomachWAG genetic parameter)
- **Womb:** Egg production and clutch size (supported by WombWAG genetic parameter)  
- **Brain:** Neural network complexity support (no direct WAG parameter observed in templates)
- **Fat Storage:** Energy reserves (supported by FatWAG genetic parameter)
- **Armor:** Defense system (supported by ArmorWAG genetic parameter)
- **Throat:** Feeding apparatus (supported by ThroatWAG genetic parameter)
- **Mouth Muscles:** Bite strength (supported by MouthMusclesWAG genetic parameter)
- **Movement Muscles:** Locomotion system (supported by MoveMusclesWAG genetic parameter)

**TEMPLATE DATA CONFIRMATION:** WAG (Weight Allocation Gene) parameters in genes section directly control organ investment, with 8 distinct organ systems represented in the genetic data.

## Prediction Opportunities

### 1. Survival Metrics
- **Lifespan Prediction:** Based on aging threshold, metabolism, and strength
- **Energy Efficiency:** Ratio of energy gained vs. consumed
- **Health Maintenance:** Ability to maintain >50% health threshold

### 2. Reproductive Success
- **Egg Production Rate:** Frequency and clutch size
- **Offspring Viability:** Energy allocation vs. mutation burden
- **Generational Fitness:** Comparative success across generations

### 3. Behavioral Classification
- **Dietary Strategy:** Herbivore, carnivore, or omnivore tendencies
- **Social Behavior:** Herding, altruistic, or antisocial patterns
- **Communication Usage:** Pheromone production and response patterns

### 4. Environmental Adaptation
- **Zone Specialization:** Performance in different environmental conditions
- **Population Dynamics:** Carrying capacity and competition outcomes
- **Evolutionary Trajectory:** Direction and rate of genetic change

### 5. Neural Network Complexity
- **Brain Topology:** Network size and connection density (directly measurable from nodes/synapses arrays)
- **Behavioral Repertoire:** Range and sophistication of behaviors (determinable from output node types and connections)
- **Learning Capability:** Adaptation speed to environmental changes (no direct template measurement - would require temporal analysis)

**TEMPLATE DATA SUPPORT:** Network complexity fully quantifiable from template format - node counts, synapse counts, connection patterns, and specialized node types (Types 0-13) are all documented in template structure.

## Game Version Considerations

**Version Evolution:**
- v0.5.0: Modernization and progress updates
- v0.6.0: Introduction of internal organ system and scientific improvements
- Ongoing development with mechanic refinements

**Stability Factors:**
- Core NEAT algorithm remains consistent
- Energy system fundamentals stable
- New features add complexity without breaking existing mechanics

## Format Data Validation Status

### CONFIRMED BY TEMPLATE DATA:
- **Neural Network Structure**: All input/output neuron types documented match template node descriptions
- **Organ System**: WAG genetic parameters provide complete organ allocation control (8 organ types)
- **Genetic Parameters**: All mutation, sensory, behavioral parameters present in genes section
- **Pheromone System**: Three-channel system confirmed by PheroSense1-3 inputs and PhereOut1-3 outputs
- **Network Complexity**: Specialized node types (0-13) enable diverse behavioral architectures
- **Version Evolution**: Template format versions align with claimed game versions (0.6, 0.6.1a4, 0.6.2.1)

### GAPS - SIMULATION WORLD PARAMETERS:
- **Brain Energy Costs**: Global simulation parameter, applies to all organisms equally (default values typically used)
- **Aging Thresholds**: Global simulation parameter for aging mechanics (default values typically used) 
- **Environmental Mechanics**: World generation parameters - when/where/how many plant/meat pellets spawn (simulation-wide settings)
- **Energy Flow Rates**: Global simulation parameters for energy conversion rates and inefficiencies (default values typically used)
- **Behavioral Emergence**: Emergent property from neural network + environment interaction (not directly encoded)

### RESEARCH VS. TEMPLATE ALIGNMENT:
**HIGH CONFIDENCE**: Neural architecture, organ systems, genetic parameters, pheromone communication
**MEDIUM CONFIDENCE**: Mutation mechanics, reproduction requirements, sensory capabilities  
**SIMULATION-LEVEL**: Energy system details, aging mechanics, environmental interactions are global simulation parameters (typically default values)
**EMERGENT**: Behavioral outcomes emerge from neural network + environment interaction

The template format provides excellent structural and parametric data for individual organisms. Global simulation parameters are separate from organism-specific data and typically use default values.

## Sources

1. The Bibites Wiki - https://the-bibites.fandom.com/
2. The Bibites Official Website - https://www.thebibites.com/
3. Steam Store Page - https://store.steampowered.com/app/2736860/The_Bibites_Digital_Life/
4. Itch.io Game Page - https://thebibites.itch.io/the-bibites
5. Various wiki pages on specific mechanics (Energy, Aging, Reproduction, etc.)
6. Developer update logs and community discussions
7. **Template Data Analysis**: Cross-referenced against 70+ .bb8template files (August 2025)

---

*Research conducted: August 26, 2025*  
*Format validation conducted: August 26, 2025*
*Focus: Game mechanics understanding for prediction system development*