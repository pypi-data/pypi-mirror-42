
# This file is part of MSMTools.
#
# Copyright (c) 2015, 2014 Computational Molecular Biology Group, Freie Universitaet Berlin (GER)
#
# MSMTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
utility functions for python setup
"""
import tempfile
import os
import sys
import shutil
from distutils.ccompiler import new_compiler
import setuptools
import contextlib


@contextlib.contextmanager
def TemporaryDirectory():
    n = tempfile.mkdtemp()
    yield n
    shutil.rmtree(n)


@contextlib.contextmanager
def stdchannel_redirected(stdchannel, dest_filename, fake=False):
    """
    A context manager to temporarily redirect stdout or stderr

    e.g.:

    with stdchannel_redirected(sys.stderr, os.devnull):
        if compiler.has_function('clock_gettime', libraries=['rt']):
            libraries.append('rt')
    """
    if fake:
        yield
        return
    oldstdchannel = dest_file = None
    try:
        oldstdchannel = os.dup(stdchannel.fileno())
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), stdchannel.fileno())

        yield
    finally:
        if oldstdchannel is not None:
            os.dup2(oldstdchannel, stdchannel.fileno())
        if dest_file is not None:
            dest_file.close()


# From http://stackoverflow.com/questions/
# 7018879/disabling-output-when-compiling-with-distutils
def has_function(compiler, funcname, headers):
    if not isinstance(headers, (tuple, list)):
        headers = [headers]
    with TemporaryDirectory() as tmpdir, stdchannel_redirected(sys.stderr, os.devnull), \
             stdchannel_redirected(sys.stdout, os.devnull):
        try:
            fname = os.path.join(tmpdir, 'funcname.c')
            f = open(fname, 'w')
            for h in headers:
                f.write('#include <%s>\n' % h)
            f.write('int main(void) {\n')
            f.write(' %s();\n' % funcname)
            f.write('return 0;}')
            f.close()
            objects = compiler.compile([fname], output_dir=tmpdir)
            compiler.link_executable(objects, os.path.join(tmpdir, 'a.out'))
        except (setuptools.distutils.errors.CompileError, setuptools.distutils.errors.LinkError):
            return False
        except:
            import traceback
            traceback.print_last()
            return False
        return True


def detect_openmp(compiler):
    from distutils.log import debug
    from copy import deepcopy
    compiler = deepcopy(compiler) # avoid side-effects
    has_openmp = has_function(compiler, 'omp_get_num_threads', headers='omp.h')
    debug('[OpenMP] compiler %s has builtin support', compiler)
    additional_libs = []
    if not has_openmp:
        debug('[OpenMP] compiler %s needs library support', compiler)
        if sys.platform == 'darwin':
            compiler.add_library('iomp5')
        elif sys.platform.startswith('linux'):
            compiler.add_library('gomp')
        has_openmp = has_function(compiler, 'omp_get_num_threads', headers='omp.h')
        if has_openmp:
            additional_libs = [compiler.libraries[-1]]
            debug('[OpenMP] added library %s', additional_libs)
    return has_openmp, additional_libs


# has_flag and cpp_flag taken from https://github.com/pybind/python_example/blob/master/setup.py
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    with TemporaryDirectory() as tmpdir, \
            stdchannel_redirected(sys.stderr, os.devnull), \
            stdchannel_redirected(sys.stdout, os.devnull):
        f = tempfile.mktemp(suffix='.cpp', dir=tmpdir)
        with open(f, 'w') as fh:
            fh.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f], extra_postargs=[flagname], output_dir=tmpdir)
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.
    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler ({})-- at least C++11 support '
                           'is needed!'.format(compiler))


class lazy_cythonize(list):
    """evaluates extension list lazily.
    pattern taken from http://tinyurl.com/qb8478q"""
    def __init__(self, callback):
        self._list, self.callback = None, callback
    def c_list(self):
        if self._list is None: self._list = self.callback()
        return self._list
    def __iter__(self):
        for e in self.c_list(): yield e
    def __getitem__(self, ii): return self.c_list()[ii]
    def __len__(self): return len(self.c_list())


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def search_pybind11_headers(self):
        import pybind11

        def recommended():
            return pybind11.get_include(self.user)

        def setuptools_temp_egg():
            # If users of setuptools drag in pybind11 only as a setup_require(ment), the pkg will be placed
            # temporarily into .eggs, but we can not use the headers directly. So we have to
            # link non-installed header files to correct subdirectory, so they can be used during compilation
            found = False
            for p in pybind11.__path__:
                if '.egg' in p:
                    found = True
            if not found:
                return ''

            header_src = os.path.abspath(os.path.join(pybind11.__path__[0], '..'))
            hdrs = []

            for _, _, filenames in os.walk(header_src):
                hdrs += [f for f in filenames if f.endswith('.h')]
            for h in sorted(hdrs):
                if 'detail' in h:
                    sub = 'detail'
                else:
                    sub = ''
                dest = os.path.join(pybind11.__path__[0], sub, os.path.basename(h))
                try:
                    os.link(h, dest)
                except OSError:
                    pass
            return header_src

        methods = (recommended(),
                   setuptools_temp_egg(),
                   )
        for m in methods:
            if os.path.exists(os.path.join(m, 'pybind11', 'pybind11.h')):
                return m
        return ''

    def __str__(self):
        result = self.search_pybind11_headers()
        if not result:
            raise RuntimeError('pybind11 headers not found')
        return result
