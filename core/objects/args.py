class Arg:

    def __init__(self, index):
        self.index = index

    def __str__(self):
        if self.index <= 9:
            return f"arg{self.index}"
        elif self.index <= 19:
            return f"ar{self.index}"


class Args:

    index = 1

    def next_arg(self):
        if self.index > 19:
            raise ValueError(
                "Args only supports up to 19 arguments (arg1-arg9, ar10-ar19)"
            )
        arg = Arg(self.index)
        self.index += 1
        return arg
