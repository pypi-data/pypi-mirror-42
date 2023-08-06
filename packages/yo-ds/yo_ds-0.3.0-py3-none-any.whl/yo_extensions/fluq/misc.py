from yo_core import *

def strjoin(separator: str) -> Callable[[Queryable],str]:
    return lambda en: separator.join(Query.en(en).select(str))



class count_by(Callable[[Queryable[T]],Queryable[KeyValuePair[T,int]]]):
    def __init__(self,selector):
        self.selector = selector
    def __call__(self,en):
        return en.group_by(self.selector).select(lambda z: KeyValuePair(z.key,len(z.value)))


class pairwise(Callable[[Queryable[T]],Queryable[Tuple[T,T]]]):
    def __init__(self):
        pass

    def _make(self, en):
        old = None
        firstTime = True
        for e in en:
            if not firstTime:
                yield (old, e)
            old = e
            if firstTime:
                firstTime = False

    def __call__(self, en):
        return Queryable(self._make(en))


