# Copyright (C) 2015-2018 CS-SI. All Rights Reserved.
# Author: Yoann Vandoorselaere <yoannv@gmail.com>
#
# This file is part of the Prewikka program.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import absolute_import, division, print_function, unicode_literals

import collections

from prewikka import dataprovider, hookmanager, mainmenu, usergroup, utils
from prewikka.dataprovider import Criterion
from prewikka.renderer import RendererItem


class Query(object):
    def __init__(self, **kwargs):
        keys = ["datatype", "path", "aggregate", "limit", "criteria"]
        datatype, path, aggregate, limit, criteria = [kwargs.get(i) for i in keys]

        if isinstance(path, list):
            self.paths = path
        else:
            self.paths = [path] if path else []

        self.datatype = datatype
        self.aggregation = aggregate or "count(1)"
        self.limit = int(limit or env.request.parameters["limit"])
        self.criteria = criteria or Criterion()


class GenericChart(object):
    default_link_mode = "immediate"

    def __init__(self, chart_type, title, query, **options):
        self.chart_type = chart_type
        self.title = title
        self.query = query
        self.options = options
        self._set_menu()

        self._link_mode = options.pop("linkmode", self.default_link_mode)
        self._link_view = options.pop("linkview", None)
        self._link_params = options.pop("linkparams", {})

    def _make_link(self, force_default=False, **params):
        if self._link_mode is None:
            return None

        elif self._link_mode == "immediate":
            linkview = self._link_view or self._default_view

        elif self._link_mode == "zoom":
            linkview = (self._link_view or env.request.view) if not(force_default) else self._default_view

        if not linkview:
            return None

        if self._link_view and self._link_params:
            params.pop("criteria")  # Since the calling view provides its own parameters, we should not pass criteria
            params.update(self._link_params)

        return linkview.make_url(**params)

    def _set_menu(self):
        period = self.options.get("period")

        if not period:
            self._menu = env.request.menu
        else:
            parameters = {
                "mode": "relative",
                "value": 1,
                "unit": "month"
            }
            parameters.update(period)
            self._menu = mainmenu.TimePeriod(dict(("timeline_%s" % k, v) for k, v in parameters.items()))

    def _prepare_query(self, query):
        all_paths = ["%s/order_desc" % query.aggregation]
        for path in query.paths:
            all_paths += ["%s/group_by" % path]

        if not query.datatype:
            query.datatype = env.dataprovider.guess_datatype(all_paths, query.criteria, default=None)

        self._default_view = env.viewmanager.get(datatype=query.datatype, keywords=["listing"])
        if self._default_view:
            self._default_view = self._default_view[-1]

        list(hookmanager.trigger("HOOK_CHART_PREPARE", query, self.options))
        all_criteria = self._menu.get_criteria() & query.criteria

        return all_paths, all_criteria

    def _query(self, paths, criteria, **kwargs):
        try:
            return env.dataprovider.query(paths, criteria, **kwargs)
        except (usergroup.PermissionDeniedError, dataprovider.NoBackendError):
            return []

    def get_data(self):
        pass

    def render(self):
        self.data = self.get_data()
        return env.renderer.render(self.chart_type, self.data, query=self.query, **self.options)


class DiagramChart(GenericChart):
    TYPES = ["pie", "bar", "radar", "polar", "doughnut", "line", "table"]

    def _get_series(self, query):
        for value, label, crit in self._get_categories(query):
            link = self._make_link(criteria=crit & query.criteria, **self._menu.get_parameters())
            yield RendererItem(value, label, link)

    def _get_categories(self, query):
        all_paths, all_criteria = self._prepare_query(query)

        for row in self._query(all_paths, all_criteria, limit=query.limit, type=query.datatype):
            value = row[0]
            label = ", ".join((text_type(i) or _("n/a") for i in row[1:]))
            crit = reduce(lambda x, y: x & y, (Criterion(path, '=', row[i + 1])
                                               for i, path in enumerate(query.paths)))
            yield value, label, crit

    def get_data(self):
        if len(self.query) == 1:
            return [list(self._get_series(self.query[0]))]

        data = []
        subquery = self.query[1]
        base_criteria = subquery.criteria
        self.options["subtitle"] = []
        for value, label, crit in self._get_categories(self.query[0]):
            subquery.criteria = crit & base_criteria
            subchart = DiagramChart(self.chart_type, label, [subquery], period=self.options.get("period"))
            data.append(subchart.get_data()[0])
            self.options["subtitle"].append(label)

        return data


