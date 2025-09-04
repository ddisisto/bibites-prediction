"""
bibites_crosspolinate.py - Cross-pollination functionality for bibites ecosystem manipulation.

Handles cross-pollination operations including:
- Fitness ranking and selection of top organisms
- Template injection between different save files
- Position randomization within ecosystem bounds
- Save file creation with combined populations

This module enables evolutionary experimentation by transferring fittest organisms
between different ecosystem saves.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from rich.console import Console
import json
import zipfile
import random
from datetime import datetime
import shutil

# Import data access functions
from .bibites_data import (
    load_bibites_from_directory, 
    BibitesDataError
)

# Import save access functions
from ..extract_save import (
    find_save_by_name, get_output_directory, is_directory_cached, 
    extract_save_files, SaveExtractionError, SAVEFILES_PATH
)

console = Console()

class BibitesCrossPollinateError(Exception):
    """Raised when cross-pollination operation fails."""
    pass

def get_fittest_bibites(bibites: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
    """Get the fittest bibites based on generation number.
    
    Args:
        bibites: List of bibite JSON dictionaries
        count: Number of fittest bibites to return
        
    Returns:
        List of top fittest bibites (copies of original data)
    """
    # Sort by generation number (fitness proxy) in descending order
    sorted_bibites = sorted(bibites, key=lambda b: b.get('genes', {}).get('gen', 0), reverse=True)
    
    # Return deep copies of the top N bibites to avoid modifying originals
    fittest = []
    for i in range(min(count, len(sorted_bibites))):
        fittest.append(json.loads(json.dumps(sorted_bibites[i])))
    
    return fittest

def randomize_bibite_positions(bibites: List[Dict[str, Any]], bounds: Tuple[float, float, float, float]) -> None:
    """Randomize positions of bibites within specified bounds.
    
    Args:
        bibites: List of bibite JSON dictionaries (modified in-place)
        bounds: Tuple of (min_x, max_x, min_y, max_y) coordinates
    """
    min_x, max_x, min_y, max_y = bounds
    
    for bibite in bibites:
        if 'transform' in bibite and 'position' in bibite['transform']:
            new_x = random.uniform(min_x, max_x)
            new_y = random.uniform(min_y, max_y)
            bibite['transform']['position'] = [new_x, new_y]

def create_save_zip(output_path: Path, bibites_dir: Path, eggs_dir: Path, images_dir: Path) -> None:
    """Create a new save zip file from extracted directories.
    
    Args:
        output_path: Path for the new .zip file
        bibites_dir: Directory containing bibite .bb8 files
        eggs_dir: Directory containing egg .bb8 files
        images_dir: Directory containing image files
        
    Raises:
        BibitesCrossPollinateError: If save creation fails
    """
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add bibites
            if bibites_dir.exists():
                for bb8_file in bibites_dir.glob('*.bb8'):
                    arcname = f"bibites/{bb8_file.name}"
                    zf.write(bb8_file, arcname)
            
            # Add eggs
            if eggs_dir.exists():
                for bb8_file in eggs_dir.glob('*.bb8'):
                    arcname = f"eggs/{bb8_file.name}"
                    zf.write(bb8_file, arcname)
            
            # Add images
            if images_dir.exists():
                for img_file in images_dir.iterdir():
                    if img_file.is_file():
                        arcname = f"images/{img_file.name}"
                        zf.write(img_file, arcname)
        
        console.print(f"[green]Successfully created save file: {output_path}[/green]")
        
    except Exception as e:
        raise BibitesCrossPollinateError(f"Failed to create save zip file: {e}")

def run_inject_fittest(source_name: str, target_name: str, count: int, 
                      output_name: Optional[str]) -> None:
    """Inject fittest bibites from source save into target save.
    
    Args:
        source_name: Name pattern for source save
        target_name: Name pattern for target save
        count: Number of fittest bibites to inject
        output_name: Optional custom output name (without .zip extension)
        
    Raises:
        BibitesCrossPollinateError: If cross-pollination fails
    """
    try:
        # Find source and target saves
        source_zip = find_save_by_name(source_name)
        target_zip = find_save_by_name(target_name)
        
        console.print(f"[blue]Source: {source_zip.name}[/blue]")
        console.print(f"[blue]Target: {target_zip.name}[/blue]")
        
        # Extract source and target data if needed
        source_dir = get_output_directory(source_zip)
        target_dir = get_output_directory(target_zip)
        
        # Ensure data is extracted
        if not is_directory_cached(source_dir):
            console.print(f"[green]Extracting source: {source_zip.name}[/green]")
            extract_save_files(source_zip, source_dir)
        
        if not is_directory_cached(target_dir):
            console.print(f"[green]Extracting target: {target_zip.name}[/green]")
            extract_save_files(target_zip, target_dir)
        
        # Load bibites from source and target
        source_bibites = load_bibites_from_directory(source_dir / 'bibites')
        target_bibites = load_bibites_from_directory(target_dir / 'bibites')
        
        console.print(f"[cyan]Found {len(source_bibites)} bibites in source[/cyan]")
        console.print(f"[cyan]Found {len(target_bibites)} bibites in target[/cyan]")
        
        # Get fittest bibites from source
        fittest = get_fittest_bibites(source_bibites, count)
        
        if not fittest:
            raise BibitesCrossPollinateError("No fittest bibites found in source")
        
        console.print(f"[green]Selected top {len(fittest)} fittest bibites (generations: {[b['genes']['gen'] for b in fittest]})[/green]")
        
        # Determine position bounds from target bibites
        target_positions = []
        for bibite in target_bibites:
            if 'transform' in bibite and 'position' in bibite['transform']:
                pos = bibite['transform']['position']
                target_positions.append((pos[0], pos[1]))
        
        if target_positions:
            xs = [pos[0] for pos in target_positions]
            ys = [pos[1] for pos in target_positions]
            bounds = (min(xs) - 50, max(xs) + 50, min(ys) - 50, max(ys) + 50)
        else:
            # Default bounds if no target positions found
            bounds = (-100, 100, -100, 100)
        
        # Randomize positions of fittest bibites
        randomize_bibite_positions(fittest, bounds)
        console.print(f"[cyan]Randomized positions within bounds: {bounds}[/cyan]")
        
        # Create temporary directory for combined save
        temp_dir = Path('./tmp') / f"cross_pollination_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        temp_bibites_dir = temp_dir / 'bibites'
        temp_eggs_dir = temp_dir / 'eggs'
        temp_images_dir = temp_dir / 'images'
        
        temp_bibites_dir.mkdir(exist_ok=True)
        temp_eggs_dir.mkdir(exist_ok=True)
        temp_images_dir.mkdir(exist_ok=True)
        
        # Copy target data to temp directory
        if (target_dir / 'eggs').exists():
            shutil.copytree(target_dir / 'eggs', temp_eggs_dir, dirs_exist_ok=True)
        if (target_dir / 'images').exists():
            shutil.copytree(target_dir / 'images', temp_images_dir, dirs_exist_ok=True)
        
        # Write combined bibites (target + injected fittest)
        combined_bibites = target_bibites + fittest
        
        for i, bibite in enumerate(combined_bibites):
            output_file = temp_bibites_dir / f"bibite_{i}.bb8"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(bibite, f, separators=(',', ':'))
        
        console.print(f"[green]Combined {len(target_bibites)} target + {len(fittest)} injected = {len(combined_bibites)} total bibites[/green]")
        
        # Generate output filename
        if output_name:
            output_filename = f"{output_name}.zip"
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"generated_{timestamp}_{target_zip.stem}.zip"
        
        # Create output path in Savefiles directory
        output_path = SAVEFILES_PATH / output_filename
        
        # Create the new save zip file
        create_save_zip(output_path, temp_bibites_dir, temp_eggs_dir, temp_images_dir)
        
        # Clean up temp directory
        shutil.rmtree(temp_dir)
        
        console.print(f"[bold green]Cross-pollination complete![/bold green]")
        console.print(f"[green]Output: {output_path}[/green]")
        console.print(f"[cyan]Added {len(fittest)} evolved predators to {len(target_bibites)} herbivores[/cyan]")
        console.print(f"[cyan]Total organisms: {len(combined_bibites)}[/cyan]")
        
    except (SaveExtractionError, BibitesDataError, IOError, json.JSONDecodeError) as e:
        raise BibitesCrossPollinateError(f"Cross-pollination failed: {e}")