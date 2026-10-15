#!/usr/bin/env python3
"""Build the distributable skill without repository presentation files.

Usage: python3 tools/package_skill.py /path/to/plainzh.zip
The archive contains SKILL.md, its references, and the MIT license.
"""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def package(output: Path) -> list[str]:
    root = Path(__file__).resolve().parents[1]
    files = [root / "SKILL.md", root / "LICENSE"]
    files.extend(sorted((root / "references").rglob("*")))
    files = [path for path in files if not path.is_dir()]
    for path in files:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Expected a regular source file: {path}")
    if output.resolve().is_relative_to(root):
        raise ValueError("Write the archive outside the repository.")
    output.parent.mkdir(parents=True, exist_ok=True)
    names = []
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            name = path.relative_to(root).as_posix()
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
            names.append(name)
    return names


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Destination .zip file outside the repository")
    args = parser.parse_args()
    if args.output.suffix.lower() != ".zip":
        parser.error("output must end in .zip")
    names = package(args.output)
    print(f"Created {args.output} ({len(names)} files)")
    print("\n".join(names))


if __name__ == "__main__":
    main()
