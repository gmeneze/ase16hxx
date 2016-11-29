import numpy
from collections import defaultdict
from functools import partial
from itertools import chain


def identity(obj):
    """Returns directly the argument *obj*.
    """
    return obj

class Statistics(object):
    """Object that compiles statistics on a list of arbitrary objects.
    When created the statistics object receives a *key* argument that
    is used to get the values on which the function will be computed.
    If not provided the *key* argument defaults to the identity function.
    The value returned by the key may be a multi-dimensional object, i.e.:
    a tuple or a list, as long as the statistical function registered
    support it. So for example, statistics can be computed directly on
    multi-objective fitnesses when using numpy statistical function.
    :param key: A function to access the values on which to compute the
                statistics, optional.

    ::

        >>> s = Statistics()
        >>> s.register("mean", numpy.mean)
        >>> s.register("max", max)
        >>> s.compile([1, 2, 3, 4])
        {'max': 4, 'mean': 2.5}
        >>> s.compile([5, 6, 7, 8])
        {'max': 8, 'mean': 6.5}
    """

    def __init__(self, key=identity):
        self.key = key
        self.functions = dict()
        self.fields = []

    def register(self, name, function, *args, **kargs):
        """Register a *function* that will be applied on the sequence each
        time :meth:`record` is called.
        :param name: The name of the statistics function as it would appear
                     in the dictionnary of the statistics object.
        :param function: A function that will compute the desired statistics
                         on the data as preprocessed by the key.
        :param argument: One or more argument (and keyword argument) to pass
                         automatically to the registered function when called,
                         optional.
        """
        self.functions[name] = partial(function, *args, **kargs)
        self.fields.append(name)

    def compile(self, data):
        """Apply to the input sequence *data* each registered function
        and return the results as a dictionnary.

        :param data: Sequence of objects on which the statistics are computed.
        """
        values = tuple(self.key(elem) for elem in data)

        entry = dict()
        for key, func in self.functions.iteritems():
            entry[key] = func(values)
        return entry


