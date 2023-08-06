class Lazy:
    def __init__(self, func):
        self.func = func

    def __call__(self):
        try:
            return self.result
        except AttributeError:
            self.result = self.func()
            return self.result
