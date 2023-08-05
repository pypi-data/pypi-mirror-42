# Copyright (C) 2017-2018 CS-SI. All Rights Reserved.
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
import croniter
import datetime
import gevent

from prewikka.compat.gevent import fix_ssl
from prewikka.utils import timeutil
from prewikka import database, error, hookmanager, log, registrar, usergroup, utils


fix_ssl()

logger = log.getLogger(__name__)


DEFAULT_SCHEDULE = collections.OrderedDict((("0 * * * *", N_("Hourly")),
                                            ("0 0 * * *", N_("Daily")),
                                            ("0 0 * * 1", N_("Weekly")),
                                            ("0 0 1 * *", N_("Monthly")),
                                            ("0 0 1 1 *", N_("Yearly")),
                                            ("custom", N_("Custom")),
                                            ("disabled", N_("Disabled"))))

_SCHEDULE_PARAMS = dict((("0 * * * *", "hour"),
                         ("0 0 * * *", "day"),
                         ("0 0 * * 1", "week"),
                         ("0 0 1 * *", "month"),
                         ("0 0 1 1 *", "year")))


class CronJob(object):
    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __init__(self, id, name, schedule, func, base, runcnt, ext_type=None, ext_id=None, user=None, error=None, enabled=True):
        self.id = id
        self.name = name
        self.user = user
        self.schedule = schedule
        self.callback = func
        self.error = error
        self.ext_type = ext_type
        self.ext_id = ext_id
        self.enabled = enabled
        self.base = base
        self.runcnt = runcnt

        self._running = False
        self._timedelta = self._prev_schedule = self._next_schedule = None

    def _timeinit_once(self):
        if self._timedelta:
            return

        # Interpret the cronjob configuration as local time
        c = croniter.croniter(self.schedule, self.base.astimezone(utils.timeutil.tzlocal()))

        self._next_schedule = c.get_next(datetime.datetime)
        self._prev_schedule = c.get_prev(datetime.datetime)
        self._timedelta = self._next_schedule - self._prev_schedule

    @property
    def timedelta(self):
        self._timeinit_once()
        return self._timedelta

    @property
    def prev_schedule(self):
        self._timeinit_once()
        return self._prev_schedule

    @property
    def next_schedule(self):
        self._timeinit_once()
        return self._next_schedule

    def _run(self):
        self._running = True

        # setup the environment
        env.request.init(None)
        env.request.user = self.user

        if self.user:
            self.user.set_locale()

        err = None
        try:
            if self.callback:
                self.callback(self)
            else:
                raise self.error
        except Exception as err:
            logger.exception("[%d/%s]: cronjob failed: %s", self.id, self.name, err)
            err = utils.json.dumps(error.PrewikkaError(err, N_("Scheduled job execution failed")))

        self.runcnt += 1
        self._running = False
        self.base = timeutil.utcnow()
        env.db.query("UPDATE Prewikka_Crontab SET base=%s, runcnt=runcnt+1, error=%s WHERE id=%d", self.base, err, self.id)

    def run(self, now):
        if not(self.next_schedule) or now < self.next_schedule or self._running:
            return

        env.log.info("[%d/%s]: RUNNING JOB schedule=%s callback=%s" % (self.id, self.name, self.schedule, self.callback))
        gevent.spawn(self._run)


