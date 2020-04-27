class Lazy:
  def __eq__(self, o):
    return Eq(self, o)

  def __ne__(self, o):
    return Ne(self, o)

  def __lt__(self, o):
    return Lt(self, o)

  def __le__(self, o):
    return Le(self, o)

  def __gt__(self, o):
    return Gt(self, o)

  def __ge__(self, o):
    return Ge(self, o)

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

  def __call__(self, **kwargs):
    return Call(self, kwargs)

  def eval(self, **kwargs):
    raise NotImplementedError()

  def partial(self, **kwargs):
    return self.eval(__partial__=True, **kwargs)


def evaluate(o, **kwargs):
  if isinstance(o, Lazy):
    return o.eval(**kwargs)
  else:
    return o


def partial_evaluate(o, **kwargs):
  return evaluate(o, __partial__=True, **kwargs)


class Func(Lazy):
  def __init__(self, name, expr):
    super().__init__()
    self.name = name
    self.expr = expr

  def __str__(self):
    return f'{self.name}'

  def eval(self, **kwargs):
    return evaluate(self.expr, **kwargs)


class Call(Lazy):
  def __init__(self, callable, kwargs):
    super().__init__()
    self.callable = callable
    self.kwargs = kwargs

  def __str__(self):
    str_kwargs = ', '.join(map(lambda x: f'{x[0]}={x[1]}', self.kwargs.items()))
    return f'{self.callable}({str_kwargs})'

  def eval(self, **kwargs):
    return evaluate(partial_evaluate(self.callable, **self.kwargs), **kwargs)


class If(Lazy):
  def __init__(self, expr, expr_true, expr_false):
    super().__init__()
    self.expr = expr
    self.expr_true = expr_true
    self.expr_false = expr_false

  def __str__(self):
    return f'If({self.expr}, {self.expr_true}, {self.expr_false})'

  def eval(self, **kwargs):
    return evaluate(self.expr_true, **kwargs) if evaluate(self.expr, **kwargs) else evaluate(self.expr_false, **kwargs)


class Eq(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} == {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) == evaluate(self.b, **kwargs)


class Ne(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} != {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) != evaluate(self.b, **kwargs)


class Lt(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} < {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) < evaluate(self.b, **kwargs)


class Le(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} <= {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) <= evaluate(self.b, **kwargs)


class Gt(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} > {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) > evaluate(self.b, **kwargs)


class Ge(Lazy):
  def __init__(self, a, b):
    super().__init__()
    self.a = a
    self.b = b

  def __str__(self):
    return f'({self.a} >= {self.b})'

  def eval(self, **kwargs):
    return evaluate(self.a, **kwargs) >= evaluate(self.b, **kwargs)


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


class LazySelfReference(Exception):
  def __init__(self, message):
    super().__init__(message)


class Var(Lazy):
  def __init__(self, name):
    super().__init__()
    self.name = name

  def __str__(self):
    return f'{self.name}'

  def eval(self, __partial__=False, **kwargs):
    try:
      val = kwargs[self.name]
      if val is self:
        raise LazySelfReference(f'variable self reference on {self.name}')
      return evaluate(val, __partial__=__partial__, **kwargs)
    except KeyError:
      pass

    if __partial__:
      return self
    else:
      raise LazyNoSuchVariableException(f'variable "{self.name}" not found')
