# SAY POOP: DON'T EDIT THIS LIBRARY!

#
# Copyright 2014, Martin Owens <doctormo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Ideas from gnome-schedule: Philip Van Hoof, Gaute Hope, Kristof Vansant
#
# REQUEST: Please do NOT simply copy and paste this code into your own
#          projects. Please package this module for your distribution and
#          use as a direct dependancy.
#
"""
from crontab import CronTab
import sys

# Create a new non-installed crontab
cron = CronTab(tab='')
job  = cron.new(command='/usr/bin/echo')

job.minute.during(5,50).every(5)
job.hour.every(4)

job.dow.on('SUN')
job.month.during('APR', 'JUN')
job.month.also.during('OCT', 'DEC')

job.every(2).days()
job.setall(1, 12, None, None, None)

job2 = cron.new(command='/foo/bar', comment='SomeID')
job2.every_reboot()

jobs = list(cron.find_command('bar'))
job3 = jobs[0]
job3.clear()
job3.minute.every(1)

sys.stdout.write(str(cron.render()))

job3.enable(False)

for job4 in cron.find_command('echo'):
    sys.stdout.write(job4)

for job5 in cron.find_comment('SomeID'):
    sys.stdout.write(job5)

for job6 in cron:
    sys.stdout.write(job6)

for job7 in cron:
    job7.every(3).hours()
    sys.stdout.write(job7)
    job7.every().dow()

cron.remove_all(command='/foo/bar')
cron.remove_all(comment='This command')
cron.remove_all(time='* * * * *')
cron.remove_all()

output = cron.render()

cron.write()

cron.write(filename='/tmp/output.txt')

#cron.write_to_user(user=True)

#cron.write_to_user(user='root')

# Croniter Extentions allow you to ask for the scheduled job times, make
# sure you have croniter installed, it's not a hard dependancy.

job3.schedule().get_next()
job3.schedule().get_prev()

"""

import os
import re
import sys

import codecs
import tempfile
import subprocess as sp

from datetime import date, datetime

__pkgname__ = 'python-crontab'
__version__ = '1.9.3'

ITEMREX = re.compile(r'^\s*([^@#\s]+)\s+([^@#\s]+)\s+([^@#\s]+)\s+([^@#\s]+)'
                     r'\s+([^@#\s]+)\s+([^#\n]*)(\s+#\s*([^\n]*)|$)')
SPECREX = re.compile(r'^\s*@(\w+)\s([^#\n]*)(\s+#\s*([^\n]*)|$)')
DEVNULL = ">/dev/null 2>&1"

WEEK_ENUM = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

MONTH_ENUM = [None, 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
              'sep', 'oct', 'nov', 'dec']

SPECIALS = {"reboot":   '@reboot',
            "hourly":   '0 * * * *',
            "daily":    '0 0 * * *',
            "weekly":   '0 0 * * 0',
            "monthly":  '0 0 1 * *',
            "yearly":   '0 0 1 1 *',
            "annually": '0 0 1 1 *',
            "midnight": '0 0 * * *'}

SPECIAL_IGNORE = ['midnight', 'annually']

S_INFO = [
    {'name': 'Minutes',      'max': 59, 'min': 0},
    {'name': 'Hours',        'max': 23, 'min': 0},
    {'name': 'Day of Month', 'max': 31, 'min': 1},
    {'name': 'Month',        'max': 12, 'min': 1, 'enum': MONTH_ENUM},
    {'name': 'Day of Week',  'max': 6,  'min': 0, 'enum': WEEK_ENUM},
]

# Detect Python3 and which OS for temperments.
import platform
PY3 = platform.python_version()[0] == '3'
WINOS = platform.system() == 'Windows'
SYSTEMV = not WINOS and os.uname()[0] in ["SunOS", "AIX", "HP-UX"]

if not WINOS:
    import pwd

CRONCMD = "/usr/bin/crontab"

if PY3:
    # pylint: disable=W0622
    unicode = str
    basestring = str


def pipeOpen(cmd, *args, **flags):
    """Runs a program and orders the arguments for compatability.

    a. keyword args are flags and always appear /before/ arguments for bsd
    """
    l = tuple(cmd.split(' '))
    for (k,v) in flags.items():
        if v is not None:
            l += len(k)==1 and ("-%s" % (k,), str(v)) or ("--%s=%s" % (k,v),)
    l += tuple(args)
    return sp.Popen(tuple(a for a in l if a), stdout=sp.PIPE, stderr=sp.PIPE)


