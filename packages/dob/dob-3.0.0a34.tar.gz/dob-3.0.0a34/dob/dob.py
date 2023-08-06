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

# FIXME: PROFILING
from nark.helpers.dev.profiling import profile_elapsed
# FIXME: PROFILING
# E402 module level import not at top of file
profile_elapsed('To dob:   _top')  # noqa: E402

import os
import re
import sys
from functools import update_wrapper

from click_alias import ClickAliasedGroup
from gettext import gettext as _

import click

from . import cmd_options, help_strings, migrate, update
from .cmd_common import (
    induct_newbies,
    insist_germinated,
    must_no_more_than_one_file,
    post_processor
)
from .cmd_options import (
    OptionWithDynamicHelp,
    cmd_options_edit_item,
    cmd_options_fact_add,
    cmd_options_fact_dryable,
    cmd_options_fact_nocarousel,
    cmd_options_factoid,
    cmd_options_limit_offset,
    cmd_options_list_activitied,
    cmd_options_list_categoried,
    cmd_options_list_fact,
    cmd_options_search,
    cmd_options_table_bunce,
    cmd_options_usage,
    postprocess_options_table_bunce
)
from .cmds_list import activity as list_activity
from .cmds_list import category as list_category
from .cmds_list import fact as list_fact
from .cmds_list import tag as list_tag
from .cmds_list.fact import echo_latest_ended, echo_ongoing_fact, echo_ongoing_or_ended
from .cmds_usage import activity as usage_activity
from .cmds_usage import category as usage_category
from .cmds_usage import tag as usage_tag
from .complete import tab_complete
from .copyright import echo_copyright, echo_license
from .create import add_fact, cancel_fact, stop_fact
from .demo import demo_config, demo_dob
from .details import echo_app_details, echo_app_environs, echo_data_stats
from .helpers import click_echo, dob_in_user_exit, dob_in_user_warning
from .migrate import upgrade_legacy_database_file
from .run_cli import dob_versions, pass_controller, run
from .transcode import export_facts, import_facts

# Disable the python_2_unicode_compatible future import warning.
click.disable_unicode_literals_warning = True

__all__ = (
    # 'version',
    # '_version',
    # 'license',
    # '_license',
    # 'copyright',
    # 'banner',  # 'dance',
    # 'details',
    # 'list_group',
    # 'list_activities',
    # 'list_categories',
    # 'list_tags',
    # 'list_facts',
    # 'search',
    # 'usage_group',
    # 'usage_activities',
    # 'usage_categories',
    # 'usage_tags',
    # 'stop',
    # 'cancel',
    # 'current',
    # 'latest',
    # 'add_fact_on',
    # 'add_fact_at',
    # 'add_fact_to',
    # 'add_fact_then',
    # 'add_fact_after',
    # 'add_fact_from',
    # 'edit_group',
    # 'dob_edit_fact',
    # 'transcode_export',
    # 'transcode_import',
    # 'complete',
    # 'migrate_group',
    # 'migrate_control',
    # 'migrate_downgrade',
    # 'migrate_upgrade',
    # 'migrate_version',
)


@run.command(hidden=True, help=help_strings.HELP_HELP)
@click.pass_context
def help(ctx):
    """Show help."""
    click_echo(run.get_help(ctx))


# ***
# *** [VERSION] Ye rote version command.
# ***

@run.command(help=help_strings.VERSION_HELP)
def version():
    """Show version information."""
    _version()


def _version():
    """Show version information."""
    click_echo(dob_versions())


# ***
# *** [LICENSE] Command.
# ***

@run.command(hidden=True, help=help_strings.LICENSE_HELP)
def license():
    """Show license information."""
    _license()


def _license():
    """Show license information."""
    echo_license()


# ***
# *** [BANNER] Command.
# ***

@run.command(aliases=['about'], help=_('View copyright information'))
@pass_controller
def copyright(controller):
    """Display copyright information.."""
    echo_copyright()


# ***
# *** [DETAILS] Command [about paths, config, etc.].
# ***

