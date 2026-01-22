#!/usr/bin/env python3
"""
Convert SVG files to PNG for UML v1.5.0
"""
import os
import subprocess
import shutil
from pathlib import Path

# Source directory
src_dir = Path(r"C:\Users\LG\.gemini\antigravity\mobileID_faq\UML\1.5.0\안전지갑_CA_version_v1.5.0")

# Output directory (in mobileid project)
out_dir = Path(r"C:\Users\LG\.gemini\antigravity\mobileid\uml\v1.5.0")
out_dir.mkdir(parents=True, exist_ok=True)

# Find all SVG files
svg_files = list(src_dir.rglob("*.svg"))

print(f"Found {len(svg_files)} SVG files")

# Try using chrome/chromium for rendering, or fallback to Inkscape
converted = 0
failed = []

for svg_file in svg_files:
    # Create output filename (flatten directory structure)
    png_name = svg_file.stem + ".png"
    png_path = out_dir / png_name
    
    # Skip if already converted
    if png_path.exists():
        print(f"  Skip (exists): {png_name}")
        converted += 1
        continue
    
    # Try Inkscape first
    inkscape_path = r"C:\Program Files\Inkscape\bin\inkscape.exe"
    if os.path.exists(inkscape_path):
        try:
            result = subprocess.run([
                inkscape_path,
                str(svg_file),
                "--export-type=png",
                f"--export-filename={png_path}",
                "--export-dpi=150"
            ], capture_output=True, text=True, timeout=60)
            if png_path.exists():
                converted += 1
                print(f"  OK: {png_name}")
                continue
        except Exception as e:
            pass
    
    # Try cairosvg (Python library)
    try:
        import cairosvg
        cairosvg.svg2png(url=str(svg_file), write_to=str(png_path), scale=2.0)
        converted += 1
        print(f"  OK (cairosvg): {png_name}")
        continue
    except ImportError:
        pass
    except Exception as e:
        pass
    
    # Fallback: just copy as marker
    failed.append(svg_file.name)

print(f"\n✅ Converted: {converted}/{len(svg_files)}")
if failed:
    print(f"❌ Failed: {len(failed)}")
    for f in failed[:5]:
        print(f"   - {f}")
