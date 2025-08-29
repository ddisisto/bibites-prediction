#!/usr/bin/env python3
"""
validate_format.py - Validate .bb8 file format compliance.

Checks required JSON structure (transform, genes, brain, etc.) and provides
detailed validation results with batch processing support.

Usage examples:
  python -m src.tools.validate_format data/bibites/bibite_18.bb8
  python -m src.tools.validate_format --batch data/bibites/
  python -m src.tools.validate_format --detailed --batch data/bibites/
"""

import click
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.tree import Tree
import json

from ..core.parser import load_bb8_file, BB8ParseError

console = Console()

class ValidationResult:
    """Container for validation results."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.is_valid = True
        self.errors = []
        self.warnings = []
        self.structure_info = {}
    
    def add_error(self, message: str):
        """Add a validation error."""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Add a validation warning."""
        self.warnings.append(message)

def validate_bb8_structure(data: Dict[str, Any], file_path: Path, detailed: bool = False) -> ValidationResult:
    """
    Comprehensive validation of BB8 file structure.
    
    Args:
        data: Parsed JSON data
        file_path: Path to the file being validated
        detailed: Whether to perform detailed structural analysis
        
    Returns:
        ValidationResult with validation status and details
    """
    result = ValidationResult(file_path)
    
    # Required top-level fields
    required_fields = ['transform', 'genes', 'brain', 'rb2d', 'body', 'clock']
    
    for field in required_fields:
        if field not in data:
            result.add_error(f"Missing required top-level field: '{field}'")
    
    # Validate transform structure
    if 'transform' in data:
        transform = data['transform']
        if not isinstance(transform, dict):
            result.add_error("'transform' must be an object")
        else:
            transform_fields = ['position', 'rotation', 'scale']
            for field in transform_fields:
                if field not in transform:
                    result.add_error(f"Missing transform field: '{field}'")
                elif field == 'position' and not _is_vector2(transform[field]):
                    result.add_error("'transform.position' must be a 2-element array")
                elif field == 'rotation' and not isinstance(transform[field], (int, float)):
                    result.add_error("'transform.rotation' must be a number") 
                elif field == 'scale' and not isinstance(transform[field], (int, float)):
                    result.add_error("'transform.scale' must be a number")
    
    # Validate genes structure
    if 'genes' in data:
        genes = data['genes']
        if not isinstance(genes, dict):
            result.add_error("'genes' must be an object")
        else:
            # Check for nested genes structure (genes.genes)
            if 'genes' not in genes:
                result.add_error("Missing 'genes.genes' nested structure")
            else:
                nested_genes = genes['genes']
                if not isinstance(nested_genes, dict):
                    result.add_error("'genes.genes' must be an object")
                elif detailed:
                    # Count gene fields for detailed analysis
                    gene_count = len([k for k in nested_genes.keys() if not k.startswith('_')])
                    result.structure_info['gene_count'] = gene_count
    
    # Validate brain structure
    if 'brain' in data:
        brain = data['brain']
        if not isinstance(brain, dict):
            result.add_error("'brain' must be an object")
        else:
            # Check for actual brain structure (Nodes/Synapses with capital letters)
            brain_fields = ['Nodes', 'Synapses']
            for field in brain_fields:
                if field not in brain:
                    result.add_error(f"Missing brain field: '{field}'")
                elif not isinstance(brain[field], list):
                    result.add_error(f"'brain.{field}' must be an array")
                elif detailed:
                    result.structure_info[f'brain_{field.lower()}_count'] = len(brain[field])
            
            # Validate nodes structure if present
            if 'Nodes' in brain and isinstance(brain['Nodes'], list):
                for i, node in enumerate(brain['Nodes']):
                    if not isinstance(node, dict):
                        result.add_error(f"brain.Nodes[{i}] must be an object")
                    else:
                        # Check for common node fields (actual structure uses different field names)
                        node_fields = ['Type', 'TypeName', 'Index']
                        for field in node_fields:
                            if field not in node:
                                result.add_error(f"Missing brain.Nodes[{i}].{field}")
    
    # Validate rb2d (rigidbody2d) structure
    if 'rb2d' in data:
        rb2d = data['rb2d']
        if not isinstance(rb2d, dict):
            result.add_error("'rb2d' must be an object")
        else:
            # Check for common rb2d fields
            expected_rb2d_fields = ['bodyType', 'mass', 'drag', 'angularDrag']
            for field in expected_rb2d_fields:
                if field not in rb2d:
                    result.add_warning(f"Missing common rb2d field: '{field}'")
    
    # Validate body structure
    if 'body' in data:
        body = data['body']
        if not isinstance(body, dict):
            result.add_error("'body' must be an object")
        elif detailed:
            # Count body parts for detailed analysis
            if 'bodyParts' in body and isinstance(body['bodyParts'], list):
                result.structure_info['body_parts_count'] = len(body['bodyParts'])
    
    # Validate clock structure  
    if 'clock' in data:
        clock = data['clock']
        if not isinstance(clock, dict):
            result.add_error("'clock' must be an object")
        else:
            # Basic clock validation
            if 'age' not in clock:
                result.add_warning("Missing 'clock.age' field")
    
    # Additional structural validations
    if detailed:
        # Check file size estimate
        try:
            json_size = len(json.dumps(data))
            result.structure_info['json_size_bytes'] = json_size
            
            if json_size < 1000:
                result.add_warning("File seems unusually small (< 1KB)")
            elif json_size > 100000:
                result.add_warning("File seems unusually large (> 100KB)")
        except:
            result.add_warning("Could not estimate file size")
    
    return result

