def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def checkintvalue(val, min_val, max_val, msg='', raise_exception=True):
    if not (isint(val) and min_val <= int(val) <= max_val):
        if raise_exception:
            raise ValueError(msg)
        return False
    return True
