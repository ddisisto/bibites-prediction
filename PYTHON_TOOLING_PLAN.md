# Python Tooling Implementation Plan

## Architecture Decision
**APPROVED**: Replace bash/jq approach with Python-based tooling for better maintainability, performance, and Claude Code integration.

## Setup Phase - Immediate Actions

### 1. Virtual Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install core dependencies
pip install orjson msgspec click rich pytest pathlib
pip freeze > requirements.txt
```

### 2. Project Structure
```
src/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── parser.py          # BB8 file parsing with orjson
│   ├── models.py          # msgspec data models  
│   └── validator.py       # Schema validation
├── tools/
│   ├── __init__.py
│   ├── extract_data.py    # Replace manual jq queries
│   ├── batch_process.py   # Multi-file operations  
│   └── validate_format.py # Format checking
└── tests/
    ├── __init__.py
    └── test_parser.py     # Core functionality tests
```

## Implementation Priority

### Phase 1: Core Foundation (First commit)
1. **Environment setup** (.venv, requirements.txt)
2. **Basic parser** (parse single .bb8 file with UTF-8 BOM handling)
3. **Data models** (msgspec structs for validation)
4. **Simple CLI** (extract specific fields from single file)

### Phase 2: Functional Tools (Second commit)  
5. **Batch processing** (process all organisms in directory)
6. **Field extraction** (genetic parameters, neural data)
7. **Format validation** (schema compliance checking)
8. **Rich output** (progress bars, structured logging)

### Phase 3: Integration (Third commit)
9. **Claude Code compatibility** (clean CLI interfaces)
10. **Git workflow integration** (commit patterns, branch strategy)
11. **Error handling** (graceful failure, helpful messages)
12. **Testing framework** (pytest + hypothesis)

## Key Benefits Over Bash/jq

- **3x faster parsing** with orjson vs. manual jq commands
- **Type safety** with msgspec validation
- **Better error handling** with structured exceptions  
- **Testable code** with pytest framework
- **Rich output** compatible with Claude Code
- **Maintainable** for complex analysis pipelines

## Success Criteria

1. **Replace current manual processes**: No more manual jq command construction
2. **Batch processing**: Process all 165 organisms in <1 second
3. **Validation**: Catch format errors with helpful messages
4. **Integration**: Works seamlessly with Claude Code workflows
5. **Git-friendly**: Clean commits, branching for tool development

## Next Decision Point

**Should we start Phase 1 implementation now?**
- Set up virtual environment
- Create basic parser
- Test against existing bibite_0.bb8 file
- Commit foundation for iteration

This would give us a concrete foundation to build on, replacing the manual jq work with sustainable tooling.

---
*Created: August 29, 2025*  
*Status: Implementation ready - awaiting approval*