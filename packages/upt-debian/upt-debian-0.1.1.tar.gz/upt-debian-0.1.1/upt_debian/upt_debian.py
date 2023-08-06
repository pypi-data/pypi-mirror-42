# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import datetime
import logging
import os
import sys

import jinja2
import upt


logger = logging.getLogger('upt')


class DebianPackage(object):
    template_ext = 'generic'

    def __init__(self, upt_pkg, output=None):
        self.upt_pkg = upt_pkg
        self.output_dir = os.path.join(output or '.', 'debian')
        self.files = [
            # Required files first.
            # See: https://www.debian.org/doc/manuals/maint-guide/dreq.en.html
            ('control', f'control.{self.template_ext}'),
            ('copyright', f'copyright.{self.template_ext}'),
            ('changelog', 'changelog'),
            ('rules', f'rules.{self.template_ext}'),
            # Other files
            ('watch', f'watch.{self.template_ext}'),
            ('compat', 'compat'),
            ('source/format', 'source/format'),
        ]

    def _render_template(self, filename, template):
        file_path = os.path.join(self.output_dir, filename)
        logger.info(f'Creating {file_path}')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.env.get_template(template).render(pkg=self))

    def create(self):
        self._setup_jinja2()
        self._create_output_directories()
        for (filename, template) in self.files:
            self._render_template(filename, template)

    @staticmethod
    def now():
        return datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

    def __getattribute__(self, name):
        if name in ['name', 'homepage', 'description', 'summary', 'version']:
            return self.upt_pkg.__getattribute__(name)
        else:
            return object.__getattribute__(self, name)

    def _setup_jinja2(self):
        self.env = jinja2.Environment(
            loader=jinja2.PackageLoader('upt_debian', 'templates'),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        self.env.filters['debianize_name'] = self.debianize_name
        self.env.filters['debianize_requirement'] = self.debianize_requirement

    def _create_output_directories(self):
        """Creates the directory layout required to port upt_pkg."""
        logger.info(f'Creating {self.output_dir}')
        try:
            os.makedirs(f'{self.output_dir}/source', exist_ok=False)
        except PermissionError:
            sys.exit(f'Cannot create {self.output_dir}: permission denied.')
        except FileExistsError:
            sys.exit(f'Cannot create {self.output_dir}: already exists.')

    def _depends(self, phase):
        return self.upt_pkg.requirements.get(phase, [])

    @property
    def build_depends(self):
        return self._depends('build')

    @property
    def run_depends(self):
        return self._depends('run')

    @property
    def test_depends(self):
        return self._depends('test')

    @staticmethod
    def _debianize_version_specifier(specifier):
        if specifier.startswith('=='):
            return specifier[1:]
        elif specifier.startswith('<') and not specifier.startswith('<='):
            return f'<{specifier}'
        elif specifier.startswith('>') and not specifier.startswith('>='):
            return f'>{specifier}'
        else:
            return specifier

    def debianize_requirement(self, req):
        output = []
        if req.specifier:
            specifiers = req.specifier.split(',')
            for specifier in specifiers:
                specifier = self._debianize_version_specifier(specifier)
                output.append(f'{self.debianize_name(req.name)} ({specifier})')
            return ', '.join(output)
        else:
            return self.debianize_name(req.name)


class DebianPythonPackage(DebianPackage):
    template_ext = 'python'
    section = 'python'

    def debianize_name(self, name):
        if name.startswith('python-'):
            return f'python3-{name[7:]}'
        else:
            return f'python3-{name}'


class DebianBackend(upt.Backend):
    name = 'debian'

    def create_package(self, upt_pkg, output=None):
        pkg_classes = {
            'pypi': DebianPythonPackage,
        }

        try:
            pkg_cls = pkg_classes[upt_pkg.frontend]
        except KeyError:
            raise upt.UnhandledFrontendError(self.name, upt_pkg.frontend)

        pkg_cls(upt_pkg, output).create()
