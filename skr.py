from inspect import signature
def fun(a, b):
    print(a)
    print(b)

print(signature(fun))

