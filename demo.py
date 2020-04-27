from lazy import *

def main():
  x = Var('x')
  y = Var('y')

  z = 2 + x * y
  print(z)

  u = z.partial(y=3)
  print(u)
  
  print(u.eval(x=4))


if __name__ == '__main__':
  main()