class ChronologyChart(GenericChart):
    TYPES = ["timeline", "timearea", "timebar"]
    default_link_mode = "zoom"

    def _get_series(self, query, selection, date_precision):
        selection_index = len(query.paths) + 1
        all_paths, all_criteria = self._prepare_query(query)

        crit = Criterion()
        if query.limit > 0 and query.paths:
            for values in self._query(all_paths, all_criteria, limit=query.limit, type=query.datatype):
                crit |= reduce(lambda x, y: x & y, (Criterion(query.paths[i], "=", value) for i, value in enumerate(values[1:])))

        res = []
        if query.limit != 0:
            res = self._query(all_paths + selection, all_criteria + crit, type=query.datatype)

        out = {}
        for i in res:
            label = ", ".join((text_type(j) or _("n/a") for j in i[1:selection_index])) or self.title
            tval = tuple((int(x) for x in i[selection_index:]))
            out.setdefault(label, {})[tval[:date_precision]] = i[0]

        return out

    def _ctime_as_timezone(self):
        if env.request.user.timezone.zone == "UTC":
            return "{backend}.{time_field}"
        else:
            return "timezone({backend}.{time_field}, '%s')" % (env.request.user.timezone.zone)

    def _gen_selection(self, time_unit):
        selection = []
        for idx, unit in enumerate(range(mainmenu.TimeUnit(time_unit) + 1)):
            selection += ["%s:%s/order_desc,group_by" % (self._ctime_as_timezone(), mainmenu.TimeUnit(unit).dbunit)]

        return idx + 1, selection

    def get_data(self):
        data, date_precision, base_parameters = self._prepare_timeline()
        step = self._menu.get_step(100)
        can_zoom = mainmenu.TimeUnit(step.unit) > mainmenu.TimeUnit("minute")

        out = collections.OrderedDict()
        links = []
        legends = []

        start = self._menu.start
        while start < self._menu.end:
            next = utils.timeutil.truncate(start + step.timedelta, step.unit)
            next = min(next, self._menu.end)

            if base_parameters:
                base_parameters["timeline_start"] = self._menu.mktime_param(start)
                base_parameters["timeline_end"] = self._menu.mktime_param(next)
                if next != self._menu.end:
                    base_parameters["timeline_end"] -= 1

                ret = self._make_link(force_default=not(can_zoom), criteria=self.query[0].criteria, **base_parameters)
                if ret:
                    links.append(ret)

            key = start.timetuple()[:date_precision]
            for i in data.keys():
                out.setdefault(i, []).append(data[i].get(key, 0))

            legends.append(start.strftime(step.unit_format))
            start = next

        self.options["xlegend"] = legends

        return [RendererItem(labels=name, values=value, links=links) for name, value in out.items()]

    def _prepare_timeline(self):
        step = self._menu.get_step(100)
        date_precision, selection = self._gen_selection(step.unit)

        if len(self.query) == 1:
            data = self._get_series(self.query[0], selection, date_precision)
        else:
            data = collections.OrderedDict()
            for query in self.query:
                series = self._get_series(query, selection, date_precision).get(self.title, {})
                legend = query.aggregation.replace("(1)", "(%s)" % query.datatype)
                data[legend] = series

        if self.options.get("period"):
            # Do not allow zooming when the time period is defined
            base_parameters = None
        else:
            base_parameters = self._menu.get_parameters()
            base_parameters["timeline_mode"] = "custom"

        return (data, date_precision, base_parameters)
