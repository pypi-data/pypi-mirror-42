

import logging
import datetime
import errno

from os import makedirs
from os.path import splitext, join, exists, dirname, basename
from glob import glob


class FileProcessorHandler(logging.Handler):
    """
    FileProcessorHandler is a python log handler based on Apache Airflow FileProcessorHandler that handles
    log files per execution.

    Intended to use with scripts with timed execution.
    """

    def __init__(self, log_folder: str):
        """
        :param log_folder: Base log folder to place logs
        """

        super(FileProcessorHandler, self).__init__()

        self.handler = None
        self.log_folder = log_folder
        self._cur_file_number = None  # Hold information of current file number

        # Creates a folder for current execution day
        self._cur_date = datetime.datetime.today()
        if not exists(self._get_log_directory()):
            try:
                makedirs(self._get_log_directory())
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                logging.warning("%s already exists", self._get_log_directory())

        self._setup_file_handler()

    def setFormatter(self, formatter):
        if self.handler is not None:
            self.handler.setFormatter(formatter)

    def setLevel(self, level):
        if self.handler is not None:
            self.handler.setLevel(level)

    def _setup_file_handler(self):

        local_loc = self._init_file('%d.log' % self._get_current_file_number())

        self.handler = logging.FileHandler(local_loc)
        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(self.level)

    def emit(self, record):
        if self.handler is not None:
            self.handler.emit(record)

    def flush(self):
        if self.handler is not None:
            self.handler.flush()

    def close(self):
        if self.handler is not None:
            self.handler.close()

    def _get_log_directory(self):
        now = datetime.datetime.utcnow()
        return join(self.log_folder, now.strftime('%Y-%m-%d'))

    def _init_file(self, filename):
        relative_path = filename
        full_path = join(self._get_log_directory(), relative_path)
        directory = dirname(full_path)

        if not exists(directory):
            makedirs(directory)

        if not exists(full_path):
            open(full_path, "a").close()

        return full_path

    def _get_current_file_number(self):

        file_list = glob(join(self._get_log_directory(), '*.log'))
        last_file_number = max([int(splitext(basename(f))[0]) for f in file_list]) if file_list else 0
        return last_file_number + 1
