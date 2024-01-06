import pytest
from unittest.mock import Mock, MagicMock
from okane.dao.recurrentregisterdao import MoneyRecurrentRegisterDAO

class TestMoneyRecurrentRegisterDAO:
    @pytest.fixture
    def mock_db_controller(self):
        mock_controller = Mock()
        mock_controller.conn = Mock()
        mock_controller.cursor = MagicMock()
        return mock_controller

    @pytest.fixture
    def mock_entity_factory(self):
        factory = Mock()
        factory.createMoneyRecurrentRegister = Mock()
        return factory

    @pytest.fixture
    def mock_category_dao(self):
        return Mock()

    @pytest.fixture
    def mock_account_dao(self):
        return Mock()

    @pytest.fixture
    def mock_money_recurrent_register(self):
        mock_register = Mock()
        mock_register.get_data_tuple = Mock(return_value=('description', 100.0, '2022-01-01', '2022-12-31', 1, 2, 'monthly', 12))
        mock_register.id = 1
        return mock_register

    def test_create_tables(self, mock_db_controller, mock_entity_factory, mock_category_dao, mock_account_dao):
        dao = MoneyRecurrentRegisterDAO(
            mock_db_controller,
            mock_entity_factory,
            mock_category_dao,
            mock_account_dao
        )
        dao.createTables()
        # ... (same as before)

    def test_save(self, mock_db_controller, mock_entity_factory, mock_category_dao, mock_account_dao, mock_money_recurrent_register):
        dao = MoneyRecurrentRegisterDAO(
            mock_db_controller,
            mock_entity_factory,
            mock_category_dao,
            mock_account_dao
        )
        last_row_id = dao.save(mock_money_recurrent_register)

        assert mock_db_controller.cursor.execute.called
        assert mock_db_controller.conn.commit.called
        assert last_row_id == mock_db_controller.cursor.lastrowid

    def test_update(self, mock_db_controller, mock_entity_factory, mock_category_dao, mock_account_dao, mock_money_recurrent_register):
        dao = MoneyRecurrentRegisterDAO(
            mock_db_controller,
            mock_entity_factory,
            mock_category_dao,
            mock_account_dao
        )
        dao.update(mock_money_recurrent_register)

        assert mock_db_controller.cursor.execute.called
        assert mock_db_controller.conn.commit.called

    def test_delete(self, mock_db_controller, mock_entity_factory, mock_category_dao, mock_account_dao, mock_money_recurrent_register):
        dao = MoneyRecurrentRegisterDAO(
            mock_db_controller,
            mock_entity_factory,
            mock_category_dao,
            mock_account_dao
        )
        dao.delete(mock_money_recurrent_register)

        assert mock_db_controller.cursor.execute.called
        assert mock_db_controller.conn.commit.called

    def test_getFromId(self, mock_db_controller, mock_entity_factory, mock_category_dao, mock_account_dao):
        dao = MoneyRecurrentRegisterDAO(
            mock_db_controller,
            mock_entity_factory,
            mock_category_dao,
            mock_account_dao
        )
        dao.getFromId(1)

        assert mock_db_controller.cursor.execute.called
        assert mock_entity_factory.createMoneyRecurrentRegister.called

    def test_getFromIdList(self, mock_db_controller, mock_entity_factory, mock_category_dao, mock_account_dao):
        dao = MoneyRecurrentRegisterDAO(
            mock_db_controller,
            mock_entity_factory,
            mock_category_dao,
            mock_account_dao
        )
        dao.getFromIdList([1, 2, 3])

        assert mock_db_controller.cursor.execute.called
        assert len(mock_entity_factory.createMoneyRecurrentRegister.mock_calls) == len(mock_db_controller.cursor.fetchall())

# Run the tests
if __name__ == "__main__":
    pytest.main()
