#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

from builtins import str
import sys
import os.path
import optparse

import taurus
from taurus.external.qt import Qt
from taurus.core.util.log import deprecation_decorator

def env_index(env, env_name):
    env_name = str(env_name)
    for i, e in enumerate(env):
        e = str(e)
        if e.startswith(env_name):
            return i
    return -1


def has_env(env, env_name):
    return env_index(env, env_name) != -1


def get_env(env, env_name):
    env_name = str(env_name)
    for i, e in enumerate(env):
        e = str(e)
        if e.startswith(env_name):
            return e.split("=")[1]
    return None


def append_or_create_env(env, env_name, env_value, is_path_like=True):
    i = env_index(env, env_name)
    if i == -1:
        env.append(env_name + "=" + env_value)
    else:
        if is_path_like:
            e_n, e_v = env[i].split("=")
            paths = e_v.split(os.path.pathsep)
            if env_value not in paths:
                env_value += os.path.pathsep + e_v
        env[i] = env_name + "=" + env_value


def append_or_create_env_list(env, env_name, env_value):
    env_value = os.path.pathsep.join(env_value)
    append_or_create_env(env, env_name, env_value)


def get_qtdesigner_bin():
    designer_bin = str(Qt.QLibraryInfo.location(Qt.QLibraryInfo.BinariesPath))

    plat = sys.platform
    if plat == "darwin":
        designer_bin = os.path.join(
            designer_bin, "Designer.app", "Contents", "MacOS")
    elif plat in ("win32", "nt"):
        import PyQt4
        designer_bin = os.path.abspath(os.path.dirname(PyQt4.__file__))

    designer_bin = os.path.join(designer_bin, "designer")
    return designer_bin


def get_taurus_designer_path():
    """Returns a list of directories containing taurus designer plugins"""
    # Set PYQTDESIGNERPATH to look inside taurus for designer plugins
    taurus_path = os.path.dirname(os.path.abspath(taurus.__file__))
    taurus_qt_designer_path = os.path.join(taurus_path, 'qt', 'qtdesigner')
    return [taurus_qt_designer_path]


@deprecation_decorator(alt='get_taurus_designer_env', rel='4.5')
def qtdesigner_prepare_taurus(env=None, taurus_extra_path=None):
    # Tell Qt Designer where it can find the directory containing the plugins
    if env is None:
        env = Qt.QProcess.systemEnvironment()

    # Set PYQTDESIGNERPATH to look inside taurus for designer plugins
    taurus_designer_path = get_taurus_designer_path()

    append_or_create_env_list(env, "PYQTDESIGNERPATH", taurus_designer_path)

    # Set TAURUSQTDESIGNERPATH
    if taurus_extra_path is not None:
        append_or_create_env(env, "TAURUSQTDESIGNERPATH", taurus_extra_path)
        append_or_create_env(env, "PYTHONPATH", taurus_extra_path)

    # print "PYTHONPATH=%s" % get_env(env, "PYTHONPATH")
    # print "PYQTDESIGNERPATH=%s" % get_env(env, "PYQTDESIGNERPATH")
    return env


def get_taurus_designer_env(taurus_extra_path=None):

    env = Qt.QProcessEnvironment.systemEnvironment()

    # Set PYQTDESIGNERPATH to look inside taurus for designer plugins
    (taurus_designer_path,) = get_taurus_designer_path()
    env.insert("PYQTDESIGNERPATH", taurus_designer_path)

    # Set TAURUSQTDESIGNERPATH
    if taurus_extra_path is not None:
        env.insert("TAURUSQTDESIGNERPATH", taurus_extra_path)
        env.insert("PYTHONPATH", taurus_extra_path)

    return env


def qtdesigner_start(args, env=None):

    # Start Designer.
    designer_bin = get_qtdesigner_bin()

    designer = Qt.QProcess()
    designer.setProcessChannelMode(Qt.QProcess.ForwardedChannels)
    if isinstance(env, Qt.QProcessEnvironment):
        designer.setProcessEnvironment(env)
    else: # obsolete call, only for bck-compat
        taurus.deprecated(dep='passing env which is not a QProcessEnvironment',
                          alt='QProcessEnvironment', rel='4.5')
        designer.setEnvironment(env)
    designer.start(designer_bin, args)
    designer.waitForFinished(-1)

    return designer.exitCode()


def main(env=None):
    if env is not None:
        taurus.info('ignoring obsolete env parameter to qtdesigner_start')

    version = "taurusdesigner %s" % (taurus.Release.version)
    usage = "Usage: %prog [options] <ui file(s)>"
    description = "The Qt designer application customized for taurus"
    parser = optparse.OptionParser(
        version=version, usage=usage, description=description)
    parser.add_option("--taurus-path", dest="tauruspath", default="",
                      help="additional directories to look for taurus widgets")
    parser.add_option("--qt-designer-path", dest="pyqtdesignerpath", default="",
                      help="additional directories to look for python qt widgets")

    options, args = parser.parse_args()

    taurus_extra_path = None
    # Set TAURUSQTDESIGNERPATH
    if len(options.tauruspath) > 0:
        taurus_extra_path = options.tauruspath

    if env is None:
        env = get_taurus_designer_env(taurus_extra_path=taurus_extra_path)

    sys.exit(qtdesigner_start(args, env=env))

if __name__ == "__main__":
    main()
