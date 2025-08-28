# Bibites Genetic Parameter Behavior Reference

## Overview
This document provides comprehensive behavioral specifications for all genetic parameters in The Bibites game, extracted from BibitesAssembly.dll and cross-referenced with template analysis. This reference is essential for understanding organism traits, evolutionary dynamics, and building accurate prediction models.

## Extraction Metadata
- **Source**: BibitesAssembly.dll from The Bibites game installation
- **Game Version**: 0.6.2.1 (inferred from template analysis)
- **Extraction Date**: August 28, 2025
- **Extraction Method**: `strings -e l` Unicode string extraction with genetic parameter filtering
- **Template Cross-Reference**: format-schema.md genetic parameter analysis

## Genetic Parameter Classification

### WAG System: Weighted Apportionment Genes
The WAG system governs internal organ allocation, representing competition for limited internal body area. All WAG values compete against each other, creating evolutionary trade-offs.

#### Digestive System
- **StomachWAG**: "Stomach WAG (Weighted Apportionment Gene) determines the share of the bibite's internal area that's dedicated to the stomach."
  - **Function**: Determines digestive capacity and food processing capability
  - **Trade-offs**: Larger stomach enables more food storage but reduces space for other organs
  - **Metabolic Impact**: Affects efficiency of nutrient extraction and feeding frequency requirements

#### Reproductive System  
- **WombWAG** (Egg Organ WAG): "Egg Organ WAG (Weighted Apportionment Gene) determines the share of the bibite's internal area that's dedicated to the egg organ."
  - **Function**: Controls reproductive capacity and egg storage capability
  - **Trade-offs**: Larger egg organ enables more reproductive potential but reduces other organ space
  - **Timing Dependency**: Works in conjunction with LayTime, BroodTime, and HatchTime genes

#### Energy Storage System
- **FatWAG** (Fat Organ WAG): "Fat Organ WAG (Weighted Apportionment Gene) determines the share of the bibite's internal area that's dedicated to fat storage."
  - **Function**: Determines energy storage capacity for survival during resource scarcity
  - **Trade-offs**: Larger fat storage provides survival buffer but reduces immediate functionality
  - **Energy Management**: Interacts with FatStorageThreshold and FatStorageDeadband genes

#### Defense System
- **ArmorWAG**: "Armor WAG (Weighted Apportionment Gene) determines the share of the bibite's internal area that's dedicated to armor. Armor protects the bibite from attacks by creating a harder layer that is harder to break the thicker it is."
  - **Function**: Provides damage protection through hardened outer layer
  - **Protection Mechanics**: Thickness directly correlates with damage resistance
  - **Trade-offs**: Defense capability versus mobility and other organ development

#### Feeding Apparatus
- **ThroatWAG**: "Throat WAG (Weighted Apportionment Gene) determines the share of the bibite's internal area that's dedicated to their throat. A Larger throat makes it possible to take bigger bites and swallow larger chunks of matters. Larger throat/mouths also means a longer bite period, meaning bibites will have to wait longer before after taking a bite."
  - **Function**: Controls bite size and swallowing capacity
  - **Performance Trade-off**: Larger throat = bigger bites BUT longer bite periods
  - **Feeding Efficiency**: Affects feeding speed and chunk processing capability

- **MouthMusclesWAG** (Jaw Muscles WAG): "Jaw Muscles WAG (Weighted Apportionment Gene) determines the share of the bibite's internal area that's dedicated to their jaw muscles. Bigger jaw muscles allows them to apply larger forces when biting, and taking bigger bites proportionally, or dealing more damages."
  - **Function**: Determines bite force and damage capability
  - **Combat Application**: Directly affects attack damage output
  - **Feeding Benefit**: Enables processing tougher food materials

#### Locomotion System
- **MoveMusclesWAG** (Arm Muscles WAG): "Arm Muscles WAG (Weighted Apportionment Gene) determines the share of the bibite's internal area that's dedicated to their arm muscles. Larger arm muscles makes them more powerful and allows them to move faster."
  - **Function**: Controls movement speed and physical power
  - **Performance**: Direct correlation with acceleration and maximum speed
  - **Energy Scaling**: Larger muscles provide more power but increase metabolic costs

