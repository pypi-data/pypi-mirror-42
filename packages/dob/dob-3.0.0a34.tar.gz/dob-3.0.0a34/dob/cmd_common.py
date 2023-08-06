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

from __future__ import absolute_import, unicode_literals

import sys
from functools import update_wrapper

from gettext import gettext as _

import click
from nark.helpers.colored import attr, colorize, fg

from . import __arg0name__, migrate
from .helpers import ascii_art, click_echo, dob_in_user_exit

__all__ = (
    'barf_and_exit',
    'echo_block_header',
    'error_exit_no_results',
    'fact_block_header',
    'hydrate_activity',
    'hydrate_category',
    'induct_newbies',
    'must_no_more_than_one_file',
    'post_processor',
    # Private:
    #  'backend_integrity',
    #  'insist_germinated',
)


def backend_integrity(func):
    """
    Verify that data in the database is integrit.

    (lb): I wonder if the backend should enforce this better.
    In any case, telling the user at the CLI level is better
    than not telling the user at all, I suppose.
    """

    def wrapper(controller, *args, **kwargs):
        version_must_be_latest(controller)
        time_must_be_gapless(controller)
        func(controller, *args, **kwargs)

    # ***

    def version_must_be_latest(controller):
        db_version = migrate.version(
            controller, silent_check=True, must=True,
        )
        latest_version = migrate.latest_version(
            controller, silent_check=True, must=True,
        )
        if db_version != latest_version:
            assert db_version < latest_version
            msg = _(
                'Expected database to be same version as latest migration.'
                ' {} != {}'
                '\nTrying running `{} migrate up`'
            ).format(db_version, latest_version, __arg0name__)
            dob_in_user_exit(msg)

    # ***

    def time_must_be_gapless(controller):
        endless_facts = controller.facts.endless()
        barf_on_endless_facts(endless_facts)

    def barf_on_endless_facts(endless_facts):
        # There can be only 1. Or none.
        if not endless_facts or len(endless_facts) == 1:
            return

        for fact in endless_facts:
            # FIXME/2018-05-18: (lb): Make this prettier.
            echo_block_header(_('Endless Fact Found!'))
            click_echo()
            click_echo(fact.friendly_diff(fact))
            click_echo()
        msg = _(
            'Found saved fact(s) without start time and/or end time.'
            '\nSee list of offending Facts above.'
            # MAYBE/2018-05-23 17:05: (lb): We could offer an easy way out, e.g.,
            #   '\n\nTry, e.g.,\n\n  {} edit {} --end now'.format(__arg0name__, ...)
        )
        dob_in_user_exit(msg)

    # ***

    return wrapper


def insist_germinated(func):
    """
    """

    def wrapper(controller, *args, **kwargs):
        controller.insist_germinated()
        func(controller, *args, **kwargs)

    return wrapper


def induct_newbies(func):
    """
    """
    @insist_germinated
    @backend_integrity
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return update_wrapper(wrapper, func)


# ***

def post_processor(func):
    """
    """

    def wrapper(ctx, controller, *args, **kwargs):
        # Ensure that plugins are loaded, which may have functions
        # decorated with @Controller.post_processor.
        ctx.parent.command.ensure_plugged_in()
        facts = func(ctx, controller, *args, **kwargs)
        controller.post_process(controller, facts, show_plugin_error=None)

    return update_wrapper(wrapper, func)


# ***

def barf_and_exit(msg, crude=True):
    # (lb): I made two similar error-and-exit funcs. See also: dob_in_user_exit.
    if crude:
        click_echo()
        click_echo(ascii_art.lifeless().rstrip())
        click_echo(ascii_art.infection_notice().rstrip())
        # click.pause(info='')
    click_echo()
    click_echo(colorize(msg, 'red'))
    sys.exit(1)


# ***

def echo_block_header(title, **kwargs):
    click_echo()
    click_echo(fact_block_header(title, **kwargs))


def fact_block_header(title, sep='━', full_width=False):
    """"""
    def _fact_block_header():
        header = []
        append_highlighted(header, title)
        append_highlighted(header, hr_rule())
        return '\n'.join(header)

    def append_highlighted(header, text):
        highlight_col = 'red_1'
        header.append('{}{}{}'.format(
            fg(highlight_col),
            text,
            attr('reset'),
        ))

    def hr_rule():
        if not full_width:
            horiz_rule = sep * len(title)
        else:
            # NOTE: When piping (i.e., no tty), width defaults to 80.
            term_width = click.get_terminal_size()[0]
            horiz_rule = '─' * term_width
        return horiz_rule

    return _fact_block_header()


# ***

def hydrate_activity(controller, activity_name):
    """Fetch an activity from the back end."""
    activity = False
    if activity_name:
        # FIXME: (lb): This raises KeyError if no exact match found.
        #        We should at least gracefully exit,
        #        if not do a fuzzy search.
        result = controller.activities.get_by_name(activity_name)
        activity = result if result else False
    return activity


# ***

def hydrate_category(controller, category_name):
    """Fetch a category from the backend."""
    category = False
    if category_name:
        # FIXME: (lb): This raises KeyError if no exact match found.
        #        We should at least gracefully exit,
        #        if not do a fuzzy search.
        result = controller.categories.get_by_name(category_name)
        category = result if result else False
    return category


# ***

def must_no_more_than_one_file(filename):
    # Because nargs=-1, the user could specify many files! E.g.,
    #
    #   dob import file1 file2
    #
    # Also, click supports the magic STDIN identifier, `-`, e.g.,
    #
    #   dob import -
    #
    # will read from STDIN.
    #
    # (And `dob import - <file>` will open 2 streams!)
    if len(filename) > 1:
        msg = _('Please specify only one input, file or STDIN!')
        dob_in_user_exit(msg)
    elif filename:
        return filename[0]
    else:
        return None


# ***

def error_exit_no_results(item_type):
    # MAYBE: (lb): Should we exit on error?
    #              Print message but not error?
    #              Print empty table?
    #              Only print if no facts whatsoever,
    #                as opposed to no facts matching query?
    #        I'd say either print message on stderr and exit, or
    #        print empty table on stdout, so that a tool in the
    #        pipeline would only see empty string or empty table
    #        on stdin, and never a message, so that post-processing
    #        won't die on unexpected error message string.
    msg = _('No {} were found for the specified query.').format(item_type)
    # (lb): I sorta like the message, not table, on no results,
    # because you can tell quicker that nothing was found. I.e.,
    # when I see an empty tell, I spend a nanosecond scanning it
    # for rows, because when I see table headers, I expect to see
    # table rows! So I'm kinda liking printing a message, not table.
    dob_in_user_exit(msg)

