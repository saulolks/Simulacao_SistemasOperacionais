class Disco:
    def __init__(self, size):
        self.cylinder = [] * size
        self.pointer = 0
        self.direction = True
        self.row = []
        self.found = [0] * size
        self.size = size

        self.run()

    def find(self, item):
        self.row.append(item)
        if self.found[item]:
            aux = self.found[item]
            self.found[item] = 0
            return aux

    def run(self):
        while True:
            if self.row:
                self.search()
    
    def search(self):
        if self.direction:
            for i in range(self.pointer, self.size):
                if i in self.row:
                    self.found[i] = self.cylinder[i]
                    self.row.remove(i)
                self.direction = False if i+1 == self.size else True
        else:
            for i in range(self.size, self.pointer, -1):
                if i in self.row:
                    self.found[i] = self.cylinder[i]
                    self.row.remove(i)
                self.direction = True if i-1 == 0 else False
