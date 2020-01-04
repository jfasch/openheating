from openheating.base.error import HeatingError


class Plant:
    def __init__(self, services):
        self.__services = services
        self.__running = False

    @property
    def running(self):
        return self.__running

    def startup(self):
        started = []
        start_error = None
        for s in self.__services:
            try:
                s.start()
                started.append(s)
            except HeatingError as e:
                start_error = e
                break

        if start_error is not None:
            for s in reversed(started):
                s.stop()
            raise start_error

        self.__running = True

    def shutdown(self, is_failure):
        stderrs = []
        errors = []
        for s in reversed(self.__services):
            try:
                stderr = s.stop()
                stderrs.append((s.busname, stderr))
            except Exception as e:
                errors.append(e)

        if is_failure or len(errors):
            for busname, stderr in stderrs:
                print('\n*** STDERR from {}'.format(busname), file=sys.stderr)
                if stderr is None:
                    print(' '*3, '(apparently unstarted)', file=sys.stderr)
                else:
                    for line in stderr.split('\n'):
                        print(' '*3, line, file=sys.stderr)

        if len(errors):
            msg = ['there were errors while stopping services ...']
            for e in errors:
                msg.append(str(e))
            raise RuntimeError('\n'.join(msg))

