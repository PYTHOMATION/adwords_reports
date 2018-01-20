import time

DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_SLEEP_INTERVAL = 5


class ErrorRetryer:
    """ Should be refactored to a function
    :param max_attempts: int
    :param sleep_interval: int
    :return: func
    """
    def __init__(self, max_attempts=DEFAULT_MAX_ATTEMPTS, sleep_interval=DEFAULT_SLEEP_INTERVAL):
        self.max_attempts = max_attempts
        self.sleep_interval = sleep_interval

    def __call__(self, function_to_decorate):
        def wrapped_f(*args, **kwargs):
            for counter in range(self.max_attempts):
                try:
                    return function_to_decorate(*args, **kwargs)
                except Exception as exception_type:
                    print("Retrying request because of error: %s" % exception_type)
                    time.sleep(self.sleep_interval)
            raise Exception("Gave up after {num} attempts".format(num=self.max_attempts))
        return wrapped_f
