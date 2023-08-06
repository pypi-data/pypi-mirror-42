import os
from unittest.mock import patch, MagicMock, mock_open

import pytest

from cybele.cli import utils

HERE = os.path.dirname(__file__)


@patch("cybele.cli.utils.click.prompt", return_value="passphrase")
def test_load_db(prompt_mock):
    db = utils.load_db(os.path.join(HERE, "..", "data", "encrypted_fake_entries.json"))
    assert db.entries


@patch("cybele.cli.utils.click.prompt", return_value="wrong_passphrase")
def test_load_db_with_wrong_pass(prompt_mock):
    with pytest.raises(SystemExit):
        _ = utils.load_db(os.path.join(HERE, "..", "data", "encrypted_fake_entries.json"))


@patch("cybele.cli.utils.click.prompt", side_effect=["password", "password"])
def test_ask_and_confirm_passphrase(prompt_mock):
    password = utils.ask_and_confirm_passphrase()
    assert password == "password"


@patch("cybele.cli.utils.click.prompt", side_effect=["password", "not_identical"])
def test_ask_and_confirm_passphrase_exit_if_not_identical(prompt_mock):
    with pytest.raises(SystemExit):
        _ = utils.ask_and_confirm_passphrase()


@patch("cybele.cli.utils.click.prompt", side_effect=["username", "password", "password"])
def test_ask_full_info(prompt_mock):
    res = utils.ask_full_infos()
    assert res == {"username": "username", "passphrase": "password"}


@patch("cybele.cli.utils.os")
def test_create_db_when_exists(os_mock):
    os_mock.path.split = MagicMock(return_value=("part1", "part2"))
    os_mock.path.exists = MagicMock(return_value=True)
    with pytest.raises(SystemExit):
        utils.create_db("path")
    assert os_mock.makedirs.call_count == 0


@patch("cybele.cli.utils.os")
@patch("cybele.cli.utils.open")
@patch("cybele.cli.utils.ask_and_confirm_passphrase", return_value="passphrase")
def test_create_db_nothing_exists(ask_mock, open_mock, os_mock):
    os_mock.path.split = MagicMock(return_value=("dirname", "dbname"))
    os_mock.path.exists = MagicMock(return_value=False)
    utils.create_db("dirname/dbname")
    os_mock.makedirs.assert_called_once_with("dirname")


@patch("cybele.cli.utils.os")
@patch("builtins.open")
@patch("cybele.cli.utils.ask_and_confirm_passphrase", return_value="passphrase")
def test_create_db_dir_exists(ask_mock, open_mock, os_mock):
    os_mock.path.split = MagicMock(return_value=("dirname", "dbname"))
    os_mock.path.exists = MagicMock(side_effect=[True, False])
    open_mock.return_value.__enter__.return_value = file_mock = MagicMock()
    utils.create_db("dirname/dbname")
    assert not os_mock.makedirs.called
    file_mock.write.assert_called_once()
