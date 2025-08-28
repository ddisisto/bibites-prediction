# Bibites Neural Network Node Behavior Reference

## Overview
This document provides comprehensive behavioral specifications for all neural network node types in The Bibites game, extracted from BibitesAssembly.dll and cross-referenced with template analysis. This reference is essential for accurate prediction system development and understanding of organism behaviors.

## Extraction Metadata
- **Source**: BibitesAssembly.dll from The Bibites game installation
- **Game Version**: 0.6.2.1 (inferred from template analysis)
- **Extraction Date**: August 28, 2025
- **Extraction Method**: `strings -e l` Unicode string extraction
- **Total Tooltip Strings Extracted**: 46 primary descriptions

## Node Type Classification

### Type 0: Input/Sensor Nodes
Input nodes provide environmental and internal state information to the neural network. All input nodes output values in specific ranges with defined normalization schemes.

#### Basic Physical State Inputs
- **EnergyRatio**: "Outputs the current energy level"
  - Range: [0.0, 1.0] (normalized to maximum energy)
  - Critical for survival behaviors and energy management

- **Maturity**: "Outputs the bibite's current maturity (a value of 1.0 is reached when it can reproduce/lay eggs)"
  - Range: [0.0, 1.0] 
  - Key threshold: 1.0 = reproductive capability achieved

- **LifeRatio**: "Outputs the bibite's current health (HP / maxHP)"
  - Range: [0.0, 1.0] (current health normalized to maximum health)
  - Essential for damage assessment and survival responses

- **Fullness**: "Outputs how full the bibite's stomach is"
  - Range: [0.0, 1.0] (stomach capacity utilization)
  - Critical for feeding behavior and hunger responses

#### Movement and Action State Inputs
- **Speed**: "Outputs the bibite's current forward speed (normalized for its body length) (negative value means it's going backward to where it's facing"
  - Range: Unbounded, body-length normalized
  - Directional: Positive = forward, Negative = backward
  - Accounts for bibite size differences

- **RotationSpeed**: "Outputs the bibite's current angular speed (normalized to full rotations per second) (positive values mean clockwise rotation, while negative means counterclockwise)"
  - Range: Unbounded rotations per second
  - Directional: Positive = clockwise, Negative = counterclockwise
  - Temporal normalization to per-second basis

- **IsGrabbing**: "Outputs whether the bibite is currently grabbing (1.0) or not (0.0) an object"
  - Range: Binary [0.0, 1.0]
  - State indicator for grab mechanism activation

#### Damage and Health Inputs
- **AttackedDamage**: "Outputs the normalized pain of the bibite (attacked damages it received recently (decaying exponentially) / maxHP)"
  - Range: [0.0, 1.0+] (can exceed 1.0 for severe damage)
  - Temporal decay: Exponential reduction over time
  - Pain/damage awareness for defensive behaviors

#### Reproduction Inputs
- **EggStored**: "Outputs the number of completed eggs stored in the bibite's egg organ"
  - Range: [0, unlimited integer count]
  - Directly relates to reproductive capacity and laying behaviors

#### Environmental Perception - Bibite Detection
- **BibiteCloseness**: "Outputs how close (normalize to its view radius) in its field of view the weighted average of bibites is"
  - Range: [0.0, 1.0] (normalized to view radius)
  - Aggregation: Weighted average of all visible bibites
  - Field of view constraint applies

- **BibiteAngle**: "Outputs the angle (normalized to its view angle) in its field of view the weighted average of bibites is"
  - Range: [-1.0, 1.0] (normalized to view angle)
  - Directional: Based on weighted average position
  - Field of view constraint applies

- **NBibites**: "Outputs the number of bibites in its field of view divided by 4"
  - Range: [0.0, unlimited] (count/4)
  - Scaling factor: Division by 4 for normalization
  - Population density indicator

#### Environmental Perception - Plant Detection
- **PlantCloseness**: "Outputs how close (normalize to its view radius) in its field of view the weighted average of plant pellets is"
  - Range: [0.0, 1.0] (normalized to view radius)
  - Aggregation: Weighted average of all visible plant pellets
  - Food source proximity for herbivorous behaviors

- **PlantAngle**: "Outputs the angle (normalized to its view angle) in its field of view the weighted average of plant pellets is"
  - Range: [-1.0, 1.0] (normalized to view angle)
  - Directional guidance for plant approach behaviors

- **NPlants**: "Outputs the number of plant pellets in its field of view divided by 4"
  - Range: [0.0, unlimited] (count/4)
  - Food availability assessment

#### Environmental Perception - Meat Detection
- **MeatCloseness**: "Outputs how close (normalize to its view radius) in its field of view the weighted average of meat pellets is"
  - Range: [0.0, 1.0] (normalized to view radius)
  - Carnivorous/scavenging behavior input

