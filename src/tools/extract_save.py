#!/usr/bin/env python3
"""
extract_save.py - Path-agnostic autosave extraction tool.

Simplified CLI that hardcodes paths and provides cache-transparent operation.
Always looks in Steam autosaves directory, always extracts to data/ directory.

Usage:
  python -m src.tools.extract_save --latest
  python -m src.tools.extract_save --last 3
  python -m src.tools.extract_save --name autosave_20250831204442
  python -m src.tools.extract_save --name 20250831204442  # partial match

Features:
  - Hardcoded autosaves path: no path management needed
  - Cache-transparent: automatically uses cached data when available
  - Smart organism categorization (bibites vs eggs, numbered correctly)
  - Always outputs to data/ with filename correspondence
"""

import click
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.progress import track, Progress
from rich.table import Table
import re
from datetime import datetime
import glob

console = Console()

# Hardcoded paths
AUTOSAVES_PATH = Path("/home/daniel/.local/share/Steam/steamapps/compatdata/2736860/pfx/drive_c/users/steamuser/AppData/LocalLow/The Bibites/The Bibites/Savefiles/Autosaves/")
DATA_OUTPUT_PATH = Path("data")

class SaveExtractionError(Exception):
    """Raised when save file extraction fails."""
    pass

def is_bb8_file(filename: str) -> bool:
    """Check if filename is a .bb8 file."""
    return filename.lower().endswith('.bb8')