class CronTab(object):
    """
    Crontab object which can access any time based cron using the standard.

    user    - Set the user of the crontab (default: None)
      * 'user' = Load from $username's crontab (instead of tab or tabfile)
      * None   = Don't load anything from any user crontab.
      * True   = Load from current $USER's crontab (unix only)
      * False  = This is a system crontab, each command has a username

    tab     - Use a string variable as the crontab instead of installed crontab
    tabfile - Use a file for the crontab instead of installed crontab
    log     - Filename for logfile instead of /var/log/syslog

    """
    def __init__(self, user=None, tab=None, tabfile=None, log=None):
        self.lines = None
        self.crons = None
        self.filen = None
        # Protect windows users
        self.root = not WINOS and os.getuid() == 0
        # Storing user flag / username
        self._user = user
        # Load string or filename as inital crontab
        self.intab = tab
        self.read(tabfile)
        self._log = log

    @property
    def log(self):
        """Returns the CronLog object for this tab (user or root tab only)"""
        from cronlog import CronLog
        if self._log is None or isinstance(self._log, basestring):
            self._log = CronLog(self._log, user=self.user or 'root')
        return self._log

    @property
    def user(self):
        if self._user is True and pwd:
            return pwd.getpwuid(os.getuid())[0]
        return self._user

    @property
    def user_opt(self):
        # Fedora and Mac require the current user to not specify
        # But Ubuntu/Debian doesn't care. Be careful here.
        if self._user and self._user is not True:
            return {'u': self._user}
        return {}

    def read(self, filename=None):
        """
        Read in the crontab from the system into the object, called
        automatically when listing or using the object. use for refresh.
        """
        self.crons = []
        self.lines = []
        lines = []
        if self.intab is not None:
            lines = self.intab.split('\n')
        elif filename:
            self.filen = filename
            with codecs.open(filename, 'r', encoding='utf-8') as fhl:
                lines = fhl.readlines()
        elif self.user:
            (out, err) = pipeOpen(CRONCMD, l='', **self.user_opt).communicate()
            if err and 'no crontab for' in str(err):
                pass
            elif err:
                raise IOError("Read crontab %s: %s" % (self.user, err))
            lines = out.decode('utf-8').split("\n")
        for line in lines:
            cron = CronItem(line, cron=self)
            if cron.is_valid():
                self.crons.append(cron)
                self.lines.append(cron)
            else:
                self.lines.append(line.replace('\n', ''))

    def write(self, filename=None):
        """Write the crontab to it's source or a given filename."""
        if filename:
            self.filen = filename

        # Add to either the crontab or the internal tab.
        if self.intab is not None:
            self.intab = self.render()
            # And that's it if we never saved to a file
            if not self.filen:
                return

        if self.filen:
            fileh = open(self.filen, 'wb')
        else:
            filed, path = tempfile.mkstemp()
            fileh = os.fdopen(filed, 'wb')

        fileh.write(self.render().encode('utf-8'))
        fileh.close()

        if not self.filen:
            # Add the entire crontab back to the user crontab
            pipeOpen(CRONCMD, path, **self.user_opt).wait()
            os.unlink(path)

    def write_to_user(self, user=None):
        """Write the crontab to a user (or root) instead of a file."""
        self.filen = None
        self.intab = None
        if user is not None:
            self._user = user
        self.write()

    def render(self):
        """Render this crontab as it would be in the crontab."""
        crons = []
        for cron in self.lines:
            crons.append(unicode(cron))
        result = u'\n'.join(crons)
        if result and result[-1] not in (u'\n', u'\r'):
            result += u'\n'
        return result

    def new(self, command='', comment='', user=None):
        """
        Create a new cron with a command and comment.

        Returns the new CronItem object.
        """
        if not user and self.user is False:
            raise ValueError("User is required for system crontabs.")
        item = CronItem(command=command, comment=comment, user=user, cron=self)
        self.crons.append(item)
        self.lines.append(item)
        return item

    def find_command(self, command):
        """Return an iter of jobs matching any part of the command."""
        for job in self.crons:
            if command in job.command:
                yield job

    def find_comment(self, comment):
        """Return an iter of jobs that match the comment field exactly."""
        for job in self.crons:
            if job.comment == comment:
                yield job

    def find_time(self, *args):
        """Return an iter of jobs that match this time pattern"""
        for job in self.crons:
            if job.slices == CronSlices(*args):
                yield job

    @property
    def commands(self):
        """Return a generator of all unqiue commands used in this crontab"""
        returned = []
        for cron in self.crons:
            if cron.command not in returned:
                yield cron.command
                returned.append(cron.command)

    @property
    def comments(self):
        """Return a generator of all unique comments/Id used in this crontab"""
        returned = []
        for cron in self.crons:
            if cron.comment and cron.comment not in returned:
                yield cron.comment
                returned.append(cron.comment)

    def remove_all(self, command=None, comment=None, time=None):
        """Removes all crons using the stated command OR that have the
        stated comment OR removes everything if no arguments specified."""
        if command:
            return self.remove(*self.find_command(command))
        elif comment:
            return self.remove(*self.find_comment(comment))
        elif time:
            return self.remove(*self.find_time(time))
        return self.remove(*self.crons[:])

    def remove(self, *items):
        """Remove a selected cron from the crontab."""
        result = 0
        for item in items:
            result += self._remove(item)
        return result

    def _remove(self, item):
        """Internal removal of an item"""
        # The last item often has a trailing line feed
        if self.crons[-1] == item and self.lines[-1] == '':
            self.lines.remove(self.lines[-1])
        self.crons.remove(item)
        self.lines.remove(item)
        return 1

    def __iter__(self):
        return self.crons.__iter__()

    def __getitem__(self, i):
        return self.crons[i]

    def __unicode__(self):
        return self.render()

    def __len__(self):
        return len(self.crons)

    def __str__(self):
        return self.render()


