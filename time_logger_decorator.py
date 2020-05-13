import functools
import queue
import threading
import time


def time_logger(timeout=None, time_format="%c", cash=False):
    
    """
    Allows calling decorator which measures function's execution time

    :param timeout: if decorated function had not finished working until timeout ended, the decorator would raise
                    an exception
                    Alert if function works forever, thread will flow!
    :param time_format: time format
    :param cash: if cash = True, input arguments will be saved
    """
    
    def time_decorator(func_to_decorate):

        @functools.wraps(func_to_decorate)
        def wrapper(*args, **kwargs):

            def helper(que, *ar, **kwar):
                res = func_to_decorate(*ar, **kwar)
                que.put(res)

            res_queue = queue.Queue()
            action_thread = threading.Thread(target=helper, args=(res_queue, *args), kwargs=kwargs)
            start = time.perf_counter()
            print(f"Starting '{func_to_decorate.__name__}' on {time.strftime(time_format)}")

            try:
                action_thread.start()
                action_thread.join(timeout=timeout)

                if action_thread.is_alive():
                    raise Exception("TimeLimitExceeded")

                result = res_queue.get()
            except Exception as e:
                end = time.perf_counter()
                print(
                    f"Exception {e}, "
                    f"function '{func_to_decorate.__name__}', "
                    f"execution time = {(end - start) : 0.3f}s"
                    f"{f', on args: {args}, kwargs: {kwargs}' if cash  else ''}"
                )
            else:
                end = time.perf_counter()
                print(
                    f"Finished '{func_to_decorate.__name__}', "
                    f"execution time = {(end - start) : 0.3f}s"
                    f"{f', on args: {args}, kwargs: {kwargs}' if cash  else ''}"
                )
                return result

        return wrapper

    return time_decorator
