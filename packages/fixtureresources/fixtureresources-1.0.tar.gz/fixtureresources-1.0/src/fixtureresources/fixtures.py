"""
Useful mocks for :mod:`os`, :mod:`random` and :mod:`tempfile` and :mod:`time`.
"""
import os
import pytest
import mock


__copyright__ = 'Copyright (C) 2019, Nokia'


def create_patch(mpatch, request):
    """ Helper method for creating patch for the patch functions
    implementing *start* and *stop*.

    **Args:**

    *mpatch*:  e.g. return value of *mock.patch()*

    *request*: pytest *request*.
    """
    request.addfinalizer(mpatch.stop)
    return mpatch.start()


class MockSystemRandom(object):
    def __init__(self):
        self.count = 0

    def choice(self, choices):
        ret = choices[self.count % len(choices)]
        self.count += 1
        return ret


@pytest.fixture(scope='function')
def mock_randomchoice(request):
    """ Pytest mock fixture for :func:`random.SystemRandom.choice`.
    Patched :func:`random.SystemRandom.choice` returns

    .. code-block:: python

        choices[call_number % number_of_choices]


    For example:

    .. code-block:: python

        def test_randon(mock_randomchoice):
            assert (''.join(random.SystemRandom().choice(['a', 'b', 'c'])
                            for _ in range(5)) == 'abcab')

    """
    return create_patch(mock.patch('random.SystemRandom',
                                   return_value=MockSystemRandom()),
                        request)


def mock_walk_gen(subdirs):
    for _ in range(10):
        yield ('', subdirs, [])


@pytest.fixture(scope='function')
def mock_os_walk(request):
    """ Pytest mock fixture for :func:`os.walk`. The
    default :func:`os.walk` mock directory tree depth
    is 10 and all directories contains only 'dir' directory.

    For example:

    .. code-block:: python

        def test_os_walk(mock_os_walk):
            for _ in range(10):
                for _, dirs, _  in os.walk('foo/bar'):
                    assert dirs == ['dir']

    """
    return create_patch(mock.patch('os.walk',
                                   return_value=mock_walk_gen(['dir'])),
                        request)


@pytest.fixture(scope='function')
def mock_os_path_isfile(request):
    """ Pytest mock fixture for :func:`os.path.isfile`. The default
    return value is True.
    """
    return create_patch(mock.patch('os.path.isfile', return_value=True),
                        request)


@pytest.fixture(scope='function')
def mock_os_path_abspath(request):
    """ Pytest mock fixture for :func:`os.path.abspath`. The default
    return value joins 'abspath' with given path.

    For example:

    .. code-block:: python

        def test_os_path_abspath(mock_os_path_abspath):
            assert os.path.abspath('path') == os.path.join('abspath', 'path')
    """
    def mock_abspath(path):
        return os.path.join('abspath', path)

    return create_patch(mock.patch('os.path.abspath', mock_abspath),
                        request)


@pytest.fixture(scope='function')
def mock_gettempdir(request):
    """ Pytest mock fixture for :func:`tempfile.gettempdir`. The default
    return value is 'tmp'.
    """
    return create_patch(mock.patch('tempfile.gettempdir', return_value='tmp'),
                        request)


@pytest.fixture(scope='function')
def mock_time_sleep(request):
    """ Pytest mock fixture for :func:`time.sleep`.
    """
    return create_patch(mock.patch('time.sleep'), request)