# MAYBE: (lb): Call this dob-show? dob-status? dob-info?
#   (2018-06-09: Trying aliases for now)
#   Some ideas: aliases=['show', 'status', 'info', 'config', 'details', 'appinfo'])
#   Though maybe 'show' should be alias for dob-current?
# MAYBE: Calling this 'appinfo' would make this command first in the --help....
#   @run.command(aliases=['show', 'status', 'info'], help=help_strings.DETAILS_HELP)
# See also similarly named commands that have generic meanings:
#   dob details | dob info | dob show
# i.e., details about what? info about what? showing what?
@run.command(aliases=['info'], help=help_strings.DETAILS_HELP)
@click.option('--tmi', '--full', is_flag=True, help=_('Show AppDirs paths, too.'))
@pass_controller
def details(controller, tmi):
    """List details about the runtime environment."""
    echo_app_details(controller, full=tmi)


# ***
# *** [ENVIRONS] Command [like details command, but shell-sourceable].
# ***

@run.command(help=help_strings.ENVIRONS_HELP)
@pass_controller
def environs(controller):
    """List shell-sourceable details about the runtime environment."""
    echo_app_environs(controller)


# ***
# *** [DEBUG] Dump ya on a prompt.
# ***

@run.command(help=help_strings.DEBUG_HELP)
@pass_controller
def debug(controller):
    """Break!"""
    import pdb
    pdb.set_trace()
    pass


# ***
# *** [DEMO] Command.
# ***

@run.command('demo', help=help_strings.DEMO_HELP)
@pass_controller
@demo_config
def demo_dob_and_nark(controller):
    """"""
    demo_dob(controller)


# ***
# *** [INIT] Command.
# ***

@run.command('init', help=help_strings.INIT_HELP)
@pass_controller
def init_config_and_store(controller):
    """"""
    controller.create_config_and_store()


# ***
# *** [CONFIG] Commands.
# ***

@run.group('config', cls=ClickAliasedGroup, help=help_strings.CONFIG_GROUP_HELP)
@click.pass_context
def config_group(ctx):
    """Base `config` group command run prior to any of the dob-config commands."""
    pass


@config_group.command('create', aliases=['new'], help=help_strings.CONFIG_CREATE_HELP)
@click.option('-f', '--force', is_flag=True,
              help=_('If specified, overwrite config file if is exists'))
@pass_controller
def config_create(controller, force):
    """"""
    controller.create_config(force)


# ***
# *** [STORE] Commands.
# ***

# See also: 'migrate' commands. The store commands are mostly for initial setup.

@run.group('store', cls=ClickAliasedGroup, help=help_strings.STORE_GROUP_HELP)
@click.pass_context
def store_group(ctx):
    """Base `store` group command run prior to dob-store commands."""
    pass


@store_group.command('create', aliases=['new'], help=help_strings.STORE_CREATE_HELP)
@click.option('-f', '--force', is_flag=True,
              help=_('If specified, recreate data store if is exists'))
@pass_controller
def store_create(controller, force):
    """"""
    controller.create_data_store(force)


@store_group.command('path', help=help_strings.STORE_PATH_HELP)
@pass_controller
def store_path(controller):
    """"""
    click_echo(controller.sqlite_db_path)


@store_group.command('url', help=help_strings.STORE_URL_HELP)
@pass_controller
def store_url(controller):
    """"""
    click_echo(controller.data_store_url)


@store_group.command('upgrade-legacy', help=help_strings.STORE_UPGRADE_LEGACY_HELP)
@click.argument('filename', nargs=-1, type=click.File('r'))
@click.option('-f', '--force', is_flag=True,
              help=_('If specified, overwrite data store if is exists'))
@pass_controller
@click.pass_context
@post_processor
def upgrade_legacy(ctx, controller, filename, force):
    """Migrate a legacy "Hamster" database."""
    file_in = must_no_more_than_one_file(filename)
    return upgrade_legacy_database_file(ctx, controller, file_in, force)


# ***
# *** [STATS] Command.
# ***

@run.command('stats', help=help_strings.STATS_HELP)
@pass_controller
@induct_newbies
def nark_stats(controller):
    """List stats about the user's data."""
    echo_data_stats(controller)


# ***
# *** [LIST] Commands.
# ***

