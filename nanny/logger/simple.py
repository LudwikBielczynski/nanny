class LoggerSimple():

    def info(self, *args, **kwargs):
        return print(*args, **kwargs)

    def debug(self, *args, **kwargs):
        return print(*args, **kwargs)

    def warn(self, *args, **kwargs):
        return print(*args, **kwargs)

    def error(self, *args, **kwargs):
        return print(*args, **kwargs)