- **MeatAngle**: "Outputs the angle (normalized to its view angle) in its field of view the weighted average of meat pellets is"
  - Range: [-1.0, 1.0] (normalized to view angle)
  - Directional guidance for meat approach

- **NMeats**: "Outputs the number of meat pellets in its field of view divided by 4"
  - Range: [0.0, unlimited] (count/4)
  - Protein source availability indicator

#### Social/Genetic Detection
- **RedBibite**: "Outputs the Red Color Gene of the closest seen bibite"
  - Range: [0.0, 1.0] (gene value from closest bibite)
  - Genetic compatibility/recognition mechanism

- **GreenBibite**: "Outputs the Green Color Gene of the closest seen bibite"
  - Range: [0.0, 1.0] (gene value from closest bibite)
  - Color-based identification system

- **BlueBibite**: "Outputs the Blue Color Gene of the closest seen bibite"
  - Range: [0.0, 1.0] (gene value from closest bibite)
  - Completes RGB genetic signature detection

#### Chemical Communication - Pheromone Detection
- **PheroSense1** (Red): "Outputs the perceived prevalence of red pheromones"
  - Saturation Behavior: "Outputs saturates for strong activations"
  - Range: [0.0, 1.0+] with saturation clipping
  - Chemical trail detection for red pheromone category

- **Phero1Angle** (Red): "Outputs the normalized angle to the perceived source of red pheromones"
  - Range: [-1.0, 1.0] (normalized angle)
  - Directional guidance to pheromone source

- **Phero1Heading** (Red): "Outputs the normalized angle to the perceived direction of red pheromones gradient (following the trail)"
  - Range: [-1.0, 1.0] (normalized angle)
  - Trail-following behavior (gradient following vs. source seeking)

- **PheroSense2** (Green): "Outputs the perceived prevalence of green pheromones"
  - Saturation Behavior: "Outputs saturates for strong activations"
  - Identical behavior to red pheromones, different chemical

- **Phero2Angle** (Green): "Outputs the normalized angle to the perceived source of green pheromones"
  - Range: [-1.0, 1.0] (normalized angle)

- **Phero2Heading** (Green): "Outputs the normalized angle to the perceived direction of green pheromones gradient (following the trail)"
  - Range: [-1.0, 1.0] (normalized angle)

- **PheroSense3** (Blue): "Outputs the perceived prevalence of blue pheromones"
  - Saturation Behavior: "Outputs saturates for strong activations"
  - Third pheromone category for complex chemical communication

- **Phero3Angle** (Blue): "Outputs the normalized angle to the perceived source of blue pheromones"
  - Range: [-1.0, 1.0] (normalized angle)

- **Phero3Heading** (Blue): "Outputs the normalized angle to the perceived direction of blue pheromones gradient (following the trail)"
  - Range: [-1.0, 1.0] (normalized angle)

### Type 3: Output/Action Nodes
Output nodes directly control bibite behaviors and actions. Most have activation thresholds and specific behavioral responses to positive/negative activation.

#### Basic Movement Controls
- **Accelerate**: "Controls how strongly the bibite accelerates forward (or backward, with a penalty, when negatively activated)"
  - Activation: Positive = forward acceleration, Negative = backward (with penalty)
  - Force scaling based on activation strength
  - Movement efficiency penalty for reverse movement

- **Rotate**: "Controls how strongly the bibite turn (negative activation applies torque to turn left, while positive activation result in clockwise torque)"
  - Directional Control: Negative = left turn, Positive = right turn (clockwise)
  - Torque strength scales with absolute activation value

#### Reproductive Controls
- **EggProduction**: "Controls how much active the bibite's egg organ is. At full activation (1.0), the bibite will produce eggs at an interval equal to its LayTime gene"
  - Range: [0.0, 1.0] for normal operation
  - Genetic Linkage: Production rate tied to LayTime gene
  - Negative Effect: "Negative activation instead reabsorbs the stored eggs (with an energy penalty)"

- **EggLaying**: "Controls whether the bibite will lay its stored eggs"
  - Activation Threshold: "Any activation >= 0.25 will cause stored eggs to be laid"
  - Binary behavior with clear threshold

#### Feeding and Digestion Controls
- **Want2Eat**: "Controls the bibite's mouth opening and whether it wants to swallow objects that can fit in the opening"
  - Positive Activation: Mouth opening and swallowing behavior
  - Negative Activation: "Negative activation will instead result in the bibite vomiting the stomach's content that can fit through the opening"
  - Threshold: "Any absolute activation < 0.15 will result in the bibite not swallowing/vomitting anything"

- **Digestion**: "Controls the bibite's stomach acid level, controlling how fast the content is being digested."
  - Efficiency Trade-off: "Faster digestion produces more energy, but is less efficient"
  - Metabolic control mechanism