# Use a command alias to avoid conflict with builtin of same name
# (i.e., we cannot declare this function, `def list()`).
@run.group('list', help=help_strings.LIST_GROUP_HELP)
@pass_controller
@click.pass_context
def list_group(ctx, controller):
    """Base `list` group command run prior to any of the dob-list commands."""
    pass


# *** ACTIVITIES.

@list_group.command('activities', help=help_strings.LIST_ACTIVITIES_HELP)
@cmd_options_search
@cmd_options_list_categoried
@cmd_options_usage
@cmd_options_table_bunce
@cmd_options_limit_offset
@pass_controller
@induct_newbies
def list_activities(controller, *args, usage=False, **kwargs):
    """List matching activities, filtered and sorted."""
    category = cmd_options.postprocess_options_list_categoried(kwargs)
    postprocess_options_table_bunce(kwargs)
    if usage:
        handler = usage_activity.usage_activities
    else:
        handler = list_activity.list_activities
    handler(
        controller,
        *args,
        filter_category=category,
        **kwargs
    )


# *** CATEGORIES.

@list_group.command('categories', help=help_strings.LIST_CATEGORIES_HELP)
@cmd_options_usage
@cmd_options_table_bunce
@cmd_options_limit_offset
@pass_controller
@induct_newbies
def list_categories(controller, *args, usage=False, **kwargs):
    """List matching categories, filtered and sorted."""
    postprocess_options_table_bunce(kwargs)
    if usage:
        handler = usage_category.usage_categories
    else:
        handler = list_category.list_categories
    handler(
        controller,
        *args,
        **kwargs,
    )


# *** TAGS.

@list_group.command('tags', help=help_strings.LIST_TAGS_HELP)
@cmd_options_search
@cmd_options_list_activitied
@cmd_options_list_categoried
@cmd_options_usage
@cmd_options_table_bunce
@cmd_options_limit_offset
@pass_controller
@induct_newbies
def list_tags(controller, *args, usage=False, **kwargs):
    """List all tags, with filtering and sorting options."""
    activity = cmd_options.postprocess_options_list_activitied(kwargs)
    category = cmd_options.postprocess_options_list_categoried(kwargs)
    postprocess_options_table_bunce(kwargs)
    if usage:
        handler = usage_tag.usage_tags
    else:
        handler = list_tag.list_tags
    handler(
        controller,
        *args,
        filter_activity=activity,
        filter_category=category,
        **kwargs,
    )


# *** FACTS.

def _list_facts(controller, *args, usage=False, **kwargs):
    """List matching facts, filtered and sorted."""
    """Fetch facts matching certain criteria."""
    activity = cmd_options.postprocess_options_list_activitied(kwargs)
    category = cmd_options.postprocess_options_list_categoried(kwargs)
    postprocess_options_table_bunce(kwargs)
    # FIXME: (lb): Should probably impose limit by default
    #          (without, my terminal hangs for a long while).
    list_fact.list_facts(
        controller,
        *args,
        include_usage=usage,
        filter_activity=activity,
        filter_category=category,
        **kwargs,
    )


def generate_list_facts_command(func):
    @cmd_options_search
    @cmd_options_list_activitied
    @cmd_options_list_categoried
    @cmd_options_usage
    @cmd_options_table_bunce
    @cmd_options_limit_offset
    @cmd_options_list_fact
    @pass_controller
    @induct_newbies
    def dob_list_facts(controller, *args, doc, **kwargs):
        _list_facts(controller, *args, block_format=doc, **kwargs)
    return update_wrapper(dob_list_facts, func)


@list_group.command('facts', help=help_strings.LIST_FACTS_HELP)
@generate_list_facts_command
def dob_list_facts(controller, *args, **kwargs):
    assert(False)  # Not reachable, because generate_list_facts_command.
    pass


# MAYBE: Should we alias the command at dob-search?
@run.command('search', help=help_strings.SEARCH_HELP)
@generate_list_facts_command
def search_facts(controller, *args, **kwargs):
    assert(False)  # Not reachable, because generate_list_facts_command.
    pass


# ***
# *** [USAGE] Commands.
# ***

@run.group('usage', help=help_strings.USAGE_GROUP_HELP)
@pass_controller
@click.pass_context
def usage_group(ctx, controller):
    """Base `usage` group command run prior to any of the dob-usage commands."""
    pass


# *** ACTIVITIES.