### Physical Properties and Scaling

#### Size and Metabolism
- **SizeRatio**: "The relative size of the bibite (1D, length). This increases the metabolism (energy cost each second) of the bibite, as well as many other dynamics."
  - **Scaling**: One-dimensional length scaling affecting multiple systems
  - **Metabolic Cost**: Larger size increases baseline energy consumption
  - **System Impact**: Affects movement, health, organ capacity, and resource requirements

- **SpeedRatio** (Metabolism Speed): "The relative metabolic activity of the bibite. This increases digestive activities, movement, etc., but also increases the default sustenance cost (energy/s) and energy expanses of the bibite."
  - **Function**: Controls overall metabolic rate and activity speed
  - **Performance Benefits**: Faster digestion, quicker movement, accelerated biological processes
  - **Energy Trade-off**: Higher speed increases all energy consumption rates
  - **Temporal Effects**: Affects LayTime scaling: "This also scales with the bibite's metabolic speed, so a bibite with a metabolism speed gene of 0.5 would take twice as long to produce the egg."

#### Coloration System
- **ColorR**: "The amount of red pigments in the bibite's skin."
  - **Range**: [0.0, 1.0] (red color component)
  - **Function**: Genetic identification and recognition by other bibites
  - **Social Mechanics**: Enables kin recognition and species identification

- **ColorG**: "The amount of green pigments in the bibite's skin."
  - **Range**: [0.0, 1.0] (green color component)
  - **Recognition**: Part of RGB genetic signature system

- **ColorB**: "The amount of blue pigments in the bibite's skin."
  - **Range**: [0.0, 1.0] (blue color component)
  - **Completion**: Completes RGB genetic identification system

- **EyeOffset** (Eye Hue Offset): "The hue shift of the bibite's eyes compared to it's body color"
  - **Function**: Visual variation system independent of body color
  - **Aesthetic**: Creates individual visual identity within species

### Sensory Capabilities

#### Vision System
- **ViewRadius**: "The distance up to which bibites can see"
  - **Function**: Determines maximum visual detection range
  - **Energy Cost**: "The Base Body Growth Cost each unit of body (u²) is increased by an amount proportional to the view radius multiplied by this setting"
  - **Performance**: Larger view radius enables better environment awareness but increases growth costs

- **ViewAngle**: "The bibite's field of view."
  - **Function**: Determines width of visual field
  - **Energy Cost**: "The Base Body Growth Cost each unit of body (u²) is increased by an amount proportional to the view angle multiplied by this setting"
  - **Trade-off**: Wider vision provides better awareness but increases development costs

#### Chemical Sensing
- **PheroSense** (Pheromone Sensing Radius): "Influences the distance at which the bibite can sense pheromone, as well as how much they will respond to it."
  - **Function**: Controls pheromone detection capability and sensitivity
  - **Dual Impact**: Affects both detection range AND response intensity
  - **Chemical Communication**: Enables complex social behaviors and territory marking

#### Temporal Processing
- **ClockSpeed** (Internal Clock Period): "The period of the internal clock in the bibite's brain. Influences a few senses related to time."
  - **Function**: Controls internal timing system and temporal perception
  - **Neural Integration**: "Toggles between 0.0 and 1.0 periodically based on the bibite's clock rate gene (1s by default)"
  - **Behavioral Timing**: Affects circadian-like behaviors and temporal pattern recognition

### Behavioral Parameters

#### Dietary Preferences
- **Diet**: "Decides what kind of food is best suited to the Bibite. 0 means completely herbivorous, 1 means completely carnivorous, omnivory will depend on the parameters of the respective food source."
  - **Range**: [0.0, 1.0] (herbivore to carnivore spectrum)
  - **Function**: Determines optimal food type and digestion efficiency
  - **Metabolic Efficiency**: "Maximum efficiency when digesting with maximum affinity (ex: carnivore eating meat)"
  - **Flexibility**: Omnivory possible with intermediate values

#### Social Behaviors: Herding Parameters
- **HerdSeparationWeight**: "The weight controlling how much the separation rule is applied for the herd. This rule tries to prevent the bibites from bumping into one another."
  - **Function**: Controls personal space maintenance in groups
  - **Anti-collision**: Prevents overcrowding and physical interference
  - **Flocking Behavior**: Part of Reynolds flocking model implementation

