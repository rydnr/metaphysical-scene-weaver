#!/usr/bin/env python3
"""Check status of narrator files across all scene folders."""

from pathlib import Path


def check_narrator_files():
    """Check which folders have narrator content."""
    content_dir = Path("content")
    
    print("📚 NARRATOR FILE STATUS CHECK")
    print("=" * 60)
    
    # Track what we find
    numbered_with_narrator = []
    named_with_narrator = []
    missing_narrator = []
    
    # Check all scene folders
    for scene_num in range(1, 21):
        scene_id = f"{scene_num:03d}"
        
        # Check numbered folder
        numbered_folder = content_dir / scene_id
        if numbered_folder.exists():
            narrator_file = numbered_folder / "narrator" / "commentary.txt"
            intro_file = numbered_folder / "narrator" / "introduction.txt"
            if narrator_file.exists() or intro_file.exists():
                numbered_with_narrator.append(scene_id)
        
        # Check named folders
        named_folders = list(content_dir.glob(f"{scene_id}_*"))
        for folder in named_folders:
            if folder.name != scene_id:  # Skip bare numbered folders
                narrator_file = folder / "narrator" / "commentary.txt"
                intro_file = folder / "narrator" / "introduction.txt"
                narrator_txt = folder / "narrator.txt"
                
                if any([narrator_file.exists(), intro_file.exists(), narrator_txt.exists()]):
                    named_with_narrator.append(folder.name)
                    # Show which file exists
                    if narrator_file.exists():
                        print(f"✅ {folder.name}/narrator/commentary.txt")
                    if intro_file.exists():
                        print(f"✅ {folder.name}/narrator/introduction.txt")
                    if narrator_txt.exists():
                        print(f"✅ {folder.name}/narrator.txt")
        
        # Check if scene has no narrator at all
        has_narrator = False
        if scene_id in numbered_with_narrator:
            has_narrator = True
        for named in named_with_narrator:
            if named.startswith(scene_id):
                has_narrator = True
                break
        
        if not has_narrator:
            missing_narrator.append(scene_id)
    
    # Summary
    print("\n📊 SUMMARY")
    print("=" * 60)
    print(f"Numbered folders with narrator: {len(numbered_with_narrator)}")
    print(f"Named folders with narrator: {len(named_with_narrator)}")
    print(f"Scenes missing narrator: {len(missing_narrator)}")
    
    if missing_narrator:
        print(f"\n⚠️  Missing narrator for scenes: {', '.join(missing_narrator)}")
    
    # Consolidation recommendations
    print("\n💡 CONSOLIDATION NEEDED")
    print("=" * 60)
    
    for scene_num in range(1, 21):
        scene_id = f"{scene_num:03d}"
        numbered_folder = content_dir / scene_id
        
        if numbered_folder.exists():
            narrator_file = numbered_folder / "narrator" / "commentary.txt"
            if not narrator_file.exists():
                # Look for narrator in named folders
                named_folders = list(content_dir.glob(f"{scene_id}_*"))
                for folder in named_folders:
                    if folder.name != scene_id:
                        sources = [
                            folder / "narrator" / "commentary.txt",
                            folder / "narrator" / "introduction.txt",
                            folder / "narrator.txt"
                        ]
                        for source in sources:
                            if source.exists():
                                print(f"Copy: {source} → {narrator_file}")
                                break


if __name__ == "__main__":
    check_narrator_files()