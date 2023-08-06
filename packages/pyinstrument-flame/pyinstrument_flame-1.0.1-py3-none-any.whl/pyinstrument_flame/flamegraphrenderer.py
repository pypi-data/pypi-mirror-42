from .flamegraph import flamegraph

class FlameGraphRenderer:

    def __init__(self, title: str = None, subtitle: str = None, width: int = 1200,
                   height: int = 16, minwidth: float = 0.1, fonttype: str = "sans-serif", fontsize: int = 12,
                   countname: str = "us", nametype: str = "Function:", colors: str = "hot", bgcolors: str = "yellow",
                   hash: bool = False, reverse: bool = False, inverted: bool = False, flamechart: bool = False,
                   negate: bool = False, notes: str = None):
        """
        A Python binding for flamegraph.pl and pyinstrument profiles.

        :param outstream:  the output text stream
        :param session:    the ProfilerSession instance returned by Profiler.stop()

        :param subtitle:   second level title (optional)
        :param width:      width of image (default 1200)
        :param height:     height of each frame (default 16)
        :param minwidth:   omit smaller functions (default 0.1 pixels)
        :param fonttype:   font type (default " erdana")
        :param fontsize:   font size (default 12)
        :param countname:  count type label (default "samples")
        :param nametype:   name type label (default " unction:")
        :param colors:     set color palette. choices are: hot (default), mem, io, wakeup, chain, java, js, perl, red, green, blue, aqua, yellow, purple, orange
        :param bgcolors:   set background colors. gradient choices are yellow (default), blue, green, grey; flat colors use "#rrggbb"
        :param hash:       colors are keyed by function name hash
        :param cp:         use consistent palette (palette.map)
        :param reverse:    generate stack-reversed flame graph
        :param inverted:   icicle graph
        :param flamechart: produce a flame chart (sort by time, do not merge stacks)
        :param negate:     switch differential hues (blue<->red)
        :param notes:      add notes comment in SVG (for debugging)

        :returns: None
        """
        kwargs = {k: v for k, v in locals().items() if k not in  ("self",)}

        for k, v in flamegraph.__annotations__.items():
            if kwargs.get(k) is None:
                continue
            if not isinstance(kwargs[k], v):
                raise ValueError("{} is of type {}, expected {}".format(k, type(locals()[k]), v))

        params = []
        for k, v in kwargs.items():
            if v is None or v is False:
                continue
            if v is True:
                params.append('--{}'.format(k))
            else:
                params.extend(['--{}'.format(k), str(v)])

        self.params = params

    def render(self, session):
        return flamegraph(session, self.params)

    def default_processors(self):
        return [
            processors.remove_importlib,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
        ]