- **HerdAlignmentWeight**: "The weight controlling how much the alignment rule is applied for the herd. This rule tries to align the herd so all bibites head in the same direction."
  - **Function**: Controls directional coordination in groups
  - **Movement Synchronization**: Enables coordinated group movement
  - **Leadership Dynamics**: Higher values create stronger following behaviors

- **HerdCohesionWeight**: Standard Reynolds flocking cohesion rule (inferred from template analysis)
  - **Function**: Controls attraction to group center
  - **Group Stability**: Prevents group fragmentation
  - **Social Bonding**: Maintains group integrity during movement

- **HerdVelocityWeight**: Advanced herding parameter (extracted from strings)
  - **Function**: Controls velocity matching within herds
  - **Speed Coordination**: Enables groups to move at coordinated speeds

- **HerdSeparationDistance**: "The distance bibites will try to keep between them in a herd. A regular bibite usually measures 10u."
  - **Reference Scale**: Standard bibite measures ~10 units
  - **Function**: Defines optimal spacing within groups
  - **Size Scaling**: May scale with individual bibite size

### Reproductive and Developmental Systems

#### Reproductive Timing
- **LayTime**: "Default time it takes a bibites to produce an egg if its egg production node is fully activated. This also scales with the bibite's metabolic speed, so a bibite with a metabolism speed gene of 0.5 would take twice as long to produce the egg."
  - **Function**: Controls egg production duration
  - **Metabolic Interaction**: Inversely scales with SpeedRatio gene
  - **Energy Dependency**: Requires sustained EggProduction neural activation
  - **Reproductive Strategy**: Longer times may produce higher quality offspring

- **BroodTime**: "Used in a formula to determine the bibite's maturity at birth (hatchTime/broodTime). A higher brood time will cause bibites to be born smaller. This gene used to be more consequential but is now only used in the maturity at birth formula."
  - **Function**: Influences newborn development level
  - **Maturity Formula**: Birth maturity = hatchTime/broodTime
  - **Size Impact**: Higher brood time = smaller newborns
  - **Legacy Parameter**: Reduced functionality in current game version

- **HatchTime**: "Time it takes for the egg to hatch. It's also used to calculate how developed the newborn will be when hatching. A longer hatch times usually cost more energy but makes the newborn's survival more likely."
  - **Function**: Controls egg incubation period
  - **Development Trade-off**: Longer incubation = more developed offspring
  - **Energy Cost**: Extended development requires more energy investment
  - **Survival Strategy**: Better developed offspring have higher survival rates

#### Growth and Development
- **GrowthScale** (Growth Scale Factor): "The genetic value influencing the scale of the growth function."
  - **Function**: Controls overall growth rate scaling
  - **Growth Curve**: "The bibite's growth curve as it matures. Defines how fast the bibite will grow and develop over its lifetime."
  - **Neural Interaction**: Works with Growth neural node activation

- **GrowthMaturityFactor**: "The genetic value influencing the impact of maturity on growth."
  - **Function**: Controls how maturity level affects growth rate
  - **Development**: Links growth speed to reproductive readiness
  - **Life Stage**: Affects growth patterns throughout development

- **GrowthMaturityExponent**: "The genetic value determining the exponent of maturity's influence on growth."
  - **Function**: Controls nonlinearity in maturity-growth relationship
  - **Curve Shaping**: Determines whether growth accelerates or decelerates with maturity
  - **Mathematical**: Exponential scaling of maturity impact

### Energy Management Systems

#### Fat Storage Control
- **FatStorageThreshold**: "The energy ratio that will be considered a neutral point for fat storage/retrieval."
  - **Function**: Sets energy level trigger for fat metabolism
  - **Range**: [0.0, 1.0] energy ratio threshold
  - **Storage Logic**: Above threshold = store fat, below threshold = use fat
  - **Metabolic Strategy**: Controls when to switch between storage and consumption

