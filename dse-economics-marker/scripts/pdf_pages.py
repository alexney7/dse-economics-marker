"""Read-only PDF inspection and selected-page rendering. No OCR or grading."""
import argparse
import json
from pathlib import Path

import pymupdf


def parse_pages(value, count):
    pages = []
    for token in value.split(','):
        token = token.strip()
        parts = token.split('-')
        if len(parts) == 1:
            start = end = int(parts[0])
        elif len(parts) == 2:
            start, end = map(int, parts)
        else:
            raise ValueError('Use page numbers or ranges, for example 1,3-5')
        if not 1 <= start <= end <= count:
            raise ValueError(f'Invalid range {token}; PDF has {count} pages')
        pages.extend(range(start - 1, end))
    return list(dict.fromkeys(pages))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    inspect = sub.add_parser('inspect')
    inspect.add_argument('--pdf', type=Path, required=True)
    render = sub.add_parser('render')
    render.add_argument('--pdf', type=Path, required=True)
    render.add_argument('--pages', required=True, help='1-based PDF pages, e.g. 1,3-5')
    render.add_argument('--out', type=Path, required=True)
    render.add_argument('--rotation', type=int, choices=(0, 90, 180, 270))
    render.add_argument('--dpi', type=int, default=140)
    args = parser.parse_args()
    try:
        with pymupdf.open(args.pdf) as doc:
            if doc.needs_pass:
                raise ValueError('PDF requires a password; provide an accessible copy')
            if args.command == 'inspect':
                rows = [{'pdf_page': p.number + 1,
                         'text_characters': len(p.get_text().strip()),
                         'rotation': p.rotation,
                         'width': p.rect.width, 'height': p.rect.height}
                        for p in doc]
                print(json.dumps({'file': str(args.pdf), 'pages': len(doc),
                                  'page_details': rows}, ensure_ascii=False, indent=2))
                return
            if not 72 <= args.dpi <= 300:
                raise ValueError('DPI must be 72..300')
            selected = parse_pages(args.pages, len(doc))
            if len(selected) > 30:
                raise ValueError('Render at most 30 pages per batch')
            targets = [args.out / f'page-{n+1:04d}.png' for n in selected]
            manifest_path = args.out / 'pages.json'
            if any(p.exists() for p in targets + [manifest_path]):
                raise ValueError('Output already exists; use a new output folder')
            args.out.mkdir(parents=True, exist_ok=True)
            manifest = []
            for n, dest in zip(selected, targets):
                page = doc[n]
                original_rotation = page.rotation
                if args.rotation is not None:
                    page.set_rotation(args.rotation)
                page.get_pixmap(dpi=args.dpi, alpha=False).save(dest)
                manifest.append({'pdf_page': n + 1, 'image': dest.name,
                                 'original_rotation': original_rotation,
                                 'render_rotation': page.rotation})
            manifest_path.write_text(json.dumps(
                {'source': str(args.pdf.resolve()), 'pages': manifest},
                ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'Rendered {len(selected)} pages to {args.out.resolve()}')
    except (ValueError, OSError, RuntimeError) as exc:
        parser.exit(2, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
