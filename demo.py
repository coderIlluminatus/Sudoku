from copy import copy

class c(object):
    def __init__(self):
        self.a = 9

    def recur(self, level):
        x, y = copy(self), copy(self)
        if self.a > 1:
            x.a -= 1
            y.a -= 2
            return x.recur(level) + y.recur(level)
        else:
            return self.a


x = c()
print(x.recur(1))