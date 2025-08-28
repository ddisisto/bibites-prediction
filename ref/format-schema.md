# Bibites .bb8template Format Schema

## Overview
The .bb8template format is a JSON-based configuration file that defines Bibites organisms. This document provides the structural schema specification derived from analysis of 70+ template examples.

**For behavioral specifications**: See `node-behavior-reference.md` (neural network behaviors) and `gene-behavior-reference.md` (genetic parameter effects).

## Root Schema Structure

```json
{
  "name": string,              // Display name for the template
  "speciesName": string,       // Species identifier 
  "description": string?,      // Optional description (may contain escape sequences)
  "generation": number,        // Generation number (typically 0 for templates)
  "version": string,          // Format version (e.g. "0.6", "0.6.1a4", "0.6.2.1")
  "isOfficial": boolean?,     // Optional flag for official templates
  "nodes": Node[],            // Neural network nodes array
  "synapses": Synapse[],      // Neural network connections array  
  "genes": Genes             // Genetic parameters object
}
```

## Node Schema
Neural network nodes with the following structure:

```json
{
  "Type": number,             // Node type identifier (0-13 observed)
  "Index": number,            // Unique index within the network
  "Inov": number,             // Innovation number (evolutionary tracking)
  "Desc": string,             // Human-readable description/identifier
  "baseActivation": number    // Base activation value (can be negative)
}
```

### Node Type Classification
- **Type 0**: Input/sensor nodes
- **Type 1**: Basic hidden processing nodes  
- **Type 2**: Hidden processing nodes
- **Type 3**: Output/action nodes
- **Types 4-13**: Specialized hidden nodes (memory, temporal, logic, etc.)

### Standard Node Descriptions (By Type)

**Note**: For detailed behavioral specifications, activation ranges, and thresholds, see `node-behavior-reference.md`.

#### Type 0 (Input/Sensor Nodes)
- Physical state: `EnergyRatio`, `Maturity`, `LifeRatio`, `Fullness`, `Speed`, `RotationSpeed`, `IsGrabbing`, `AttackedDamage`, `EggStored`
- Environmental sensing: `BibiteCloseness`, `BibiteAngle`, `NBibites`, `PlantCloseness`, `PlantAngle`, `NPlants`, `MeatCloseness`, `MeatAngle`, `NMeats`
- Chemical detection: `PheroSense1-3`, `Phero1-3Angle`, `Phero1-3Heading`
- Social recognition: `RedBibite`, `GreenBibite`, `BlueBibite`
- Temporal awareness: `Tic`, `Minute`, `TimeAlive`

#### Type 1 (Basic Processing Nodes)  
- `Want2Lay`, `Digestion`, `ClkReset`, `Want2Grow`, `Want2Heal`, `Want2Attack`

#### Type 2 (Hidden Processing Nodes)
- Generic processing and intermediate calculations

#### Type 3 (Output/Action Nodes)
- Movement: `Accelerate`, `Rotate`, `Herding`
- Feeding: `Want2Eat`, `Grab`
- Reproduction: `EggProduction`

#### Types 4-13 (Specialized Processing Nodes)
- Mathematical: Absolute, Gaussian, Sinusoidal, Sigmoid, TanH, Linear, ReLU
- Temporal: Differential, Inhibitory, Integrator
- Memory: Latch, SoftLatch

## Synapse Schema
Connections between nodes with the following structure:

```json
{
  "Inov": number,             // Innovation number (unique identifier)
  "NodeIn": number,           // Index of input node
  "NodeOut": number,          // Index of output node  
  "Weight": number,           // Connection weight (can be negative)
  "En": boolean              // Whether connection is enabled
}
```

## Genes Schema
Genetic parameters controlling organism behavior and capabilities.

**Note**: For detailed behavioral effects, metabolic costs, and trade-off mechanics, see `gene-behavior-reference.md`.

```json
{
  // Reproduction and development timing
  "LayTime": number,
  "BroodTime": number, 
  "HatchTime": number,
  
  // Physical scaling properties
  "SizeRatio": number,
  "SpeedRatio": number,
  "ColorR": number,        // [0.0, 1.0]
  "ColorG": number,        // [0.0, 1.0]
  "ColorB": number,        // [0.0, 1.0]
  
  // Evolution and mutation control
  "MutationAmountSigma": number,
  "AverageMutationNumber": number,
  "BrainMutationSigma": number,
  "BrainAverageMutation": number,
  
  // Sensory system parameters
  "ViewAngle": number,     // Field of view in degrees
  "ViewRadius": number,    // Vision range
  "ClockSpeed": number,    // Internal timing rate
  "PheroSense": number,    // Pheromone detection range
  
  // Behavioral trait parameters
  "Diet": number,          // [0.0, 1.0] herbivore to carnivore
  "HerdSeparationWeight": number,
  "HerdAlignmentWeight": number,        
  "HerdCohesionWeight": number,
  "HerdVelocityWeight": number,
  "HerdSeparationDistance": number,
  
  // Growth and maturation control
  "GrowthScale": number,
  "GrowthMaturityFactor": number,
  "GrowthMaturityExponent": number,
  "EyeOffset": number,
  
  // WAG System: Organ allocation (compete for limited internal space)
  "StomachWAG": number,      // Digestive capacity
  "WombWAG": number,         // Reproductive capacity
  "FatWAG": number,          // Energy storage capacity  
  "ArmorWAG": number,        // Defense capability
  "ThroatWAG": number,       // Feeding apparatus size
  "MouthMusclesWAG": number, // Bite strength
  "MoveMusclesWAG": number,  // Locomotion power
  
  // Energy management system
  "FatStorageThreshold": number,
  "FatStorageDeadband": number
}
```

## Format Validation Rules

1. **Required Fields**: `name`, `speciesName`, `generation`, `version`, `nodes`, `synapses`, `genes`
2. **Optional Fields**: `description`, `isOfficial`
3. **Node Constraints**: 
   - All nodes must have unique `Index` values within the organism
   - `Type` values range from 0-13
   - `Inov` numbers track evolutionary history
4. **Synapse Constraints**:
   - `NodeIn`/`NodeOut` must reference valid node indices
   - `Inov` numbers must be unique within the organism
   - `Weight` can be positive or negative
   - `En` determines if connection is active
5. **Gene Constraints**: All genes object fields are required numbers

## Version Variations

### Observed Versions
- **0.6**: Base format with standard node types
- **0.6.1a4**: Minor additions, same core structure  
- **0.6.2.1**: Added `RotationSpeed` input node in some organisms

### Version-Specific Differences
- Node type availability may vary by version
- Some specialized nodes (Types 10-13) appear only in newer versions
- Input node set may expand with version updates

## Complexity Patterns

### Simple Organisms (~47 nodes)
- Basic input/output connectivity
- Minimal hidden layer processing
- Standard behavioral nodes only

### Complex Organisms (50+ nodes)
- Extensive hidden layer networks
- Specialized node types (memory, temporal, logic)
- Multi-layered processing architectures

## Key-Value Type Summary

### String Fields
- `name`, `speciesName`, `description`, `version`
- Node `Desc` field

### Number Fields  
- `generation` (integer, typically 0)
- Node `Type`, `Index`, `Inov`, `baseActivation`
- Synapse `Inov`, `NodeIn`, `NodeOut`, `Weight`
- All genes fields (various numeric ranges)

### Boolean Fields
- `isOfficial` (optional)
- Synapse `En`

### Array Fields
- `nodes` (array of Node objects)
- `synapses` (array of Synapse objects)

### Object Fields
- `genes` (single object with numeric properties)