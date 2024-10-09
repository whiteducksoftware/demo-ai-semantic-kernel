class MyModel:
    def __init__(self):
        self.x = 0
        self.y = 0

    def set_fib(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"MyModel(x={self.x}, y={self.y})"