class CronItem(object):
    """
    An item which objectifies a single line of a crontab and
    May be considered to be a cron job object.
    """
    def __init__(self, line=None, command='', comment='', user=None, cron=None):
        self.cron    = cron
        self.user    = user
        self.valid   = False
        self.enabled = True
        self.special = False
        self.comment = None
        self.command = None

        self._log = None

        # Initalise five cron slices using static info.
        self.slices = CronSlices()

        self.set_comment(comment)

        if line and line.strip():
            self.parse(line.strip())
        elif command:
            self.set_command(command)
            self.valid = True

    def delete(self):
        """Delete this item and remove it from it's parent"""
        if not self.cron:
            raise UnboundLocalError("Cron item is not associated with a crontab!")
        else:
            self.cron.remove(self)

    def set_command(self, cmd):
        """Set the command and filter as needed"""
        self.command = cmd.strip()

    def set_comment(self, cmt):
        """Set the comment and don't filter"""
        self.comment = cmt

    def parse(self, line):
        """Parse a cron line string and save the info as the objects."""
        if type(line) is str and not PY3:
            line = unicode(line, 'utf-8')
        if not line or line[0] == '#':
            self.enabled = False
            line = line[1:].strip()
        self._set_parse(ITEMREX.findall(line))
        self._set_parse(SPECREX.findall(line))

    def _set_parse(self, result):
        if not result:
            return
        if self.cron.user == False:
            # Special flag to look for per-command user
            (self.user, cmd) = (result[0][-3] + ' ').split(' ', 1)
            self.set_command(cmd)
        else:
            self.set_command(result[0][-3])

        self.valid = self.setall(*result[0][:-3])
        self.comment = result[0][-1]
        self.enabled = self.enabled and self.valid

    def enable(self, enabled=True):
        """Set if this cron job is enabled or not"""
        if enabled in [True, False]:
            self.enabled = enabled
        return self.enabled

    def is_enabled(self):
        """Return true if this job is enabled (not commented out)"""
        return self.enabled

    def is_valid(self):
        """Return true if this job is valid"""
        return self.valid

    def render(self):
        """Render this set cron-job to a string"""
        if type(self.command) is str and not PY3:
            self.command = unicode(self.command, 'utf-8')
        user = ''
        if self.cron and self.cron.user is False:
            if not self.user:
                raise ValueError("Job to system-cron format, no user set!")
            user = self.user + ' '
        result = u"%s %s%s" % (str(self.slices), user, self.command)
        if self.comment:
            if type(self.comment) is str and not PY3:
                self.comment = unicode(self.comment, 'utf-8')
            result += u" # " + self.comment
        if not self.enabled:
            result = u"# " + result
        return result

    def every_reboot(self):
        """Set to every reboot instead of a time pattern: @reboot"""
        self.clear()
        return self.slices.setall('@reboot')

    def every(self, unit=1):
        """
        Replace existing time pattern with a single unit, setting all lower
        units to first value in valid range.

        For instance job.every(3).days() will be `0 0 */3 * *`
        while job.day().every(3) would be `* * */3 * *`

        Many of these patterns exist as special tokens on Linux, such as
        `@midnight` and `@hourly`
        """
        return ItemEveryInterface(self.slices, unit)

    def setall(self, *args):
        """Replace existing time pattern with these five values given as args:

           job.setall("1 2 * * *")
           job.setall(1, 2) == '1 2 * * *'
           job.setall(0, 0, None, '>', 'SUN') == '0 0 * 12 SUN'
        """
        return self.slices.setall(*args)

    def clear(self):
        """Clear the special and set values"""
        return self.slices.clear()

    def frequency(self, year=None):
        """Returns the number of times this item will execute in a given year
           (defaults to this year)
        """
        return self.slices.frequency(year=year)

    def frequency_per_year(self, year=None):
        """Returns the number of /days/ this item will execute on in a year
           (defaults to this year)
        """
        return self.slices.frequency_per_year(year=year)

    def frequency_per_day(self):
        """Returns the number of time this item will execute in any day"""
        return self.slices.frequency_per_day()

    def schedule(self, date_from=None):
        """Return a croniter schedule is available."""
        if not date_from:
            date_from = datetime.now()
        try:
            # Croniter is an optional import
            from croniter.croniter import croniter
        except ImportError:
            raise ImportError("Croniter is not available. Please install croniter"
                          " python module via pip or your package manager")

        class Croniter(croniter):
            """Same as normal croniter, but always return datetime objects"""
            def get_next(self, type_ref=datetime):
                return croniter.get_next(self, type_ref)

            def get_prev(self, type_ref=datetime):
                return croniter.get_prev(self, type_ref)

            def get_current(self, type_ref=datetime):
                return croniter.get_current(self, type_ref)

        return Croniter(self.slices.clean_render(), date_from)

    @property
    def log(self):
        """Return a cron log specific for this job only"""
        if not self._log and self.cron:
            self._log = self.cron.log.for_program(self.command)
        return self._log

    @property
    def minute(self):
        """Return the minute slice"""
        return self.slices[0]

    @property
    def minutes(self):
        """Same as minute"""
        return self.minute

    @property
    def hour(self):
        """Return the hour slice"""
        return self.slices[1]

    @property
    def hours(self):
        """Same as hour"""
        return self.hour

    @property
    def day(self):
        return self.dom

    @property
    def dom(self):
        """Return the day-of-the month slice"""
        return self.slices[2]

    @property
    def month(self):
        """Return the month slice"""
        return self.slices[3]

    @property
    def months(self):
        """Same as month"""
        return self.month

    @property
    def dow(self):
        """Return the day of the week slice"""
        return self.slices[4]

    def __repr__(self):
        return "<CronJob '%s'>" % str(self)

    def __len__(self):
        return len(str(self))

    def __getitem__(self, x):
        return self.slices[x]

    def __lt__(self, value):
        return self.frequency() < CronSlices(value).frequency()

    def __gt__(self, value):
        return self.frequency() > CronSlices(value).frequency()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        if not self.is_valid():
            raise ValueError('Refusing to render invalid crontab. Disable to continue.')
        return self.render()


