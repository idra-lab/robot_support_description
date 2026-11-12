#!/usr/bin/env python3
"""Validate URDF files by parsing xacro and checking XML structure."""
import sys
import subprocess
from pathlib import Path
from lxml import etree


def validate_xacro(xacro_file):
    """Validate that a xacro file compiles to valid URDF."""
    try:
        result = subprocess.run(
            ["xacro", str(xacro_file)],
            capture_output=True,
            text=True,
            check=True
        )
        urdf_content = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to compile xacro: {xacro_file}")
        print(f"  Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ xacro command not found. Is ROS installed?")
        return False

    try:
        etree.fromstring(urdf_content.encode())
        print(f"✓ Valid URDF: {xacro_file}")
        return True
    except etree.XMLSyntaxError as e:
        print(f"✗ Invalid URDF XML from {xacro_file}: {e}")
        return False


def main():
    """Find and validate all xacro files in urdf directory."""
    urdf_dir = Path(__file__).parent.parent / "urdf"

    if not urdf_dir.exists():
        print(f"✗ URDF directory not found: {urdf_dir}")
        return 1

    xacro_files = sorted(urdf_dir.glob("*.urdf.xacro"))

    if not xacro_files:
        print(f"✗ No xacro files found in {urdf_dir}")
        return 1

    print(f"Validating {len(xacro_files)} xacro file(s)...\n")

    results = [validate_xacro(f) for f in xacro_files]

    print(f"\n{'='*50}")
    print(f"Results: {sum(results)}/{len(results)} passed")

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
