from .if_block import IfBlock
from .do_block import DoBlock


class Controlflows:

    def if_block(self):
        return IfBlock(self)

    def do_block(self, start, end, step=1, var="i"):
        return DoBlock(self, var, start, end, step)

    def range(self, start, end, step=1, var="i"):
        with DoBlock(self, var, start, end, step) as i:
            yield i
