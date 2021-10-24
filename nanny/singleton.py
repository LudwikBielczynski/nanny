import threading

class SingletonMeta(type):
    _instances = {} # type: ignore
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                # Second check needed if during acquiring lock a new instance was not created
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
