"""Resolve an external library and check inventory paths, without reading answers."""
import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path)
    args = parser.parse_args()
    skill = Path(__file__).resolve().parents[1]
    config = skill / 'library.local.json'
    root = args.root or os.environ.get('ECON_MARKER_LIBRARY')
    if root is None and config.exists():
        root = json.loads(config.read_text(encoding='utf-8-sig')).get('root')
    if not root:
        parser.exit(2, 'Provide --root or ECON_MARKER_LIBRARY or library.local.json\n')
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        parser.exit(2, 'Library root does not exist or is not accessible\n')
    catalog = json.loads((skill / 'references/library-index.json').read_text(encoding='utf-8'))
    result = []
    for item in catalog['files']:
        target = (root / item['path']).resolve()
        if not target.is_relative_to(root):
            parser.exit(2, 'Inventory path escapes the library root\n')
        result.append({'path': item['path'], 'exists': target.is_file(),
                       'role': item['role']})
    missing = sum(not r['exists'] for r in result)
    print(json.dumps({'root': str(root), 'checked': len(result),
                      'missing_files': missing, 'files': result,
                      'known_content_gaps': catalog['known_content_gaps']},
                     ensure_ascii=False, indent=2))
    # Existence is not completeness: known content gaps are reported independently.
    if missing:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
