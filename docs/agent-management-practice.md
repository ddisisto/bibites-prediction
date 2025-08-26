# Agent Management Practice & Agency

## Core Principles

**Task Context vs Agent Context:**
- **Task Context**: Specific work scope, deliverables, success criteria
- **Agent Context**: Persistent identity, owned content, meta-learning, evolution

**Agency Ownership:**
- Each agent must review and evolve their own definition at @.claude/agents/[name].md
- Agents track owned content via @path/to/file references
- Meta-learning captured in agent definitions for future invocations
- Self-management responsibility across context windows

## Project Manager Handover Process

**Standard PM Handover Sequence:**
1. **Git Status Check**: Ensure clean repo state
2. **Update CLAUDE.md**: Reflect current phase and progress
3. **Update Own Context**: Review/evolve @.claude/agents/project-manager.md
4. **Git Commit**: Persist state changes
5. **Propose Next Steps**: Include @agent Task prompt for review
6. **Execute Delegation**: After user approval of Task scope

## Agent Task Management

**Task Prompt Structure:**
- MANDATORY: Agent definition review at start
- Core mission with focused scope
- Clear deliverables and output requirements
- MANDATORY: Agent definition update at completion with owned content references

**Success Metrics:**
- All work persisted to files
- Temp files cleaned up
- Agent definitions evolved with learnings
- Clear handoff documentation

## Meta-Learning Capture

**Agent Evolution:**
- Agents update their own definitions based on task learnings
- Document @path/to/file ownership for persistence
- Capture insights for future context windows
- Maintain scope boundaries and expertise areas

**Cross-Agent Coordination:**
- Clear @agent references for delegation
- Explicit scope boundaries and handoff protocols
- File-based state persistence for continuity
- Context compression through structured documentation

---
*This document evolves with our agent management learnings and practices.*