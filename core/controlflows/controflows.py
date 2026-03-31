from .if_block import IfBlock
from .do_block import DoBlock
from .do_while_block import DoWhileBlock
from sapdl.core.ast import CommandNode


class Controlflows:

    def if_block(self):
        return IfBlock(self)

    def do_block(self, start, end, step=1, var=None):
        return DoBlock(self, var, start, end, step)

    def do_while(self, condition):
        return DoWhileBlock(self, condition)

    def range(self, start, end, step=1, var=None):
        with DoBlock(self, var, start, end, step) as i:
            yield i

    def continue_(self):
        self.body.add(CommandNode("*CYCLE"))

    def break_(self):
        self.body.add(CommandNode("*EXIT"))
