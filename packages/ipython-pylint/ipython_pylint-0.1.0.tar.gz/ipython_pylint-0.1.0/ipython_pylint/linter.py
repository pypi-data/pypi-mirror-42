#!/usr/bin/env python3
"""
A modification of PyLinter for use on in-memory code text.
"""
# pylint: disable=missing-docstring

import os
from astroid.builder import AstroidBuilder
from astroid.exceptions import AstroidBuildingException
import astroid.scoped_nodes
from pylint.lint import PyLinter
from pylint.reporters.json import JSONReporter
from pylint.reporters.text import TextReporter


DEFAULT_DISABLE = (
    'missing-docstring',
    'invalid-name',
)
# Default effective formatting of the TextFormatter.
# Unused keys: module, type, obj
DEFAULT_FMT = '{path}:{line}:{column}: {message-id}: {message} ({symbol})'


class InMemoryMessagesBuffer:

    def __init__(self):
        self.content = []

    def write(self, string):
        self.content.append(string)

    def messages(self):
        return self.content

    def reset(self):
        self.content = []


# pylint: disable=too-many-ancestors
class StringPyLinter(PyLinter):
    """ PyLinter for running on code from a string """

    def __init__(self, *args, **kwargs):
        # options=(), reporter=None, option_groups=(), pylintrc=None):
        super(StringPyLinter, self).__init__(*args, **kwargs)
        self._inmem_modules = {}
        # self._walker = None
        # self._used_checkers = None
        # self._tokencheckers = None
        # self._rawcheckers = None
        # self.initCheckers()

    # def __del__(self):
    #     self.cleanup_import_path()
    #     self.destroyCheckers()

    # def initCheckers(self):
    #     self._walker = PyLintASTWalker(self)
    #     self._used_checkers = self.prepare_checkers()
    #     self._tokencheckers = [c for c in self._used_checkers if implements(c, ITokenChecker)
    #                            and c is not self]
    #     self._rawcheckers = [c for c in self._used_checkers if implements(c, IRawChecker)]
    #     # notify global begin
    #     for checker in self._used_checkers:
    #         checker.open()
    #         if implements(checker, IAstroidChecker):
    #             self._walker.add_checker(checker)

    # def destroyCheckers(self):
    #     self._used_checkers.reverse()
    #     for checker in self._used_checkers:
    #         checker.close()

    def check_string(self, string, modname='__in_memory__'):
        """
        Run linter on code text `string`.
        """
        # self.set_current_module(modname)
        node = self.get_astroid_node(string, modname)
        # self.check_astroid_module(astroid, self._walker, self._rawcheckers, self._tokencheckers)
        return self.check(node)

    def get_astroid_node(self, string, modname):
        """ Return an astroid module representation from code text """
        try:
            return AstroidBuilder().string_build(string, modname)
        except SyntaxError as exc:
            self.add_message('syntax-error', line=exc.lineno, args=exc.msg)
        except AstroidBuildingException as exc:
            self.add_message('parse-error', args=exc)
        except Exception as exc:  # pylint: disable=broad-except
            import traceback
            traceback.print_exc()
            self.add_message('astroid-error', args=(exc.__class__, exc))

    # Hacks for `self.check` to handle prepared astroid modules
    def expand_files(self, modules, *args, **kwargs):  # pylint: disable=arguments-differ
        filtered = []
        prepared = []
        for module in modules:
            if module is None:
                pass
            elif not isinstance(module, (bytes, str, os.PathLike)):
                assert isinstance(module, astroid.scoped_nodes.Module)
                prepared.append(module)
            else:
                filtered.append(module)

        result = super().expand_files(filtered, *args, **kwargs)

        for module in prepared:
            if module.file == '<?>':
                module_id = module.file
            else:
                module_id = '__inmem_module__{}'.format(id(module))
            assert (
                module_id not in self._inmem_modules or
                self._inmem_modules[module_id] is module), "module uniqueness catch"
            result.append(dict(
                path=module_id,
                name=module.name,
                isarg=True,
                basepath='.',  # `realpath()`?
                basename=module.name,
                _module=module,
            ))
            self._inmem_modules[module_id] = module
        return result

    def get_ast(self, filepath, *args, **kwargs):  # pylint: disable=arguments-differ
        result = self._inmem_modules.get(filepath)
        if result is not None:
            return result
        return super().get_ast(filepath, *args, **kwargs)


def validate_code(code_string, formatted=False, disable=DEFAULT_DISABLE):
    messages = InMemoryMessagesBuffer()
    if formatted:
        reporter = TextReporter(output=messages)
    else:
        reporter = JSONReporter(output=messages)

    # For reference, see `pylint.lint.Run.__init__` (used as the main entry point).
    linter = StringPyLinter()
    linter.load_default_plugins()
    # linter.load_plugin_modules(self._plugins)
    # linter.disable("I")
    for name in disable:
        linter.disable(name)
    # linter.enable("c-extension-no-member")
    # linter.read_config_file(verbose=self.verbose)
    # linter.load_config_file()
    linter.set_reporter(reporter)
    # linter.load_command_line_configuration(args)
    # linter.config.jobs = ...
    if hasattr(linter, 'load_plugin_configuration'):  # for fresh enough pylint
        linter.load_plugin_configuration()
    linter.check_string(code_string)
    # linter.generate_reports()
    return dict(
        linter=linter,
        messages=messages.content if formatted else reporter.messages,
        stats=linter.stats,
        status=linter.msg_status,
    )


def main():
    test_code = (
        "a = 1\n"
        "print(a)\n"
        "v\n"
        "\n"
        "print(1)\n"
    )

    res = validate_code(test_code)
    # <?>:4:0: W0104: Statement seems to have no effect (pointless-statement)
    fmt = DEFAULT_FMT
    print('\n'.join(
        fmt.format(**msg)
        for msg in res['messages']))


if __name__ == '__main__':
    main()
