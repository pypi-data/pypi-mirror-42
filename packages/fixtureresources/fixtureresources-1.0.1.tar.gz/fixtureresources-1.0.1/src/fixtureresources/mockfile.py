"""
.. module:: mockfile
    :platform: Unix, Windows
    :synopsis: file mock

.. moduleauthor:: Petri Huovinen <petri.huovinen@nokia.com>

"""
import mock
import io
try:
    import __builtin__
    builtins_module = __builtin__.__name__
except ImportError:
    import builtins
    builtins_module = builtins.__name__


__copyright__ = 'Copyright (C) 2019, Nokia'


# Heuristics for I/O stream selection for text files
# BytesIO works better in 2.7 while in 3.4 StringIO works better
try:
    io.StringIO('')
    SavedIOBase = io.StringIO
except TypeError:
    SavedIOBase = io.BytesIO


class SavedIO(SavedIOBase):

    def __init__(self, content='', saver=None, mode=None):
        super(SavedIO, self).__init__(self.get_updated_content(content, mode))
        self._saver = saver
        if mode is not None and mode.startswith('a'):
            self.seek(0, 2)

    def get_updated_content(self, content, mode):
        if mode is not None:
            content = '' if mode.startswith('w') else content
        return content

    def __exit__(self, *args, **kwargs):
        if self._saver:
            self._saver(self.getvalue())
        super(SavedIO, self).__exit__(*args, **kwargs)


class MockFile(object):
    """ Simple string IO based mock for a file to be used via open.

        Example usage:

            >>> with MockFile(filename='foo.txt', content='bar') as mockfile:
            ...      with open('foo.txt', 'a') as f:
            ...          f.write('foo')
            ...      with open('foo.txt') as f:
            ...         print(f.read())
            ...
            3L
            barfoo
            >>> def raise_io_error():
            ...     raise IOError('message')
            ...
            >>> with MockFile(filename='filename',
            ...               side_effect=lambda *args: raise_io_error()):
            ...    open('filename')
            ...
            Traceback (most recent call last):
              File "<stdin>", line 2, in <module>
              File "mockfile.py", line 123, in __enter__
                return self.mock_open_file(self.filename, self.args)
              File "mockfile.py", line 102, in mock_open_file
                self.side_effect(*args)
              File "<stdin>", line 2, in <lambda>
              File "<stdin>", line 2, in raise_io_error
            IOError: message
            >>>

        .. note::

            Tested only for one file at time and for text files.

    """

    def __init__(self,
                 filename=None,
                 content='',
                 side_effect=None,
                 args=None):
        self.filename = None
        self.content = None
        self.side_effect = None
        self.set_filename(filename)
        self.set_content(content)
        self.set_side_effect(side_effect)
        self.args = args
        self.mocked_open = None
        self.mock_open = None
        self.saver = self.set_content

    def set_filename(self, filename):
        """Set filename"""
        self.filename = filename

    def set_content(self, content):
        """Set content"""
        self.content = content

    def set_side_effect(self, side_effect):
        """Set side_effect"""
        self.side_effect = side_effect

    def set_saver(self, saver):
        self.saver = saver

    def mock_open_file(self, *args, **kwargs):
        if args[0] == self.filename:
            f = SavedIO(content=self.content,
                        saver=self.saver,
                        mode=args[1] if len(args) > 1 else None)
            f.name = self.filename
            if self.side_effect:
                self.side_effect(*args)
        else:
            self.mocked_open.stop()
            f = open(*args)
            self.mocked_open.start()
        return f

    def start(self):
        if self.mock_open is None:
            self.mocked_open = mock.patch(
                '{module}.open'.format(module=builtins_module),
                self.mock_open_file)
            self.mock_open = self.mocked_open.start()

    def stop(self):
        if self.mock_open is not None:
            self.mocked_open.stop()
            self.mock_open = None

    def __enter__(self):
        self.start()
        return self.mock_open_file(self.filename, self.args)

    def __exit__(self, *args):
        self.stop()
