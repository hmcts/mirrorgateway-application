import logging

class CustomLogger:
    """
    Class that instantiates a template logger.

    Usage:
        CustomLogger().logger.info("Custom message")
    """
    logger = None

    def __init__(self, basename="default", log_level='INFO', log_format='json', log_file=None):
        """
        Constructor

        Args:
            basename(string): The text to use as the base of log messages
            log_level(string): The logging.LOG_LEVEL to set.
            log_format(string): The type of log format to create.
            log_file(string): File to pipe logs to
        """
        self._setup_logger(basename, log_level, log_format, log_file)

    def _setup_logger(self,
                      basename="default",
                      log_level='INFO',
                      log_format='json',
                      log_file=None):
            """
            Setup the logger

            Args:
                basename(string): The text to use as the base of log messages
                log_level(string): The logging.LOG_LEVEL to set. Default is 'INFO'
                log_format(string): The type of log format to create.
                                    - 'json' for json format
                                    - 'text' for json format for text format
                                    - anything else for default 'text' format
                log_file(string): File to pipe logs to
            """
            if log_format == 'json':
                logging_format_str = '{"timestamp": "%(asctime)s","name": "%(name)s", "level": "%(levelname)s", "level_no": %(levelno)i, "message": "%(message)s"}'
            elif log_format == 'text':
                logging_format_str = '%(asctime)s %(name)s: %(levelname)s: %(message)s'
            else:
                logging_format_str = '%(asctime)s %(name)s: %(levelname)s: %(message)s'

            # Set up the logging
            logging.basicConfig(format=logging_format_str,
                                level=logging.getLevelName(log_level),
                                filename=log_file)

            self.logger = logging.getLogger(basename)
            logging.getLogger("requests").setLevel(logging.WARNING)
            logging.getLogger('boto').setLevel(logging.CRITICAL)
