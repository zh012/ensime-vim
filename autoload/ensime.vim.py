# coding: utf-8

import inspect
import os
import sys

import vim


def ensime_init_path():
    path = os.path.abspath(inspect.getfile(inspect.currentframe()))
    if path.endswith('/rplugin/python/ensime.py'):  # nvim rplugin
        sys.path.append(os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(path)))))
    elif path.endswith('/autoload/ensime.vim.py'):  # vim plugin
        sys.path.append(os.path.join(
            os.path.dirname(os.path.dirname(path))))

ensime_init_path()

from ensime_shared.ensime import Ensime  # noqa: E402
ensime_plugin = Ensime(vim)
