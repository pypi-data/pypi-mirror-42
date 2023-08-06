# nano_profiler
Extreme simple profiler of time execution of code.
The major goal of `none_profiler` is simple time measure in long chain of code execution,
such as web applications.

## Quick example

```python
from time import sleep

from nano_profiler import NanoProfiler

n_p = NanoProfiler(name='Foo bar baz profiler', autostart=True)

def foo():
    sleep(0.1)
    n_p.mark('Foo')

def bar():
    sleep(0.1)
    n_p.mark('bar')

def baz():
    foo()
    bar()
    n_p.mark('baz')

baz()
```

Output:
```
-------------------Statistic of profiler Foo bar baz profiler-------------------
1: Foo execute in 0.102 seconds
2: bar execute in 0.100 seconds
3: baz execute in 0.000 seconds
```
