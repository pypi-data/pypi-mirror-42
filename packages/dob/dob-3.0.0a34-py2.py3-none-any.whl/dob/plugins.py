# -*- coding: utf-8 -*-

# This file is part of 'dob'.
#
# 'dob' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 'dob' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 'dob'.  If not, see <http://www.gnu.org/licenses/>.

"""A time tracker for the command line. Utilizing the power of hamster! [nark]."""

from __future__ import absolute_import, unicode_literals

import glob
import os
import shutil
import sys

from gettext import gettext as _

import click
from click_alias import ClickAliasedGroup

from .cmd_config import AppDirs, get_appdirs_subdir_file_path
from .helpers import dob_in_user_warning
from .helpers.path import compile_and_eval_source

__all__ = (
    'install_plugin',
    'ClickAliasablePluginGroup',
)


class ClickAliasablePluginGroup(ClickAliasedGroup):

    def __init__(self, *args, **kwargs):
        super(ClickAliasablePluginGroup, self).__init__(*args, **kwargs)
        self.plugins_basepath = os.path.join(
            AppDirs.user_config_dir, 'plugins',
        )
        self.has_loaded = False

    @property
    def plugin_paths(self):
        py_paths = glob.glob(os.path.join(self.plugins_basepath, '*.py'))
        return py_paths

    def list_commands(self, ctx):
        """Called by click-alias to get list of commands."""
        set_names = set()
        for cmd in self.get_commands_from_plugins(name=None):
            set_names.add(cmd.name)
        cmd_names = super(ClickAliasablePluginGroup, self).list_commands(ctx)
        return cmd_names

    def get_command(self, ctx, name):
        # Aha!:
        #   assert ctx.command is self  # So True.
        # NOTE: get_command is called via self.resolve_command, from
        #       click.MultiCommand.invoke. Just FYI. -(lb)
        # Call the get-commands func., which really just sources the plugins, so they
        # can tie into Click; then we can just call the base class implementation.
        cmd = super(ClickAliasablePluginGroup, self).get_command(ctx, name)
        if cmd is None:
            # (lb): Profiling: Loading plugins [2018-07-15: I have 3]: 0.139 secs.
            #       So only call if necessary.
            self.get_commands_from_plugins(name)
            cmd = super(ClickAliasablePluginGroup, self).get_command(ctx, name)
        return cmd

    def ensure_plugged_in(self):
        if self.has_loaded:
            return
        self.get_commands_from_plugins(name=None)

    def get_commands_from_plugins(self, name):
        cmds = set()
        for py_path in self.plugin_paths:
            try:
                files_cmds = self.open_source_eval_and_poke_around(py_path, name)
                # (lb): Use a set, because if different plugins all import the
                # same object, e.g., `from dob.run_cli import run`, we dont'
                # want to return multiple matches.
                cmds |= files_cmds
            except Exception as err:
                msg = _(
                    'ERROR: Could not open plugins file "{}": {}'
                ).format(py_path, str(err))
                dob_in_user_warning(msg)
        self.has_loaded = True
        return list(cmds)

    def open_source_eval_and_poke_around(self, py_path, name):
        # NOTE: The code that's eval()ed might append to self._aliases!
        #       (Or anything else!)
        eval_globals = compile_and_eval_source(py_path)
        cmds = self.probe_source_for_commands(eval_globals, name)
        return cmds

    def probe_source_for_commands(self, eval_globals, name):
        # Check for alias now, after having sourced the plugin.
        cmd_name = None
        if name:
            cmd_name = self.resolve_alias(name)

        cmds = set()
        for lname, obj in eval_globals.items():
            if not isinstance(obj, click.Command):
                continue
            if self is obj:
                # This is the 'run' object created in the run_cli module.
                continue
            if not cmd_name or obj.name == cmd_name:
                cmds.add(obj)
        return cmds


# ***
# *** Install-Plugin helper.
# ***

def install_plugin(package_module_path, package_plugin_name):
    """
    Helper function for Dob plugins to use to install themselves.

    For an example, see:

        https://github.com/hotoffthehamster/dob-plugin-example

    and search PyPI for matching "dob-plugin-\*" projects.
    """
    def _install_plugin():
        src_plugin = must_src_plugin_path()
        dst_plugin = must_dst_target_path()
        symlink_or_copy_plugin_or_die(src_plugin, dst_plugin)

    def must_src_plugin_path():
        src_plugin = os.path.join(
            os.path.dirname(package_module_path),
            '..',
            'plugins',
            package_plugin_name,
        )
        assert os.path.exists(src_plugin)
        return src_plugin

    def must_dst_target_path():
        dst_plugin = get_appdirs_subdir_file_path(
            file_basename=package_plugin_name,
            dir_dirname='plugins',
            appdirs_dir=AppDirs.user_config_dir,
        )
        if os.path.exists(dst_plugin):
            print("The plugin is already installed!")
            sys.exit(1)
        return dst_plugin

    def symlink_or_copy_plugin_or_die(src_plugin, dst_plugin):
        try:
            symlink_or_copy_plugin(src_plugin, dst_plugin)
        except Exception as err:
            exit_error_unknown(err)

    def symlink_or_copy_plugin(src_plugin, dst_plugin):
        try:
            symlink_plugin(src_plugin, dst_plugin)
        except NotImplementedError:
            on_windows_copy_plugin(src_plugin, dst_plugin)

    def symlink_plugin(src_plugin, dst_plugin):
        os.symlink(src_plugin, dst_plugin, target_is_directory=False)
        print(_(
            "Successfully installed plugin (using symlink) to: {}"
        ).format(dst_plugin))

    def on_windows_copy_plugin(src_plugin, dst_plugin):
        shutil.copyfile(src_plugin, dst_plugin)
        print(_(
            "Successfully copied plugin to: {}"
        ).format(dst_plugin))
        print(_(
            "NOTE: To upgrade the plugin after upgrading the package, "
            "run this same command again."
        ))

    def exit_error_unknown(err):
        print(_(
            "OOPS! Something bad happened: {}"
        ).format(str(err)))
        print(_(
            "Please report this bug to the plugin author! Thanks!!"
            " (And for what it's worth, sorry!)"
        ))
        sys.exit(1)

    _install_plugin()

