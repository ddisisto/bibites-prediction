# Bibites .bb8template Format Schema

## Overview
The .bb8template format is a JSON-based configuration file that defines Bibites organisms. This document provides the structural schema specification derived from analysis of 70+ template examples.

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

### Standard Node Descriptions (Type 0 - Inputs)
- `EnergyRatio`, `Maturity`, `LifeRatio`, `Fullness`, `Speed`
- `IsGrabbing`, `AttackedDamage`, `EggStored`
- `BibiteCloseness`, `BibiteAngle`, `NBibites`
- `PlantCloseness`, `PlantAngle`, `NPlants`
- `MeatCloseness`, `MeatAngle`, `NMeats`
- `RedBibite`, `GreenBibite`, `BlueBibite`
- `Tic`, `Minute`, `TimeAlive`
- `PheroSense1-3`, `Phero1-3Angle`, `Phero1-3Heading`
- `RotationSpeed` (version-dependent)

### Standard Node Descriptions (Type 3 - Outputs)
- `Accelerate`, `Rotate`, `Herding`
- `Want2Eat`, `Grab`
- `EggProduction`

### Standard Node Descriptions (Type 1 - Processing)
- `Want2Lay`, `Digestion`, `ClkReset`
- `Want2Grow`, `Want2Heal`, `Want2Attack`

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
Genetic parameters controlling organism behavior:

```json
{
  // Reproduction timing
  "LayTime": number,                    // Time to lay eggs
  "BroodTime": number,                  // Brooding duration
  "HatchTime": number,                  // Hatching time
  
  // Physical properties
  "SizeRatio": number,                  // Size scaling factor
  "SpeedRatio": number,                 // Movement speed scaling
  "ColorR": number,                     // Red color component [0-1]
  "ColorG": number,                     // Green color component [0-1] 
  "ColorB": number,                     // Blue color component [0-1]
  
  // Mutation parameters
  "MutationAmountSigma": number,        // Genetic mutation variance
  "AverageMutationNumber": number,      // Expected mutations per generation
  "BrainMutationSigma": number,         // Neural mutation variance
  "BrainAverageMutation": number,       // Expected brain mutations
  
  // Sensory capabilities
  "ViewAngle": number,                  // Field of view in degrees
  "ViewRadius": number,                 // Vision range
  "ClockSpeed": number,                 // Internal timing rate
  "PheroSense": number,                 // Pheromone sensitivity range
  
  // Behavioral parameters
  "Diet": number,                       // Dietary preference [0-1]
  "HerdSeparationWeight": number,       // Flocking behavior weights
  "HerdAlignmentWeight": number,        
  "HerdCohesionWeight": number,
  "HerdVelocityWeight": number,
  "HerdSeparationDistance": number,
  
  // Growth and development
  "GrowthScale": number,                // Growth rate scaling
  "GrowthMaturityFactor": number,       // Maturity growth influence
  "GrowthMaturityExponent": number,     // Maturity curve shape
  "EyeOffset": number,                  // Visual system positioning
  
  // Resource allocation (WAG = Weight Allocation Gene)
  "StomachWAG": number,                 // Digestive system investment
  "WombWAG": number,                    // Reproductive system investment
  "FatWAG": number,                     // Energy storage investment  
  "ArmorWAG": number,                   // Defense investment
  "ThroatWAG": number,                  // Feeding apparatus investment
  "MouthMusclesWAG": number,            // Bite strength investment
  "MoveMusclesWAG": number,             // Locomotion investment
  
  // Energy management
  "FatStorageThreshold": number,        // Energy storage trigger point
  "FatStorageDeadband": number          // Storage hysteresis range
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