class ItemEveryInterface(object):
    """Provide an interface to the job.every() method:
        Available Calls:
          minute, minutes, hour, hours, dom, doms, month, months, dow, dows

       Once run all units will be cleared (set to *) then proceeding units
       will be set to '0' and the target unit will be set as every x units.
    """
    def __init__(self, item, units):
        self.slices = item
        self.unit = units
        for (x, i) in enumerate(['minute', 'hour', 'dom', 'month', 'dow',
                                 'min', 'hour', 'day', 'moon', 'weekday']):
            setattr(self, i, self._set(x % 5))
            setattr(self, i+'s', self._set(x % 5))

    def _set(self, target):
        def innercall():
            """Returned inner call for setting slice targets"""
            self.slices.clear()
            # Day-of-week is actually a level 2 set, not level 4.
            for p in range(target == 4 and 2 or target):
                self.slices[p].on('<')
            self.slices[target].every(self.unit)
        return innercall

    def year(self):
        """Special every year target"""
        if self.unit > 1:
            raise ValueError("Invalid value '%s', outside 1 year" % self.unit)
        self.slices.setall('@yearly')


class CronSlices(list):
    """Controls a list of five time 'slices' which reprisent:
        minute frequency, hour frequency, day of month frequency,
        month requency and finally day of the week frequency.
     """
    def __init__(self, *args):
        for info in S_INFO:
            self.append(CronSlice(info))
        self.special = None
        if args and not self.setall(*args):
            raise ValueError("Can't set cron value to: %s" % str(args))

    def setall(self, to, *slices):
        """Parses the various ways date/time frequency can be specified"""
        self.clear()
        if isinstance(to, CronItem):
            slices = to.slices
        elif isinstance(to, list):
            slices = to
        elif slices:
            slices = (to,) + slices
        elif isinstance(to, basestring) and to:
            if to.count(' ') == 4:
                slices = to.strip().split(' ')
            elif to.strip()[0] == '@':
                to = to[1:]
            else:
                slices = [to]

            if to == 'reboot':
                self.special = '@reboot'
                return True
            elif to in SPECIALS.keys():
                return self.setall(SPECIALS[to])

        if id(slices) == id(self):
            raise AssertionError("Can not set cron to itself!")

        for a, b in zip(self, slices):
            try:
                a.parse(b)
            except ValueError as error:
                sys.stderr.write("WARNING: %s\n" % str(error))
                return False
            except Exception:
                return False
        return True

    def clean_render(self):
        """Return just numbered parts of this crontab"""
        return ' '.join([unicode(s) for s in self])

    def render(self):
        "Return just the first part of a cron job (the numbers or special)"
        time = self.clean_render()
        if self.special:
            return self.special
        elif not SYSTEMV:
            for (name, value) in SPECIALS.items():
                if value == time and name not in SPECIAL_IGNORE:
                    return "@%s" % name
        return time

    def clear(self):
        """Clear the special and set values"""
        self.special = None
        for s in self:
            s.clear()

    def frequency(self, year=None):
        return self.frequency_per_year(year=year) * self.frequency_per_day()

    def frequency_per_year(self, year=None):
        result = 0
        if not year:
            year = date.today().year

        weekdays = list(self[4])

        for month in self[3]:
            for day in self[2]:
                try:
                    if date(year, month, day).weekday() in weekdays:
                        result += 1
                except ValueError:
                    continue
        return result

    def frequency_per_day(self):
        """Returns the number of time this item will execute in any day"""
        return len(self[0]) * len(self[1])

    def __str__(self):
        return self.render()

    def __eq__(self, arg):
        return self.render() == CronSlices(arg).render()


