from copy import deepcopy


class Expression:
    pass


class Number(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<{self.value}>'

    @property
    def reducible(self):
        return False


class Boolean(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<{self.value}>'

    @property
    def reducible(self):
        return False


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<{self.name}>'

    @property
    def reducible(self):
        return True

    def reduce(self, env):
        return env[self.name]


class Add(Expression):
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


class Multiply(Expression):
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


class LessThan(Expression):
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


class Statement:
    pass


class DoNothing(Statement):

    def __repr__(self):
        return '<do-nothing>'

    def __eq__(self, other):
        return isinstance(other, DoNothing)

    @property
    def reducible(self):
        return False


class Assign(Statement):

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f'<{self.name} = {self.expression}>'

    @property
    def reducible(self):
        return True

    def reduce(self, env):
        if self.expression.reducible:
            return Assign(self.name, self.expression.reduce(env)), env
        else:
            new_env = deepcopy(env)
            new_env[self.name] = self.expression

            return DoNothing(), new_env


class IF(Statement):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self):
        return f'<if {self.condition}: ' \
            f'{self.consequence} ' \
            f'else: {self.alternative}'

    @property
    def reducible(self):
        return True

    def reduce(self, env):
        if self.condition.reducible:
            return IF(self.condition.reduce(env), self.consequence, self.alternative), env
        else:
            if self.condition.value is True:
                return self.consequence, env
            else:
                return self.alternative, env


class Sequence(Statement):

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return f'<{self.first}; {self.second}>'

    @property
    def reducible(self):
        return True

    def reduce(self, env):
        if isinstance(self.first, DoNothing):
            return self.second, env
        else:
            reduced_first, env = self.first.reduce(env)
            return Sequence(reduced_first, self.second), env


class While(Statement):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'<while {self.condition}: {self.body}>'

    @property
    def reducible(self):
        return True

    def reduce(self, env):
        # just do once IF statement and make it again with env changed
        return IF(self.condition, Sequence(self.body, self), DoNothing()), env


class ExpressionMachine:
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


class StatementMachine:
    def __init__(self, statement, env=None):
        self.statement = statement
        if env is None:
            env = {}
        self.env = env

    def step(self):
        self.statement, self.env = self.statement.reduce(self.env)

    def run(self):
        while self.statement.reducible:
            print(self.statement)
            print(self.env)
            self.step()
        print(self.statement)
        print(self.env)