@usage_group.command('activities', help=help_strings.USAGE_ACTIVITIES_HELP)
@cmd_options_search
@cmd_options_list_categoried
@cmd_options_table_bunce
@cmd_options_limit_offset
@pass_controller
@induct_newbies
def usage_activities(controller, *args, **kwargs):
    """List all activities. Provide optional filtering by name."""
    category = cmd_options.postprocess_options_list_categoried(kwargs)
    postprocess_options_table_bunce(kwargs)
    usage_activity.usage_activities(
        controller,
        *args,
        filter_category=category,
        **kwargs
    )


# *** CATEGORIES.

@usage_group.command('categories', help=help_strings.USAGE_CATEGORIES_HELP)
@cmd_options_search
@cmd_options_table_bunce
@cmd_options_limit_offset
@pass_controller
@induct_newbies
def usage_categories(controller, *args, **kwargs):
    """List all categories. Provide optional filtering by name."""
    postprocess_options_table_bunce(kwargs)
    usage_category.usage_categories(
        controller,
        *args,
        **kwargs
    )


# *** TAGS.

@usage_group.command('tags', help=help_strings.USAGE_TAGS_HELP)
@cmd_options_search
@cmd_options_list_activitied
@cmd_options_list_categoried
@cmd_options_table_bunce
@cmd_options_limit_offset
@pass_controller
@induct_newbies
def usage_tags(controller, *args, **kwargs):
    """List all tags' usage counts, with filtering and sorting options."""
    activity = cmd_options.postprocess_options_list_activitied(kwargs)
    category = cmd_options.postprocess_options_list_categoried(kwargs)
    postprocess_options_table_bunce(kwargs)
    usage_tag.usage_tags(
        controller,
        *args,
        filter_activity=activity,
        filter_category=category,
        **kwargs,
    )


# *** FACTS.

@usage_group.command('facts', help=help_strings.USAGE_FACTS_HELP)
@cmd_options_search
@cmd_options_list_activitied
@cmd_options_list_categoried
@cmd_options_table_bunce
@cmd_options_limit_offset
@pass_controller
@induct_newbies
def usage_facts(controller, *args, **kwargs):
    """List all tags' usage counts, with filtering and sorting options."""
    activity = cmd_options.postprocess_options_list_activitied(kwargs)
    category = cmd_options.postprocess_options_list_categoried(kwargs)
    postprocess_options_table_bunce(kwargs)
    list_fact.list_facts(
        controller,
        *args,
        include_usage=True,
        filter_activity=activity,
        filter_category=category,
        **kwargs,
    )


# ***
# *** [CURRENT-FACT] Commands: stop/cancel/current.
# ***

@run.command('stop', help=help_strings.STOP_HELP)
# FIXME/2018-08-26: Do we really want optional factoid argument for stop command?
#   What happens if user specifies factoid on stop?
@cmd_options_factoid
@pass_controller
@induct_newbies
@click.pass_context
@post_processor
def stop(ctx, controller, factoid):
    """Stop tracking current fact (by setting its 'end')."""
    # FIXME/BACKLOG/2019-01-22 22:57: Add factoid to end of ongoing fact.
    return stop_fact(controller)


@run.command('cancel', help=help_strings.CANCEL_HELP)
@click.option(
    '-f', '--force', '--purge', is_flag=True,
    help=_('Completely delete fact, rather than just marking deleted.'),
)
@pass_controller
@induct_newbies
@click.pass_context
@post_processor
def cancel(ctx, controller, force):
    """Cancel 'ongoing fact'. Stop it without storing in the backend."""
    return cancel_fact(controller, purge=force)


@run.command('current', help=help_strings.CURRENT_HELP)
@pass_controller
@induct_newbies
def current(controller):
    """Display current *ongoing* fact."""
    echo_ongoing_fact(controller)


@run.command('latest', aliases=['last'], help=help_strings.LATEST_HELP)
@pass_controller
@induct_newbies
def latest(controller):
    """Display last saved fact."""
    echo_latest_ended(controller)


@run.command('show', help=help_strings.HELP_CMD_SHOW)
@pass_controller
@induct_newbies
def show(controller):
    """Display latest saved, or ongoing Fact."""
    echo_ongoing_or_ended(controller)


