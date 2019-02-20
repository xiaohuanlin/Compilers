class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<{self.value}>'

    @property
    def reducible(self):
        return False


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'<{self.left} + {self.right}>'

    @property
    def reducible(self):
        return True

    def reduce(self, env):
        # by using reduce function, we can get a new expression
        if self.left.reducible:
            return Add(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return Add(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value + self.right.value)


class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'<{self.left} * {self.right}>'

    @property
    def reducible(self):
        return True

    def reduce(self, env):
        if self.left.reducible:
            return Multiply(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return Multiply(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value * self.right.value)


class Boolean:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<{self.value}>'

    @property
    def reducible(self):
        return False


class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'<{self.left} < {self.right}>'

    @property
    def reducible(self):
        return True

    def reduce(self, env):
        if self.left.reducible:
            return LessThan(self.left.reduce(env), self.right)
        elif self.right.reducible:
            return LessThan(self.left, self.right.reduce(env))
        else:
            return Boolean(self.left.value < self.right.value)


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<{self.name}>'

    @property
    def reducible(self):
        return True

    def reduce(self, env):
        return env[self.name]


class Machine:
    def __init__(self, expression, env=None):
        self.expression = expression
        if env is None:
            env = {}
        self.env = env

    def step(self):
        self.expression = self.expression.reduce(self.env)

    def run(self):
        while self.expression.reducible:
            print(self.expression)
            self.step()
        print(self.expression)