#### Physical Interaction Controls  
- **Grabbing**: "Controls the bibite's grab strength"
  - Activation Behavior: "If activated, any object newly entering the mouth will be grabbed"
  - Negative Activation: "Sudden negative activation will result in grabbed objects instead being thrown"
  - Force Distribution: "Stronger activation makes the hold on more tightly, or throw object more violently, but Force is always distributed across all held/thrown objects"
  - Threshold: "Any absolute activation < 0.15 will result in the bibite not grabbing/throwing anything"

- **AttackClosest**: "Controls the bibite's bite strength"
  - Attack Behavior: "If activated, the bibite will try to bite any object that is already present in its mouth or that newly enters it"
  - Continuous Attack: "If it was already attacking the target (successfully did so last Tic), it will instead continue the bite without needing to wait the bite period and drain/suck the target (like a mosquito)"
  - Threshold: "Any activation < 0.15 will result in the bibite not attacking anything"

#### Chemical Communication Controls
- **PheroEmit1** (Red): "Controls the bibite's red pheromones production"
  - Chemical trail laying for red pheromone category

- **PheroEmit2** (Green): "Controls the bibite's green pheromones production"
  - Independent green pheromone control

- **PheroEmit3** (Blue): "Controls the bibite's blue pheromones production"
  - Blue pheromone emission control

#### Biological Process Controls
- **Growth**: "Controls the bibite's growth speed"
  - Activation Range: "An activation of 0.0 results in no growth at all, while a value of 1.0 lets growth follow the bibite's natural growth curve"
  - Growth curve controlled by genetic parameters

- **Healing**: "Controls the bibite's healing process"
  - Health restoration mechanism
  - Likely energy-consuming when activated

#### Advanced Social Behaviors
- **Herding**: "Gradually overrides the bibite's default movement behavior (Accelerate and Rotate nodes) to follow the other seen bibites based on its herding genes"
  - Movement Override: "An activation of 0.0 will leave movement unchanged, but as the activation increases, will gradually replace them with herding behavior. A value of 1.0 meaning the movement completely follows the herding behavior"
  - Negative Behavior: "Negative activation behaves similarly but instead replaces default movement with the opposite of what the herding genes dictates"
  - Genetic Dependency: Behavior depends on herding-related genes

### Types 1-2: Basic Hidden Processing Nodes
Standard hidden layer nodes with activation functions for neural processing.

#### Activation Functions Available:
- **Sigmoid**: "output = sigmoid(x) of the full activation"
  - Characteristics: "Useful if signal needs to be capped between [0.0, 1.0]. The downside is that the unactivated output is 0.5"
  - Range: [0.0, 1.0]

- **TanH**: "output = tanH(x) of the full activation" 
  - Characteristics: "Useful if a signal need to taper-off and be capped between [-1f, 1f]"
  - Range: [-1.0, 1.0]

- **Linear**: "output = the sum of the activations"
  - Characteristics: "Useful if no transformation of signals is desired"
  - Usage: "Can be used as an OR gate"
  - Range: Unbounded

- **ReLU**: Standard Rectified Linear Unit activation
  - Range: [0, unlimited]

### Types 4-13: Specialized Hidden Nodes
Advanced processing nodes with specific behavioral functions for complex neural operations.

#### Mathematical Operations
- **Absolute (Type 4)**: "output = abs(x) of the full activation"
  - Purpose: "Useful if no transformation of signals is desired aside from turning negatives into positive"
  - Range: [0, unlimited]

- **Gaussian (Type 5)**: "output = 1/(x^2 +1) of total activation"
  - Purpose: "Useful for inverting a signal, or defining a band of activation, since a total activation of 0 will result in an output of 1.0, but any activation (both positive or negative) will make it gradually go down to 0"
  - Behavior: Bell-curve response with maximum at zero input
  - Range: (0.0, 1.0]

- **Sinusoidal (Type 6)**: "output = sin(x) of the full activation"
  - Purpose: "Useful to generate periodic responses"
  - Range: [-1.0, 1.0]
  - Enables oscillatory behaviors

#### Temporal Processing
- **Differential (Type 7)**: "output = rate of change of total activation"
  - Purpose: "Useful to differentiate a signal, and receive its rate of change. As an example, inputting the plantCloseness would mean the output equals the rate at which the plant is getting closer."
  - Initial Behavior: "Since the node's bias doesn't change during lifetime, it will only result in an output on the bibite's first tic of life"
  - Range: Unbounded (rate values)

- **Inhibitory (Type 8)**: "The output will behave similarly to the differential, but will return toward 0 more gradually as the input remains stable"
  - Bias Control: "The bias is used to regulate how quickly the node self-inhibits"
  - Purpose: "Useful to produce acclimating behaviors"
  - Adaptation mechanism for sensory habituation

