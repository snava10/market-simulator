from datetime import datetime


class Logger:
    def log(self, log_type, message):
        class_name = self.__class__.__name__
        print('%s %s: %s: %s ' % (datetime.now(), log_type, class_name, message))

    def info(self, message):
        self.log('INFO', message)

    def warning(self, message):
        self.log('WARNING', message)

    def error(self, message):
        self.log('ERROR', message)

    def debug(self, message):
        self.log('DEBUG', message)
