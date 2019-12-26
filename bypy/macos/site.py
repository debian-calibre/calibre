import builtins
import os
import sys

import _sitebuiltins


def nuke_stdout():
    # Redirect stdout, stdin and stderr to /dev/null
    from calibre.constants import plugins
    plugins['speedup'][0].detach(os.devnull)


def set_helper():
    builtins.help = _sitebuiltins._Helper()


def set_quit():
    eof = 'Ctrl-D (i.e. EOF)'
    builtins.quit = _sitebuiltins.Quitter('quit', eof)
    builtins.exit = _sitebuiltins.Quitter('exit', eof)


def main():
    sys.argv[0] = sys.calibre_basename
    dfv = os.environ.get('CALIBRE_DEVELOP_FROM')
    if dfv and os.path.exists(dfv):
        sys.path.insert(0, os.path.abspath(dfv))
    set_helper()
    set_quit()
    if sys.gui_app and not (
        sys.stdout.isatty() or sys.stderr.isatty() or sys.stdin.isatty()
    ):
        nuke_stdout()
    mod = __import__(sys.calibre_module, fromlist=[1])
    func = getattr(mod, sys.calibre_function)
    return func()


if __name__ == '__main__':
    main()
