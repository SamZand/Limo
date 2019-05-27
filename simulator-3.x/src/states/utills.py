class Enum:
    def __init__(self, *args):
        for var in args:
            var = var.upper()
            setattr(self, var, var)