- **FatStorageDeadband**: "The delta energy ratio around the neutral point (threshold) where fat storage/retrieval will not be activated."
  - **Function**: Creates hysteresis around storage threshold
  - **Stability**: Prevents rapid switching between storage/retrieval states
  - **Efficiency**: Reduces metabolic oscillation and energy waste
  - **Control Theory**: Deadband prevents system instability

### Mutation and Evolution Parameters

#### Genetic Mutation System
- **MutationAmountSigma** (Gene Mutation Variance): "The standard deviation of the amount of change on mutations in genes. Expressed in fraction of the total gene span, but a portion (based on the 'Mutation Value Relativity' parameter) will be scaled to the present value of the gene."
  - **Function**: Controls magnitude of genetic changes during mutation
  - **Statistical**: Standard deviation of mutation distribution
  - **Scaling**: Combines absolute and relative mutation components
  - **Evolutionary**: Determines evolutionary step size

- **AverageMutationNumber** (Average Gene Mutations): "The average number of mutations that occurs in every generations."
  - **Function**: Controls frequency of genetic changes
  - **Generational**: Expected mutations per reproduction cycle
  - **Evolutionary Pressure**: Higher values increase evolutionary speed
  - **Population Genetics**: Affects fixation rates and diversity

#### Neural Network Mutation System  
- **BrainMutationSigma** (Brain Mutation Variance): "The standard deviation of the amount of change on mutations in the brain. Expressed in fraction of the total gene span, but a portion (based on the 'Mutation Value Relativity' parameter) will be scaled to the present value of the gene."
  - **Function**: Controls magnitude of neural network changes
  - **Network Evolution**: Affects synapse weights, node parameters, and topology
  - **Behavioral**: Directly impacts behavioral evolution rate
  - **Complexity**: Enables evolution of complex neural architectures

- **BrainAverageMutation** (Average Brain Mutations): "The average number of brain mutations that occurs in every generations."
  - **Function**: Controls frequency of neural network modifications
  - **Cognitive Evolution**: Determines rate of behavioral adaptation
  - **Learning**: Balances stability versus adaptability in neural networks
  - **Population**: Affects behavioral diversity within populations

## Cross-Reference with Template Analysis

### Genetic Parameter Ranges from Templates
From analysis of 70+ template organisms, genetic parameters show these empirical ranges:

#### WAG System Competition
- All WAG values compete for total internal area allocation
- Typical WAG distributions show clear trade-offs between systems
- High StomachWAG often correlates with herbivorous diet values
- High MouthMusclesWAG and ArmorWAG associated with carnivorous builds
- MoveMusclesWAG varies widely based on survival strategy

#### Physical Scaling Patterns
- SizeRatio values cluster around species-typical sizes
- SpeedRatio shows bimodal distribution (slow/efficient vs. fast/expensive)
- Color genes show full spectrum utilization for genetic identification

#### Sensory Capability Distribution
- ViewRadius values correlate with ecological niche (predator vs. prey)
- ViewAngle shows trade-offs between awareness and energy costs
- PheroSense values indicate varying reliance on chemical communication

#### Reproductive Strategy Clusters
- LayTime, BroodTime, HatchTime show coordinated patterns
- Fast reproduction (low times) vs. quality offspring (high times)
- GrowthScale parameters cluster around optimal development curves

### Evolutionary Implications

#### WAG System Trade-offs
The WAG system creates fundamental evolutionary constraints:

1. **Digestive vs. Locomotive**: StomachWAG vs. MoveMusclesWAG trade-offs
2. **Defense vs. Offense**: ArmorWAG vs. MouthMusclesWAG competition
3. **Current vs. Future**: FatWAG vs. WombWAG (survival vs. reproduction)
4. **Feeding Efficiency**: ThroatWAG trade-offs (bigger bites vs. bite frequency)

#### Metabolic Scaling Laws
Size and speed genes create metabolic scaling relationships:

- **Size Cost**: "This increases the metabolism (energy cost each second) of the bibite"
- **Speed Cost**: "increases the default sustenance cost (energy/s) and energy expanses"
- **Vision Cost**: View parameters increase growth and maintenance costs
- **Neural Cost**: Brain complexity adds upkeep energy requirements

#### Mutation Rate Evolution
Mutation parameters can themselves evolve:

