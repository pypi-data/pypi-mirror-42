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

"""Hamter CLI Nonbusiness Helper modules."""

from __future__ import absolute_import, unicode_literals

import sys

from gettext import gettext as _

import click
from nark.helpers.colored import attr, bg, coloring, colorize, fg

__all__ = (
    'conflict_prefix',
    'dob_in_user_exit',
    'dob_in_user_warning',
    'echo_fact',
    'highlight_value',
    'prepare_log_msg',
)


def click_echo(*args, **kwargs):
    if coloring():
        kwargs['color'] = True
    click.echo(*args, **kwargs)


def dob_in_user_exit(msg):
    # (lb): I made two similar error-and-exit funcs. See also: barf_and_exit.
    dob_in_user_warning(msg)
    sys.exit(1)


def dob_in_user_warning(msg):
    click.echo(colorize(msg, 'red_3b'), err=True)


def echo_fact(fact):
    click.echo('{}Dry run! New fact{}:\n '.format(
        attr('underlined'),
        attr('reset'),
    ))
    click.echo('{}{}{}{}'.format(
        fg('steel_blue_1b'),
        attr('bold'),
        fact.friendly_str(description_sep='\n\n'),
        attr('reset'),
    ))


def highlight_value(msg):
    highlight_color = 'medium_spring_green'
    return '{}{}{}'.format(fg(highlight_color), msg, attr('reset'))


# ***

def prepare_log_msg(fact_or_dict, msg_content):
    def _prepare_log_msg():
        try:
            line_num = fact_or_dict['line_num']
            line_raw = fact_or_dict['line_raw']
        except KeyError:
            line_num = fact_or_dict['parsed_source.line_num']
            line_raw = fact_or_dict['parsed_source.line_raw']
        except TypeError:
            line_num = fact_or_dict.parsed_source.line_num
            line_raw = fact_or_dict.parsed_source.line_raw
        line_num = line_num or 0
        line_raw = line_raw or ''
        # NOTE: Using colors overrides logger's coloring, which is great!
        return _(
            '{}{}{}: {}{}: {}{} / {}{}{}\n\n{}: {}“{}”{}\n\n{}: {}{}{}'
            .format(
                attr('bold'),
                conflict_prefix(_('Problem')),
                attr('reset'),

                fg('dodger_blue_1'),
                _('On line'),
                line_num,
                attr('reset'),

                attr('underlined'),
                msg_content,
                attr('reset'),

                conflict_prefix(_('  Typed')),
                fg('hot_pink_2'),
                line_raw.strip(),
                attr('reset'),

                conflict_prefix(_(' Parsed')),
                fg('grey_78'),
                fact_or_dict,
                attr('reset'),
            )
        )

    return _prepare_log_msg()


# ***

def conflict_prefix(prefix):
    return (
        '{}{}{}'
        .format(
            bg('medium_violet_red'),
            prefix,
            attr('reset'),
        )
    )


# ***

def integer_range_groupify(integers):
    from itertools import groupby
    from operator import itemgetter

    def _integer_range_groupify():
        srtd = sorted(map(int, integers))
        return assemble_groups(srtd)

    def range_key_recursive(srtd, ix):
        if ix[0] == 0:
            # Very first item, so always start of group.
            return ix[1]
        prev_idx = ix[0] - 1
        prev_val = int(srtd[prev_idx])
        if ix[1] == prev_val + 1:
            # Previous item value is 1 before this one, so walk backwards.
            return range_key_recursive(srtd, (prev_idx, prev_val,))
        return ix[1]

    def range_key(srtd, ix):
        key = range_key_recursive(srtd, ix)
        # print('ix:', ix, 'key:', key)
        return key

    def assemble_groups(srtd):
        grouped = []
        for key, grp in groupby(enumerate(srtd), lambda ix: range_key(srtd, ix)):
            # print('key: {} / grp: {} {}'.format(key, grp, list(grp)))
            # print(list(map(itemgetter(1), grp)))
            grouped.append(list(map(itemgetter(1), grp)))
        return grouped

    return _integer_range_groupify()

