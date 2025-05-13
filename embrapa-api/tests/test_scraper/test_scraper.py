
import unittest
from unittest.mock import patch, Mock
import src.scraper as scraper


class TestWebScraper(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_fetch_html_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html></html>'
        html = scraper.fetch_html('http://fakeurl.com')
        self.assertEqual(html, '<html></html>')

    @patch('scraper.requests.get')
    def test_fetch_html_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        with self.assertRaises(Exception):
            scraper.fetch_html('http://fakeurl.com')

    def test_extract_tables(self):
        html = '''
        <table class="tb_base tb_dados">
            <tr><th>A</th><th>B</th></tr>
            <tr><td>1</td><td>2</td></tr>
        </table>
        '''
        df = scraper.extract_tables(html)
        self.assertEqual(df.shape, (1, 2))
        self.assertListEqual(list(df.columns), ['A', 'B'])

    def test_extract_tables_no_table(self):
        html = '<html><body><p>Sem tabela</p></body></html>'
        df = scraper.extract_tables(html)
        self.assertIsNone(df)

    @patch('builtins.open')
    def test_save_json(self, mock_open):
        import pandas as pd
        df = pd.DataFrame({'A': [1], 'B': [2]})
        scraper.save_json(df, 'dummy.json')
        mock_open.assert_called_once()

if __name__ == '__main__':
    unittest.main()