def _is_vector2(value) -> bool:
    """Check if value is a 2-element numeric array."""
    return (isinstance(value, list) and 
            len(value) == 2 and 
            all(isinstance(x, (int, float)) for x in value))

def _is_vector3(value) -> bool:
    """Check if value is a 3-element numeric array."""
    return (isinstance(value, list) and 
            len(value) == 3 and 
            all(isinstance(x, (int, float)) for x in value))

def _is_vector4(value) -> bool:
    """Check if value is a 4-element numeric array."""
    return (isinstance(value, list) and 
            len(value) == 4 and 
            all(isinstance(x, (int, float)) for x in value))

@click.command()
@click.argument('input_path', type=click.Path(exists=True, path_type=Path))
@click.option('--batch', '-b', is_flag=True, 
              help='Validate all .bb8 files in directory')
@click.option('--detailed', '-d', is_flag=True,
              help='Perform detailed structural analysis')
@click.option('--output', '-o', type=click.Path(path_type=Path),
              help='Output detailed results to JSON file')
@click.option('--show-valid', is_flag=True,
              help='Show details for valid files too (default: only show problems)')
def validate_format(input_path: Path, batch: bool, detailed: bool, 
                   output: Optional[Path], show_valid: bool):
    """Validate .bb8 file format compliance."""
    
    # Determine input files
    if batch or input_path.is_dir():
        bb8_files = list(input_path.glob('*.bb8'))
        if not bb8_files:
            console.print(f"[red]No .bb8 files found in {input_path}[/red]")
            return
        console.print(f"[blue]Validating {len(bb8_files)} files...[/blue]")
    else:
        bb8_files = [input_path]
    
    # Process files
    results = []
    valid_count = 0
    error_count = 0
    warning_count = 0
    
    for file_path in track(bb8_files, description="Validating files"):
        try:
            # Load and parse file
            data = load_bb8_file(file_path)
            
            # Validate structure
            result = validate_bb8_structure(data, file_path, detailed)
            results.append(result)
            
            if result.is_valid:
                valid_count += 1
            else:
                error_count += 1
            
            warning_count += len(result.warnings)
            
        except BB8ParseError as e:
            # Create result for parse error
            result = ValidationResult(file_path)
            result.add_error(f"Parse error: {e}")
            results.append(result)
            error_count += 1
    
    # Display results
    _display_validation_results(results, show_valid, detailed)
    
    # Summary table
    console.print("\n[bold]Validation Summary[/bold]")
    table = Table()
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green")
    
    table.add_row("Files processed", str(len(bb8_files)))
    table.add_row("Valid files", str(valid_count))
    if error_count > 0:
        table.add_row("Files with errors", str(error_count))
    if warning_count > 0:
        table.add_row("Total warnings", str(warning_count))
    
    console.print(table)
    
    # Save detailed output if requested
    if output:
        output_data = []
        for result in results:
            file_data = {
                'file': str(result.file_path.name),
                'is_valid': result.is_valid,
                'errors': result.errors,
                'warnings': result.warnings
            }
            if detailed:
                file_data['structure_info'] = result.structure_info
            output_data.append(file_data)
        
        with open(output, 'w') as f:
            json.dump(output_data, f, indent=2)
        console.print(f"\n[green]Detailed results saved to: {output}[/green]")

def _display_validation_results(results: List[ValidationResult], show_valid: bool, detailed: bool):
    """Display validation results in a formatted way."""
    
    for result in results:
        # Skip valid files unless explicitly requested
        if result.is_valid and not result.warnings and not show_valid:
            continue
        
        # File header
        if result.is_valid:
            console.print(f"\n[green]✓ {result.file_path.name}[/green]")
        else:
            console.print(f"\n[red]✗ {result.file_path.name}[/red]")
        
        # Errors
        if result.errors:
            console.print("  [red]Errors:[/red]")
            for error in result.errors:
                console.print(f"    • {error}")
        
        # Warnings  
        if result.warnings:
            console.print("  [yellow]Warnings:[/yellow]")
            for warning in result.warnings:
                console.print(f"    • {warning}")
        
        # Detailed structure info
        if detailed and result.structure_info:
            console.print("  [blue]Structure Info:[/blue]")
            for key, value in result.structure_info.items():
                console.print(f"    • {key}: {value}")

if __name__ == '__main__':
    validate_format()