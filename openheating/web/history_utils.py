import datetime


def make_histogram_input__full_label(history):
    '''Give a history object, retrieve its data (which is in
    (int:UNIX-timestamp, float:temperature)) into something better
    layoutable, (str:formatted_datetime, float:temperature).
    '''

    return [(str(datetime.datetime.fromtimestamp(timestamp)), temperature)
            for timestamp, temperature in history]

def make_histogram_input__no_label(history):
    '''Give a history object, retrieve its data (which is in
    (int:UNIX-timestamp, float:temperature)) into something better
    layoutable, (str:formatted_datetime, float:temperature).
    '''

    return [('', temperature) for timestamp, temperature in history]
