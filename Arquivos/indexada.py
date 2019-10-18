class I_node:
    def __init__(self, date, name, size, node_type):
        self.date = date
        self.name = name
        self.size = size
        self.node_type = node_type
        self.indexes = []

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

class OS:
    def __init__(self, memory_size):
        self.root = {'r': {}}
        self.current = self.root['r']
        self.wayback = "/r/"
        self.index_wayback = [0]
        self.memory = Memoria(memory_size)
        self.pointer = 0
    
    def cd(self, node):
        if node == "..":
            print(self.wayback)
            nodes = self.wayback.split('/')[1:-2]
            new_wayback = "/"
            print(nodes)

            try:
                self.current = self.root
                for item in nodes:
                    new_wayback = new_wayback + str(item) + "/"
                    self.current = self.current[item]
                self.wayback = new_wayback
                self.index_wayback.pop()
            except KeyError:
                print("O diretório não existe!")
        else:
            nodes = node.split('/')
            
            try:
                for item in nodes:
                    self.current = self.current[item]
                    self.pointer = self.memory.find_node(item)
                    self.wayback = self.wayback + str(item) + "/"
                    self.index_wayback.append(self.pointer)
            except KeyError:
                print("O diretório não existe!")
        
        return self.wayback

    def mkdir(self, node):
        inode = I_node(date=None, name=node, size=1, node_type="dir")
        
        if '/' not in node and node not in self.current \
            and self.memory.add_file(self.pointer, inode):
            self.current[node] = {}
        else:
            print("O nome do diretório é inválido!")
    
    def ls(self):
        text = ""
        for a in self.current:
            text += a + " "
        print(text)
    
    def rm(self, node):
        if node in self.current:
            if self.memory.deallocate(self.pointer, node):
                del self.current[node]
    
    def info(self):
        text = f"""
        wayback: {self.wayback}
        indexes: {self.index_wayback}
        root: {self.root}
        current: {self.current}
        
        """
        return text

info = "\nuser@os:~"
text = info + "r/$ "
command = ""
opsystem = OS(memory_size=512)

while command != "exit":
    command = input(text)

    inputs = command.split(" ")
    
    if inputs[0] == "cd":
        text = info + opsystem.cd(inputs[1]) + "$ "
    elif inputs[0] == "ls":
        opsystem.ls()
    elif inputs[0] == "mkdir":
        print("mkdir")
        opsystem.mkdir(inputs[1])
    
    print(opsystem.info())

