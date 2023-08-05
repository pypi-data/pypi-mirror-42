
import datetime as dt
from collections import defaultdict

from sqlalchemy import desc

from ..names import HEART_RATE, BPM, STEPS, STEPS_UNITS, ACTIVITY, CUMULATIVE_STEPS_START, \
    CUMULATIVE_STEPS_FINISH
from ..read import Importer, AbortImportButMarkScanned, AbortImport
from ...fit.format.read import filtered_records
from ...fit.format.records import fix_degrees, unpack_single_bytes, merge_duplicates
from ...fit.profile.profile import read_fit
from ...lib.date import to_time, time_to_local_date, format_time
from ...squeal.database import add
from ...squeal.tables.monitor import MonitorJournal
from ...squeal.tables.statistic import StatisticJournalInteger, StatisticJournalText, StatisticName, StatisticJournal

ACTIVITY_TYPE_ATTR = 'activity_type'
HEART_RATE_ATTR = 'heart_rate'
MONITORING_ATTR = 'monitoring'
MONITORING_INFO_ATTR = 'monitoring_info'
STEPS_ATTR = 'steps'


class MonitorImporter(Importer):

    # the monitor steps data are cumulative, but we want incremental.
    # that's easy to do within a single file, but to be correct across files we also
    # store the cumulative value at the start and end,  we use these to "patch things up"
    # is we read a missing file.

    def run(self, paths, force=False):
        self._run(paths, force=force)

    def _check_contains(self, s, start, finish, path):
        for mjournal in s.query(MonitorJournal). \
                filter(MonitorJournal.start >= start,
                       MonitorJournal.finish <= finish).all():
            self._log.warning('Replacing %s with data from %s for %s - %s' % (mjournal, path, start, finish))
            s.delete(mjournal)

    def _check_inside(self, s, start, finish, path):
        for mjournal in s.query(MonitorJournal). \
                filter(MonitorJournal.start <= start,
                       MonitorJournal.finish >= finish).all():
            self._log.warning('%s already includes data from %s for %s - %s' % (mjournal, path, start, finish))
            raise AbortImportButMarkScanned()

    def _check_overlap(self, s, start, finish, path):
        for mjournal in s.query(MonitorJournal). \
                filter(MonitorJournal.start < finish,
                       MonitorJournal.finish > start).all():
            self._log.warning('%s overlaps data from %s for %s - %s' % (mjournal, path, start, finish))
            self._log.error('Conflict between %s and %s' % (path, mjournal.fit_file))
            raise AbortImport()

    def _check_previous(self, s, start, finish, path):
        self._check_contains(s, start, finish, path)
        self._check_inside(s, start, finish, path)
        self._check_overlap(s, start, finish, path)

    def _delete_journals(self, s, first_timestamp, path):
        # key only on time so that repeated files don't affect things
        if not first_timestamp:
            raise Exception('Missing timestamp in %s' % path)
        # need to iterate because sqlite doesn't support multi-table delete and we have inheritance.
        for mjournal in s.query(MonitorJournal). \
                filter(MonitorJournal.start == first_timestamp).all():
            self._log.debug('Deleting %s' % mjournal)
            s.delete(mjournal)
        s.flush()

    def _delta(self, steps, activity, cumulative):
        if steps >= cumulative[activity]:
            delta = steps - cumulative[activity]
        else:
            delta = steps
        cumulative[activity] = steps
        return delta

    def _save_cumulative(self, s, time, cumulative, mjournal, name):
        self._log.debug('Adding %s at time %s' % (name, format_time(time)))
        for activity in cumulative:
            self._add(s, name, STEPS_UNITS, None, activity,
                      mjournal, cumulative[activity], time, StatisticJournalInteger)
        self._log.debug('Added: %s' % ', '.join('%s:%s' % item for item in cumulative.items()))

    def _update_cumulative(self, s, time, cumulative, mjournal, name, saved):
        # go back and fill in with zeroes and missing starting values
        for activity in saved:
            del cumulative[activity]
        if cumulative:
            for activity in cumulative:
                cumulative[activity] = 0
            self._save_cumulative(s, time, cumulative, mjournal, name)

    def _read_cumulative(self, s, time, cumulative, name):
        # no constraint, so all activities
        for journal in s.query(StatisticJournalInteger).join(StatisticName). \
                filter(StatisticJournalInteger.time == time,
                       StatisticName.name == name,
                       StatisticName.owner == self).all():
            cumulative[journal.statistic_name.constraint] = journal.value
        self._log.debug('Read %s at %s' % (name, format_time(time)))
        self._log.debug('Read: %s' % ', '.join('%s:%s' % item for item in cumulative.items()))

    def _read_previous(self, s, first_timestamp, cumulative):
        prev = s.query(MonitorJournal). \
            filter(MonitorJournal.finish <= first_timestamp). \
            order_by(desc(MonitorJournal.finish)).limit(1).one_or_none()
        if prev:
            self._read_cumulative(s, prev.finish, cumulative, CUMULATIVE_STEPS_FINISH)

    def _update_next(self, s, last_timestamp, cumulative):
        self._log.debug('Checking for following file after %s' % format_time(last_timestamp))
        next = s.query(MonitorJournal). \
            filter(MonitorJournal.start >= last_timestamp). \
            order_by(MonitorJournal.start).limit(1).one_or_none()
        if next:
            self._log.debug('Found file at %s - fixing up' % format_time(next.start))
            # no constraint, so all activities
            for cumulative_journal in s.query(StatisticJournalInteger).join(StatisticName). \
                    filter(StatisticJournalInteger.time == next.start,
                           StatisticName.name == CUMULATIVE_STEPS_START,
                           StatisticName.owner == self).all():
                activity = cumulative_journal.statistic_name.constraint
                if activity in cumulative and cumulative[activity] != cumulative_journal.value:
                    self._log.debug('Found %s with inconsistent value (%s != %s)' %
                                    (CUMULATIVE_STEPS_START, cumulative_journal.value, cumulative[activity]))
                    steps_journal = StatisticJournal.after(s, next.start, STEPS, self, activity)
                    self._log.debug('Found %s with value %s' % (STEPS, steps_journal.value))
                    # only fix up if the cumulative value didn't reset
                    if steps_journal.value + cumulative_journal.value >= cumulative[activity]:
                        steps_journal.value = steps_journal.value - cumulative[activity] + cumulative_journal.value
                        self._log.debug('Updated %s at %s to %s' %
                                        (STEPS, format_time(last_timestamp), steps_journal.value))
                        cumulative_journal.value = cumulative[activity]
                        if steps_journal.value == 0:
                            activity_journal = StatisticJournal.at(s, steps_journal.time, ACTIVITY, self, activity)
                            s.delete(steps_journal)
                            s.delete(activity_journal)
                            self._log.debug('Deleted %s and %s' % (STEPS, ACTIVITY))

    def _create_journals(self, s, records, cumulative, mjournal):
        n_heart_rate, n_steps, steps_journals = 0, 0, defaultdict(lambda: {})
        for record in records:
            if HEART_RATE_ATTR in record.data:
                self._add(s, HEART_RATE, BPM, None, None, mjournal, record.data[HEART_RATE_ATTR][0][0],
                          record.timestamp, StatisticJournalInteger)
                n_heart_rate += 1
            if STEPS_ATTR in record.data:
                for (activity, steps) in zip(record.data[ACTIVITY_TYPE_ATTR][0], record.data[STEPS_ATTR][0]):
                    steps = self._delta(steps, activity, cumulative)
                    if steps:
                        if activity in steps_journals[record.timestamp]:
                            # sometimes get values at exactly the same time :(
                            steps_journals[record.timestamp][activity].value += steps
                        else:
                            steps_journals[record.timestamp][activity] = \
                                self._create(s, STEPS, STEPS_UNITS, None, activity,
                                             mjournal, steps, record.timestamp,
                                             StatisticJournalInteger)
                        n_steps += 1
        self._log.debug('Found %d steps and %d heart rate values' % (n_heart_rate, n_steps))
        return steps_journals

    def _merge_boundary(self, s, steps_journals, time):
        if time in steps_journals:
            for activity in list(steps_journals[time].keys()):
                sjournal = StatisticJournal.at(s, time, STEPS, self, activity)
                if sjournal:
                    if sjournal.value == steps_journals[time][activity].value:
                        self._log.debug('Matching data at %s' % format_time(time))
                    else:
                        # we have a contradiction, so simply use the latest
                        # could maybe use max() instead?
                        self._log.warning('Replacing %s data at %s (%s replaced by %s)' %
                                       (STEPS, format_time(time), sjournal.value,
                                        steps_journals[time][activity].value))
                        sjournal.value = steps_journals[time][activity].value
                    del steps_journals[time][activity]

    def _import(self, s, path):

        types, messages, records = filtered_records(self._log, read_fit(self._log, path))
        records = [record.as_dict(merge_duplicates, fix_degrees, unpack_single_bytes)
                   for _, _, record in sorted(records,
                                              key=lambda r: r[2].timestamp if r[2].timestamp else to_time(0.0))]

        first_timestamp = self._first(path, records, MONITORING_INFO_ATTR).timestamp
        last_timestamp = self._last(path, records, MONITORING_ATTR).timestamp
        if first_timestamp == last_timestamp:
            self._log.debug('File %s is empty (no timespan)' % path)
            raise AbortImportButMarkScanned()

        self._log.info('Importing monitor data from %s for %s - %s' %
                       (path, format_time(first_timestamp), format_time(last_timestamp)))
        self._check_previous(s, first_timestamp, last_timestamp, path)
        mjournal = add(s, MonitorJournal(start=first_timestamp, fit_file=path, finish=last_timestamp))

        cumulative = defaultdict(lambda: 0)
        self._read_previous(s, first_timestamp, cumulative)
        self._save_cumulative(s, first_timestamp, cumulative, mjournal, CUMULATIVE_STEPS_START)
        saved_activities = list(cumulative.keys())

        steps_journals = self._create_journals(s, records, cumulative, mjournal)

        self._save_cumulative(s, last_timestamp, cumulative, mjournal, CUMULATIVE_STEPS_FINISH)
        self._update_next(s, last_timestamp, cumulative)
        self._update_cumulative(s, first_timestamp, cumulative, mjournal, CUMULATIVE_STEPS_START, saved_activities)

        self._merge_boundary(s, steps_journals, first_timestamp)
        self._merge_boundary(s, steps_journals, last_timestamp)

        # write steps at end, when adjoining data have been fixed
        self._log.debug('Adding %s to database' % STEPS)
        for timestamp in steps_journals:
            for activity in steps_journals[timestamp]:
                add(s, steps_journals[timestamp][activity])
                self._add(s, ACTIVITY, None, None, activity, mjournal,
                          activity, timestamp, StatisticJournalText)


def missing_dates(log, s):
    # we don't try to be perfect here.  the idea is that it's called to get the latest
    # updates, rather than fill in all gaps (do the bulk download thing for that).
    # we also don't try to get fractional data.
    # and as for timezones... we just assume garmin uses the local timezone.
    latest = s.query(MonitorJournal).order_by(desc(MonitorJournal.start)).limit(1).one_or_none()
    if latest is None:
        log.warning('No existing monitor data - ' +
                 'do a bulk download instead: https://www.garmin.com/en-US/account/datamanagement/')
        return
    # find the mid-point to avoid any problems with timezones and edge cases
    # (these files don't span more than a day)
    seconds = (latest.finish - latest.start).total_seconds() / 2
    start = time_to_local_date(latest.start + dt.timedelta(seconds=seconds) + dt.timedelta(days=1))
    finish = dt.date.today()
    days = (finish - start).days
    if days > 10:
        raise Exception('Too many days (%d) - ' % days +
                        'do a bulk download instead: https://www.garmin.com/en-US/account/datamanagement/')
    if days:
        # exclude today since it will be incomplete
        while start < finish:
            yield start
            start += dt.timedelta(days=1)
    else:
        log.warning('No dates to download')
