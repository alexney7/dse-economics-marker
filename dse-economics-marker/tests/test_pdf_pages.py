"""Checks output safety and page selection using synthetic PDFs, not exam content."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import pymupdf

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/pdf_pages.py'
SPEC = importlib.util.spec_from_file_location('pdf_pages', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PdfTests(unittest.TestCase):
    def test_selection(self):
        self.assertEqual(MODULE.parse_pages('1,3-4,3', 4), [0, 2, 3])

    def test_invalid_selection(self):
        for value in ['0', '5', '4-2', 'a', '1-2-3']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                MODULE.parse_pages(value, 4)

    def test_render_and_protect_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'source.pdf'
            with pymupdf.open() as doc:
                doc.new_page().insert_text((40, 40), 'Source page one')
                doc.new_page().insert_text((40, 40), 'Source page two')
                doc.save(source)
            original = source.read_bytes()
            cmd = [sys.executable, str(SCRIPT), 'render', '--pdf', str(source),
                   '--pages', '2', '--out', str(root/'render'), '--rotation', '90']
            first = subprocess.run(cmd, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue((root/'render/page-0002.png').is_file())
            self.assertFalse((root/'render/page-0001.png').exists())
            self.assertEqual(source.read_bytes(), original)
            second = subprocess.run(cmd, capture_output=True)
            self.assertEqual(second.returncode, 2)
            self.assertIn(b'already exists', second.stderr)


if __name__ == '__main__':
    unittest.main()
