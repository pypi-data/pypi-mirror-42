import inspect

def serialize_arguments():
    frame = inspect.currentframe().f_back
    _, _, _, values = inspect.getargvalues(frame)
    return values