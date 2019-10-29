
class global_():
    def __init__(self):
        self.x = {}

    def a(self):

        self.x['a'] = 1

    def b(self):

        self.x['b'] = 2

    def main(self):
        self.a()
        self.b()
        print(self.x)


if __name__ == "__main__":
    g = global_()
    g.main()
