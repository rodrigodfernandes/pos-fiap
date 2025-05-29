import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Connection
from src.core.services import data_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestDataServiceWithGet(unittest.TestCase):

    @patch("src.core.services.data_service.load_data")
    @patch("src.core.services.data_service.insert_into_product")
    @patch("src.core.services.data_service.delete_product_data")
    def test_insert_product_data_and_get(self, mock_delete, mock_insert, mock_load):
        logger.info("Rodando teste de para inserção de produto")
        mock_conn = MagicMock(spec=Connection)
        mock_data = [
            {"produto": "VINHO DE MESA", "valor": 1000, "ano": 2023},
            {"produto": "Tinto", "valor": 500, "ano": 2023},
        ]
        mock_load.return_value = mock_data

        data_service.insert_product_data(mock_conn)

        # Esperado: duas inserções, uma para cada registro processado
        expected_calls = [
            {
                "name": "VINHO DE MESA",
                "wine_derivative_name": "VINHO DE MESA",
                "quantity": 1000,
                "year_no": 2023
            },
            {
                "name": "Tinto",
                "wine_derivative_name": "VINHO DE MESA",
                "quantity": 500,
                "year_no": 2023
            }
        ]

        actual_calls = [call[0][1] for call in mock_insert.call_args_list]
        self.assertEqual(actual_calls, expected_calls)
        self.assertEqual(mock_insert.call_count, 2)
        mock_delete.assert_called_once()
    
    @patch("src.core.services.data_service.load_data")
    @patch("src.core.services.data_service.insert_into_process")
    @patch("src.core.services.data_service.delete_process_data")
    def test_insert_process_data(self, mock_delete, mock_insert, mock_load):
        logger.info("Rodando teste de para inserção de processamento")
        mock_conn = MagicMock(spec=Connection)
        mock_data = [
            {"cultivar": "TINTAS", "Quantidade (Kg)": 2000, "type": "Americanas e híbridas", "ano": 2022},
            {"cultivar": "Bacarina", "Quantidade (Kg)": 1500, "type": "Americanas e híbridas", "ano": 2022},
        ]
        mock_load.return_value = mock_data

        data_service.insert_process_data(mock_conn)

        expected_calls = [
            {
                "color_name": "TINTAS",
                "kind_name": "Americanas e híbridas",
                "cultivar": "TINTAS",
                "quantity_kg": 2000,
                "year_no": 2022
            },
            {
                "color_name": "TINTAS",
                "kind_name": "Americanas e híbridas",
                "cultivar": "Bacarina",
                "quantity_kg": 1500,
                "year_no": 2022
            }
        ]

        actual_calls = [call[0][1] for call in mock_insert.call_args_list]
        self.assertEqual(actual_calls, expected_calls)
        self.assertEqual(mock_insert.call_count, 2)
        mock_delete.assert_called_once()

    @patch("src.core.services.data_service.load_data")
    @patch("src.core.services.data_service.insert_into_sales")
    @patch("src.core.services.data_service.delete_sales_data")
    def test_insert_sales_data(self, mock_delete, mock_insert, mock_load):
        logger.info("Rodando teste de para inserção de comercialização")
        mock_conn = MagicMock(spec=Connection)
        mock_data = [
            {"Produto": "VINHO DE MESA", "valor": 3000, "ano": 2021},
            {"Produto": "Rosado", "valor": 1200, "ano": 2021},
        ]
        mock_load.return_value = mock_data

        data_service.insert_sales_data(mock_conn)

        expected_calls = [
            {
                "name": "VINHO DE MESA",
                "wine_derivative_name": "VINHO DE MESA",
                "quantity_liters": 3000,
                "year_no": 2021
            },
            {
                "name": "Rosado",
                "wine_derivative_name": "VINHO DE MESA",
                "quantity_liters": 1200,
                "year_no": 2021
            }
        ]

        actual_calls = [call[0][1] for call in mock_insert.call_args_list]
        self.assertEqual(actual_calls, expected_calls)
        self.assertEqual(mock_insert.call_count, 2)
        mock_delete.assert_called_once()

    @patch("src.core.services.data_service.load_data")
    @patch("src.core.services.data_service.insert_into_import")
    @patch("src.core.services.data_service.delete_import_data")
    def test_insert_import_data(self, mock_delete, mock_insert, mock_load):
        logger.info("Rodando teste de para inserção de importação")
        mock_conn = MagicMock(spec=Connection)
        mock_data = [
            {"País": "Africa do Sul", "Quantidade (Kg)": 500, "type": "Espumantes", "ano": 2020},
            {"País": "Alemanha", "Quantidade (Kg)": 800, "type": "Espumantes", "ano": 2020},
        ]
        mock_load.return_value = mock_data

        data_service.insert_import_data(mock_conn)

        expected_calls = [
            {
                "grape_type_name": "Espumantes",
                "country": "Africa do Sul",
                "quantity_kg": 500,
                "value_usd": 0,
                "year_no": 2020
            },
            {
                "grape_type_name": "Espumantes",
                "country": "Alemanha",
                "quantity_kg": 800,
                "value_usd": 0,
                "year_no": 2020
            }
        ]

        actual_calls = [call[0][1] for call in mock_insert.call_args_list]
        self.assertEqual(actual_calls, expected_calls)
        self.assertEqual(mock_insert.call_count, 2)
        mock_delete.assert_called_once()

    @patch("src.core.services.data_service.load_data")
    @patch("src.core.services.data_service.insert_into_export")
    @patch("src.core.services.data_service.delete_export_data")
    def test_insert_export_data(self, mock_delete, mock_insert, mock_load):
        logger.info("Rodando teste de para inserção de exportação")
        mock_conn = MagicMock(spec=Connection)
        mock_data = [
            {"País": "Mauritânia", "Quantidade (Kg)": 100, "type": "Uvas frescas", "ano": 2019},
            {"País": "Mexico", "Quantidade (Kg)": 200, "type": "Uvas frescas", "ano": 2019},
        ]
        mock_load.return_value = mock_data

        data_service.insert_export_data(mock_conn)

        expected_calls = [
            {
                "grape_type_name": "Uvas frescas",
                "country": "Mauritânia",
                "quantity_kg": 100,
                "value_usd": 0,
                "year_no": 2019
            },
            {
                "grape_type_name": "Uvas frescas",
                "country": "Mexico",
                "quantity_kg": 200,
                "value_usd": 0,
                "year_no": 2019
            }
        ]

        actual_calls = [call[0][1] for call in mock_insert.call_args_list]
        self.assertEqual(actual_calls, expected_calls)
        self.assertEqual(mock_insert.call_count, 2)
        mock_delete.assert_called_once()

if __name__ == "__main__":
    unittest.main()