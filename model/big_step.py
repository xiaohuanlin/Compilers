from copy import deepcopy


class Expression:
    pass


class Number(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<{self.value}>'

    def evaluate(self, env):
        # we can't evaluate it to have a valid value, so visit its value property
        return self

    def to_python(self):
        return f'lambda env: {self.value}'


class Boolean(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<{self.value}>'

    def evaluate(self, env):
        return self

    def to_python(self):
        return f'lambda env: {self.value}'


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<{self.name}>'

    def evaluate(self, env):
        return env[self.name]

    def to_python(self):
        return f'lambda env: env["{self.name}"]'


class Add(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'<{self.left} + {self.right}>'

    def evaluate(self, env):
        return Number(self.left.evaluate(env).value + self.right.evaluate(env).value)

    def to_python(self):
        return f'lambda env: ({self.left.to_python()})(env) + ({self.right.to_python()})(env)'


class Multiply(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'<{self.left} * {self.right}>'

    def evaluate(self, env):
        return Number(self.left.evaluate(env).value * self.right.evaluate(env).value)

    def to_python(self):
        return f'lambda env: ({self.left.to_python()})(env) * ({self.right.to_python()})(env)'


class LessThan(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'<{self.left} < {self.right}>'

    def evaluate(self, env):
        left_value = self.left.evaluate(env).value
        right_value = self.right.evaluate(env).value
        return Boolean(left_value < right_value)

    def to_python(self):
        return f'lambda env: ({self.left.to_python()})(env) < ({self.right.to_python()})(env)'


class Statement:
    pass


class DoNothing(Statement):

    def __repr__(self):
        return '<do-nothing>'

    def __eq__(self, other):
        return isinstance(other, DoNothing)

    def evaluate(self, env):
        return env

    def to_python(self):
        return 'lambda env: env'


class Assign(Statement):

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f'<{self.name} = {self.expression}>'

    def evaluate(self, env):
        new_env = deepcopy(env)
        new_env[self.name] = self.expression.evaluate(env)
        return new_env

    def to_python(self):
        return f'lambda env: dict([pair for pair in env.items() if pair[0] != "{self.name}"] + [("{self.name}", ({self.expression.to_python()})(env))])'


class IF(Statement):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self):
        return f'<if {self.condition}: ' \
            f'{self.consequence} ' \
            f'else: {self.alternative}'

    def evaluate(self, env):
        if self.condition.evaluate(env).value is True:
            return self.consequence.evaluate(env)
        else:
            return self.alternative.evaluate(env)

    def to_python(self):
        return f'lambda env: ({self.consequence.to_python()})(env) if ({self.condition.to_python()})(env) else ({self.alternative.to_python()})(env)'


class Sequence(Statement):

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return f'<{self.first}; {self.second}>'

    def evaluate(self, env):
        new_env = self.first.evaluate(env)
        new_env = self.second.evaluate(new_env)
        return new_env

    def to_python(self):
        return f'lambda env: ({self.second.to_python()})(({self.first.to_python()})(env))'


class While(Statement):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'<while {self.condition}: {self.body}>'

    def evaluate(self, env):
        if self.condition.evaluate(env).value is True:
            # just run and change the env, and then do it again
            new_env = self.body.evaluate(env)
            return self.evaluate(new_env)
        else:
            return env

    def to_python(self):
        return f'lambda env: ({self.to_python()})(({self.body.to_python()})(env)) if ({self.condition.to_python()})(env) else env'


class Machine:
    def __init__(self, statement, env=None):
        self.statement = statement
        if env is None:
            env = {}
        self.env = env

    def run(self):
        print(self.statement.evaluate(self.env))
