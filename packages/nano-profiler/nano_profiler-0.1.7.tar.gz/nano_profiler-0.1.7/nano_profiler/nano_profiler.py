import time


class NanoProfiler:
    def __init__(self, name='default', autostart=False):
        self.name = name
        self._points = []
        self._label_counter = 0

        self._was_started = False

        if autostart:
            self.start()

    def _get_default_label(self):
        self._label_counter += 1
        return 'Label {}'.format(self._label_counter)

    def start(self):
        if self._was_started:
            return

        self._points.append({
            'time': time.time(),
            'label': 'start',
        })
        self._was_started = True

    def mark(self, label=None):
        if not self._was_started:
            raise RuntimeError('Nano profiler was not start')

        self._points.append({
            'time': time.time(),
            'label': label or self.get_default_label()
        })

    def get_stat(self):
        if len(self._points) < 2:
            return []

        it = iter(self._points)
        start = next(it)

        previous_time = start['time']
        for index, value in enumerate(it, start=1):
            label = value['label']
            diff_time = value['time'] - previous_time
            yield (index, label, diff_time)
            previous_time = value['time']

    def print_stat(self):
        if not self._was_started:
            return

        stat = self.get_stat()

        print('{:-^80}'.format('Statistic of profiler ' + self.name))
        for index, label, diff in stat:
            print('{}: {} execute in {:0.3f} seconds'.format(index, label, diff))

    def __del__(self):
        self.print_stat()


# Global scope profiler
if globals().get('nano_profiler', None) is None:
    nano_profiler = NanoProfiler('GLOBAL')
