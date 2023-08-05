from enum import Enum, auto
from .is_definition import isdefinition
from .logging import warning, error
from .passes import DefinitionPass


class MultipleDefinitionException(Exception):
    pass


class UniquificationMode(Enum):
    WARN = auto()
    ERROR = auto()
    UNIQUIFY = auto()


class UniquificationPass(DefinitionPass):
    def __init__(self, main, mode):
        super(UniquificationPass, self).__init__(main)
        self.mode = mode
        self.seen = {}
        self.original_names = {}

    def __call__(self, definition):
        name = definition.name
        key = hash(definition)
        insert = False
        if name not in self.seen:
            self.seen[name] = {}
            insert = True
        elif self.mode is UniquificationMode.UNIQUIFY:
            seen = self.seen[name]
            if key in seen:
                new_name = seen[key].name
                insert = False
            else:
                idx = len(seen)
                new_name = name + "_unq" + str(idx)
                insert = True
            self.original_names[definition] = name
            type(definition).rename(definition, new_name)
        else:
            insert = True
        if insert:
            self.seen[name][key] = definition

    def _run(self, definition):
        if not isdefinition(definition):
            return

        for instance in definition.instances:
            instancedefinition = type(instance)
            if isdefinition(instancedefinition):
                self._run( instancedefinition )

        self(definition)

    def run(self):
        super(UniquificationPass, self).run()
        duplicated = []
        for name, definitions in self.seen.items():
            if len(definitions) > 1:
                duplicated.append((name, definitions))
        UniquificationPass.handle(duplicated, self.mode)

    @staticmethod
    def handle(duplicated, mode):
        if len(duplicated):
            msg = f"Multiple definitions: {[name for name, _ in duplicated]}"
            if mode is UniquificationMode.ERROR:
                error(msg)
                raise MultipleDefinitionException([name for name, _ in duplicated])
            elif mode is UniquificationMode.WARN:
                warning(msg)


# This pass runs uniquification according to @mode and returns a dictionary
# mapping any renamed circuits to their original names. If @mode is ERROR or
# WARN the returned dictionary should be empty.
def uniquification_pass(circuit, mode):
    pass_ = UniquificationPass(circuit, mode)
    pass_.run()
    return pass_.original_names
