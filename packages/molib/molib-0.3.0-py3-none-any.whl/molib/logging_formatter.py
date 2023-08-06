import logging
import sys

# Custom formatter
class LogFormatter(logging.Formatter):
    '''adapted from https://stackoverflow.com/a/14859558'''
    err_fmt  = "\n***ERROR: %(msg)s"
    dbg_fmt  = "\n***DEBUG: %(module)s: %(lineno)d: %(msg)s"
    info_fmt = "\n%(msg)s"

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = LogFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._style._fmt = LogFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = LogFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result

def console_logger(level):
    fmt = LogFormatter()
    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setFormatter(fmt)
    logging.root.addHandler(hdlr)
    logging.root.setLevel(level)