def is_image_file(filename: str) -> bool:
    """Check if filename is an image file."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    return Path(filename).suffix.lower() in image_extensions

def categorize_bb8_file(filename: str) -> tuple[str, Optional[int]]:
    """
    Categorize a .bb8 file and extract its number.
    
    Args:
        filename: The filename (e.g., "bibites/bibite_5.bb8", "bibites\\bibite_5.bb8", or "eggs/egg_2.bb8")
        
    Returns:
        Tuple of (category, number) where category is 'bibite', 'egg', or 'unknown'
    """
    # Normalize path separators and get basename
    normalized_path = filename.replace('\\', '/')
    basename = Path(normalized_path).name.lower()
    
    # Check if path contains bibites or eggs directory
    path_parts = normalized_path.lower().split('/')
    
    # Match bibite_N.bb8 pattern
    bibite_match = re.match(r'bibite_(\d+)\.bb8$', basename)
    if bibite_match and ('bibites' in path_parts or 'bibite' in basename):
        return ('bibite', int(bibite_match.group(1)))
    
    # Match egg_N.bb8 pattern  
    egg_match = re.match(r'egg_(\d+)\.bb8$', basename)
    if egg_match and ('eggs' in path_parts or 'egg' in basename):
        return ('egg', int(egg_match.group(1)))
    
    return ('unknown', None)

def get_all_autosaves() -> List[Path]:
    """
    Get all autosave files from the hardcoded autosaves directory.
    
    Returns:
        List of autosave file paths, sorted by filename (oldest to newest)
        
    Raises:
        SaveExtractionError: If autosaves directory not found or no autosave files
    """
    if not AUTOSAVES_PATH.exists():
        raise SaveExtractionError(f"Autosaves directory not found: {AUTOSAVES_PATH}")
    
    # Find all autosave zip files
    autosave_files = list(AUTOSAVES_PATH.glob('autosave_*.zip'))
    if not autosave_files:
        raise SaveExtractionError(f"No autosave files found in {AUTOSAVES_PATH}")
    
    # Sort by filename (which contains timestamp)
    autosave_files.sort(key=lambda x: x.name)
    return autosave_files

def find_latest_autosave() -> Path:
    """Find the most recent autosave file."""
    autosaves = get_all_autosaves()
    latest = autosaves[-1]
    console.print(f"[blue]Found latest autosave: {latest.name}[/blue]")
    return latest

def find_last_n_autosaves(n: int) -> List[Path]:
    """Find the last N autosave files."""
    autosaves = get_all_autosaves()
    if n > len(autosaves):
        console.print(f"[yellow]Requested {n} autosaves, but only {len(autosaves)} available[/yellow]")
        return autosaves
    return autosaves[-n:]

def find_autosave_by_name(name_pattern: str) -> Path:
    """
    Find autosave by name or partial name match.
    
    Args:
        name_pattern: Full or partial autosave name (with or without .zip extension)
        
    Returns:
        Path to matching autosave file
        
    Raises:
        SaveExtractionError: If no match found or multiple matches
    """
    autosaves = get_all_autosaves()
    
    # Normalize the pattern (remove .zip if present)
    clean_pattern = name_pattern.replace('.zip', '').lower()
    
    # Find matches
    matches = []
    for autosave in autosaves:
        autosave_name = autosave.stem.lower()  # Remove .zip extension
        if clean_pattern in autosave_name or autosave_name == clean_pattern:
            matches.append(autosave)
    
    if not matches:
        raise SaveExtractionError(f"No autosave found matching '{name_pattern}'")
    elif len(matches) > 1:
        match_names = [m.name for m in matches]
        raise SaveExtractionError(f"Multiple autosaves match '{name_pattern}': {match_names}")
    
    found = matches[0]
    console.print(f"[blue]Found autosave: {found.name}[/blue]")
    return found

def get_output_directory(zip_path: Path) -> Path:
    """
    Get the output directory for an autosave file in the hardcoded data/ directory.
    
    Args:
        zip_path: Path to the autosave zip file
        
    Returns:
        Path to the output directory (data/autosave_timestamp/)
    """
    # Use filename stem directly for 1:1 correspondence (e.g., autosave_20250829205409.zip -> data/autosave_20250829205409/)
    filename = zip_path.stem
    return DATA_OUTPUT_PATH / filename

def is_directory_cached(output_dir: Path) -> bool:
    """
    Check if output directory exists and contains extracted data.
    
    Args:
        output_dir: Directory to check for cached data
        
    Returns:
        True if directory exists and has content, False otherwise
    """
    if not output_dir.exists():
        return False
        
    # Check if directory has any .bb8 files (main indicator of successful extraction)
    bb8_files = list(output_dir.rglob('*.bb8'))
    return len(bb8_files) > 0

def extract_save_files(zip_path: Path, output_dir: Path) -> Dict[str, Any]:
    """
    Extract all .bb8 files and images from a save zip file.
    
    Args:
        zip_path: Path to the save .zip file
        output_dir: Directory to extract files to
        
    Returns:
        Dict with extraction statistics
        
    Raises:
        SaveExtractionError: If extraction fails
    """
    if not zip_path.exists():
        raise SaveExtractionError(f"Save file not found: {zip_path}")
    
    if not zip_path.suffix.lower() == '.zip':
        raise SaveExtractionError(f"File is not a .zip file: {zip_path}")
    
    # Create output directories
    bibites_dir = output_dir / 'bibites'
    eggs_dir = output_dir / 'eggs'
    unknown_dir = output_dir / 'unknown'
    images_dir = output_dir / 'images'
    
    bibites_dir.mkdir(parents=True, exist_ok=True)
    eggs_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    
    stats = {
        'save_name': zip_path.stem,
        'bibites': 0,
        'eggs': 0,
        'unknown': 0,
        'images': 0,
        'errors': []
    }
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # Get all .bb8 files and images in the archive
            bb8_files = [name for name in zip_file.namelist() if is_bb8_file(name)]
            image_files = [name for name in zip_file.namelist() if is_image_file(name)]
            
            if not bb8_files and not image_files:
                console.print(f"[yellow]No .bb8 files or images found in {zip_path.name}[/yellow]")
                return stats
            
            console.print(f"[blue]Found {len(bb8_files)} .bb8 files and {len(image_files)} images in {zip_path.name}[/blue]")
            
            for file_path in bb8_files:
                try:
                    category, number = categorize_bb8_file(file_path)
                    
                    # Determine output location and filename
                    if category == 'bibite':
                        target_dir = bibites_dir
                        target_name = f"bibite_{number}.bb8"
                        stats['bibites'] += 1
                    elif category == 'egg':
                        target_dir = eggs_dir  
                        target_name = f"egg_{number}.bb8"
                        stats['eggs'] += 1
                    else:
                        # Unknown category - create directory if needed and preserve name
                        unknown_dir.mkdir(parents=True, exist_ok=True)
                        target_dir = unknown_dir
                        target_name = Path(file_path).name
                        stats['unknown'] += 1
                    
                    target_path = target_dir / target_name
                    
                    # Extract the file
                    with zip_file.open(file_path) as source:
                        with open(target_path, 'wb') as target:
                            target.write(source.read())
                    
                except Exception as e:
                    error_msg = f"Failed to extract {file_path}: {e}"
                    stats['errors'].append(error_msg)
                    console.print(f"[red]{error_msg}[/red]")
            
            # Extract image files
            for file_path in image_files:
                try:
                    # Use original filename for images
                    target_name = Path(file_path).name
                    target_path = images_dir / target_name
                    
                    # Handle duplicate filenames by adding number suffix
                    if target_path.exists():
                        stem = target_path.stem
                        suffix = target_path.suffix
                        counter = 1
                        while target_path.exists():
                            target_name = f"{stem}_{counter}{suffix}"
                            target_path = images_dir / target_name
                            counter += 1
                    
                    # Extract the image file
                    with zip_file.open(file_path) as source:
                        with open(target_path, 'wb') as target:
                            target.write(source.read())
                    
                    stats['images'] += 1
                    
                except Exception as e:
                    error_msg = f"Failed to extract image {file_path}: {e}"
                    stats['errors'].append(error_msg)
                    console.print(f"[red]{error_msg}[/red]")
        
        return stats
                    
    except zipfile.BadZipFile:
        raise SaveExtractionError(f"Invalid or corrupted zip file: {zip_path}")
    except Exception as e:
        raise SaveExtractionError(f"Error extracting {zip_path}: {e}")

@click.command()
@click.option('--latest', is_flag=True,
              help='Extract the latest autosave file')
@click.option('--last', type=int, metavar='N',
              help='Extract the last N autosave files')
@click.option('--name', type=str, metavar='PATTERN',
              help='Extract autosave by name or partial name match')
@click.option('--overwrite', is_flag=True,
              help='Overwrite existing cached data')
def extract_save(latest: bool, last: Optional[int], name: Optional[str], overwrite: bool):
    """Path-agnostic autosave extraction tool.
    
    Automatically looks in Steam autosaves directory and extracts to data/ directory.
    Cache-transparent operation: uses existing data when available.
    
    Examples:
        # Extract latest autosave
        python -m src.tools.extract_save --latest
        
        # Extract last 3 autosaves  
        python -m src.tools.extract_save --last 3
        
        # Extract specific autosave by name
        python -m src.tools.extract_save --name autosave_20250831204442
        python -m src.tools.extract_save --name 20250831204442  # partial match
    """
    
    # Validate exactly one option is specified
    options_count = sum([latest, last is not None, name is not None])
    if options_count == 0:
        console.print("[red]Error: Must specify exactly one option: --latest, --last N, or --name PATTERN[/red]")
        console.print("Use --help for usage examples")
        return
    elif options_count > 1:
        console.print("[red]Error: Cannot combine --latest, --last, and --name options[/red]")
        return
    
    try:
        # Determine which autosave files to process
        if latest:
            zip_files = [find_latest_autosave()]
        elif last is not None:
            if last <= 0:
                console.print("[red]Error: --last must be a positive number[/red]")
                return
            zip_files = find_last_n_autosaves(last)
            console.print(f"[blue]Found last {len(zip_files)} autosaves[/blue]")
        elif name is not None:
            zip_files = [find_autosave_by_name(name)]
        
    except SaveExtractionError as e:
        console.print(f"[red]Error: {e}[/red]")
        return
    
    # Process files
    all_stats = []
    total_bibites = 0
    total_eggs = 0
    total_unknown = 0
    total_images = 0
    total_errors = 0
    cached_files = 0
    output_paths = []
    
    with Progress() as progress:
        task = progress.add_task("[green]Processing autosaves...", total=len(zip_files))
        
        for zip_file in zip_files:
            try:
                # Get output directory for this autosave
                output_dir = get_output_directory(zip_file)
                output_paths.append(output_dir)
                
                # Check cache first (unless overwrite requested)
                if not overwrite and is_directory_cached(output_dir):
                    console.print(f"[blue]Using cached data from {output_dir}[/blue]")
                    cached_files += 1
                    
                    # Generate stats from cached files
                    bb8_files = list(output_dir.rglob('*.bb8'))
                    image_files = list((output_dir / 'images').glob('*')) if (output_dir / 'images').exists() else []
                    
                    # Count bibites vs eggs from cached files
                    bibites_count = len(list((output_dir / 'bibites').glob('*.bb8'))) if (output_dir / 'bibites').exists() else 0
                    eggs_count = len(list((output_dir / 'eggs').glob('*.bb8'))) if (output_dir / 'eggs').exists() else 0
                    unknown_count = len(bb8_files) - bibites_count - eggs_count
                    
                    stats = {
                        'save_name': zip_file.stem,
                        'bibites': bibites_count,
                        'eggs': eggs_count,
                        'unknown': max(0, unknown_count),
                        'images': len(image_files),
                        'errors': [],
                        'cached': True
                    }
                else:
                    # Extract the autosave
                    stats = extract_save_files(zip_file, output_dir)
                    stats['cached'] = False
                
                all_stats.append(stats)
                
                total_bibites += stats['bibites']
                total_eggs += stats['eggs'] 
                total_unknown += stats['unknown']
                total_images += stats['images']
                total_errors += len(stats['errors'])
                
                # Display individual file results
                if stats.get('cached', False):
                    console.print(f"[cyan]✓ {zip_file.name} (cached):[/cyan] "
                                f"{stats['bibites']} bibites, {stats['eggs']} eggs, {stats['images']} images"
                                + (f", {stats['unknown']} unknown" if stats['unknown'] > 0 else ""))
                else:
                    console.print(f"[green]✓ {zip_file.name}:[/green] "
                                f"{stats['bibites']} bibites, {stats['eggs']} eggs, {stats['images']} images"
                                + (f", {stats['unknown']} unknown" if stats['unknown'] > 0 else "")
                                + (f", {len(stats['errors'])} errors" if stats['errors'] else ""))
                
            except SaveExtractionError as e:
                console.print(f"[red]✗ {zip_file.name}: {e}[/red]")
                total_errors += 1
            
            progress.advance(task)
    
    # Summary table
    console.print("\n[bold]Extraction Summary[/bold]")
    table = Table()
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green")
    
    table.add_row("Autosave files processed", str(len(zip_files)))
    if cached_files > 0:
        table.add_row("Files from cache", str(cached_files), style="cyan")
        table.add_row("Files extracted", str(len(zip_files) - cached_files))
    table.add_row("Bibites total", str(total_bibites))
    table.add_row("Eggs total", str(total_eggs))
    table.add_row("Images total", str(total_images))
    if total_unknown > 0:
        table.add_row("Unknown files", str(total_unknown))
    if total_errors > 0:
        table.add_row("Errors", str(total_errors), style="red")
    
    console.print(table)
    
    # Display data paths for chaining with analysis tools
    console.print("\n[bold]Data Available At:[/bold]")
    for path in output_paths:
        if path.exists():
            console.print(f"[green]{path.resolve()}[/green]")
        else:
            console.print(f"[red]{path.resolve()} (extraction failed)[/red]")

if __name__ == '__main__':
    extract_save()