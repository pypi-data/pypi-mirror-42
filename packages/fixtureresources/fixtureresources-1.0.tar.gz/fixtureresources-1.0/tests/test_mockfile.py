import os
import pytest
from fixtureresources.mockfile import MockFile


__copyright__ = 'Copyright (C) 2019, Nokia'


def test_mockfile():
    with MockFile(filename='filename', content='content'):
        with open('filename', 'a') as f:
            f.write('more_content')
        with open('filename') as f:
            assert f.read() == 'contentmore_content'
    assert not os.path.isfile('filename')


def test_mockfile_sideeffect():
    def raise_io_error():
        raise IOError('message')

    with pytest.raises(IOError) as excinfo:
        with MockFile(filename='filename',
                      side_effect=lambda *args: raise_io_error()):
            open('filename')

    assert excinfo.value.args[0] == 'message'


def test_mockfile_saver():
    mfile = MockFile()
    assert mfile.saver == mfile.set_content


def test_set_filename():
    mfile = MockFile()
    mfile.set_filename('filename')
    assert mfile.filename == 'filename'


def test_set_content():
    mfile = MockFile()
    mfile.set_content('content')
    assert mfile.content == 'content'


def test_set_sideeffect():
    mfile = MockFile()
    mfile.set_side_effect('side_effect')
    assert mfile.side_effect == 'side_effect'


def test_set_saver():
    mfile = MockFile(filename='filename')

    def saver(content):
        mfile.set_content(content + 'more_content')

    mfile.set_saver(saver)
    with mfile:
        with open('filename', 'w') as f:
            f.write('content')
        with open('filename') as f:
            assert f.read() == 'contentmore_content'
