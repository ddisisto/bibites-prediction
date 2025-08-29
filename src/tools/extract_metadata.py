#!/usr/bin/env python3
"""
extract_metadata.py - Extract ecosystem metadata and zone settings from Bibites save .zip files.

Extracts ALL non-.bb8 files from save zips and attempts to parse zone/world
configuration settings. Looks for zone names, descriptions, environmental
parameters, and ecosystem configuration.

Usage examples:
  python -m src.tools.extract_metadata Savefiles/3i1m6x-4.zip
  python -m src.tools.extract_metadata --raw Savefiles/validation-1.zip
  python -m src.tools.extract_metadata --output ./tmp/debug/ Savefiles/exp1.zip
"""

import click
import zipfile
import json
import xml.etree.ElementTree as ET
import configparser
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.tree import Tree
import re

console = Console()

class MetadataExtractionError(Exception):
    """Raised when metadata extraction fails."""
    pass

def is_metadata_file(filename: str) -> bool:
    """Check if filename is likely a metadata/config file (not .bb8 or image)."""
    # Exclude .bb8 files and common image formats
    excluded_extensions = {'.bb8', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
    return Path(filename).suffix.lower() not in excluded_extensions

def parse_json_content(content: str, filename: str) -> Optional[Dict[str, Any]]:
    """Attempt to parse JSON content."""
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        console.print(f"[yellow]Failed to parse {filename} as JSON: {e}[/yellow]")
        return None

def parse_xml_content(content: str, filename: str) -> Optional[ET.Element]:
    """Attempt to parse XML content."""
    try:
        return ET.fromstring(content)
    except ET.ParseError as e:
        console.print(f"[yellow]Failed to parse {filename} as XML: {e}[/yellow]")
        return None

def parse_ini_content(content: str, filename: str) -> Optional[configparser.ConfigParser]:
    """Attempt to parse INI/config content."""
    try:
        config = configparser.ConfigParser()
        config.read_string(content)
        return config
    except configparser.Error as e:
        console.print(f"[yellow]Failed to parse {filename} as INI: {e}[/yellow]")
        return None

def extract_zone_info_from_json(data: Dict[str, Any], filename: str) -> List[Dict[str, Any]]:
    """Extract zone information from JSON data."""
    zones = []
    
    def search_for_zones(obj: Any, path: str = "") -> None:
        """Recursively search for zone-like data structures."""
        if isinstance(obj, dict):
            # Look for direct zones array (common in Bibites saves)
            if 'zones' in obj and isinstance(obj['zones'], list):
                for i, zone in enumerate(obj['zones']):
                    if isinstance(zone, dict):
                        zone_copy = zone.copy()
                        zone_copy['_source_path'] = f"{path}.zones[{i}]" if path else f"zones[{i}]"
                        zone_copy['_source_file'] = filename
                        zones.append(zone_copy)
            
            # Look for zone-like keys
            zone_indicators = ['zone', 'region', 'area', 'island', 'habitat', 'biome', 'territory']
            zone_data = {}
            
            # Check if this object contains zone-like information
            has_zone_info = False
            for key, value in obj.items():
                key_lower = key.lower()
                
                # Direct zone indicators
                if any(indicator in key_lower for indicator in zone_indicators):
                    has_zone_info = True
                    zone_data[key] = value
                
                # Look for descriptive fields
                elif key_lower in ['name', 'title', 'description', 'type', 'id', 'index', 'material',
                                 'distribution', 'fertility', 'biomassensity', 'pelletsize', 
                                 'movement', 'speed', 'posx', 'posy', 'radius', 'insideradius']:
                    zone_data[key] = value
                
                # Look for environmental parameters
                elif key_lower in ['temperature', 'humidity', 'pressure', 'gravity', 'light', 
                                 'food', 'nutrients', 'toxicity', 'size', 'width', 'height',
                                 'capacity', 'population', 'energy', 'resources']:
                    zone_data[key] = value
                
                # Don't recursively search if we already found zones array
                elif isinstance(value, (dict, list)) and key != 'zones':
                    search_for_zones(value, f"{path}.{key}" if path else key)
            
            # If we found zone-like information, add it
            if has_zone_info and zone_data and 'zones' not in obj:
                zone_data['_source_path'] = path if path else "root"
                zone_data['_source_file'] = filename
                zones.append(zone_data)
                
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                search_for_zones(item, f"{path}[{i}]" if path else f"[{i}]")
    
    search_for_zones(data)
    return zones

def extract_settings_info_from_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract general settings and configuration from JSON data."""
    settings = {}
    
    def extract_settings(obj: Any, prefix: str = "") -> None:
        """Recursively extract settings."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_key = f"{prefix}.{key}" if prefix else key
                
                if isinstance(value, (str, int, float, bool)):
                    settings[current_key] = value
                elif isinstance(value, (dict, list)) and len(str(value)) < 200:
                    # Only include small nested structures to avoid clutter
                    settings[current_key] = value
                elif isinstance(value, dict):
                    extract_settings(value, current_key)
        elif isinstance(obj, list):
            # Handle lists of settings objects
            for i, item in enumerate(obj):
                if isinstance(item, dict) and len(item) < 10:  # Small objects only
                    extract_settings(item, f"{prefix}[{i}]" if prefix else f"[{i}]")
    
    extract_settings(data)
    return settings

def analyze_binary_file(content: bytes, filename: str) -> Dict[str, Any]:
    """Analyze binary file content for any readable strings."""
    # Try to find readable strings in binary content
    readable_strings = []
    current_string = ""
    
    for byte in content:
        if 32 <= byte <= 126:  # Printable ASCII
            current_string += chr(byte)
        else:
            if len(current_string) >= 4:  # Minimum string length
                readable_strings.append(current_string)
            current_string = ""
    
    # Add final string if exists
    if len(current_string) >= 4:
        readable_strings.append(current_string)
    
    # Look for interesting patterns
    zone_strings = []
    setting_strings = []
    
    for s in readable_strings:
        s_lower = s.lower()
        if any(word in s_lower for word in ['zone', 'region', 'island', 'area', 'habitat']):
            zone_strings.append(s)
        elif any(word in s_lower for word in ['setting', 'config', 'param', 'value']):
            setting_strings.append(s)
    
    return {
        'file_size': len(content),
        'readable_strings_count': len(readable_strings),
        'zone_related_strings': zone_strings[:10],  # Limit output
        'setting_related_strings': setting_strings[:10],
        'sample_strings': readable_strings[:20]  # First 20 strings
    }

def extract_metadata_from_save(zip_path: Path, output_dir: Path, extract_raw: bool = False) -> Dict[str, Any]:
    """
    Extract ecosystem metadata from a save zip file.
    
    Args:
        zip_path: Path to the save .zip file
        output_dir: Directory for temporary file extraction
        extract_raw: If True, extract all files for examination
        
    Returns:
        Dict containing extracted metadata and zone information
    """
    if not zip_path.exists():
        raise MetadataExtractionError(f"Save file not found: {zip_path}")
    
    if not zip_path.suffix.lower() == '.zip':
        raise MetadataExtractionError(f"File is not a .zip file: {zip_path}")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    metadata = {
        'save_name': zip_path.stem,
        'save_path': str(zip_path),
        'zones': [],
        'settings': {},
        'files_analyzed': [],
        'raw_files': [] if extract_raw else None,
        'errors': []
    }
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # Get all non-.bb8, non-image files
            all_files = zip_file.namelist()
            metadata_files = [f for f in all_files if is_metadata_file(f)]
            
            console.print(f"[blue]Found {len(metadata_files)} metadata files in {zip_path.name}[/blue]")
            
            for file_path in metadata_files:
                try:
                    # Read file content
                    with zip_file.open(file_path) as file_obj:
                        raw_content = file_obj.read()
                    
                    filename = Path(file_path).name
                    
                    # If raw extraction requested, save the file
                    if extract_raw:
                        raw_file_path = output_dir / filename
                        with open(raw_file_path, 'wb') as f:
                            f.write(raw_content)
                        metadata['raw_files'].append(str(raw_file_path))
                    
                    file_info = {
                        'filename': filename,
                        'path': file_path,
                        'size': len(raw_content),
                        'type': 'unknown',
                        'content': None,
                        'zones': [],
                        'settings': {}
                    }
                    
                    # Try to decode as text first, handling UTF-8 BOM
                    try:
                        # Try UTF-8 with BOM first
                        try:
                            text_content = raw_content.decode('utf-8-sig')
                        except UnicodeDecodeError:
                            text_content = raw_content.decode('utf-8')
                        
                        # Try JSON parsing
                        json_data = parse_json_content(text_content, filename)
                        if json_data:
                            file_info['type'] = 'json'
                            file_info['content'] = json_data
                            file_info['zones'] = extract_zone_info_from_json(json_data, filename)
                            file_info['settings'] = extract_settings_info_from_json(json_data)
                            metadata['zones'].extend(file_info['zones'])
                            metadata['settings'].update(file_info['settings'])
                        
                        # Try XML parsing if not JSON
                        elif text_content.strip().startswith('<'):
                            xml_root = parse_xml_content(text_content, filename)
                            if xml_root is not None:
                                file_info['type'] = 'xml'
                                # Convert XML to dict for zone extraction
                                xml_dict = xml_to_dict(xml_root)
                                file_info['content'] = xml_dict
                                file_info['zones'] = extract_zone_info_from_json(xml_dict, filename)
                                metadata['zones'].extend(file_info['zones'])
                        
                        # Try INI/config parsing
                        elif '=' in text_content or '[' in text_content:
                            config = parse_ini_content(text_content, filename)
                            if config:
                                file_info['type'] = 'ini'
                                config_dict = {section: dict(config[section]) for section in config.sections()}
                                file_info['content'] = config_dict
                                file_info['zones'] = extract_zone_info_from_json(config_dict, filename)
                                file_info['settings'] = extract_settings_info_from_json(config_dict)
                                metadata['zones'].extend(file_info['zones'])
                                metadata['settings'].update(file_info['settings'])
                        
                        # Plain text
                        else:
                            file_info['type'] = 'text'
                            file_info['content'] = text_content[:1000]  # Truncate long text
                    
                    except UnicodeDecodeError:
                        # Binary file
                        file_info['type'] = 'binary'
                        binary_analysis = analyze_binary_file(raw_content, filename)
                        file_info['content'] = binary_analysis
                    
                    metadata['files_analyzed'].append(file_info)
                    
                except Exception as e:
                    error_msg = f"Failed to analyze {file_path}: {e}"
                    metadata['errors'].append(error_msg)
                    console.print(f"[red]{error_msg}[/red]")
        
        return metadata
                        
    except zipfile.BadZipFile:
        raise MetadataExtractionError(f"Invalid or corrupted zip file: {zip_path}")
    except Exception as e:
        raise MetadataExtractionError(f"Error extracting metadata from {zip_path}: {e}")

def xml_to_dict(element: ET.Element) -> Dict[str, Any]:
    """Convert XML element to dictionary."""
    result = {}
    
    # Add attributes
    if element.attrib:
        result.update(element.attrib)
    
    # Add text content
    if element.text and element.text.strip():
        if not result:  # If no attributes, just return text
            return element.text.strip()
        result['_text'] = element.text.strip()
    
    # Add child elements
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            # Handle multiple children with same tag
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
    
    return result

def display_metadata_results(metadata: Dict[str, Any]) -> None:
    """Display extracted metadata in a formatted way."""
    
    console.print(f"\n[bold cyan]Metadata Analysis: {metadata['save_name']}[/bold cyan]")
    
    # Files analyzed summary
    files_table = Table(title="Files Analyzed")
    files_table.add_column("Filename", style="cyan")
    files_table.add_column("Type", style="green")
    files_table.add_column("Size", style="yellow")
    files_table.add_column("Zones Found", style="magenta")
    
    for file_info in metadata['files_analyzed']:
        files_table.add_row(
            file_info['filename'],
            file_info['type'],
            f"{file_info['size']:,} bytes",
            str(len(file_info['zones']))
        )
    
    console.print(files_table)
    
    # Zone information
    if metadata['zones']:
        console.print(f"\n[bold green]Zone Information ({len(metadata['zones'])} zones found)[/bold green]")
        
        for i, zone in enumerate(metadata['zones']):
            zone_name = zone.get('name', f"Zone {i+1}")
            zone_tree = Tree(f"[bold cyan]{zone_name}[/bold cyan] (from {zone.get('_source_file', 'unknown')})")
            
            # Show important zone properties first
            important_keys = ['id', 'material', 'distribution', 'fertility', 'biomassDensity', 
                            'pelletSize', 'posX', 'posY', 'radius', 'insideRadius', 'movement', 'speed']
            
            for key in important_keys:
                if key in zone:
                    value = zone[key]
                    if isinstance(value, float):
                        zone_tree.add(f"[green]{key}:[/green] {value:.3f}")
                    else:
                        zone_tree.add(f"[green]{key}:[/green] {value}")
            
            # Show other properties
            for key, value in zone.items():
                if not key.startswith('_') and key not in important_keys:
                    if isinstance(value, (dict, list)):
                        zone_tree.add(f"[yellow]{key}:[/yellow] {json.dumps(value, indent=2)[:100]}...")
                    else:
                        zone_tree.add(f"[yellow]{key}:[/yellow] {value}")
            
            console.print(zone_tree)
            console.print()
    
    else:
        console.print("[yellow]No zone information found in structured format[/yellow]")
    
    # Settings summary
    if metadata['settings']:
        console.print(f"[bold blue]Configuration Settings ({len(metadata['settings'])} found)[/bold blue]")
        
        # Group settings by prefix for better organization
        setting_groups = {}
        for key, value in metadata['settings'].items():
            prefix = key.split('.')[0] if '.' in key else 'root'
            if prefix not in setting_groups:
                setting_groups[prefix] = {}
            setting_groups[prefix][key] = value
        
        for group_name, settings in setting_groups.items():
            if len(settings) <= 10:  # Only show small groups
                group_tree = Tree(f"[bold]{group_name}[/bold]")
                for key, value in list(settings.items())[:10]:  # Limit to 10 items
                    group_tree.add(f"[green]{key}:[/green] {value}")
                console.print(group_tree)
    
    # Raw file list if requested
    if metadata['raw_files']:
        console.print(f"\n[bold]Raw Files Extracted[/bold]")
        for file_path in metadata['raw_files']:
            console.print(f"  • {file_path}")
    
    # Errors
    if metadata['errors']:
        console.print(f"\n[bold red]Errors ({len(metadata['errors'])})[/bold red]")
        for error in metadata['errors']:
            console.print(f"  • {error}")

@click.command()
@click.argument('save_path', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', 'output_dir', type=click.Path(path_type=Path), 
              default='./tmp', help='Output directory for temporary files')
@click.option('--raw', '-r', is_flag=True, 
              help='Extract all non-.bb8 files for examination')
def extract_metadata(save_path: Path, output_dir: Path, raw: bool):
    """Extract ecosystem metadata and zone settings from Bibites save .zip files."""
    
    try:
        metadata = extract_metadata_from_save(save_path, output_dir, extract_raw=raw)
        display_metadata_results(metadata)
        
        if raw:
            console.print(f"\n[green]Raw files extracted to: {output_dir.resolve()}[/green]")
        
    except MetadataExtractionError as e:
        console.print(f"[red]Extraction failed: {e}[/red]")
        raise click.Abort()

if __name__ == '__main__':
    extract_metadata()