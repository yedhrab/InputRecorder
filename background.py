import threading


def do_background(func, args=(), kwargs={}):
    return threading.Thread(target=func, args=args, kwargs=kwargs).start()


def do_delayed(func, duration, args=(), kwargs={}):
    return threading.Timer(duration, func, args, kwargs).start()


def background(func):

    def inner(*args, **kwargs):
        do_background(func, args=args, kwargs=kwargs)

    return inner


def delayed(duration):
    def background(func):

        def inner(*args, **kwargs):
            do_delayed(func, duration, args=args, kwargs=kwargs)

        return inner
    return background


@delayed(1)
def test(val1, val2):
    for i in range(val1, val2):
        print(i)


if __name__ == "__main__":
    test(10, 20)
    test(20, 30)
