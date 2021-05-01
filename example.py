from main import Arity, with_arity


class A(metaclass = Arity):
    def __init__(self, secret = 42):
        self.secret = secret

    @with_arity
    def foo(self, a):
        return a + self.secret

    @foo
    def foo(self, a, b):
        return a + b

assert A().foo(3) == 45
assert A().foo(3, 5) == 8

assert A.foo(A(58), 42) == 100

