def f(func):
    def adder(a):
        return func() + a
    return adder

@f
def g():
    return 100

a = g(100)
b = g(10.0)
print(a)
print(b)