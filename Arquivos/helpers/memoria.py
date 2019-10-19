class Memoria:
    def __init__(self, size):
        self.data = [False]*size
        self.size = size

        self.data[0] = I_node(None, 'r', 1, node_type='dir')

    def add_file(self, index, file):
        if self.check_storage(file.size):
            pass

    def check_storage(self, filesize):
        if self.data.count(False) >= filesize:
            return True
        return False

    def allocate(self, file):
        pass

        return indexes

    def deallocate(self, index, file):
        pass

    def find_node(self, node):
        return 1
