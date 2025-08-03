"""Command-line interface for the Metaphysical Scene Weaver."""

import click
from pathlib import Path
import json
import logging
from typing import Optional
import sys

from .core.scene_weaver import SceneWeaver
from .core.script_parser import ScriptParser


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Metaphysical Scene Weaver - Transform philosophical dialogue into visual narratives."""
    pass


@cli.command()
@click.argument('script_file', type=click.Path(exists=True, path_type=Path))
@click.option(
    '--characters', '-c',
    type=click.Path(exists=True, path_type=Path),
    default='characters.json',
    help='Path to characters JSON file'
)
@click.option(
    '--places', '-p',
    type=click.Path(exists=True, path_type=Path),
    default='places.json',
    help='Path to places JSON file'
)
@click.option(
    '--output', '-o',
    type=click.Path(path_type=Path),
    default='output',
    help='Output directory for generated prompts'
)
@click.option(
    '--style', '-s',
    type=click.Choice(['comic book', 'manga', 'graphic novel', 'cinematic']),
    default='comic book',
    help='Visual style for prompt generation'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose logging'
)
def process(
    script_file: Path,
    characters: Path,
    places: Path,
    output: Path,
    style: str,
    verbose: bool
):
    """Process a script file and generate enriched scene prompts."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize the scene weaver
        click.echo(f"Initializing Scene Weaver with style: {style}")
        weaver = SceneWeaver(characters, places, style)
        
        # Process the script
        click.echo(f"Processing script: {script_file}")
        with click.progressbar(length=100, label='Processing scenes') as bar:
            scenes = weaver.process_script(script_file)
            bar.update(100)
        
        # Export results
        click.echo(f"Exporting {len(scenes)} scenes to {output}/")
        weaver.export_prompts(output)
        
        click.echo(click.style("✓ Processing complete!", fg='green'))
        click.echo(f"Generated prompts saved to: {output}/")
        
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'), err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('script_file', type=click.Path(exists=True, path_type=Path))
@click.option(
    '--output', '-o',
    type=click.Path(path_type=Path),
    help='Output JSON file'
)
def parse(script_file: Path, output: Optional[Path]):
    """Parse a script file and output structured JSON."""
    try:
        parser = ScriptParser()
        
        click.echo(f"Parsing script: {script_file}")
        entries = parser.parse_file(script_file)
        
        click.echo(f"Parsed {len(entries)} entries")
        
        if output:
            parser.to_json(entries, output)
            click.echo(f"Saved parsed data to: {output}")
        else:
            # Print summary to console
            for i, entry in enumerate(entries[:5]):
                click.echo(f"\n[{entry.id}] {entry.speaker}: {entry.dialogue[:50]}...")
            if len(entries) > 5:
                click.echo(f"\n... and {len(entries) - 5} more entries")
                
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('entry_id')
@click.argument('script_file', type=click.Path(exists=True, path_type=Path))
@click.option(
    '--characters', '-c',
    type=click.Path(exists=True, path_type=Path),
    default='characters.json',
    help='Path to characters JSON file'
)
@click.option(
    '--places', '-p',
    type=click.Path(exists=True, path_type=Path),
    default='places.json',
    help='Path to places JSON file'
)
@click.option(
    '--style', '-s',
    type=click.Choice(['comic book', 'manga', 'graphic novel', 'cinematic']),
    default='comic book',
    help='Visual style for prompt generation'
)
def preview(
    entry_id: str,
    script_file: Path,
    characters: Path,
    places: Path,
    style: str
):
    """Preview a single scene's generated prompt."""
    try:
        # Parse script
        parser = ScriptParser()
        entries = parser.parse_file(script_file)
        
        # Find the requested entry
        target_entry = None
        entry_index = None
        for i, entry in enumerate(entries):
            if entry.id == entry_id:
                target_entry = entry
                entry_index = i
                break
        
        if not target_entry:
            click.echo(click.style(f"✗ Entry {entry_id} not found", fg='red'))
            sys.exit(1)
        
        # Initialize weaver and process single entry
        weaver = SceneWeaver(characters, places, style)
        scene = weaver.process_entry(target_entry, entry_index, entries)
        
        # Display results
        click.echo(click.style(f"\n=== Scene {entry_id} ===", fg='cyan', bold=True))
        click.echo(f"\nSpeaker: {target_entry.speaker}")
        click.echo(f"Dialogue: {target_entry.dialogue}")
        
        if target_entry.stage_directions:
            click.echo(f"\nStage Directions:")
            for direction in target_entry.stage_directions:
                click.echo(f"  • {direction}")
        
        click.echo(click.style("\n=== Generated Prompt ===", fg='green', bold=True))
        click.echo(scene.prompt)
        
        click.echo(click.style("\n=== Scene Analysis ===", fg='yellow', bold=True))
        click.echo(f"Complexity: {scene.metadata.get('visual_complexity', 'unknown')}")
        click.echo(f"Philosophy: {scene.philosophy.get('primary_concept', 'none')} (depth: {scene.philosophy.get('depth_level', 0)})")
        click.echo(f"Emotion: {scene.emotion.get('primary', 'neutral')}")
        
        if scene.visual_elements:
            click.echo(f"\nVisual Elements:")
            for element in scene.visual_elements:
                click.echo(f"  • {element}")
                
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
def analyze():
    """Analyze script patterns and generate insights."""
    click.echo("Analysis feature coming soon...")
    # TODO: Implement script analysis features


@cli.command()
@click.option(
    '--host', '-h',
    default='127.0.0.1',
    help='Host to run the server on'
)
@click.option(
    '--port', '-p',
    default=8000,
    type=int,
    help='Port to run the server on'
)
def serve(host: str, port: int):
    """Start the API server for real-time processing."""
    try:
        import uvicorn
        from .api import app
        
        click.echo(f"Starting Metaphysical Scene Weaver API server on {host}:{port}")
        uvicorn.run(app, host=host, port=port)
        
    except ImportError:
        click.echo(click.style("✗ API dependencies not installed. Run: pip install metaphysical-scene-weaver[api]", fg='red'))
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
def validate():
    """Validate configuration and data files."""
    issues = []
    
    # Check for required files
    required_files = ['characters.json', 'places.json']
    for file in required_files:
        path = Path(file)
        if not path.exists():
            issues.append(f"Missing required file: {file}")
        else:
            try:
                with open(path) as f:
                    data = json.load(f)
                click.echo(click.style(f"✓ {file} is valid JSON", fg='green'))
            except json.JSONDecodeError as e:
                issues.append(f"Invalid JSON in {file}: {str(e)}")
    
    # Check for required dependencies
    try:
        import spacy
        click.echo(click.style("✓ spaCy is installed", fg='green'))
        
        # Check for language model
        try:
            nlp = spacy.load("en_core_web_sm")
            click.echo(click.style("✓ spaCy English model is installed", fg='green'))
        except OSError:
            issues.append("spaCy English model not installed. Run: python -m spacy download en_core_web_sm")
    except ImportError:
        issues.append("spaCy not installed properly")
    
    # Report results
    if issues:
        click.echo(click.style("\n✗ Validation failed:", fg='red'))
        for issue in issues:
            click.echo(f"  • {issue}")
        sys.exit(1)
    else:
        click.echo(click.style("\n✓ All validations passed!", fg='green'))


if __name__ == '__main__':
    cli()