# ***
# *** [CREATE-FACT] Commands.
# ***

def generate_add_fact_command(time_hint):
    def _generate_add_fact_command(func):
        @cmd_options_factoid
        @cmd_options_fact_add
        @cmd_options_fact_dryable
        @pass_controller
        @induct_newbies
        @click.pass_context
        @post_processor
        def _add_fact(ctx, controller, *args, carousel, **kwargs):
            return add_fact(
                controller, *args, time_hint=time_hint, use_carousel=carousel, **kwargs
            )
        return update_wrapper(_add_fact, func)
    return _generate_add_fact_command


@run.command("on", aliases=["on:", "now", "now:"], help=help_strings.START_HELP_ON)
@generate_add_fact_command("verify_none")
def add_fact_on(controller, *args, **kwargs):
    """Start or add a fact using the `on`/`now` directive."""
    assert(False)  # Not reachable, because generate_add_fact_command.
    pass


@run.command("from", help=help_strings.START_HELP_FROM)
@generate_add_fact_command("verify_both")
def add_fact_from(controller, *args, **kwargs):
    """Add a fact using the `from ... to/until` directive."""
    assert(False)  # Not reachable, because generate_add_fact_command.
    pass


@run.command("at", aliases=["at:"], help=help_strings.START_HELP_AT)
@generate_add_fact_command("verify_start")
def add_fact_at(controller, *args, **kwargs):
    """Start or add a fact using the `at` directive."""
    assert(False)  # Not reachable, because generate_add_fact_command.
    pass


@run.command("to", aliases=["to:", "until", "until:"], help=help_strings.START_HELP_TO)
@generate_add_fact_command("verify_end")
def add_fact_to(controller, *args, **kwargs):
    """Start or add a fact using the `to`/`until` directive."""
    assert(False)  # Not reachable, because generate_add_fact_command.
    pass


@run.command("then", aliases=["then:"], help=help_strings.START_HELP_THEN)
@generate_add_fact_command("verify_then")
def add_fact_then(controller, *args, **kwargs):
    """Start or add a fact using the `then` directive."""
    assert(False)  # Not reachable, because generate_add_fact_command.
    pass


@run.command("still", aliases=["still:"], help=help_strings.START_HELP_STILL)
@generate_add_fact_command("verify_still")
def add_fact_still(controller, *args, **kwargs):
    """Start or add a fact using the `still` directive."""
    assert(False)  # Not reachable, because generate_add_fact_command.
    pass


@run.command(
    "after",
    # (lb): Is "after"/"after:" good enough?
    #       Is "next"/""next:" also useful?
    aliases=["after:", "next", "next:", ],
    help=help_strings.START_HELP_AFTER
)
@generate_add_fact_command("verify_after")
def add_fact_after(controller, *args, **kwargs):
    """Start or add a fact using the `after` directive."""
    assert(False)  # Not reachable, because generate_add_fact_command.
    pass


# ***
# *** [EDIT] Command(s).
# ***

@run.group('edit', help=help_strings.EDIT_GROUP_HELP, invoke_without_command=True)
@cmd_options_edit_item
@cmd_options_fact_nocarousel
@pass_controller
@induct_newbies
@click.pass_context
@post_processor
def edit_group(ctx, controller, *args, **kwargs):
    """Base `edit` group command run prior to any of the dob-edit commands."""
    if ctx.invoked_subcommand:
        return None

    # (lb): 2019-01-31: Default `dob edit` behavior is same as `dob edit fact -1`.
    # - Intention was to someday have `dob edit activity`, `dob edit tag`, etc.,
    #   but that feature so far not implemented, and likely to be named different,
    #   anyway. (So maybe `dob edit fact` can just be `dob edit`; for now, both!)
    return edit_fact_by_key(ctx, controller, *args, **kwargs)


# *** FACTS.

@edit_group.command('fact', help=help_strings.EDIT_FACT_HELP)
@cmd_options_edit_item
@cmd_options_fact_nocarousel
@pass_controller
@induct_newbies
@click.pass_context
@post_processor
def dob_edit_fact(ctx, controller, *args, **kwargs):
    """Inline-Edit specified Fact using preferred $EDITOR."""
    return edit_fact_by_key(ctx, controller, *args, **kwargs)


