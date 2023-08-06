
# pylint: disable=missing-docstring,fixme

import ast
from IPython.core import magic_arguments
from IPython.core.magic import Magics, magics_class, cell_magic

from . import linter


def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    ipython.register_magics(Linter(ipython))


def unload_ipython_extension(ipython):  # pylint: disable=unused-argument
    # If you want your extension to be unloadable, put that logic here.
    pass


LINT_SETTINGS = dict(
    disable=linter.DEFAULT_DISABLE,
    message_tpl=linter.DEFAULT_FMT,
    employ_history=True,
    history_messages=False,
    debug=True,
)

LINT_DEBUG = {}


@magics_class
class Linter(Magics):

    settings = LINT_SETTINGS  # Note: global mutability is intended.

    @staticmethod
    def _is_valid_code(code):
        try:
            ast.parse(code)
        # except SyntaxError:
        # # Alas, it is not particularly documented what can it raise.
        except Exception:  # pylint: disable=broad-except
            return False
        return True

    def _get_history(self, ipy=None, sep='\n\n', valid_only=True, **kwargs):
        if ipy is None:
            ipy = self.shell
        code_pieces = [
            code
            # Notable parameters:
            # `raw`: return untranslated input (e.g. ipy magic).
            # `output`: attempt to include output.
            for sess, lineno, code in ipy.history_manager.get_range(**kwargs)]
        if valid_only:
            code_pieces = [code for code in code_pieces if self._is_valid_code(code)]
        return sep.join(code_pieces)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        '--optional', action="store_true", help="Execute even with lint errors")
    @magic_arguments.argument(
        '--no-history', action="store_true", help=(
            "Do not prepend the command history for checking.\n"
            "Useful for cells that should not depend on other cells."))
    @cell_magic
    def lint(self, line, cell):
        ipy = self.shell
        # TODO: arg-overrides of all settings.
        settings = self.settings

        args = magic_arguments.parse_argstring(self.lint, line)
        optional = args.optional
        employ_history = settings['employ_history'] and not args.no_history

        code = cell
        min_line = 0
        history = None
        full_code = code

        # Synopsis: in jupyter, it would be most correct to get the current
        # cells' contents.
        # However, that does not seem viable.
        # Another option for checking is to check in the context of current
        # global variables.
        # However, that is problematic with pylint.
        # The remaining option is to check together with the current session history.
        # This is workable but often very slow.
        if employ_history:
            history = self._get_history(ipy) + '\n\n'
            full_code = history + code
            if not settings['history_messages']:
                min_line = history.count('\n') + 1  # A somewhat tricky '+ 1'. Might be wrong.

        lint_result = linter.validate_code(full_code, disable=settings['disable'])

        messages = lint_result['messages']
        if min_line:
            messages = [message for message in messages if message['line'] >= min_line]

        if settings['debug']:
            LINT_DEBUG.update(last_result=dict(
                linter=self,
                args=args,
                code=code,
                settings=settings,
                history=history,
                min_line=min_line,
                lint_result=lint_result,
                messages=messages,
            ))

        if messages:
            print("Lint errors:")
            messages_string = '\n'.join(
                settings['message_tpl'].format(**message)
                for message in messages)
            print(messages_string)

        if not messages or optional:
            ipy.run_cell(cell)
        else:
            print("Run aborted.")


def _register():
    from IPython import get_ipython
    ipython = get_ipython()
    if ipython:
        load_ipython_extension(ipython)


if __name__ == '__main__':
    _register()
