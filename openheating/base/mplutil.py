import matplotlib
# gosh. suppress tkinter usage; otherwise matplotlib.pyplot won't
# load.
matplotlib.use('agg')
import matplotlib.pyplot as plt

from contextlib import contextmanager
import datetime
import threading
import functools
import io


# matplotlib is entirely unsafe (this is bloody Matlab heritage - the
# most popular interface is "MATLAB style" which is inherently global)
_lock = threading.Lock()
def _locked(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        with _lock: return f(*args, **kwargs)
    return wrap

@_locked
def show_samples(samples):
    matplotlib.use('GTK3Cairo')
    plt.plot([datetime.datetime.fromtimestamp(ts) for ts,_ in samples], [temp for _,temp in samples])
    plt.show()
    plt.clf()

@contextmanager
def plot(title=None, xlabel=None, ylabel=None, legend=True,
         xlim=None, ylim=None, size_inches=None):
    try:
        _lock.acquire()

        # plt.xkcd()

        if title is not None:
            plt.title(title)
        if xlabel is not None:
            plt.xlabel(xlabel)
        if ylabel is not None:
            plt.ylabel(ylabel)
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)
        if size_inches is not None:
            plt.gcf().set_size_inches(*size_inches)

        # disable xticks until someone needs them
        plt.xticks([])


        yield
        
        # wtf: clear global variables first. I used to test this in a
        # jupyter notebook and got confused. reason: IPython does a
        # plt.show() or something, and that *always* resets
        # matplotlib's global bullshit.
        plt.clf()
        plt.cla()
        plt.close()
    finally:
        _lock.release()
    
def plot_samples(samples, label=None):
    plt.plot(
        [ts for ts,_ in samples],
        [temp for _,temp in samples],
        label = label)

def as_svg_io(legend=True):
    'return io.BytesIO, suitable as input to flask.send_file()'

    data = io.BytesIO()
    plt.savefig(data, format='svg')
    data.seek(0)
    return data

def as_embeddable_svg(legend=True):
    data = io.StringIO()
    plt.savefig(data, format='svg')

    # get rid of all the xml gibberish around the bare SVG which we
    # want to embed.
    gibberish = data.getvalue()
    return gibberish[gibberish.index('<svg'):]
