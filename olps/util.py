# This is a set of functions to provide readable unit -> nanosecond conversion.
# This is so we don't have magic numbers all over backtesting code.

def millisecond(n: int) -> int:
    # 1e6 ns = 1 ms
    return int(1e6 * n)


def second(n: int) -> int:
    # 1e3 ms = 1 s
    return int(millisecond(1e3) * n)


def minute(n: int) -> int:
    # 60 s = 1 min
    return int(second(60) * n)


def hour(n: int) -> int:
    # 60 min = 1 hr
    return int(minute(60) * n)
