from okane.dao.recurrentregisterdao import MoneyRecurrentRegisterDAO
import pytest
from unittest.mock import Mock, MagicMock

# Example test class
class TestMoneyRecurrentRegisterDAO:
    @pytest.fixture
    def mock_db_controller(self):
        mock_controller = Mock()
        mock_controller.conn = Mock()
        mock_controller.cursor = MagicMock()
        return mock_controller

    @pytest.fixture
    def mock_entity_factory(self):
        return Mock()

    @pytest.fixture
    def mock_category_dao(self):
        return Mock()

    @pytest.fixture
    def mock_account_dao(self):
        return Mock()

    def test_create_tables(self, mock_db_controller, mock_entity_factory, mock_category_dao, mock_account_dao):
        dao = MoneyRecurrentRegisterDAO(
            mock_db_controller,
            mock_entity_factory,
            mock_category_dao,
            mock_account_dao
        )

        dao.createTables()

        expected_sql = '''
            CREATE TABLE IF NOT EXISTS FinancialRecurrentRegisters (
                id_recurrent_register INTEGER,
                description TEXT,
                amount REAL,
                start_dt TEXT,
                end_dt TEXT,
                id_category INTEGER,
                id_account INTEGER,
                recurrence TEXT,
                recurrence_number INTEGER,
                FOREIGN KEY (id_category) REFERENCES Categories (id_category)
                FOREIGN KEY (id_account) REFERENCES Accounts (id_account)
                PRIMARY KEY (id_recurrent_register)
                )
        '''

        mock_db_controller.cursor.execute.assert_called_with(expected_sql)
