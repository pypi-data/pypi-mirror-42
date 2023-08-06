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

from gettext import gettext as _

from . import generate_usage_table
from ..cmd_common import error_exit_no_results, hydrate_category

__all__ = ('usage_activities', )


def usage_activities(
    controller,
    filter_category='',
    table_type='friendly',
    truncate=False,
    **kwargs
):
    """
    List all activities. Provide optional filtering by name.

    Args:
        search_term (str): String to match ``Activity.name`` against.

    Returns:
        None: If success.
    """
    category = hydrate_category(controller, filter_category)
    results = controller.activities.get_all_by_usage(
        category=category, **kwargs
    )

    if not results:
        error_exit_no_results(_('activities'))

    def name_fmttr(activity):
        if activity.category:
            category_name = activity.category.name
        else:
            category_name = ''
        actegory = '{}@{}'.format(activity.name, category_name)
        return actegory

    generate_usage_table(
        results,
        name_fmttr=name_fmttr,
        table_type=table_type,
        truncate=truncate,
    )

