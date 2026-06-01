from math import gcd


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


def eval_expr(line):
    tokens = line.split()
    vals, i = [], 0
    while i < len(tokens):
        if tokens[i] in ('+', '-'):
            vals.append(tokens[i]); i += 1
        else:
            v = Rational(tokens[i]); i += 1
            while i < len(tokens) and tokens[i] in ('*', '/'):
                op = tokens[i]; i += 1
                r = Rational(tokens[i]); i += 1
                v = v * r if op == '*' else v / r
            vals.append(v)
    res = vals[0]
    for j in range(1, len(vals), 2):
        res = res + vals[j+1] if vals[j] == '+' else res - vals[j+1]
    return res


if __name__ == '__main__':
    with open("input01.txt") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if line:
                r = eval_expr(line)
                print(f"{i}: {r} ≈ {r():.6f}")
