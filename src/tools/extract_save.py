#!/usr/bin/env python3
"""
extract_save.py - Extract .bb8 files and images from Bibites save .zip files.

Organizes extracted files (living vs eggs, numbered correctly) and extracts
ecosystem screenshots. Handles multiple save files with batch processing.

Usage examples:
  python -m src.tools.extract_save Savefiles/validation-1.zip data/extracted/
  python -m src.tools.extract_save --batch Savefiles/ data/batch_extracted/
"""

import click
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.progress import track, Progress
from rich.table import Table
import re

console = Console()

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
@click.argument('input_path', type=click.Path(exists=True, path_type=Path))
@click.argument('output_dir', type=click.Path(path_type=Path))
@click.option('--batch', '-b', is_flag=True, 
              help='Process all .zip files in directory')
@click.option('--overwrite', is_flag=True,
              help='Overwrite existing files in output directory')
def extract_save(input_path: Path, output_dir: Path, batch: bool, overwrite: bool):
    """Extract .bb8 files and images from Bibites save .zip files."""
    
    # Determine input files
    if batch or input_path.is_dir():
        zip_files = list(input_path.glob('*.zip'))
        if not zip_files:
            console.print(f"[red]No .zip files found in {input_path}[/red]")
            return
        console.print(f"[blue]Found {len(zip_files)} zip files for batch processing[/blue]")
    else:
        zip_files = [input_path]
    
    # Check output directory
    if output_dir.exists() and not overwrite:
        existing_bb8_files = list(output_dir.rglob('*.bb8'))
        existing_image_files = list(output_dir.rglob('images/*'))
        if existing_bb8_files or existing_image_files:
            console.print(f"[yellow]Output directory {output_dir} contains {len(existing_bb8_files)} .bb8 files and {len(existing_image_files)} image files[/yellow]")
            console.print("[yellow]Use --overwrite to overwrite existing files[/yellow]")
            if not click.confirm("Continue anyway?"):
                return
    
    # Process files
    all_stats = []
    total_bibites = 0
    total_eggs = 0
    total_unknown = 0
    total_images = 0
    total_errors = 0
    
    with Progress() as progress:
        task = progress.add_task("[green]Extracting saves...", total=len(zip_files))
        
        for zip_file in zip_files:
            try:
                # Create subdirectory for this save if batch processing
                if len(zip_files) > 1:
                    save_output_dir = output_dir / zip_file.stem
                else:
                    save_output_dir = output_dir
                
                stats = extract_save_files(zip_file, save_output_dir)
                all_stats.append(stats)
                
                total_bibites += stats['bibites']
                total_eggs += stats['eggs'] 
                total_unknown += stats['unknown']
                total_images += stats['images']
                total_errors += len(stats['errors'])
                
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
    
    table.add_row("Save files processed", str(len(zip_files)))
    table.add_row("Bibites extracted", str(total_bibites))
    table.add_row("Eggs extracted", str(total_eggs))
    table.add_row("Images extracted", str(total_images))
    if total_unknown > 0:
        table.add_row("Unknown files", str(total_unknown))
    if total_errors > 0:
        table.add_row("Errors", str(total_errors), style="red")
    
    console.print(table)
    
    console.print(f"\n[green]Files extracted to: {output_dir.resolve()}[/green]")

if __name__ == '__main__':
    extract_save()