class Crontab(object):
    _REFRESH = datetime.timedelta(minutes=1)

    def _reinit(self):
        self._plugin_callback = {}

    def __init__(self):
        self._reinit()
        self._joblist = set()
        hookmanager.register("HOOK_PLUGINS_RELOAD", self._reinit)
        hookmanager.register("HOOK_USER_DELETE", lambda user: self.delete(user=user))

    def _make_job(self, res):
        err = func = None
        id, name, userid, schedule, ext_type, ext_id, base, runcnt, enabled, error_s = res

        func = self._plugin_callback.get(ext_type)
        if not func:
            err = error.PrewikkaUserError(N_("Invalid job extension"), N_("Scheduled job with invalid extension type '%s'") % (ext_type))

        if error_s and not(err):
            err = utils.json.loads(error_s)

        if ext_id:
            ext_id = int(ext_id)

        if base:
            base = env.db.parse_datetime(base)

        user = None
        if userid:
            user = usergroup.User(userid=userid)

        return CronJob(int(id), name, schedule, func, base, int(runcnt), ext_type=ext_type, ext_id=ext_id, user=user, error=err, enabled=bool(int(enabled)))

    @database.use_lock("Prewikka_Crontab")
    def _init_system_job(self, ext_type, name, schedule, enabled, method):
        self._plugin_callback[ext_type] = method

        res = env.db.query("SELECT 1 FROM Prewikka_Crontab WHERE ext_type=%s AND userid IS NULL", ext_type)
        if not res:
            self.add(name, schedule, ext_type=ext_type, enabled=enabled)

    def _update_joblist(self):
        mainlist = set(self.list(enabled=True))

        # Suppress jobs that were removed from the main list
        self._joblist -= self._joblist.difference(mainlist)

        # Add jobs that were added to the main list
        self._joblist |= mainlist.difference(self._joblist)

        return self._joblist

    def _run_jobs(self):
        first = now = timeutil.utcnow()

        for job in self._update_joblist():
            job.run(now)
            now = timeutil.utcnow()

        return (self._REFRESH - (now - first)).total_seconds()

    def run(self):
        while True:
            next = self._run_jobs()
            if next > 0:
                gevent.sleep(next)

    def list(self, **kwargs):
        qs = env.db.kwargs2query(kwargs, prefix=" WHERE ")
        for res in env.db.query("SELECT id, name, userid, schedule, ext_type, ext_id, base, runcnt, enabled, error FROM Prewikka_Crontab%s" % qs):
            yield self._make_job(res)

    def get(self, id):
        res = env.db.query("SELECT id, name, userid, schedule, ext_type, ext_id, base, runcnt, enabled, error FROM Prewikka_Crontab WHERE id=%d", id)
        if not res:
            raise error.PrewikkaError(N_('Invalid CronJob'), N_('CronJob with id=%d cannot be found in database', id))

        return self._make_job(res[0])

    def delete(self, **kwargs):
        user = kwargs.pop("user", None)
        if user:
            kwargs["userid"] = getattr(user, "id", user)  # Can be None / NotNone

        qs = env.db.kwargs2query(kwargs, " WHERE ")
        env.db.query("DELETE FROM Prewikka_Crontab%s" % qs)

    def update(self, id, **kwargs):
        accept = {
            "name": None,
            "schedule": None,
            "user": lambda x: ("userid", getattr(x, "id", None)),
            "ext_type": None,
            "ext_id": None,
            "enabled": lambda x: ("enabled", int(x))
        }

        cols = []
        data = []
        for field, value in kwargs.items():
            dec = accept[field]
            if dec:
                field, value = dec(value)

            if id:
                data.append("%s = %s" % (field, env.db.escape(value)))
            else:
                cols.append(field)
                data.append(value)

        if not id:
            env.db.query("INSERT INTO Prewikka_Crontab (%s) VALUES %%s" % (", ".join(cols + ["base"])), data + [timeutil.utcnow()])
            return env.db.getLastInsertIdent()
        else:
            env.db.query("UPDATE Prewikka_Crontab SET %s WHERE id IN %%s" % (", ".join(data)), env.db._mklist(id))
            return id

        # FIXME: there is an issue with upsert() when using PostgreSQL CTE (serial problem + cast problem)
        # id = int(env.db.upsert("Prewikka_Crontab", cols, [data], pkey=("id",), returning=["id"])[0])
        # return id

    def add(self, name, schedule, user=None, ext_type=None, ext_id=None, enabled=True):
        return self.update(None, name=name, schedule=schedule, user=user, ext_type=ext_type, ext_id=ext_id, enabled=enabled)

    def update_from_parameters(self, id, parameters=None, delete_disabled=False, **kwargs):
        if parameters is None:
            parameters = env.request.parameters

        schedule = parameters.get("quick-schedule")
        if schedule != "disabled":
            kwargs["schedule"] = schedule
            try:
                croniter.croniter(schedule)
            except Exception:
                raise error.PrewikkaUserError(N_("Invalid schedule"), N_("The specified job schedule is invalid"))

        elif delete_disabled:
            return crontab.delete(id=id, **kwargs)

        crontab.update(id, name=parameters["name"], enabled=int(schedule != "disabled"), **kwargs)

    def schedule(self, ext_type, name, schedule, _regfunc=None, enabled=True):
        if _regfunc:
            self._init_system_job(ext_type, name, schedule, enabled, _regfunc)
        else:
            return registrar.DelayedRegistrar.make_decorator("crontab", self.schedule, ext_type, name, schedule, enabled=enabled)

    def setup(self, ext_type, _regfunc=None):
        if _regfunc:
            assert not(ext_type in self._plugin_callback)
            self._plugin_callback[ext_type] = _regfunc
        else:
            return registrar.DelayedRegistrar.make_decorator("crontab", self.setup, ext_type)


def format_schedule(x):
    val = DEFAULT_SCHEDULE.get(x)
    if val:
        return _(val)
    else:
        return _("Custom (%s)") % x


def schedule_to_menuparams(x):
    params = {}

    val = _SCHEDULE_PARAMS.get(x)
    if val:
        params["timeline_mode"] = "relative"
        params["timeline_value"] = 1
        params["timeline_unit"] = val
    else:
        now = timeutil.now()
        params["timeline_mode"] = "custom"
        params["timeline_start"] = timeutil.get_timestamp_from_datetime(croniter.croniter(x, now).get_prev(datetime.datetime))
        params["timeline_end"] = timeutil.get_timestamp_from_datetime(now)

    return params


crontab = Crontab()

list = crontab.list
run = crontab.run
get = crontab.get
add = crontab.add
update = crontab.update
delete = crontab.delete
schedule = crontab.schedule
setup = crontab.setup
update_from_parameters = crontab.update_from_parameters
