# coding: utf-8

import collections
import os

import sexpdata

from ensime_shared.util import Util

BOOTSTRAPS_ROOT = os.path.join(os.environ['HOME'], '.config/ensime-vim/')
"""Default directory where ENSIME server bootstrap projects will be created."""

LOG_FORMAT = '%(levelname)-8s <%(asctime)s> (%(filename)s:%(lineno)d) - %(message)s'

gconfig = {
    "ensime_server": "ws://127.0.0.1:{}/jerky",
    "localhost": "http://127.0.0.1:{}/{}",
}

feedback = {
    "analyzer_ready": "Analyzer is ready",
    "displayed_type": "The type %s has been displayed",
    "failed_refactoring": "The refactoring could not be applied (more info at logs)",
    "full_types_enabled_off": "Qualified type display disabled",
    "full_types_enabled_on": "Qualified type display enabled",
    "handler_not_implemented":
        "The feature {} is not supported by the current Ensime server version {}",
    "indexer_ready": "Indexer is ready",
    "invalid_java": "Java not found or not executable, verify :java-home in your .ensime config",
    "manual_doc": "Go to {}",
    "missing_debug_class": "You must specify a class to debug",
    "module_missing": "{} missing: do a `pip install {}` and restart vim",
    "notify_break": "Execution breaked at {} {}",
    "prompt_server_install":
        "Please run :EnInstall to install the ENSIME server for Scala {scala_version}",
    "spawned_browser": "Opened tab {}",
    "start_message": "Server has been started...",
    "typechecking": "Typechecking...",
    "unhandled_response": "Response has not been handled: %s",
    "unknown_symbol": "Symbol not found",
}

commands = {
    "enerror_matcher": "matchadd('EnErrorStyle', '\\%{}l\\%>{}c\\%<{}c')",
    "highlight_enerror": "highlight EnErrorStyle ctermbg=red gui=underline",
    "exists_enerrorstyle": "exists('g:EnErrorStyle')",
    "set_enerrorstyle": "let g:EnErrorStyle='EnError'",
    # http://vim.wikia.com/wiki/Timer_to_execute_commands_periodically
    # Set to low values to improve responsiveness
    "set_updatetime": "set updatetime=1000",
    "current_file": "expand('%:p')",
    "until_last_char_word": "normal e",
    "until_first_char_word": "normal b",
    # Avoid triggering requests to server when writing
    "write_file": "noautocmd w",
    "input_save": "call inputsave()",
    "input_restore": "call inputrestore()",
    "set_input": "let user_input = input('{}')",
    "get_input": "user_input",
    "edit_file": "edit {}",
    "reload_file": "checktime",
    "display_message": "echo \"{}\"",
    "split_window": "split {}",
    "vert_split_window": "vsplit {}",
    "new_vertical_window": "{}vnew {}",
    "new_vertical_scratch":
        "{}vnew {} | setlocal nobuflisted buftype=nofile bufhidden=wipe noswapfile",
    "doautocmd_bufleave": "doautocmd BufLeave",
    "doautocmd_bufreadenter": "doautocmd BufReadPre,BufRead,BufEnter",
    "filetype": "&filetype",
    "set_filetype": "set filetype={}",
    "go_to_char": "goto {}",
    "set_ensime_completion": "set omnifunc=EnCompleteFunc",
    "set_quickfix_list": "call setqflist({}, '')",
    "open_quickfix": "copen",
    "disable_plugin": "set runtimepath-={}",
    "runtimepath": "&runtimepath",
    "syntastic_available": 'exists("g:SyntasticRegistry")',
    "syntastic_enable": "if exists('g:SyntasticRegistry') | let &runtimepath .= ',' . {!r} | endif",
    "syntastic_append_notes":
        'if ! exists("b:ensime_scala_notes") | let b:ensime_scala_notes = [] | endif |'
        'let b:ensime_scala_notes += {}',
    "syntastic_reset_notes": 'let b:ensime_scala_notes = []',
    "syntastic_show_notes": "silent! SyntasticCheck ensime",
    "get_cursor_word": 'expand("<cword>")',
    "select_item_list": 'inputlist({})',
    "append_line": 'call append({}, {!r})',
    "redraw": "redraw!"
}


class ProjectConfig(collections.Mapping):
    """A dict-like immutable representation of an ENSIME project configuration.

    Args:
        filepath (str): Path of an ``.ensime`` file to parse.
    """

    def __init__(self, filepath):
        self._filepath = os.path.realpath(filepath)
        self.__data = self.parse(filepath)

    # Provide the Mapping protocol requirements

    def __getitem__(self, key):
        return self.__data[key]

    def __iter__(self):
        return iter(self.__data)

    def __len__(self):
        return len(self.__data)

    def __repr__(self):
        return "{name}({path!r})".format(
            name=self.__class__.__name__,
            path=self.filepath
        )

    @property
    def filepath(self):
        """str: The canonical path of the represented config file."""
        return self._filepath

    @staticmethod
    def parse(path):
        """Parse an ``.ensime`` config file from S-expressions.

        Args:
            path (str): Path of an ``.ensime`` file to parse.

        Returns:
            dict: Configuration values with string keys.
        """

        def paired(iterable):
            """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
            cursor = iter(iterable)
            return zip(cursor, cursor)

        def unwrap_if_sexp_symbol(datum):
            """Convert Symbol(':key') to ':key' (Symbol isn't hashable for dict keys).
            """
            return datum.value() if isinstance(datum, sexpdata.Symbol) else datum

        def sexp2dict(sexps):
            """Transforms a nested list structure from sexpdata to dict."""
            newdict = {}

            # Turn flat list into associative pairs
            for key, value in paired(sexps):
                key = str(unwrap_if_sexp_symbol(key)).lstrip(':')

                # Recursively transform nested lists
                if isinstance(value, list) and value and isinstance(value[0], list):
                    newdict[key] = [sexp2dict(value[0])]
                else:
                    newdict[key] = value

            return newdict

        conf = sexpdata.loads(Util.read_file(path))
        return sexp2dict(conf)