def edit_fact_by_key(ctx, controller, *args, key, no_carousel, **kwargs):
    def _edit_fact_by_key():

        if controller.client_config['carousel_centered']:
            click.clear()
            # (lb): Revisit this? A little hacky.
            # Newlines seem to nudge Carousel centered.
            # Not sure why 3 is magic number, or if always.
            click.echo()
            click.echo()
            click.echo()

        keys = assemble_keys()
        return process_edit_command(keys)

    def assemble_keys():
        keys = []
        # The 'key' click.argument is nargs=-1, so it's an iterable.
        for arg_key in key:
            keys.append(arg_key)
        # See also if user specified '-1', '-2', etc.
        for kwg_key in kwargs.keys():
            match = re.match(r'^(latest_(\d+))$', kwg_key)
            if match is not None:
                # Check whether enabled (True) or not.
                if kwargs[match.groups()[0]]:
                    to_last_index = -1 * int(match.groups()[1])
                    keys.append(to_last_index)
        # (lb): If no keys, dob will display docs, e.g.,
        #   `dob edit` same as `dob edit --help`.
        # But we could also default to last Fact, seems
        # like friendlier behavior. So
        #   `dob edit` same as `dob edit -1` (or even `dob edit fact -1`).
        if not keys:
            keys = [-1]
        return keys

    def process_edit_command(keys):
        if not keys:
            click_echo(ctx.get_help())
            edited_facts = None
        elif len(keys) > 1:
            dob_in_user_exit(_("Too many Fact keys specified! Try just one."))
        else:
            edited_facts = update.edit_fact_by_pk(
                controller,
                key=keys[0],
                use_carousel=(not no_carousel),
            )
        return edited_facts

    return _edit_fact_by_key()


# ***
# *** [EXPORT] Command.
# ***

CMD_EXPORT_OPT_FORMAT_CHOICES = ['csv', 'tsv', 'xml', 'ical']


CMD_EXPORT_OPT_FORMAT_DEFAULT = 'csv'


def cmd_export_opt_output_default(controller):
    if controller is not None:
        return '{}.{{format}}'.format(controller.client_config['export_path'])
    else:
        return _('(Dynamic)')


@run.command('export', help=help_strings.EXPORT_HELP)
@click.option(
    '-o', '--output',
    cls=OptionWithDynamicHelp,
    help=_('Path to export file.'),
    default=cmd_export_opt_output_default,
    show_default=True,
)
@click.option(
    '-f', '--format',
    type=click.Choice(CMD_EXPORT_OPT_FORMAT_CHOICES),
    help=_('Output format.'),
    default=CMD_EXPORT_OPT_FORMAT_DEFAULT,
    show_default=True,
)
@click.option('--csv', is_flag=True, help=_('Alias for `--format csv`'))
@click.option('--tsv', is_flag=True, help=_('Alias for `--format tsv`'))
@click.option('--xml', is_flag=True, help=_('Alias for `--format xml`'))
@click.option('--ical', is_flag=True, help=_('Alias for `--format ical`'))
@cmd_options_search
@cmd_options_limit_offset
@cmd_options_list_activitied
@cmd_options_list_categoried
@pass_controller
@induct_newbies
def transcode_export(
    controller, *args, output, format, **kwargs
):
    """Export all facts of within a given timewindow to a file of specified format."""
    def _transcode_export():
        activity = cmd_options.postprocess_options_list_activitied(kwargs)
        category = cmd_options.postprocess_options_list_categoried(kwargs)
        export_facts(
            controller,
            *args,
            to_format=consolidate_format_options(),
            file_out=output,
            filter_activity=activity,
            filter_category=category,
            **kwargs
        )

    def consolidate_format_options():
        chosen_fmt = format
        fmts_specified = []
        if chosen_fmt != CMD_EXPORT_OPT_FORMAT_DEFAULT:
            fmts_specified = [chosen_fmt, ]
        for switch in CMD_EXPORT_OPT_FORMAT_CHOICES:
            if kwargs[switch]:
                chosen_fmt = switch
                fmts_specified.append(switch)
            del kwargs[switch]
        if len(fmts_specified) > 1:
            dob_in_user_warning(_(
                'More than one format specified: {}'
            ).format(fmts_specified))
        return chosen_fmt

    _transcode_export()