- **Integrator (Type 9)**: "The output will be the sum of the previous output and the total activation over the last tick period (y = y + x/TPS)."
  - Mathematical Form: Discrete integration over time
  - Purpose: "Useful for multiple things like memory, counting, averaging, etc. Anything that requires keeping track of a progress"
  - Accumulative behavior over time

#### Memory and State
- **Latch (Type 10)**: Binary memory with hysteresis
  ```
  output = 
      1.0 if x >= 1.0 
      0.0 if x <= 0.0
      its last output otherwise
  ```
  - Purpose: "Useful for binary memory or as a Trigger/Reset for a behavior, as it acts as a switch (either ON or OFF)"
  - State persistence between clear thresholds

- **SoftLatch (Type 11)**: "The output will tend to keep its last value, the full activation needs to differ significantly to alter the output."
  - Bias Control: "The bias is used to instead control the hysteresis (resistance to change) of the node"
  - Behavior Spectrum: "A low bias makes the node essentially linear, but the closer it'll be to the Latch function as the bias increases"
  - Purpose: "Useful for memory, or to smooth out noise"
  - Analog memory with adjustable persistence

## Cross-Reference with Template Analysis

### Node Type Distribution in Templates
From analysis of 70+ templates, the following patterns emerge:

#### Type 0 (Input) - Standard Sensors Found
- Energy/health monitoring: EnergyRatio, LifeRatio, Maturity, Fullness
- Movement sensing: Speed, RotationSpeed, IsGrabbing
- Damage detection: AttackedDamage
- Environmental detection: BibiteCloseness, PlantCloseness, MeatCloseness
- Chemical sensing: PheroSense1-3, Phero1-3Angle
- Time awareness: Tic, Minute, TimeAlive (temporal nodes confirmed)

#### Type 3 (Output) - Action Controls Found
- Basic movement: Accelerate, Rotate (confirmed as primary movement system)
- Feeding: Want2Eat, Digestion
- Reproduction: EggProduction, EggLaying
- Combat: AttackClosest
- Chemical: PheroEmit1-3
- Physical: Grabbing
- Biological: Growth, Healing
- Social: Herding

#### Specialized Nodes (Types 4-13) Usage
- Template analysis shows Types 4-11 are used for complex behavioral circuits
- Type 12-13 exist in templates but tooltips not yet fully extracted
- Memory nodes (Integrator, Latch, SoftLatch) commonly used for behavioral state machines

## Behavioral Specifications Summary

### Critical Thresholds
- **Binary Actions**: 0.15 minimum activation for Grabbing, AttackClosest, Want2Eat
- **Egg Laying**: 0.25 minimum activation threshold
- **Memory Latches**: 1.0 for set, 0.0 for reset

### Normalization Conventions
- **Spatial**: Distances normalized to view radius [0.0, 1.0]
- **Angular**: Angles normalized to view angle [-1.0, 1.0] 
- **Temporal**: Speeds normalized per second
- **Biological**: Health, energy, maturity as ratios [0.0, 1.0]
- **Population**: Counts divided by 4 for normalization

### Directional Conventions
- **Rotation**: Positive = clockwise, Negative = counterclockwise
- **Movement**: Positive = forward, Negative = backward
- **Spatial**: Standard coordinate system with normalized ranges

### Saturation Behaviors
- Pheromone sensors saturate for strong activations
- Output ranges may be clipped to prevent overflow
- Some nodes (Gaussian) have natural saturation curves

## Implementation Notes for Prediction System

### Feature Engineering Considerations
1. **Input Normalization**: All input nodes provide pre-normalized values
2. **Threshold Awareness**: Binary behaviors require threshold modeling
3. **Temporal Dependencies**: Differential and integrator nodes have frame-rate dependencies
4. **Memory State**: Latch-type nodes require state persistence modeling
5. **Activation Functions**: Neural processing depends on node-specific functions

### Behavioral Pattern Recognition
1. **Survival Circuits**: Monitor EnergyRatio, LifeRatio, Fullness combinations
2. **Feeding Behaviors**: Track Want2Eat, Digestion, proximity sensor correlations
3. **Reproductive Strategies**: EggProduction, EggLaying activation patterns
4. **Social Behaviors**: Herding interactions with movement controls
5. **Combat Responses**: AttackClosest triggers and damage sensor feedback

### Validation Opportunities
1. **Range Verification**: Confirm template node activations match specified ranges
2. **Threshold Testing**: Validate binary behavior activation thresholds
3. **Function Consistency**: Ensure activation functions match extracted specifications
4. **Temporal Accuracy**: Verify time-dependent node behaviors in simulations

---

*This reference provides the foundation for accurate behavioral modeling in the Bibites prediction system. Regular updates should be made as new game versions are released or additional tooltip data is discovered.*