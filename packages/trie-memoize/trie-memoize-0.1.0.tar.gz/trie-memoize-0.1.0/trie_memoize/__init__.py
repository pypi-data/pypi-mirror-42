import functools


def get_cache(cache_types):
    depth = len(cache_types)
    base_cache = cache_types[0]()

    if depth == 1:
        def getter(args):
            return base_cache[args[0]]

        def setter(args, value):
            base_cache[args[0]] = value
            return value
    elif depth == 2:
        def getter(args):
            base = base_cache[args[0]]
            return base[args[1]]

        def setter(args, value):
            try:
                base = base_cache[args[0]]
            except KeyError:
                map = cache_types[1]()
                base_cache[args[0]] = map
                base = map
            finally:
                base[args[1]] = value

            return value
    else:
        def getter(args):
            node = base_cache
            for arg in args:
                node = node[arg]
            return node

        def setter(args, value):
            node = base_cache

            for i in range(depth - 1):
                arg = args[i]

                try:
                    map = node[arg]
                except KeyError:
                    map = cache_types[i]()
                    node[arg] = map
                finally:
                    node = map

            node[args[-1]] = value
            return value

    return [getter, setter]


def memoize(*cache_types):
    [get, set] = get_cache(cache_types)

    def wrapper(fn):
        @functools.wraps(fn)
        def call(*args, **kwargs):
            try:
                return get(args)
            except KeyError:
                return set(args, fn(*args, **kwargs))
        return call

    return wrapper


