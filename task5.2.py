from math import gcd
import sys


class Rational:
    def __init__(self, n=0, d=1):
        if isinstance(n, Rational):
            self._n, self._d = n._n, n._d
            return
        if isinstance(n, str):
            n = n.strip()
            if '/' in n:
                a, b = n.split('/')
                n, d = int(a), int(b)
            else:
                n, d = int(n), 1
        n, d = int(n), int(d)
        if d == 0:
            raise ValueError("Знаменник = 0")
        if d < 0:
            n, d = -n, -d
        g = gcd(abs(n), d)
        self._n, self._d = n // g, d // g

    def __call__(self):
        return self._n / self._d

    def __getitem__(self, key):
        if key == 'n': return self._n
        if key == 'd': return self._d
        raise KeyError(key)

    def __setitem__(self, key, v):
        v = int(v)
        if key == 'n': self.__init__(v, self._d)
        elif key == 'd': self.__init__(self._n, v)
        else: raise KeyError(key)

    def __repr__(self):
        return str(self._n) if self._d == 1 else f"{self._n}/{self._d}"

    def _coerce(self, other):
        return other if isinstance(other, Rational) else Rational(other)

    def __add__(self, o):
        o = self._coerce(o)
        return Rational(self._n * o._d + o._n * self._d, self._d * o._d)
    def __radd__(self, o): return self.__add__(o)

    def __sub__(self, o):
        o = self._coerce(o)
        return Rational(self._n * o._d - o._n * self._d, self._d * o._d)
    def __rsub__(self, o): return Rational(o).__sub__(self)

    def __mul__(self, o):
        o = self._coerce(o)
        return Rational(self._n * o._n, self._d * o._d)
    def __rmul__(self, o): return self.__mul__(o)

    def __truediv__(self, o):
        o = self._coerce(o)
        return Rational(self._n * o._d, self._d * o._n)
    def __rtruediv__(self, o): return Rational(o).__truediv__(self)


class RationalList:
    def __init__(self, items=None):
        self._data = [self._r(x) for x in (items or [])]

    @staticmethod
    def _r(x):
        return x if isinstance(x, Rational) else Rational(x)

    def __len__(self): return len(self._data)
    def __getitem__(self, i): return self._data[i]
    def __setitem__(self, i, v): self._data[i] = self._r(v)

    def __add__(self, o):
        res = RationalList(self._data)
        if isinstance(o, RationalList): res._data.extend(o._data)
        else: res._data.append(self._r(o))
        return res

    def __iadd__(self, o):
        if isinstance(o, RationalList): self._data.extend(o._data)
        else: self._data.append(self._r(o))
        return self

    def __repr__(self):
        return f"[{', '.join(str(x) for x in self._data)}]"

    def sum(self):
        s = Rational(0)
        for x in self._data:
            s = s + x
        return s


def process(path):
    total = RationalList()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                row = RationalList()
                for t in line.split():
                    row += Rational(t)
                total += row
    s = total.sum()
    print(f"{path}: {s} ≈ {s():.6f}")


if __name__ == '__main__':
    files = sys.argv[1:] if len(sys.argv) > 1 else ["input01.txt", "input02.txt", "input03.txt"]
    for f in files:
        process(f)
