class Lazy:
  def __add__(self, o):
    return Add(self, o)

  def __radd__(self, o):
    return Add(o, self)

  def __sub__(self, o):
    return Sub(self, o)

  def __rsub__(self, o):
    return Sub(o, self)

  def __mul__(self, o):
    return Mul(self, o)

  def __rmul__(self, o):
    return Mul(o, self)

  def __truediv__(self, o):
    return TrueDiv(self, o)

  def __rtruediv__(self, o):
    return TrueDiv(o, self)

  def eval(self, **kwargs):
    raise NotImplementedError()


def evaluate(o, **kwargs):
  if isinstance(o, Lazy):
    return o.eval(**kwargs)
  else:
    return o


class Add(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} + {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) + evaluate(self.b, **kwargs)


class Sub(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} - {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) - evaluate(self.b, **kwargs)


class Mul(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} * {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) * evaluate(self.b, **kwargs)


class TrueDiv(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} / {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) / evaluate(self.b, **kwargs)


class Num(Lazy):
  def __init__(self, v):
    super().__init__()
    self.v = v

  def __str__(self):
    return f'{self.v}'

  def eval(self, **kwargs):
    return self.v


class LazyNoSuchVariableException(Exception):
  def __init__(self, message):
    super().__init__(message)


class Var(Lazy):
  def __init__(self, name):
    super().__init__()
    self.name = name

  def __str__(self):
    return f'{self.name}'

  def eval(self, **kwargs):
    try:
      return kwargs[self.name]
    except KeyError:
      raise LazyNoSuchVariableException(f'variable "{self.name}" not found')
