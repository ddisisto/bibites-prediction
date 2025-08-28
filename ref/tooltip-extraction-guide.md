# Bibites Neural Network Tooltip Extraction Guide

## Overview
This document provides a repeatable process for extracting neural network node tooltip/help text from The Bibites Unity game files. The tooltips contain crucial behavioral specifications not available elsewhere.

## Key Findings

### Successful Extraction Location
- **Primary Source**: `/The Bibites_Data/Managed/BibitesAssembly.dll`
- **Extraction Method**: `strings -e l` (little-endian Unicode strings)
- **Data Format**: Complete tooltip descriptions with behavioral specifications

### Sample Extracted Data

#### Input Node Tooltips (Type 0)
```
- EnergyRatio: "Outputs the current energy level"
- Maturity: "Outputs the bibite's current maturity (a value of 1.0 is reached when it can reproduce/lay eggs)"
- LifeRatio: "Outputs the bibite's current health (HP / maxHP)"
- Fullness: "Outputs how full the bibite's stomach is"
- Speed: "Outputs the bibite's current forward speed (normalized for its body length) (negative value means it's going backward to where it's facing"
- RotationSpeed: "Outputs the bibite's current angular speed (normalized to full rotations per second) (positive values mean clockwise rotation, while negative means counterclockwise)"
- IsGrabbing: "Outputs whether the bibite is currently grabbing (1.0) or not (0.0) an object"
- AttackedDamage: "Outputs the normalized pain of the bibite (attacked damages it received recently (decaying exponentially) / maxHP)"
- EggStored: "Outputs the number of completed eggs stored in the bibite's egg organ"
- BibiteCloseness: "Outputs how close (normalize to its view radius) in its field of view the weighted average of bibites is"
- BibiteAngle: "Outputs the angle (normalized to its view angle) in its field of view the weighted average of bibites is"
- NBibites: "Outputs the number of bibites in its field of view divided by 4"
```

#### Output Node Tooltips (Type 3)
```
- Grab: "Controls the bibite's grab strength
         If activated, any object newly entering the mouth will be grabbed
         Sudden negative activation will result in grabbed objects instead being thrown
         Stronger activation makes the hold on more tightly, or throw object more violently, but Force is always distributed across all held/thrown objects
         Any absolute activation < [threshold] will result in the bibite not grabbing/throwing anything"
```

#### Universal Patterns Found
```
- Output Range Format: "Output range: {0} to {1}" / "Output range: {2} to {3}"
- Directional Conventions: "Negative value are to the left, positive values to the right"
- Saturation Behavior: "Outputs saturates for strong activations"
```

## Extraction Process

### Prerequisites
- The Bibites game installed via Steam
- Game process running (optional, but confirms installation path)

### Step-by-Step Process

1. **Locate Game Installation**
   ```bash
   # Find running process for path confirmation
   ps aux | grep -i bibite
   
   # Standard Steam path
   cd "/home/daniel/.local/share/Steam/steamapps/common/The Bibites/The Bibites_Data"
   ```

2. **Extract Tooltip Strings**
   ```bash
   # Primary extraction command
   strings -e l Managed/BibitesAssembly.dll | grep -E "^(Controls|Outputs|Output range|Default Activation|Function).*"
   
   # Search for specific node behaviors
   strings -e l Managed/BibitesAssembly.dll | grep -A1 -B1 "grab.*strength\|activation.*result"
   ```

3. **Verification Commands**
   ```bash
   # Confirm node names exist
   strings Managed/BibitesAssembly.dll | grep "EnergyRatio\|BibiteCloseness\|Want2Eat\|PheroSense"
   
   # Find activation function references
   strings Managed/BibitesAssembly.dll | grep -i "tanh\|default.*activation"
   ```

### Key File Locations

#### Game Installation Structure
```
The Bibites/
├── The Bibites.exe
├── The Bibites_Data/
│   ├── Managed/
│   │   ├── BibitesAssembly.dll          ← PRIMARY TOOLTIP SOURCE
│   │   ├── UnityEngine.dll
│   │   └── [other .dll files]
│   ├── resources.assets                 ← Node names only
│   ├── sharedassets*.assets            ← Limited content
│   └── globalgamemanagers*             ← No relevant tooltip data
```

#### Template Data Cross-Reference
- Node descriptions in templates: `/templates/*.bb8template` → `nodes[].Desc`
- Extracted tooltips provide behavioral specifications missing from templates
- Template node types (0-13) correspond to tooltip categories

## Data Completeness Assessment

### Successfully Extracted
- ✅ Input node behavioral descriptions (Type 0)
- ✅ Output node control specifications (Type 3) 
- ✅ Range and normalization information
- ✅ Activation thresholds and behaviors
- ✅ Directional conventions and saturation patterns

### Limitations Found
- ❌ Direct tooltip text search ("Controls the bibite's grab strength") failed in standard Unity assets
- ❌ Structured tooltip association with node types requires manual correlation
- ⚠️ Some specialized node types (4-13) may have limited tooltip coverage

### Version Considerations
- Tooltip extraction tested on game version corresponding to template format 0.6.2.1
- Method should work for future versions but content may change
- Re-extraction recommended after major game updates

## Future Automation Potential

### Scriptable Components
1. **Path Detection**: Automatically locate Steam installation via registry/config
2. **String Extraction**: Parse BibitesAssembly.dll programmatically  
3. **Node Correlation**: Match extracted tooltips to template node descriptions
4. **Documentation Generation**: Auto-generate comprehensive node reference

### Update Detection
- Monitor game version in template files
- Compare extracted string counts between versions
- Flag new/changed tooltip content for review

## Integration with Prediction System

### Immediate Value
- Enhanced node behavioral understanding for feature engineering
- Activation range specifications for input normalization
- Output interpretation guidelines for prediction validation

### Long-term Applications  
- Behavioral classification based on tooltip specifications
- Threshold-aware prediction modeling
- Node interaction pattern recognition from described behaviors

---

*Documentation created: August 28, 2025*  
*Game version tested: 0.6.2.1 (Steam)*  
*Extraction method: Unity .NET assembly string analysis*