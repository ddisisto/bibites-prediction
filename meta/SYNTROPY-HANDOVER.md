# SYNTROPY HANDOVER: Bibites Prediction System

## Project Setup & Rationale

**Created:** 2025-08-26  
**SYNTROPY Version:** v1.0  
**Project Type:** Research & Development - AI Evaluation System

### Core Mission
Develop an AI system that analyzes Bibites organism genetic/neural configurations and predicts their behavioral outcomes, with potential applications as multi-dimensional evaluation framework for AI capabilities.

### Why This Architecture

**FAANG-Inspired Pipeline**: Applied enterprise development practices in simplified form:
- Design-first approach with technical documentation
- Agent specialization with clear scope boundaries  
- JIT agent instantiation to reduce premature assumptions
- MVP focus while maintaining extensible architecture

**File-Based State Management**: Leverages Claude Code's stateless agent architecture:
- Persistent project state via structured documentation
- Cross-session continuity through markdown files
- Agent coordination via shared file system
- Context window optimization through delegation

**Research-Heavy Approach**: No external research - build understanding from examples:
- Reverse-engineer Bibites formats from provided templates
- Develop prediction models from first principles
- Create evaluation frameworks based on empirical analysis
- Maintain scientific rigor in methodology

### Directory Structure

```
bibites-prediction/
├── templates/          # Symlinked Bibites organism configs (read-only)
├── .claude/
│   └── agents/
│       ├── project-manager.md    # Pipeline coordination & JIT agent creation
│       └── format-analyst.md     # Genetic/neural format understanding
├── design/            # Technical design documents (created as needed)
├── analysis/          # Format specs and structural understanding
├── src/               # Implementation code and prediction systems
├── evaluation/        # Tournament results and performance metrics
├── docs/              # Living documentation and milestone tracking
├── CLAUDE.md          # Living project context and decisions
└── SYNTROPY-HANDOVER.md  # This static setup documentation
```

### Agent Coordination Strategy

**@project-manager**: Central coordinator
- Assesses project phase and determines next steps
- Creates specialist agents JIT when expertise boundaries reached
- Delegates Tasks between agents using @agent pattern
- Maintains development pipeline progression
- Manages context window optimization

**@format-analyst**: Genetic/neural specialist  
- Analyzes Bibites organism configuration formats
- Builds structural understanding from template examples
- Creates machine-readable specifications
- Develops feature extraction pipelines

**Future Agents** (JIT instantiated as needed):
- **@prediction-architect**: ML model design and implementation
- **@tournament-engineer**: Multi-dimensional Elo system development
- **@performance-optimizer**: System scaling and optimization
- **@evaluation-specialist**: Accuracy assessment and validation

### Context Window Management (~160k token phases)

**Phase 1: Format Discovery & Analysis**
- Parse all template organism configurations
- Document genetic encoding patterns and neural architectures
- Create formal data structure specifications
- Build feature extraction utilities
- **Deliverable**: Complete format understanding and extraction pipeline

**Phase 2: Prediction Architecture & Implementation**
- Design behavioral prediction system architecture
- Implement ML models for organism outcome prediction
- Create validation frameworks and test suites
- Develop baseline performance metrics
- **Deliverable**: Working prediction system with validation

**Phase 3: Tournament System Development**
- Design multi-dimensional Elo tournament framework
- Implement competitive evaluation simulation
- Create performance metrics and ranking systems
- Validate against actual evolutionary outcomes
- **Deliverable**: Complete tournament evaluation system

**Phase 4: Optimization & Advanced Features**
- Performance tuning and system scaling
- Advanced prediction techniques and feature engineering
- Extended tournament formats and evaluation criteria
- System generalization for broader applications
- **Deliverable**: Production-ready evaluation platform

### Success Criteria by Phase

**Phase 1 Success:**
- Parse 100% of template configs without errors
- Generate machine-readable format specifications
- Extract meaningful features for behavioral prediction
- Document data structures and relationships

**Phase 2 Success:**
- Implement working prediction models
- Beat random baseline by significant margin
- Create robust validation and testing framework
- Demonstrate prediction capability on sample organisms

**Phase 3 Success:**
- Deploy functional multi-dimensional tournament system
- Correlate predictions with actual evolutionary outcomes
- Generate meaningful ranking and evaluation metrics
- Validate system accuracy and reliability

**Phase 4 Success:**
- Achieve production-level performance and reliability
- Demonstrate advanced prediction capabilities
- Support complex tournament formats and evaluation
- Enable autonomous AI capability evaluation workflows

### Key Design Principles

**Empirical Foundation**: Build understanding solely from provided examples
**Explicit Scoping**: Every agent and task has clear boundaries and deliverables
**File-Based Persistence**: Maintain state through structured documentation
**Context Optimization**: Use Task delegation to extend effective working memory
**MVP Focus**: Deliver working system incrementally with clean extensibility
**Scientific Rigor**: Maintain validation and testing throughout development

### Handover Notes

**Immediate Next Step**: Begin with @project-manager to assess current phase and initiate format analysis

**Template Access**: Bibites organism configs available via `templates/` symlink

**Living Documentation**: Update `CLAUDE.md` as major decisions are made and milestones reached

**Agent Creation**: Use JIT approach - create specialists only when current context reaches expertise boundaries

**Context Management**: Each phase should fit within ~160k tokens; use Task delegation for complex operations

---

**This document represents the static handover from SYNTROPY setup to active project development. All future documentation should be maintained in the living project files.**