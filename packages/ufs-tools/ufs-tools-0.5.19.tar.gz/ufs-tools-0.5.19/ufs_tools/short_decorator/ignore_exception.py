import traceback


def ignore_exc(func):
    """
    Usage:
    @ignore_exc
    def test(a):
        pass
    :param func: the function we want to ignore exception
    :return:
    """
    return ignore_exc_with_result()(func)


def ignore_exc_with_result(exception_result=None,
                           exception=Exception,
                           is_notification_needed=False,
                           success_callback=None,
                           exception_callback=None,
                           ):
    """
    Usage:
    @ignore_exc_with_result()(func)
    def test(a):
        pass
    :param success_callback: called if execution is successful
    :param exception_callback: called if exception occurred
    :param is_notification_needed: whether to show the exception message
    :param exception_result: if exception occurred, this will be returned
    :param exception: a list of exception classes that will be captured
    :return: will return a wrapper function for the decorator
    """
    # Ref: http://wklken.me/posts/2012/10/27/python-base-decorator.html
    def exc_wrapper(func):
        # print "executing--------------"
        def wrap_with_exc(*args):
            # noinspection PyBroadException
            try:
                # print "executing!!!!!!!!!!!!!!!!"
                result = func(*args)
                if success_callback:
                    success_callback(result)
                return result
            except exception as e:
                if is_notification_needed:
                    print("ignored the following exception:______________________________________________")
                    traceback.print_exc()
                    return exception_result
                if exception_callback:
                    exception_callback(e)
                return exception_result

        return wrap_with_exc

    return exc_wrapper
