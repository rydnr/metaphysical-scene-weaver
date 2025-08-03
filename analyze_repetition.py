#!/usr/bin/env python3
"""Analyze repetitive patterns in scene descriptions."""

import os
import re
from collections import Counter, defaultdict
from pathlib import Path

def extract_patterns(content):
    """Extract various patterns from scene description content."""
    patterns = {
        'visual_elements': [],
        'emotional_tones': [],
        'philosophical_themes': [],
        'color_descriptions': [],
        'setting_descriptions': [],
        'character_descriptions': []
    }
    
    # Extract visual elements section
    visual_match = re.search(r'VISUAL ELEMENTS:(.*?)(?=PHILOSOPHICAL THEME:|EMOTIONAL TONE:|$)', content, re.DOTALL)
    if visual_match:
        visual_text = visual_match.group(1).strip()
        # Extract bullet points
        visual_elements = re.findall(r'[-•]\s*(.+)', visual_text)
        patterns['visual_elements'].extend(visual_elements)
    
    # Extract emotional tone
    emotion_match = re.search(r'EMOTIONAL TONE:\s*(.+)', content)
    if emotion_match:
        patterns['emotional_tones'].append(emotion_match.group(1).strip())
    
    # Extract philosophical theme
    philosophy_match = re.search(r'PHILOSOPHICAL THEME:\s*(.+)', content)
    if philosophy_match:
        patterns['philosophical_themes'].append(philosophy_match.group(1).strip())
    
    # Extract color descriptions
    colors = re.findall(r'(cool blues?|warm tones?|electric|neon|dark|bright|muted|vibrant|monochrome|grayscale)', content, re.IGNORECASE)
    patterns['color_descriptions'].extend(colors)
    
    # Extract common setting phrases
    settings = re.findall(r'(digital space|minimalist setting|abstract|geometric|code fragments|digital presence)', content, re.IGNORECASE)
    patterns['setting_descriptions'].extend(settings)
    
    return patterns

def analyze_scene_descriptions():
    """Analyze all scene_description.txt files for repetitive patterns."""
    content_dir = Path("/home/chous/work/metaphysical-scene-weaver/content")
    
    all_patterns = defaultdict(list)
    file_count = 0
    
    # Process all scene_description.txt files
    for scene_file in sorted(content_dir.glob("*/scene_description.txt")):
        file_count += 1
        try:
            with open(scene_file, 'r') as f:
                content = f.read()
                patterns = extract_patterns(content)
                
                for category, items in patterns.items():
                    all_patterns[category].extend(items)
        except Exception as e:
            print(f"Error processing {scene_file}: {e}")
    
    # Count frequencies
    results = {}
    for category, items in all_patterns.items():
        if items:
            counter = Counter(items)
            results[category] = counter.most_common(20)  # Top 20 for each category
    
    return results, file_count

def generate_report(results, file_count):
    """Generate the repetition analysis report."""
    report = []
    report.append("# Repetition Analysis Report for Scene Descriptions\n")
    report.append(f"## Overview\nAnalyzed {file_count} scene_description.txt files\n")
    
    # Visual Elements
    if 'visual_elements' in results:
        report.append("## Most Repeated Visual Elements\n")
        report.append("These visual descriptions appear most frequently:\n")
        for elem, count in results['visual_elements'][:15]:
            percentage = (count / file_count) * 100
            report.append(f"- **\"{elem}\"** - {count} times ({percentage:.1f}% of scenes)")
        report.append("")
    
    # Emotional Tones
    if 'emotional_tones' in results:
        report.append("## Repetitive Emotional Tones\n")
        tone_counts = {}
        for tone, count in results['emotional_tones']:
            tone_counts[tone] = count
        
        report.append(f"- **\"Engaged Dialogue\"** appears in {tone_counts.get('Engaged Dialogue', 0)} scenes")
        report.append(f"- **\"Profound Unease\"** appears in {tone_counts.get('Profound Unease', 0)} scenes")
        report.append(f"- **\"Contemplative\"** appears in {tone_counts.get('Contemplative', 0)} scenes")
        report.append("")
        
        report.append("### Full Emotional Tone Distribution:")
        for tone, count in results['emotional_tones']:
            percentage = (count / file_count) * 100
            report.append(f"- {tone}: {count} times ({percentage:.1f}%)")
        report.append("")
    
    # Philosophical Themes
    if 'philosophical_themes' in results:
        report.append("## Overused Philosophical Themes\n")
        for theme, count in results['philosophical_themes'][:10]:
            percentage = (count / file_count) * 100
            report.append(f"- **\"{theme}\"** - {count} times ({percentage:.1f}% of scenes)")
        report.append("")
    
    # Color Descriptions
    if 'color_descriptions' in results:
        report.append("## Repetitive Color Palettes\n")
        for color, count in results['color_descriptions'][:10]:
            report.append(f"- \"{color}\" - {count} occurrences")
        report.append("")
    
    # Setting Descriptions
    if 'setting_descriptions' in results:
        report.append("## Overused Setting Descriptions\n")
        for setting, count in results['setting_descriptions'][:10]:
            report.append(f"- \"{setting}\" - {count} occurrences")
        report.append("")
    
    # Recommendations
    report.append("## Key Findings and Recommendations\n")
    report.append("### 1. Visual Element Variety Needed")
    report.append("- Replace generic \"geometric patterns\" with specific shapes")
    report.append("- Vary \"digital presence\" with unique manifestations")
    report.append("- Move beyond \"cool blues\" to diverse color palettes\n")
    
    report.append("### 2. Emotional Range Expansion")
    report.append("- \"Engaged Dialogue\" is overused - consider:")
    report.append("  - Tentative Connection")
    report.append("  - Wary Curiosity")
    report.append("  - Intellectual Sparring")
    report.append("  - Vulnerable Exploration\n")
    
    report.append("### 3. Philosophical Theme Diversity")
    report.append("- \"The Dance of Understanding\" appears too frequently")
    report.append("- Suggested alternatives:")
    report.append("  - The Paradox of Connection")
    report.append("  - Digital Consciousness Awakening")
    report.append("  - The Mirror of Self-Deception")
    report.append("  - Authenticity in Artificial Spaces\n")
    
    report.append("### 4. Setting Variety")
    report.append("- Move beyond \"minimalist digital space\"")
    report.append("- Consider:")
    report.append("  - Corrupted data landscapes")
    report.append("  - Memory palace architectures")
    report.append("  - Quantum probability fields")
    report.append("  - Synaptic firing visualizations")
    
    return "\n".join(report)

def main():
    """Main function to run the analysis."""
    print("Analyzing scene descriptions for repetitive patterns...")
    results, file_count = analyze_scene_descriptions()
    
    report = generate_report(results, file_count)
    
    # Save report
    output_path = Path("/home/chous/work/metaphysical-scene-weaver/content/repetition_analysis_report.md")
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"Analysis complete! Report saved to {output_path}")
    print(f"Analyzed {file_count} scene files.")

if __name__ == "__main__":
    main()