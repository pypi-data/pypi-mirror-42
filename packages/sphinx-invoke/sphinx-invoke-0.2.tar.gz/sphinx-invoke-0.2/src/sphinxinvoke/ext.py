import os
import importlib
import inspect
# pylint: disable=import-error
from docutils.nodes import title, literal_block, section, make_id
from docutils.parsers.rst.directives import unchanged
from docutils.parsers.rst import Directive
from invoke.program import Program
# pylint: enable=import-error


__copyright__ = 'Copyright (C) 2019, Nokia'


class ExtProgram(Program):

    def get_task_help(self, task):

        ret = ''
        # Use the parser's contexts dict as that's the easiest way to obtain
        # Context objects here - which are what help output needs.
        ctx = self.parser.contexts[task]
        tuples = ctx.help_tuples()
        ret += self._get_usage(task).format(
            "[--options] " if tuples else "") + '\n\n'
        ret += self._get_docstring(task) + '\n'
        ret += self._get_options(tuples)
        return ret.rstrip()

    def _get_usage(self, task):
        return ("Usage: {1} "
                "{0} {{0}}[other tasks here ...]".format(
                    task, self.binary))

    def _get_docstring(self, task):
        ret = 'Docstring:\n'
        docstring = inspect.getdoc(self.collection[task])
        if docstring:
            ret += self._get_indended_docstring(docstring)
        else:
            ret += self.indent + "none\n"
        return ret

    def _get_indended_docstring(self, docstring):
        ret = ''
        for line in docstring.splitlines():
            if line.strip():
                ret += self.indent + line
            ret += '\n'
        return ret

    def _get_options(self, tuples):
        ret = "Options:\n"
        if tuples:
            ret += self._get_help_columns(tuples)
        else:
            ret += self.indent + "none"
        return ret

    def _get_help_columns(self, tuples):
        ret = ''
        for name, _ in tuples:
            name_padding = self._get_name_width(tuples) - len(name)
            spec = ''.join((self.indent,
                            name,
                            name_padding * ' ',
                            self.col_padding * ' '))
            ret += spec.rstrip() + '\n'
        return ret

    @staticmethod
    def _get_name_width(tuples):
        return max(len(x[0]) for x in tuples)


class InvokeDirective(Directive):

    option_spec = dict(module=unchanged, prog=unchanged)

    def __init__(self, *args, **kwargs):
        super(InvokeDirective, self).__init__(*args, **kwargs)
        self._mod = None

    def run(self):
        return [node for node in self._get_nodes()]

    def _get_nodes(self):
        for task in self._tasks:
            yield self._get_node_for_task(task)

    def _get_node_for_task(self, task):
        node = section(ids=[make_id(task)],
                       names=task)
        node += title(text=task)
        node += self._get_task_help_literal(task)
        return node

    @property
    def _tasks(self):
        return sorted(
            [task for task in self._create_program().collection.task_names])

    def _create_program(self, task=None):
        p = ExtProgram(name=self._name)
        p.normalize_argv(self._get_argv(task))
        p.parse_core_args()
        p.load_collection()
        if task:
            p.parse_tasks()
        return p

    def _get_argv(self, task):
        argv = [self._name,
                '-r', self._moduledir,
                '-c', self._modulename]
        if task:
            argv += ['-h', task]
        return argv

    @property
    def _name(self):
        return self.options.get('prog', 'invoke')

    @property
    def _module(self):
        if self._mod is None:
            self._mod = importlib.import_module(self.options['module'])
        return self._mod

    @property
    def _modulename(self):
        return os.path.splitext(os.path.basename(self._module.__file__))[0]

    @property
    def _moduledir(self):
        return os.path.dirname(self._module.__file__)

    def _get_task_help_literal(self, task):
        return literal_block(text=self._get_task_help(task))

    def _get_task_help(self, task):
        return self._create_program(task).get_task_help(task)


def setup(app):
    app.add_directive('invoke', InvokeDirective)
