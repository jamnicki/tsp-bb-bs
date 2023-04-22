class Node(object):
    def __init__(self, level=None, path=None, bound=None):
        self.level = level
        self.path = path
        self.bound = bound

    # def __cmp__(self, other):
    #     return cmp(self.bound, other.bound)

    def __eq__(self, other):
        return self.bound == other.bound

    def __le__(self, other):
        return self.bound <= other.bound

    def __lt__(self, other):
        return self.bound < other.bound

    def __ge__(self, other):
        return self.bound >= other.bound

    def __gt__(self, other):
        return self.bound > other.bound

    def __str__(self):
        return str(tuple([self.level, self.path, self.bound]))
