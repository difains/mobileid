#!/usr/bin/env python3
"""
Update flowchart.json to add pngPath_v150 for each item
Matches items by code (P100, P102, etc.)
"""
import json
import os
from pathlib import Path

# Paths
flowchart_path = Path(r"C:\Users\LG\.gemini\antigravity\mobileid\flowchart.json")
v150_png_dir = Path(r"C:\Users\LG\.gemini\antigravity\mobileid\uml\v1.5.0")

# Load existing flowchart.json
with open(flowchart_path, 'r', encoding='utf-8') as f:
    flowchart_data = json.load(f)

# Get list of v1.5.0 PNG files
v150_files = list(v150_png_dir.glob("*.png"))
v150_map = {}

for png_file in v150_files:
    # Extract code from filename (e.g., P100 from "P100_월렛접근(walletToken).png")
    name = png_file.stem
    if name.startswith('P'):
        # Handle cases like P142-2, P311-1, etc.
        parts = name.split('_')
        code = parts[0]  # e.g., "P100", "P142-2"
        v150_map[code] = f"uml/v1.5.0/{png_file.name}"

print(f"Found {len(v150_map)} v1.5.0 PNG files")

# Update flowchart.json entries
updated = 0
for item in flowchart_data:
    code = item.get('code', '')
    if code in v150_map:
        # Also update pngPath to use uml/ prefix if it doesn't already
        if 'pngPath' in item and not item['pngPath'].startswith('uml/'):
            item['pngPath'] = item['pngPath']  # Keep as-is, it should already be correct
        item['pngPath_v150'] = v150_map[code]
        updated += 1

# Save updated flowchart.json
with open(flowchart_path, 'w', encoding='utf-8') as f:
    json.dump(flowchart_data, f, ensure_ascii=False, indent=2)

print(f"✅ Updated {updated} items with pngPath_v150")
print(f"   Output: {flowchart_path}")
