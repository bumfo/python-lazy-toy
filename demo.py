from lazy import *

def main():
  x = Var('x')
  f = Var('f')
  f = Func('f', If(x > 1, x * f(x=x - 1), 1))

  print(f(x=5))
  print(f(x=5).eval())
  print(f())
  print(f().partial())
  print(f().partial().eval(x=5))


if __name__ == '__main__':
  main()
