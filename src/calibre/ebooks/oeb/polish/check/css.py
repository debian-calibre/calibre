#!/usr/bin/env python
# License: GPL v3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>

import atexit
import json
import numbers
import sys
from collections import namedtuple
from itertools import repeat

from qt.core import QApplication, QEventLoop, pyqtSignal, sip
from qt.webengine import (
    QWebEnginePage, QWebEngineProfile, QWebEngineScript
)

from calibre import detect_ncpus as cpu_count, prints
from calibre.ebooks.oeb.polish.check.base import ERROR, WARN, BaseError
from calibre.gui2 import must_use_qt
from calibre.utils.webengine import secure_webengine, setup_profile


class CSSParseError(BaseError):
    level = ERROR
    is_parsing_error = True
    FIXABLE_CSS_ERROR = False


class CSSError(BaseError):
    level = ERROR
    FIXABLE_CSS_ERROR = False


class CSSWarning(BaseError):
    level = WARN
    FIXABLE_CSS_ERROR = False


def as_int_or_none(x):
    if x is not None and not isinstance(x, numbers.Integral):
        try:
            x = int(x)
        except Exception:
            x = None
    return x


def message_to_error(message, name, line_offset, rule_metadata):
    rule_id = message.get('rule')
    if rule_id == 'CssSyntaxError':
        cls = CSSParseError
    else:
        cls = CSSError if message.get('severity') == 'error' else CSSWarning
    title = message.get('text') or _('Unknown error')
    title = title.rpartition('(')[0].strip()
    line = as_int_or_none(message.get('line'))
    col = as_int_or_none(message.get('column'))
    if col is not None:
        col -= 1
    if line is not None:
        line += line_offset
    ans = cls(title, name, line, col)
    ans.HELP = message.get('text') or ''
    if ans.HELP:
        ans.HELP += '. '
    ans.css_rule_id = rule_id
    m = rule_metadata.get(rule_id) or {}
    if 'url' in m:
        ans.HELP += _('See <a href="{}">detailed description</a>.').format(m['url']) + ' '
    if m.get('fixable'):
        ans.FIXABLE_CSS_ERROR = True
        ans.HELP += _('This error will be automatically fixed if you click "Try to correct all fixable errors" below.')
    return ans


def stylelint_js():
    ans = getattr(stylelint_js, 'ans', None)
    if ans is None:
        ans = stylelint_js.ans = (
            ('stylelint-bundle.min.js', P('stylelint-bundle.min.js', data=True, allow_user_override=False).decode('utf-8')),
            ('stylelint.js', P('stylelint.js', data=True, allow_user_override=False).decode('utf-8')),
        )
    return ans


def create_profile():
    ans = getattr(create_profile, 'ans', None)
    if ans is None:
        ans = create_profile.ans = QWebEngineProfile(QApplication.instance())
        setup_profile(ans)
        for (name, code) in stylelint_js():
            s = QWebEngineScript()
            s.setName(name)
            s.setSourceCode(code)
            s.setWorldId(QWebEngineScript.ScriptWorldId.ApplicationWorld)
            ans.scripts().insert(s)
    return ans


class Worker(QWebEnginePage):

    work_done = pyqtSignal(object, object)

    def __init__(self):
        must_use_qt()
        QWebEnginePage.__init__(self, create_profile(), QApplication.instance())
        self.titleChanged.connect(self.title_changed)
        secure_webengine(self.settings())
        self.ready = False
        self.working = False
        self.pending = None
        self.setHtml('')

    def title_changed(self, new_title):
        new_title = new_title.partition(':')[0]
        if new_title == 'ready':
            self.ready = True
            if self.pending is not None:
                self.check_css(*self.pending)
                self.pending = None
        elif new_title == 'checked':
            self.runJavaScript('window.get_css_results()', QWebEngineScript.ScriptWorldId.ApplicationWorld, self.check_done)

    def javaScriptConsoleMessage(self, level, msg, lineno, source_id):
        msg = f'{source_id}:{lineno}:{msg}'
        try:
            print(msg)
        except Exception:
            pass

    def check_css(self, src, fix=False):
        self.working = True
        self.runJavaScript(
            f'window.check_css({json.dumps(src)}, {"true" if fix else "false"})', QWebEngineScript.ScriptWorldId.ApplicationWorld)

    def check_css_when_ready(self, src, fix=False):
        if self.ready:
            self.check_css(src, fix)
        else:
            self.working = True
            self.pending = src, fix

    def check_done(self, results):
        self.working = False
        for result in results:
            self.work_done.emit(self, result)


class Pool:

    def __init__(self):
        self.workers = []
        self.max_workers = cpu_count()

    def add_worker(self):
        w = Worker()
        w.work_done.connect(self.work_done)
        self.workers.append(w)

    def check_css(self, css_sources, fix=False):
        self.doing_fix = fix
        self.pending = list(enumerate(css_sources))
        self.results = list(repeat(None, len(css_sources)))
        self.working = True
        self.assign_work()
        app = QApplication.instance()
        while self.working:
            app.processEvents(QEventLoop.ProcessEventsFlag.WaitForMoreEvents | QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
        return self.results

    def assign_work(self):
        while self.pending:
            if len(self.workers) < self.max_workers:
                self.add_worker()
            for w in self.workers:
                if not w.working:
                    idx, src = self.pending.pop()
                    w.result_idx = idx
                    w.check_css_when_ready(src, self.doing_fix)
                    break
            else:
                break

    def work_done(self, worker, result):
        self.results[worker.result_idx] = result
        self.assign_work()
        if not self.pending and not any(w for w in self.workers if w.working):
            self.working = False

    def shutdown(self):

        def safe_delete(x):
            if not sip.isdeleted(x):
                sip.delete(x)

        for i in self.workers:
            safe_delete(i)
        self.workers = []


pool = Pool()
shutdown = pool.shutdown
atexit.register(shutdown)
Job = namedtuple('Job', 'name css line_offset fix_data')


def create_job(name, css, line_offset=0, is_declaration=False, fix_data=None):
    if is_declaration:
        css = 'div{\n' + css + '\n}'
        line_offset -= 1
    return Job(name, css, line_offset, fix_data)


def check_css(jobs):
    errors = []
    if not jobs:
        return errors
    results = pool.check_css([j.css for j in jobs])
    for job, result in zip(jobs, results):
        if result['type'] == 'error':
            errors.append(CSSParseError(_('Failed to process CSS in {name} with errors: {errors}').format(
                name=job.name, errors=result['error']), job.name))
            continue
        result = json.loads(result['results']['output'])
        rule_metadata = result['rule_metadata']
        for msg in result['results']['warnings']:
            err = message_to_error(msg, job.name, job.line_offset, rule_metadata)
            if err is not None:
                errors.append(err)
    return errors


def main():
    with open(sys.argv[-1], 'rb') as f:
        css = f.read().decode('utf-8')
    errors = check_css([create_job(sys.argv[-1], css)])
    for error in errors:
        prints(error)


if __name__ == '__main__':
    try:
        main()
    finally:
        shutdown()
