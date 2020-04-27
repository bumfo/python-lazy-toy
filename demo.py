from lazy import *

def main():
  x = Var('x')
  y = Var('y')
  z = Var('z')

  f = Func('f', x + y * z)
  print(f)

  a = Var('a')

  g = Func('g', f(x=1, y=2, z=a) + f(x=a, y=3, z=5))
  print(g)
  print(g(a=-1))

  print(g.partial())


if __name__ == '__main__':
  main()
