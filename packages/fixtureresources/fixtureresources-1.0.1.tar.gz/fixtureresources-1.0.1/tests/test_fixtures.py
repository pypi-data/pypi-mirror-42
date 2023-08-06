import pytest
import random
import os
import tempfile
import time
from fixtureresources.fixtures import (
    mock_randomchoice,
    mock_os_walk,
    mock_os_path_isfile,
    mock_os_path_abspath,
    mock_gettempdir,
    mock_time_sleep)


__copyright__ = 'Copyright (C) 2019, Nokia'


def test_mock_randomchoice(mock_randomchoice):
    assert (''.join(random.SystemRandom().choice(['a', 'b', 'c'])
                    for _ in range(5)) == 'abcab')


def test_mock_os_walk(mock_os_walk):
    for _ in range(10):
        for _, dirs, _ in os.walk('foo/bar'):
            assert dirs == ['dir']


def test_mock_os_path_isfile(mock_os_path_isfile):
    assert os.path.isfile('filename')


def test_mock_os_path_abspath(mock_os_path_abspath):
    assert os.path.abspath('path') == os.path.join('abspath', 'path')


def test_get_mock_tempdir(mock_gettempdir):
    assert tempfile.gettempdir() == 'tmp'


def test_mock_time_sleep(mock_time_sleep):
    time.sleep(1)
    mock_time_sleep.assert_called_once_with(1)