# ***
# *** [IMPORT] Command.
# ***

@run.command('import', help=help_strings.IMPORT_HELP)
@click.argument('filename', nargs=-1, type=click.File('r'))
@click.option('-o', '--output', type=click.File('w', lazy=True),
              help=_('If specified, write to output file rather than saving'))
@click.option('-f', '--force', is_flag=True,
              help=_('Overwrite --output file if is exists'))
@click.option('-r', '--rule', '--sep', nargs=1, default='',
              help=_('With --output, split facts with a horizontal rule'))
@click.option('--backup/--no-backup', '-B', default=True, show_default=True,
              help=_('Keep plaintext backup of edited facts until committed'))
@click.option('-X', '--leave-backup', is_flag=True,
              help=_('Leave working backup file after commit'))
@cmd_options_fact_nocarousel
@cmd_options_fact_dryable
@pass_controller
@induct_newbies
@click.pass_context
@post_processor
def transcode_import(
    ctx,
    controller,
    filename,
    output,
    force,
    no_carousel,
    *args,
    **kwargs
):
    """Import from file or STDIN (pipe)."""
    file_in = must_no_more_than_one_file(filename)

    # NOTE: You can get tricky and enter Facts LIVE! E.g.,
    #
    #           dob import -
    #
    #       will open pipe from STDIN, and Dob will wait for
    #       you to type! (lb): Though I did not verify ^D EOFs.

    if output and not force and os.path.exists(output.name):
        msg = _('Outfile already exists at: {}'.format(output.name))
        click_echo(msg)
        sys.exit(1)

    return import_facts(
        controller,
        *args,
        file_in=file_in,
        file_out=output,
        use_carousel=(not no_carousel),
        **kwargs
    )


# ***
# *** [COMPLETE] Command [Bash tab completion].
# ***

# FIXME: YAS! `hidden` is from a branch at:
#          sstaszkiewicz-copperleaf:6.x-maintenance
#        Watch the PR, lest you want to remove this before publishing:
#          https://github.com/pallets/click/pull/985
#          https://github.com/pallets/click/pull/500
@run.command('complete', hidden=True, help=help_strings.COMPLETE_HELP)
@pass_controller
@induct_newbies
def complete(controller):
    """Bash tab-completion helper."""
    controller.disable_logging()
    tab_complete(controller)


# ***
# *** [MIGRATE] Commands [database transformations].
# ***

@run.group('migrate', help=help_strings.MIGRATE_GROUP_HELP, invoke_without_command=True)
@pass_controller
@click.pass_context
def migrate_group(ctx, controller):
    """Base `migrate` group command run prior to any of the dob-migrate commands."""
    if not ctx.invoked_subcommand:
        click_echo(ctx.get_help())


@migrate_group.command('control', help=help_strings.MIGRATE_CONTROL_HELP)
@pass_controller
@insist_germinated
def migrate_control(controller):
    """Mark a database as under version control."""
    migrate.control(controller)


@migrate_group.command('down', help=help_strings.MIGRATE_DOWN_HELP)
@pass_controller
@insist_germinated
def migrate_downgrade(controller):
    """Downgrade the database according to its migration version."""
    migrate.downgrade(controller)


@migrate_group.command('up', help=help_strings.MIGRATE_UP_HELP)
@pass_controller
@insist_germinated
def migrate_upgrade(controller):
    """Upgrade the database according to its migration version."""
    migrate.upgrade(controller)


@migrate_group.command('version', help=help_strings.MIGRATE_VERSION_HELP)
@pass_controller
@insist_germinated
def migrate_version(controller):
    """Show migration information about the database."""
    migrate.version(controller)


# 2018-07-15 14:00ish: To loaded: 0.440 secs.
# After adding lazy-loading:
# 2018-07-15 18:06:    To loaded: 0.060 secs.
# 2018-07-15 18:06:    To run:    0.329 secs.
# About ~ 0.150 is sqlalchemy, which is unavoidable?
# About ~ 0.005 is loading config.
# The other half of the time, ~ 0.145, is plugins.
profile_elapsed('To dob: loaded')

