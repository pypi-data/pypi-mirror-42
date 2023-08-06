


class Makefile:
    """Abstracts the construction of the project Makefile."""

    @property
    def variables(self):
        return sorted(self._variables, key=lambda x: x['name'])

    def __init__(self, assembler, spec):
        self.assembler = assembler
        self.spec = spec
        self.targets = {}
        self._variables = []
        assembler.notify('setup_makefile', self)

    def setvariable(self, name, default):
        """Sets a global variable for the Makefile."""
        self._variables.append({'name': name, 'default': default})

    def target(self, name):
        """Add a new target to the Makefile and return a
        :class:`Target` instance.
        """
        if name not in self.targets:
            self.targets[name] = Target(self.assembler, self, name)
        return self.targets[name]

    def __iter__(self):
        for k in sorted(self.targets.keys()):
            yield self.targets[k]


class Target:
    """Represents a target in the project Makefile."""

    def __init__(self, assembler, make, name):
        self.assembler = assembler
        self.make = make
        self.name = name
        self.statements = []
        assembler.notify(f'setup_makefile_target', make, self)
        assembler.notify(f'setup_makefile_target_{name.replace("-", "_")}',
            make, self)

    def execute(self, stmt):
        """Instruct the target to execute the specified statement."""
        if isinstance(stmt, (str, list)):
            stmt = BashStatement(stmt)
        self.statements.append(stmt)

    def __iter__(self):
        return iter(self.statements)

    def __str__(self):
        return '\n\t'.join(map(str, self))


class BashStatement:
    """Represents a single bash statement, that may be compiled over
    multiple lines.
    """

    def __init__(self, stmt):
        self.stmt = stmt if isinstance(stmt, list) else [stmt]

    def __str__(self):
        return '\n\t'.join(self.stmt)
