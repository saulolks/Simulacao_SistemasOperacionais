class I_node:
    def __init__(self, date, name, size, node_type, head = -1):
        self.date = date
        self.name = name
        self.size = size
        self.node_type = node_type
        self.head = head
        self.indexes = []
    
    def __repr__(self):
        return self.node_type + " " + self.name