- **Adaptive Mutation**: Higher mutation rates in unstable environments
- **Conservatism**: Lower mutation rates when adapted to stable niches
- **Brain vs. Body**: Different mutation rates for neural vs. genetic systems
- **Generational Memory**: Mutation parameters carry environmental history

## Behavioral Specifications Summary

### Critical Gene Interactions

#### Survival Circuit Integration
1. **Energy Management**: FatStorageThreshold + FatStorageDeadband + FatWAG
2. **Feeding Efficiency**: Diet + StomachWAG + ThroatWAG + MouthMusclesWAG
3. **Locomotion Performance**: SpeedRatio + SizeRatio + MoveMusclesWAG
4. **Defensive Capability**: ArmorWAG + Size scaling + SizeRatio

#### Reproductive Success Factors
1. **Timing Optimization**: LayTime + BroodTime + HatchTime coordination
2. **Energy Investment**: WombWAG + reproductive timing parameters
3. **Offspring Quality**: HatchTime investment vs. energy costs
4. **Developmental Programming**: Growth genes + maturity factors

#### Social Behavior Architecture
1. **Herding Coordination**: HerdSeparationWeight + HerdAlignmentWeight + HerdCohesionWeight
2. **Chemical Communication**: PheroSense + pheromone neural outputs
3. **Recognition Systems**: ColorR/G/B + genetic identification
4. **Group Dynamics**: Herding parameters + individual behavioral variations

### Metabolic Cost Relationships

#### Base Costs (from game settings extraction)
- **Size Scaling**: "Default energy cost that a bibite have to burn for each units of area (u²) to stay alive"
- **Speed Scaling**: Costs scale "proportionally" with SpeedRatio gene
- **Vision Costs**: ViewRadius and ViewAngle add to growth costs
- **Neural Costs**: Brain complexity increases upkeep requirements

#### Energy Efficiency Trade-offs
- **Fast Digestion**: "Faster digestion produces more energy, but is less efficient"
- **Movement Efficiency**: Backward movement has "penalty" compared to forward
- **Growth Investment**: Energy costs for development vs. immediate survival
- **Fat Storage**: "What percentage of the stored Fat energy does the bibite need to expand to sustain it"

## Implementation Notes for Prediction System

### Feature Engineering Priorities

#### High-Impact Genetic Features
1. **WAG Ratios**: Relative organ allocations more important than absolute values
2. **Metabolic Scaling**: SizeRatio * SpeedRatio interactions for energy costs
3. **Reproductive Timing**: LayTime/HatchTime ratios for offspring quality
4. **Sensory Investment**: ViewRadius * ViewAngle for awareness capability

#### Evolutionary Constraint Modeling
1. **WAG Conservation**: Sum of all WAG values represents allocation constraints
2. **Energy Balance**: Metabolic costs vs. energy acquisition capabilities
3. **Development Trade-offs**: Growth investment vs. immediate survival needs
4. **Mutation Load**: Mutation rates vs. population fitness landscapes

#### Behavioral Pattern Recognition
1. **Feeding Strategies**: Diet + digestive WAG combinations
2. **Survival Strategies**: Armor + fat storage + defensive behaviors
3. **Social Strategies**: Herding genes + communication capabilities
4. **Reproductive Strategies**: Timing + investment + offspring care

### Validation Opportunities
1. **WAG Trade-off Analysis**: Verify organ allocation competition in templates
2. **Metabolic Scaling Validation**: Test energy cost relationships
3. **Mutation Rate Impact**: Analyze evolutionary stability vs. adaptation
4. **Reproductive Success Correlation**: Link timing parameters to offspring survival

### Prediction Model Integration
1. **Genetic Compatibility**: Color gene matching for mate selection
2. **Niche Specialization**: Gene combinations that define ecological roles
3. **Evolutionary Stability**: Gene combinations that persist in stable ecosystems
4. **Adaptation Potential**: Mutation parameters that enable environmental adaptation

---

*This reference provides the foundation for understanding genetic behavioral specifications in the Bibites prediction system. The genetic parameters work in complex networks with neural systems to create emergent behaviors and evolutionary dynamics.*