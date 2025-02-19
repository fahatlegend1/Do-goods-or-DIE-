class Parent:
    def __init__(self, x=10, y=20):
        self.x = x
        self.y = y

class Child(Parent):
    def __init__(self, x=30):  # No default for y
        super().__init__(x, y)  # Calls Parent with x=30, y takes default (y=20)

c = Child()  # Equivalent to Parent(30, 20)
print(c.x, c.y)  # Output: 30 20
