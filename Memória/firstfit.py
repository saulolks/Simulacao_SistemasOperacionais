class Memory:
    def __init__(self, size):
        self.size = size
        if size > 0:
            self.__data = [None] * size
            self.bitmap = [0] * size
            self.map = {}
            self.show()
        else: 
            raise Exception("Size must be a positive scalar!")
    
    def allocate(self, tag, space):
        i = -1
        index = -1
        
        while i < self.size-1:
            i += 1
            if self.bitmap[i] == 0:
                free = 0
                for j in range(i, self.size):
                    #print(free, self.bitmap[i], self.bitmap[j])
                    if self.bitmap[j] == 0:
                        free += 1
                    else:
                        free = 0
                        i = j
                        break
                    if free == space:
                        index = i
                        i = self.size
                        break
        
        if index < 0:
            print(f"Full memory to allocate {space}MB to {tag}!")
            print("Trying to compact memory...")
            
            if self.bitmap.count(0) >= space:
                self.compact()
                self.allocate(tag, space)
        else:
            for i in range(index, index+space):
                self.__data[i] = tag
                self.bitmap[i] = 1
                
            self.map[tag] = space
            print("Allocating", space, "MB to", tag)
            self.show()
    
    def deallocate(self, tag):
        aux = False
        for i in range(self.size):
            if self.__data[i] == tag:
                aux = True
                self.__data[i] = None
                self.bitmap[i] = 0
        
        if aux:
            del self.map[tag]
            print("Deallocating ", tag)
            self.show()
    
    def compact(self):
        count = 0

        while 0 in self.bitmap:
            self.bitmap.remove(0)
            self.__data.remove(None)
            count += 1

        for i in range(count):
            self.bitmap.append(0)
            self.__data.append(None)

        print(f"Memory compacted. Processes has up to {count-1}MB allow now!")
        self.show()
    
    def show(self):
        info = ""
        
        tags = []
        size = []
        i = -1
        while i < self.size-1:
            i += 1
            if self.__data[i] is None:
                for j in range(i, self.size):
                    if self.__data[j] != None or j == self.size-1:
                        tags.append("FREE")
                        size.append(j-i)
                        i = j if j == self.size-1 else j - 1
                        break
            else:
                tags.append(self.__data[i])
                size.append(self.map[self.__data[i]])
                i = i + self.map[self.__data[i]] - 1
        
        sizeaux = [None] * len(size)
        for i in range(len(size)):
            sizeaux[i] = int( (size[i]/max(size) * 20))

        for i in range(len(tags)):
            aux = ""
            m = sizeaux[i]//2
            if m == 0:
                if tags[i] == None:
                    aux += "_"
                else:
                    aux += "|" + tags[i] + " " + str(size[i]) + "MB" + "|"
            else:
                aux += "|"
                for j in range(sizeaux[i]):
                    if j == m:
                        aux = aux + tags[i] + " " + str(size[i]) + "MB"
                    else:
                        aux += " "
                aux += "|"
            
            info += aux

        info = "\n|" + info.replace('||', '|') + "|\n"
        border = "=" * (len(info)-2)

        print(border + info + border)
                    
mp = Memory(512)

print("\n\n")
mp.allocate("A", 58)
print("\n\n")
mp.allocate("B", 150)
print("\n\n")
mp.allocate("C", 110)
print("\n\n")
mp.deallocate("B")
print("\n\n")
mp.allocate("E", 90)
print("\n\n")
mp.allocate("F", 10)
print("\n\n")
mp.allocate("G", 51)
print("\n\n")
mp.allocate("H", 26)
print("\n\n")
mp.allocate("I", 56)
print("\n\n")
mp.allocate("J", 100)