class SundayError(KeyError):
    pass


class CronSlice(object):
    """Cron slice object which shows a time pattern"""
    def __init__(self, info, value=None):
        self.min = info.get('min', None)
        self.max = info.get('max', None)
        self.name = info.get('name', None)
        self.enum = info.get('enum', None)
        self.parts = []
        if value:
            self.parse(value)

    def parse(self, value):
        """Set values into the slice."""
        self.parts = []
        if value is None:
            return self.clear()
        for part in str(value).split(','):
            if part.find("/") > 0 or part.find("-") > 0 or part == '*':
                self.parts.append(self.get_range(part))
            else:
                try:
                    self.parts.append(self._v(part))
                except SundayError:
                    self.parts.append(0)
                except ValueError as err:
                    raise ValueError('%s:%s/%s' % (str(err), self.name, part))

    def render(self, resolve=False):
        """Return the slice rendered as a crontab.

        resolve - return integer values instead of enums (default False)

        """
        if len(self.parts) == 0:
            return '*'
        return _render_values(self.parts, ',', resolve)

    def __repr__(self):
        return "<CronSlice '%s'>" % str(self)

    def __eq__(self, value):
        return str(self) == str(value)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.render()

    def every(self, n_value, also=False):
        """Set the every X units value"""
        if not also:
            self.clear()
        self.parts.append(self.get_range(int(n_value)))
        return self.parts[-1]

    def on(self, *n_value, **opts):
        """Set the time values to the specified placements."""
        if not opts.get('also', False):
            self.clear()
        for av in n_value:
            try:
                self.parts += self._v(av),
            except SundayError:
                self.parts += 0,
        return self.parts

    def during(self, vfrom, vto, also=False):
        """Set the During value, which sets a range"""
        if not also:
            self.clear()
        self.parts.append(self.get_range(self._v(vfrom), self._v(vto)))
        return self.parts[-1]

    @property
    def also(self):
        """Appends rather than replaces the new values"""
        outself = self

        class Also(object):
            """Will append new values"""
            def every(self, *a):
                """Also every one of these"""
                return outself.every(*a, also=True)

            def on(self, *a):
                """Also on these"""
                return outself.on(*a, also=True)

            def during(self, *a):
                """Also during these"""
                return outself.during(*a, also=True)
        return Also()

    def clear(self):
        """clear the slice ready for new vaues"""
        self.parts = []

    def get_range(self, *vrange):
        """Return a cron range for this slice"""
        return CronRange(self, *vrange)

    def __iter__(self):
        """Return the entire element as an iterable"""
        r = {}
        # An empty part means '*' which is every(1)
        if not self.parts:
            self.every(1)
        for part in self.parts:
            if isinstance(part, CronRange):
                for bit in part.range():
                    r[bit] = 1
            else:
                r[int(part)] = 1
        for x in r:
            yield x

    def __len__(self):
        """Returns the number of times this slice happens in it's range"""
        return len(list(self.__iter__()))

    def _v(self, v):
        if v == '>':
            v = self.max
        elif v == '<':
            v = self.min
        try:
            out = get_cronvalue(v, self.enum)
        except ValueError:
            raise ValueError("Unrecognised '%s'='%s'" % (self.name, v))
        except KeyError:
            raise KeyError("No enumeration '%s' got '%s'" % (self.name, v))

        if self.max == 6 and int(out) == 7:
            raise SundayError("Detected Sunday as 7 instead of 0!")

        if int(out) < self.min or int(out) > self.max:
            raise ValueError("Invalid value '%s', expected %d-%d for %s" % (
                str(v), self.min, self.max, self.name))
        return out

    def filter_v(self, v):
        """Support wrapper for enumerations and check for range"""
        return self._v(v)