class Logbook(list):
    """Evolution records as a chronological list of dictionaries.
    Data can be retrieved via the :meth:`select` method given the appropriate
    names.
    The :class:`Logbook` class may also contain other logbooks refered to
    as chapters. Chapters are used to store information associated to a
    specific part of the evolution. For example when computing statistics
    on different components of individuals (namely :class:`MultiStatistics`),
    chapters can be used to distinguish the average fitness and the average
    size.
    """

    def __init__(self):
        self.buffindex = 0
        self.chapters = defaultdict(Logbook)
        """Dictionary containing the sub-sections of the logbook which are also
        :class:`Logbook`. Chapters are automatically created when the right hand
        side of a keyworded argument, provided to the *record* function, is a
        dictionnary. The keyword determines the chapter's name. For example, the
        following line adds a new chapter "size" that will contain the fields
        "max" and "mean". ::
            logbook.record(gen=0, size={'max' : 10.0, 'mean' : 7.5})
        To access a specific chapter, use the name of the chapter as a
        dictionnary key. For example, to access the size chapter and select
        the mean use ::
            logbook.chapters["size"].select("mean")
        Compiling a :class:`MultiStatistics` object returns a dictionary
        containing dictionnaries, therefore when recording such an object in a
        logbook using the keyword argument unpacking operator (**), chapters
        will be automatically added to the logbook.
        ::

            >>> fit_stats = Statistics(key=attrgetter("fitness.values"))
            >>> size_stats = Statistics(key=len)
            >>> mstats = MultiStatistics(fitness=fit_stats, size=size_stats)
            >>> # [...]
            >>> record = mstats.compile(population)
            >>> logbook.record(**record)
            >>> print logbook
              fitness          length
            ------------    ------------
            max     mean    max     mean
            2       1       4       3
        """

        self.columns_len = None
        self.header = None
        """Order of the columns to print when using the :data:`stream` and
        :meth:`__str__` methods. The syntax is a single iterable containing
        string elements. For example, with the previously
        defined statistics class, one can print the generation and the
        fitness average, and maximum with
        ::
            logbook.header = ("gen", "mean", "max")

        If not set the header is built with all fields, in arbritrary order
        on insertion of the first data. The header can be removed by setting
        it to :data:`None`.
        """

        self.log_header = True
        """Tells the log book to output or not the header when streaming the
        first line or getting its entire string representation. This defaults
        :data:`True`.
        """

    def record(self, **infos):
        """Enter a record of event in the logbook as a list of key-value pairs.
        The informations are appended chronogically to a list as a dictionnary.
        When the value part of a pair is a dictionnary, the informations contained
        in the dictionnary are recorded in a chapter entitled as the name of the
        key part of the pair. Chapters are also Logbook.
        """
        for key, value in infos.items():
            if isinstance(value, dict):
                self.chapters[key].record(**value)
                del infos[key]
        self.append(infos)

    def select(self, *names):
        """Return a list of values associated to the *names* provided
        in argument in each dictionary of the Statistics object list.
        One list per name is returned in order.
        ::
            >>> log = Logbook()
            >>> log.record(gen = 0, mean = 5.4, max = 10.0)
            >>> log.record(gen = 1, mean = 9.4, max = 15.0)
            >>> log.select("mean")
            [5.4, 9.4]
            >>> log.select("gen", "max")
            ([0, 1], [10.0, 15.0])
        With a :class:`MultiStatistics` object, the statistics for each
        measurement can be retrieved using the :data:`chapters` member :
        ::
            >>> log = Logbook()
            >>> log.record(**{'gen' : 0, 'fit' : {'mean' : 0.8, 'max' : 1.5},
            ... 'size' : {'mean' : 25.4, 'max' : 67}})
            >>> log.record(**{'gen' : 1, 'fit' : {'mean' : 0.95, 'max' : 1.7},
            ... 'size' : {'mean' : 28.1, 'max' : 71}})
            >>> log.chapters['size'].select("mean")
            [25.4, 28.1]
            >>> log.chapters['fit'].select("gen", "max")
            ([0, 1], [1.5, 1.7])
        """
        if len(names) == 1:
            return [entry.get(names[0], None) for entry in self]
        return tuple([entry.get(name, None) for entry in self] for name in names)

    @property
    def stream(self):
        """Retrieve the formatted not streamed yet entries of the database
        including the headers.
        ::
            >>> log = Logbook()
            >>> log.append({'gen' : 0})
            >>> print log.stream
            gen
              0
            >>> log.append({'gen' : 1})
            >>> print log.stream
              1
        """
        startindex, self.buffindex = self.buffindex, len(self)
        return self.__str__(startindex)

    def __delitem__(self, key):
        if isinstance(key, slice):
            for i, in range(*key.indices(len(self))):
                self.pop(i)
                for chapter in self.chapters.values():
                    chapter.pop(i)
        else:
            self.pop(key)
            for chapter in self.chapters.values():
                chapter.pop(key)

    def pop(self, index=0):
        """Retrieve and delete element *index*. The header and stream will be
        adjusted to follow the modification.
        :param item: The index of the element to remove, optional. It defaults
                     to the first element.

        You can also use the following syntax to delete elements.
        ::

            del log[0]
            del log[1::5]
        """
        if index < self.buffindex:
            self.buffindex -= 1
        return super(self.__class__, self).pop(index)

    def __txt__(self, startindex):
        columns = self.header
        if not columns:
            columns = sorted(self[0].keys()) + sorted(self.chapters.keys())
        if not self.columns_len or len(self.columns_len) != len(columns):
            self.columns_len = map(len, columns)

        chapters_txt = {}
        offsets = defaultdict(int)
        for name, chapter in self.chapters.items():
            chapters_txt[name] = chapter.__txt__(startindex)
            if startindex == 0:
                offsets[name] = len(chapters_txt[name]) - len(self)

        str_matrix = []
        for i, line in enumerate(self[startindex:]):
            str_line = []
            for j, name in enumerate(columns):
                if name in chapters_txt:
                    column = chapters_txt[name][i + offsets[name]]
                else:
                    value = line.get(name, "")
                    string = "{0:n}" if isinstance(value, float) else "{0}"
                    column = string.format(value)
                self.columns_len[j] = max(self.columns_len[j], len(column))
                str_line.append(column)
            str_matrix.append(str_line)

        if startindex == 0 and self.log_header:
            header = []
            nlines = 1
            if len(self.chapters) > 0:
                nlines += max(map(len, chapters_txt.values())) - len(self) + 1
            header = [[] for i in xrange(nlines)]
            for j, name in enumerate(columns):
                if name in chapters_txt:
                    length = max(len(line.expandtabs()) for line in chapters_txt[name])
                    blanks = nlines - 2 - offsets[name]
                    for i in xrange(blanks):
                        header[i].append(" " * length)
                    header[blanks].append(name.center(length))
                    header[blanks + 1].append("-" * length)
                    for i in xrange(offsets[name]):
                        header[blanks + 2 + i].append(chapters_txt[name][i])
                else:
                    length = max(len(line[j].expandtabs()) for line in str_matrix)
                    for line in header[:-1]:
                        line.append(" " * length)
                    header[-1].append(name)
            str_matrix = chain(header, str_matrix)

        template = "\t".join("{%i:<%i}" % (i, l) for i, l in enumerate(self.columns_len))
        text = [template.format(*line) for line in str_matrix]

        return text

    def __str__(self, startindex=0):
        text = self.__txt__(startindex)
        return "\n".join(text)

