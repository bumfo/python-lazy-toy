from lazy import *

def main():
  x = Var('x')
  y = Var('y')
  f = Var('f')
  f = Func('f', If(x > 0, y + f(x=x - 1), 0))

  print(f(x=5))
  print(f(x=5).partial())

  print()

  fact = Var('fact')
  fact = Func('fact', If(x > 1, x * fact(x=x - 1), 1))

  print(fact())
  print(fact().partial())
  print(fact().partial().eval(x=5))


if __name__ == '__main__':
  main()
