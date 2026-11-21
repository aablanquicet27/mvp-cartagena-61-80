import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote

import build


class GeneratorTests(unittest.TestCase):
    def test_selected_rows_and_contacts(self):
        with build.LEADS.open(encoding='utf-8-sig') as source:
            rows = list(csv.DictReader(source))[60:80]
        kits = {json.loads(p.read_text())['negocio']:p.parent for p in build.KITS.glob('*/brand.json')}
        self.assertEqual(len(rows), 20)
        for row in rows:
            site = (build.DIST/kits[row['Negocio']].name/'index.html').read_text()
            self.assertIn('tel:'+row['Teléfono'],site)
            self.assertIn(build.e(row['Dirección']),site)
            if row['Email']:
                self.assertIn('mailto:'+row['Email'],site)
            else:
                self.assertEqual(site.count('mailto:'),1)

    def test_seller_empty_and_configured(self):
        for seller,expected in [('', 'https://wa.me/?text='),('573001234567','https://wa.me/573001234567?text=')]:
            with patch.object(build,'SELLER_WHATSAPP',seller):
                result = build.offer('Marca & más')
                self.assertIn(expected,result)
                self.assertIn('Hola, quiero reservar mi página web para Marca & más por $200.000',unquote(result))

    def test_escaping(self):
        self.assertEqual(build.e('<script>"&'), '&lt;script&gt;&quot;&amp;')

    def test_missing_content_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'content').mkdir()
            (root/'content/copy.json').write_text('[]')
            (root/'content/photos.json').write_text('{}')
            with patch.object(build,'ROOT',root),patch.object(build,'DIST',root/'dist'):
                with self.assertRaisesRegex(ValueError,'exactly 20'):
                    build.main()


if __name__ == '__main__':
    unittest.main()
