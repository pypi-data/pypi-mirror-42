
from abc import abstractmethod

from ch2.stoats import DbPipeline
from ...lib.io import for_modified_files
from ...squeal.database import add
from ...squeal.tables.statistic import StatisticJournal, StatisticName


class AbortImport(Exception):
    pass


class AbortImportButMarkScanned(AbortImport):
    pass


class Importer(DbPipeline):

    def _on_init(self, *args, **kargs):
        super()._on_init(*args, **kargs)
        self.__statistics_cache = {}

    def _first(self, path, records, *names):
        try:
            return next(iter(record for record in records if record.name in names))
        except StopIteration:
            self._log.debug('No %s entry(s) in %s' % (str(names), path))
            raise AbortImportButMarkScanned()

    def _last(self, path, records, *names):
        save = None
        for record in records:
            if record.name in names:
                save = record
        if not save:
            self._log.debug('No %s entry(s) in %s' % (str(names), path))
            raise AbortImportButMarkScanned()
        return save

    def _run(self, paths, force=False):
        with self._db.session_context() as s:
            for_modified_files(self._log, s, paths, self._callback(), self, force=force)

    def _callback(self):
        def callback(file):
            self._log.debug('Scanning %s' % file)
            with self._db.session_context() as s:
                try:
                    self._import(s, file)
                    return True
                except AbortImport as e:
                    self._log.debug('Aborted %s' % file)
                    return isinstance(e, AbortImportButMarkScanned)
        return callback

    @abstractmethod
    def _import(self, s, path):
        pass

    def _create(self, s, name, units, summary, constraint, source, value, time, type):
        # cache statistic_name instances for speed (avoid flush on each query)
        key = (name, constraint)
        if key not in self.__statistics_cache:
            self.__statistics_cache[key] = \
                StatisticName.add_if_missing(self._log, s, name, units, summary, self, constraint)
        if key not in self.__statistics_cache or not self.__statistics_cache[key]:
            raise Exception('Failed to get StatisticName for %s' % key)
        return type(statistic_name=self.__statistics_cache[key], source=source, value=value, time=time)

    def _add(self, s, name, units, summary, constraint, source, value, time, type):
        return add(s, self._create(s, name, units, summary, constraint, source, value, time, type))
