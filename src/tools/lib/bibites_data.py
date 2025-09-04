"""
bibites_data.py - Data access and path resolution for bibites ecosystem analysis.

Handles all data access operations including:
- Save file discovery (autosaves and manual saves)
- Path resolution and metadata extraction
- Data extraction and caching logic
- Save listing and information display

This module provides the foundational data access layer for the unified bibites tool.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.table import Table
import json

# Import data access layer from extract_save.py
from ..extract_save import (
    find_latest_autosave, find_last_n_autosaves, find_autosave_by_name,
    find_save_by_name, list_all_saves, get_save_info,
    get_output_directory, is_directory_cached, extract_save_files,
    SaveExtractionError, SAVEFILES_PATH, get_all_autosaves
)

console = Console()

class BibitesDataError(Exception):
    """Raised when data access operation fails."""
    pass

def resolve_data_paths(latest: bool, last: Optional[int], name: Optional[str], 
                      overwrite: bool = False) -> List[Path]:
    """
    Resolve user data selection to extracted data paths.
    Transparently handles extraction and caching for both autosaves and manual saves.
    
    Args:
        latest: Get latest autosave
        last: Get last N autosaves  
        name: Get save by name pattern (searches both autosaves and manual saves)
        overwrite: Force re-extraction even if cached
        
    Returns:
        List of data directory paths ready for analysis
        
    Raises:
        BibitesDataError: If data access fails
    """
    # Validate exactly one data selection option (this function should only be called when one is selected)
    options_count = sum([latest, last is not None, name is not None])
    if options_count == 0:
        raise BibitesDataError("Internal error: resolve_data_paths called with no data selection")
    elif options_count > 1:
        raise BibitesDataError("Cannot combine --latest, --last, and --name options")
    
    try:
        # Determine which save files to process
        if latest:
            zip_files = [find_latest_autosave()]
        elif last is not None:
            if last <= 0:
                raise BibitesDataError("--last must be a positive number")
            zip_files = find_last_n_autosaves(last)
            console.print(f"[blue]Found last {len(zip_files)} autosaves[/blue]")
        elif name is not None:
            # Use enhanced find_save_by_name that searches both autosaves and manual saves
            zip_files = [find_save_by_name(name)]
        
    except SaveExtractionError as e:
        raise BibitesDataError(f"Data access failed: {e}")
    
    # Extract/cache data transparently
    output_paths = []
    extraction_needed = False
    
    for zip_file in zip_files:
        try:
            # Get output directory for this save (works for both autosaves and manual saves)
            output_dir = get_output_directory(zip_file)
            output_paths.append(output_dir)
            
            # Check cache first (unless overwrite requested)
            if not overwrite and is_directory_cached(output_dir):
                console.print(f"[cyan]Using cached data: {zip_file.name}[/cyan]")
                continue
            else:
                console.print(f"[green]Extracting: {zip_file.name}[/green]")
                stats = extract_save_files(zip_file, output_dir)
                extraction_needed = True
                
                if stats['errors']:
                    console.print(f"[yellow]Extraction completed with {len(stats['errors'])} errors[/yellow]")
                    
        except SaveExtractionError as e:
            raise BibitesDataError(f"Failed to extract {zip_file.name}: {e}")
    
    if extraction_needed:
        console.print("[green]Data extraction complete[/green]")
    
    return output_paths

def display_save_listing() -> None:
    """Display a formatted listing of all available saves with metadata."""
    try:
        saves = list_all_saves()
        
        if not saves:
            console.print("[yellow]No save files found[/yellow]")
            return
        
        console.print(f"[bold]Available Save Files ({len(saves)} total)[/bold]\n")
        
        # Create table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Name", style="white", width=35)
        table.add_column("Type", justify="center", width=8)
        table.add_column("Size (MB)", justify="right", width=10)
        table.add_column("Modified", width=16)
        table.add_column("Organisms", justify="right", width=10)
        table.add_column("Status", justify="center", width=8)
        
        for save in saves:
            # Format type display
            save_type = "Auto" if save['type'] == 'autosave' else "Manual"
            
            # Format modified time
            modified_str = save['modified'].strftime("%m/%d %H:%M")
            
            # Format organism count
            organisms_str = str(save['organisms']) if save['organisms'] is not None else "—"
            
            # Format status
            status = "Cached" if save['cached'] else "New"
            status_style = "cyan" if save['cached'] else "green"
            
            # Truncate long names
            display_name = save['name']
            if len(display_name) > 33:
                display_name = display_name[:30] + "..."
            
            table.add_row(
                display_name,
                save_type,
                str(save['size_mb']),
                modified_str,
                organisms_str,
                f"[{status_style}]{status}[/{status_style}]"
            )
        
        console.print(table)
        console.print(f"\n[dim]Use --name PATTERN to select a save for analysis[/dim]")
        console.print(f"[dim]Use --latest to select the newest autosave[/dim]")
        
    except SaveExtractionError as e:
        console.print(f"[red]Error listing saves: {e}[/red]")

def get_zip_file_from_data_path(data_path: Path) -> Optional[Path]:
    """
    Find the original zip file from an extracted data path.
    This is used for metadata analysis that needs the source zip.
    
    Args:
        data_path: Path to extracted data directory
        
    Returns:
        Path to original zip file or None if not found
        
    Raises:
        BibitesDataError: If zip file cannot be located
    """
    # data_path should be like data/autosave_20250831115522/
    autosave_name = data_path.name
    
    try:
        all_saves = get_all_autosaves()
        for save in all_saves:
            if save.stem == autosave_name:
                return save
        
        raise BibitesDataError(f"Could not find source zip for dataset: {autosave_name}")
        
    except SaveExtractionError as e:
        raise BibitesDataError(f"Failed to locate source zip: {e}")

def load_bibites_from_directory(bibites_dir: Path) -> List[Dict[str, Any]]:
    """Load all bibite JSON data from a directory.
    
    Args:
        bibites_dir: Directory containing .bb8 files
        
    Returns:
        List of bibite JSON dictionaries
        
    Raises:
        BibitesDataError: If directory not found or loading fails
    """
    if not bibites_dir.exists():
        raise BibitesDataError(f"Bibites directory not found: {bibites_dir}")
    
    bibites = []
    bb8_files = list(bibites_dir.glob('*.bb8'))
    
    if not bb8_files:
        raise BibitesDataError(f"No .bb8 files found in {bibites_dir}")
    
    for bb8_file in bb8_files:
        try:
            with open(bb8_file, 'r', encoding='utf-8') as f:
                # Handle BOM if present
                content = f.read()
                if content.startswith('\ufeff'):
                    content = content[1:]
                bibite_data = json.loads(content)
                bibites.append(bibite_data)
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"[yellow]Warning: Failed to load {bb8_file.name}: {e}[/yellow]")
    
    if not bibites:
        raise BibitesDataError(f"Failed to load any valid bibite data from {bibites_dir}")
    
    return bibites