def get_cronvalue(value, enums):
    """Returns a value as int (pass-through) or a special enum value"""
    if isinstance(value, int):
        return value
    elif str(value).isdigit():
        return int(str(value))
    if not enums:
        raise KeyError("No enumeration allowed")
    return CronValue(str(value), enums)


class CronValue(object):
    """Represent a special value in the cron line"""
    def __init__(self, value, enums):
        self.enum = value
        self.value = enums.index(value.lower())

    def __lt__(self, value):
        return self.value < int(value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.enum

    def __int__(self):
        return self.value


def _render_values(values, sep=',', resolve=False):
    """Returns a rendered list, sorted and optionally resolved"""
    if len(values) > 1:
        values.sort()
    return sep.join([_render(val, resolve) for val in values])


def _render(value, resolve=False):
    """Return a single value rendered"""
    if isinstance(value, CronRange):
        return value.render(resolve)
    if resolve:
        return str(int(value))
    return str(value)


class CronRange(object):
    """A range between one value and another for a time range."""
    def __init__(self, vslice, *vrange):
        self.slice = vslice
        self.cron = None
        self.seq = 1

        if not vrange:
            self.all()
        elif isinstance(vrange[0], basestring):
            self.parse(vrange[0])
        elif isinstance(vrange[0], int) or isinstance(vrange[0], CronValue):
            if len(vrange) == 2:
                (self.vfrom, self.vto) = vrange
            else:
                self.seq = vrange[0]
                self.all()

    def parse(self, value):
        """Parse a ranged value in a cronjob"""
        if value.count('/') == 1:
            value, seq = value.split('/')
            self.seq = self.slice.filter_v(seq)
            if self.seq < 1 or self.seq > self.slice.max - 1:
                raise ValueError("Sequence can not be divided by zero or max")
        if value.count('-') == 1:
            vfrom, vto = value.split('-')
            self.vfrom = self.slice.filter_v(vfrom)
            try:
                self.vto = self.slice.filter_v(vto)
            except SundayError:
                self.vto = 6
        elif value == '*':
            self.all()
        else:
            raise ValueError('Unknown cron range value "%s"' % value)

    def all(self):
        """Set this slice to all units between the miniumum and maximum"""
        self.vfrom = self.slice.min
        self.vto = self.slice.max

    def render(self, resolve=False):
        """Render the ranged value for a cronjob"""
        value = '*'
        if int(self.vfrom) > self.slice.min or int(self.vto) < self.slice.max:
            value = _render_values([self.vfrom, self.vto], '-', resolve)
        if self.seq != 1:
            value += "/%d" % self.seq
        if value != '*' and SYSTEMV:
            value = ','.join(map(str, self.range()))
        return value

    def range(self):
        """Returns the range of this cron slice as a iterable list"""
        return range(int(self.vfrom), int(self.vto)+1, self.seq)

    def every(self, value):
        """Set the sequence value for this range."""
        self.seq = int(value)

    def __lt__(self, value):
        return int(self.vfrom) < int(value)

    def __gt__(self, value):
        return int(self.vto) > int(value)

    def __int__(self):
        return int(self.vfrom)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.render()
