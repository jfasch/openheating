from . import program

import asyncio
import itertools
import sys
import re


class CLI:
    def __init__(self, programs):
        self.__programs = programs
        self.__running = {} # { taskid: (pname, task) }
        self.__ids = itertools.count(1)

    async def run(self):
        async for line in linereader(sys.stdin):
            line = line.strip()
            start = re.search(r'^start\s+(.+)$', line)
            if start:
                pname = start.group(1)
                prog = self.__programs.get(pname)
                if not prog:
                    print('no such program: "{}"'.format(pname), file=sys.stderr)
                    continue
                pid = next(self.__ids)
                task = program.launch(prog)
                self.__running[pid] = pname, task
                print(pid)
                continue

            stop = re.search(r'^stop\s+(\d+)$', line)
            if stop:
                pid = int(stop.group(1))
                _, task = self.__running.pop(pid, None)
                if task:
                    task.cancel()
                else:
                    print('no such task: {}'.format(pid), file=sys.stderr)
                continue

            if line == 'ps':
                for pid, (pname, _) in self.__running.items():
                    print(pid, pname)
                continue

                    
        # shutdown: cancel running tasks
        for _, task in self.__running.values():
            task.cancel()

class linereader:
    '''async iterator used to asyncronously iterate over a file-like.

    Python 3.5.x does not yet have `PEP 525 -- Asynchronous Generators
    <https://www.python.org/dev/peps/pep-0525/#asynchronous-generators>`_,
    so this must be handcoded.

    '''

    def __init__(self, f):
        self.__f = f
        self.__q = asyncio.Queue()
        asyncio.get_event_loop().add_reader(self.__f.fileno(), self.__inputready)
        
    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self.__q.get()
        if len(line) == 0:
            raise StopAsyncIteration()
        return line

    def __inputready(self):
        line = self.__f.readline()
        self.__q.put_nowait(line)
