def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

def beautify_float(value):
    if (type(value) is str):
        value = float(value)

    return int(value) if (value % 1 == 0) else value