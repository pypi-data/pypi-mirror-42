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
"""Zone Details End Time Code (for easier diff-meld against Start Time Code)"""

from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from ..helpers.exceptions import catch_action_exception

__all__ = (
    'ZoneDetails_TimeEnd',
)


class ZoneDetails_TimeEnd(object):
    """"""

    def add_header_end_time(self):
        self.widgets_end = self.add_header_parts(
            'end', 'end_fmt_local_nowwed', editable=True,
        )

    def refresh_time_end(self):
        self.refresh_val_widgets(self.widgets_end)

    # ***

    @catch_action_exception
    def edit_time_end(self, event=None, focus=True):
        if focus:
            edit_fact = self.zone_manager.facts_diff.edit_fact
            # Use or-now, unlike start time, because there's on one possible
            # open-ended fact (without an end time) and it'd be the latest fact.
            end_fmt_local_or_now = edit_fact.end_fmt_local_or_now
            self.widgets_end.orig_val = end_fmt_local_or_now
            self.widgets_end.text_area.text = end_fmt_local_or_now
            self.edit_time_focus(self.widgets_end)
            return True
        else:
            return self.edit_time_leave(self.widgets_end)

    # ***

    def apply_edit_time_removed_end(self, edit_fact):
        if edit_fact.end is None:
            # Already cleared; nothing changed.
            return True
        if not self.carousel.edits_manager.conjoined.is_final_fact(edit_fact):
            self.widgets_end.text_area.text = edit_fact.end_fmt_local_or_now
            return False
        else:
            edit_fact.end = None
            self.carousel.controller.affirm(False)
            return True

    # ***

    def apply_edit_time_end(self, edit_fact, edit_time):
        if edit_fact.end == edit_time:
            # Nothing changed.
            return False
        edited_facts = [edit_fact]
        edits_manager = self.carousel.edits_manager
        # Make undoable.
        was_fact = edit_fact.copy()
        undoable_facts = [was_fact]
        # Prohibit completely shadowing other facts' time windows, but allow
        # changing one fact's times to shorten the times of prev or next fact.
        edit_next = edits_manager.editable_fact_next(edit_fact)
        best_time = edit_time
        if best_time and edit_next and edit_next.end and (best_time > edit_next.end):
            # MAGIC_NUMBER: Adjust adjacent fact's time to be no less that 1 minute.
            #   MAYBE: Resurrect fact_min_delta and use in this context?
            best_time = edit_next.end - timedelta(minutes=1)
            if edit_next and edit_next.start and (best_time < edit_next.start):
                best_time = edit_next.start
        edit_fact.end = best_time
        self.carousel.controller.affirm(edit_time is not None)
        # If the edited time encroached on the neighbor, or if the neighbor
        # is an unedited gap fact, edit thy neighbor.
        if edit_next:
            if (
                (edit_next.start and (edit_fact.end > edit_next.start))
                or ('interval-gap' in edit_next.dirty_reasons)
            ):
                undoable_facts.append(edit_next.copy())
                edit_next.start = edit_fact.end
                edited_facts.append(edit_next)
            if edit_fact.end == edit_next.start:
                edit_fact.next_fact = edit_next
                edit_next.prev_fact = edit_fact
            else:
                edit_fact.next_fact = None
                edit_next.prev_fact = None
        else:
            edit_fact.next_fact = None
        edits_manager.add_undoable(undoable_facts, what='header-edit')
        edits_manager.apply_edits(*edited_facts)
        return True

