from lazy import *

def main():
  x = Var('x')
  y = If(x != 0, 10, 20)
  print(y)
  print(y.eval(x=0))
  print(y.eval(x=1))


if __name__ == '__main__':
  main()
