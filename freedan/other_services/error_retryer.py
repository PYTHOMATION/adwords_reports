import time

DEFAULT_MAX_ATTEMPTS = 4
DEFAULT_SLEEP_INTERVAL = 5


class ErrorRetryer:
    """ Execute a function and in case an error occurs retry it x times. If it fails x times, throw an exception. 
    :param max_attempts: int, how often should it attempt to execute function 
    :param sleep_interval: int, how long should it wait in between attempts
    :return: func
    """
    def __init__(self, max_attempts=DEFAULT_MAX_ATTEMPTS, sleep_interval=DEFAULT_SLEEP_INTERVAL):
        self.max_attempts = max_attempts
        self.sleep_interval = sleep_interval

    def __call__(self, function_to_decorate):
        def wrapped_f(*args, **kwargs):
            for counter in range(1, self.max_attempts+1):
                try:
                    return function_to_decorate(*args, **kwargs)
                except Exception as exception_type:
                    print("Retrying request because of error: %s" % exception_type)
                    time.sleep(self.sleep_interval)

            # error message might also be used in an email notification here
            raise Exception("Gave up after {num} attempts".format(num=self.max_attempts))
        return wrapped_f
