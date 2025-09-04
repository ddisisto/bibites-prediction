# Bibite Cross-Pollination Feature Branch Plan

**Branch:** `feature/bibite-cross-pollination`  
**Goal:** Enable read/write bibite template transfer between save files for controlled evolutionary experiments

## Scenario Context: Pred Train BR

**Source Save:** `pred train br.zip` - Contains evolved predators (loop lineage)  
**Target Save:** `pred train br - pre-herbivore staging.zip` - Herbivore-only environment needing predator injection  
**Expected Output:** `pred train br - staged.zip` - Combined ecosystem for predator training

## Technical Architecture

### Phase 1: Research & Foundation (Current Session)
- [x] Branch creation and planning documentation
- [ ] Research save file write/modification requirements
- [ ] Analyze .bb8 file structure for template extraction
- [ ] Design bibite ID management for injection conflicts
- [ ] Plan spawn positioning and zone placement strategies

### Phase 2: Core Implementation 
- [ ] Implement save file reconstruction/modification capabilities
- [ ] Add bibite template extraction by criteria (age, lineage, fitness)
- [ ] Add bibite template injection with conflict resolution
- [ ] Extend unified `bibites.py` with cross-pollination commands

### Phase 3: Integration & Testing
- [ ] Validate pred train br scenario end-to-end
- [ ] Test edge cases (ID conflicts, spawn positioning, ecosystem balance)
- [ ] Performance testing with large save files
- [ ] Documentation updates across all levels

## Command Interface Design

### Template Extraction
```bash
# Extract predators by criteria
bibites --extract-templates --from "pred train br.zip" \
        --filter "tag:loop,age:>100,fitness:top10%" \
        --output templates/evolved_predators/

# Extract entire lineage
bibites --extract-templates --from "source.zip" \
        --filter "lineage:loop" \
        --output templates/loop_lineage/
```

### Template Injection  
```bash
# Inject with automatic positioning
bibites --inject-templates --into "target.zip" \
        --templates templates/evolved_predators/ \
        --spawn-zone "central" \
        --output "staged.zip"

# Advanced injection with ID remapping
bibites --inject-templates --into "target.zip" \
        --templates templates/ \
        --remap-ids \
        --spawn-strategy "distributed" \
        --preserve-ecosystem-balance \
        --output "enhanced.zip"
```

### Combined Operations
```bash
# One-step cross-pollination
bibites --cross-pollinate \
        --source "pred train br.zip" \
        --target "pred train br - pre-herbivore staging.zip" \
        --filter "tag:loop,fitness:top20%" \
        --output "pred train br - staged.zip"
```

## Agent Delegation Strategy

### @tools-engineer Responsibilities
1. **Save File Write Capabilities**: Implement zip reconstruction with .bb8 modifications
2. **Template System**: Design extraction/injection API with conflict resolution
3. **ID Management**: Handle bibite ID remapping and reference updating
4. **Unified Interface**: Extend `bibites.py` with cross-pollination commands

### Manual Testing & Validation
1. **Scenario Validation**: Test actual pred train br use case
2. **Edge Case Testing**: ID conflicts, spawn positioning, large files
3. **Ecosystem Balance**: Ensure injected bibites don't destabilize target environment

## Technical Challenges & Solutions

### Challenge 1: Save File Integrity
- **Problem**: Modifying compressed .zip saves without corruption
- **Solution**: Implement atomic write operations with backup/rollback

### Challenge 2: Bibite ID Conflicts  
- **Problem**: Injected bibites may have conflicting IDs with target save
- **Solution**: ID remapping system with reference tracking

### Challenge 3: Ecosystem Balance
- **Problem**: Injected predators might overwhelm herbivore staging environment
- **Solution**: Population ratio analysis and controlled injection counts

### Challenge 4: Spawn Positioning
- **Problem**: Where to place injected bibites without disrupting existing populations
- **Solution**: Zone analysis and strategic positioning algorithms

## Success Criteria

### Functional Requirements
- [x] Extract specific bibites from source saves by multiple criteria
- [ ] Successfully inject templates into target saves
- [ ] Handle ID conflicts without data corruption
- [ ] Maintain save file compatibility with Bibites game
- [ ] Generate functional output saves ready for simulation

### Performance Requirements  
- [ ] Process large saves (>1000 bibites) in reasonable time (<30 seconds)
- [ ] Memory efficient template handling
- [ ] Atomic operations to prevent partial writes

### Quality Requirements
- [ ] Comprehensive error handling and user feedback
- [ ] Clear documentation for all new commands
- [ ] Integration with existing unified interface
- [ ] Backwards compatibility with read-only operations

## Documentation Maintenance

### Files to Update
- [ ] `CLAUDE.md` - Add cross-pollination capabilities to project overview
- [ ] `src/tools/README.md` - Document new bibites.py commands  
- [ ] `.claude/agents/tools-engineer.md` - Update scope to include R/W operations
- [ ] `BRANCH_PLAN.md` - Keep current with progress and learnings

### Documentation Standards
- Update docs at each major milestone
- Include example workflows and use cases
- Document technical decisions and tradeoffs
- Maintain clear separation between R/O and R/W operations

## Risk Mitigation

### Data Safety
- Always backup original saves before modification
- Implement dry-run mode for testing operations
- Atomic write operations to prevent corruption

### Game Compatibility  
- Test all generated saves load correctly in Bibites game
- Validate ecosystem functionality post-injection
- Monitor for any file format version issues

### Performance & Scale
- Profile operations with large save files
- Implement streaming processing if needed
- Memory usage monitoring and optimization

## Next Steps

1. **Research Phase**: Analyze save file structure and .bb8 template format
2. **Checkpoint**: Return with findings and technical approach recommendations  
3. **Implementation**: @tools-engineer develops core R/W capabilities
4. **Checkpoint**: Validate core functionality before interface integration
5. **Integration**: Add commands to unified bibites.py interface
6. **Checkpoint**: End-to-end testing of pred train br scenario
7. **Final**: Documentation updates and merge preparation

---

**Started:** September 4, 2025  
**Status:** Research & Foundation Phase  
**Next Milestone:** Save File Structure Analysis & Technical Approach