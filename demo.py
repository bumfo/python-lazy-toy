from lazy import *

def main():
  x = Var('x')
  y = 2 + x * 3

  print(y)
  print(y.eval(x=3))


if __name__ == '__main__':
  main()
