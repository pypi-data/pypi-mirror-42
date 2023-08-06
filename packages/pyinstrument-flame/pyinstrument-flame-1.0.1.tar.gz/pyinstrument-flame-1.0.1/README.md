
Provides a FlameGraphRenderer for pyinstrument.

Uses Brendan Gregg's flamegraph.pl in the backend to render an interactive SVG.

Example usage:

```python
import pyinstrument
import pyinstrument_flame

with pyinstrument.Profiler() as profiler:
    # do stuff

renderer = pyinstrument_flame.FlameGraphRenderer(title = "Task profile", flamechart=True)
svg = profiler.output(renderer)
```

See the flamegraph.pl documentation for all renderer options.

