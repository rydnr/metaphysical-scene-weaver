#!/usr/bin/env python3
"""
Content Consolidation Script for Metaphysical Scene Weaver
Consolidates the best content from variant folders into main numbered folders
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, List, Optional

def find_best_content(scene_num: str, content_dir: Path) -> Dict[str, Path]:
    """Find the best version of each file type for a given scene."""
    best_files = {
        'prompt': None,
        'narrator': None,
        'scene_description': None,
        'emotion': None,
        'philosophy': None
    }
    
    # Priority order for selecting files
    # 1. Check main numbered folder first
    main_folder = content_dir / scene_num
    
    # 2. Then check variant folders
    variant_folders = [d for d in content_dir.iterdir() 
                      if d.is_dir() and d.name.startswith(f"{scene_num}_")]
    
    all_folders = [main_folder] + variant_folders if main_folder.exists() else variant_folders
    
    for folder in all_folders:
        if not folder.exists():
            continue
            
        # Check for prompt files (prefer enriched versions)
        if not best_files['prompt']:
            if (folder / 'prompt_enriched.txt').exists():
                best_files['prompt'] = folder / 'prompt_enriched.txt'
            elif (folder / 'prompt.txt').exists():
                best_files['prompt'] = folder / 'prompt.txt'
        
        # Check for narrator files
        if not best_files['narrator'] and (folder / 'narrator.txt').exists():
            best_files['narrator'] = folder / 'narrator.txt'
            
        # Check for scene description
        if not best_files['scene_description'] and (folder / 'scene_description.txt').exists():
            best_files['scene_description'] = folder / 'scene_description.txt'
            
        # Check for emotion files
        for emotion_file in ['emotion_atmosphere.txt', 'emotion.txt', 'emotions.txt']:
            if not best_files['emotion'] and (folder / emotion_file).exists():
                best_files['emotion'] = folder / emotion_file
                break
                
        # Check for philosophy files
        for phil_file in ['philosophy.txt', 'philosophical_analysis.txt']:
            if not best_files['philosophy'] and (folder / phil_file).exists():
                best_files['philosophy'] = folder / phil_file
                break
    
    return best_files

def consolidate_scene(scene_num: str, content_dir: Path, backup_dir: Path) -> Dict[str, str]:
    """Consolidate all content for a single scene into the main numbered folder."""
    results = {
        'scene': scene_num,
        'status': 'success',
        'files_copied': [],
        'missing_files': [],
        'errors': []
    }
    
    # Create main folder if it doesn't exist
    main_folder = content_dir / scene_num
    main_folder.mkdir(exist_ok=True)
    
    # Find best content files
    best_files = find_best_content(scene_num, content_dir)
    
    # Copy files to main folder
    for file_type, source_path in best_files.items():
        if source_path and source_path.exists():
            # Determine target filename
            if file_type == 'prompt':
                target_name = 'prompt.txt'
            elif file_type == 'emotion':
                target_name = 'emotion_atmosphere.txt'
            else:
                target_name = f'{file_type}.txt'
            
            target_path = main_folder / target_name
            
            try:
                # Backup existing file if it exists
                if target_path.exists():
                    backup_path = backup_dir / scene_num / target_name
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target_path, backup_path)
                
                # Copy the best version
                shutil.copy2(source_path, target_path)
                results['files_copied'].append(f"{file_type}: {source_path.parent.name}/{source_path.name}")
                
            except Exception as e:
                results['errors'].append(f"Error copying {file_type}: {str(e)}")
        else:
            results['missing_files'].append(file_type)
    
    # Create metadata.json with consolidation info
    metadata = {
        'scene_number': scene_num,
        'consolidated_from': {
            file_type: str(source_path.parent.name) if source_path else None 
            for file_type, source_path in best_files.items()
        },
        'missing_content': results['missing_files']
    }
    
    metadata_path = main_folder / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    if results['errors']:
        results['status'] = 'partial'
    elif results['missing_files']:
        results['status'] = 'incomplete'
    
    return results

def clean_variant_folders(scene_num: str, content_dir: Path, archive_dir: Path) -> int:
    """Archive variant folders after consolidation."""
    count = 0
    variant_folders = [d for d in content_dir.iterdir() 
                      if d.is_dir() and d.name.startswith(f"{scene_num}_")]
    
    for folder in variant_folders:
        try:
            target = archive_dir / folder.name
            shutil.move(str(folder), str(target))
            count += 1
        except Exception as e:
            print(f"Error archiving {folder.name}: {e}")
    
    return count

def main():
    """Main consolidation process."""
    content_dir = Path('/home/chous/work/metaphysical-scene-weaver/content')
    backup_dir = content_dir / '_backups'
    archive_dir = content_dir / '_archived_variants'
    
    backup_dir.mkdir(exist_ok=True)
    archive_dir.mkdir(exist_ok=True)
    
    print("🔄 Starting Content Consolidation Process")
    print("=" * 50)
    
    # Get all scene numbers (001-020)
    scene_numbers = [f"{i:03d}" for i in range(1, 21)]
    
    all_results = []
    
    for scene_num in scene_numbers:
        print(f"\n📁 Processing Scene {scene_num}...")
        
        # Consolidate content
        result = consolidate_scene(scene_num, content_dir, backup_dir)
        all_results.append(result)
        
        # Print results
        if result['files_copied']:
            print(f"  ✅ Copied: {', '.join([f.split(':')[0] for f in result['files_copied']])}")
        if result['missing_files']:
            print(f"  ⚠️  Missing: {', '.join(result['missing_files'])}")
        if result['errors']:
            print(f"  ❌ Errors: {', '.join(result['errors'])}")
        
        # Archive variant folders
        archived_count = clean_variant_folders(scene_num, content_dir, archive_dir)
        if archived_count > 0:
            print(f"  📦 Archived {archived_count} variant folders")
    
    # Summary report
    print("\n" + "=" * 50)
    print("📊 CONSOLIDATION SUMMARY")
    print("=" * 50)
    
    complete = sum(1 for r in all_results if r['status'] == 'success')
    incomplete = sum(1 for r in all_results if r['status'] == 'incomplete')
    partial = sum(1 for r in all_results if r['status'] == 'partial')
    
    print(f"✅ Complete scenes: {complete}/20")
    print(f"⚠️  Incomplete scenes: {incomplete}")
    print(f"❌ Scenes with errors: {partial}")
    
    # List missing content
    print("\n📋 Missing Content Summary:")
    for result in all_results:
        if result['missing_files']:
            print(f"  Scene {result['scene']}: {', '.join(result['missing_files'])}")
    
    # Create final report
    report_path = content_dir / 'consolidation_report.json'
    with open(report_path, 'w') as f:
        json.dump({
            'summary': {
                'total_scenes': len(scene_numbers),
                'complete': complete,
                'incomplete': incomplete,
                'errors': partial
            },
            'details': all_results
        }, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_path}")
    print("\n✨ Consolidation complete! Variant folders archived to _archived_variants/")

if __name__ == "__main__":
    main()