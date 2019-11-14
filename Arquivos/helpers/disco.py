from helpers.i_node import I_node


class Disco:
    def __init__(self, size, qtd_discos):
        self.size = int(size/qtd_discos)
        self.qtd_discos = qtd_discos
        self.trash = []  # Lista de indices que ainda precisam ser removidos

        self._allocate_discos()

        print(f"Tamanho total = {size} \n"
              f"Tamanho de cada disco = {self.size} \n"
              f"Quantidade de discos = {self.qtd_discos} \n"
              f"Disco original = {self.discos}")

    def _allocate_discos(self, root=None):
        self.discos = []
        for i in range(self.qtd_discos):
            self.discos.append([False]*self.size)

        root = I_node(None, 'r', 1, node_type='dir', head=0)
        for i in range(self.qtd_discos):
            self.discos[i][0] = root

    """
        Verificará primeiramente se o disco (mesmo com fragmentação)
        conseguirá armazenar o `file`. Caso tenha espaço disponível, será
        realizado o `alocate`.
    """
    def add_file(self, index, file):
        if self._check_storage(file.size):
            if self.find_node(file, index) is not None:
                raise KeyError
            self.allocate(file)
            """
                Adiciona ao diretório raiz o primeiro indíce que o
                arquivo/diretório novo está localizado.
            """
            self._allocate_help(data=file.head, pos=index, is_index=True)
        else:
            raise MemoryError

    """
        Independente da quantidade de discos, sempre terá pelo menos um.
        Podendo assim fazer `self.discos[0]`.

        PS: Esse caso se repitirá outras vezes.
    """
    def _check_storage(self, filesize):
        if self.discos[0].count(False) >= filesize:
            return True
        return False

    def _get_pos(self):
        pos = next(i for i, item in enumerate(self.discos[0]) if item is False)
        return pos

    def _allocate_help(self, data, pos=None, is_index=False):
        if pos is None:
            pos = self._get_pos()

        if not is_index:
            for i in range(self.qtd_discos):
                self.discos[i][pos] = data
        else:
            for i in range(self.qtd_discos):
                self.discos[i][pos].indexes.append(data)

    """
        Recebendo um `file` que pode ser um diretório ou arquivo, será
        realizado a alocação desse `file` na memória.

        Percorre-se todas as posições de memória em busca da primeira posição
        livre. Quando acha-se ela, é inserido uma parte do `file` nesa posição.

        Continuará percorrendo a memória, ate que todo o conteúdo do `file`
        tenha sido alocado na memória.

        As posições da memória que estão armazenando o `file`, serão salvas no
        vetor `file.indexes`.
    """
    def allocate(self, file):
        primary_alocate = False

        for i, value in enumerate(self.discos[0]):
            if not value:
                if not primary_alocate:
                    file.head = i
                    self._allocate_help(data=file, pos=i)
                    primary_alocate = True
                else:
                    self._allocate_help(data=file.name, pos=i)
                    file.indexes.append(i)

                if len(file.indexes) >= file.size-1:
                    break

    def _deallocate_help(self, pos=None, index=None, data=None):
        for i in range(self.qtd_discos):
            self.discos[i][pos] = data

            if index is not None:
                self.discos[i][index].indexes.remove(pos)

    def deallocate(self, index, file):
        node = self.discos[0][index]
        find = False

        for i in node.indexes:
            _file = self.discos[0][i]
            if _file.name == file:
                find = True
                self.delete_in_cascade(_file.indexes)
                self._deallocate_help(pos=i, index=index, data=False)
                break

        print(self.trash)
        while len(self.trash) != 0:
            self._clean_trash()

        return find

    def delete_in_cascade(self, indexes):
        for i in indexes:
            self.trash.append(i)
            if (type(self.discos[0][i]) is not str
                    and self.discos[0][i].indexes):
                self.delete_in_cascade(self.discos[0][i].indexes)

    """
        Inverte a ordem dos indices, para pegar o ultimo inserido e apartir
        dele ir removendo da memória, dado que o primeiro indice é
        o nó inicial.
    """
    def _clean_memory(self, indexes):
        indexes.reverse()

        for i in indexes:
            _node = self.discos[0][i]

            """
                Caso esse node tenha mais de um indice em sua lista de
                indices, ele então tem sub pastas ou sub arquivos que
                precisam também ser removidos. Esses indices serão
                inseridos ao `trash`, que será percorrido em outro momento.
            """
            if len(_node.indexes) > 1:
                self.trash.append(i)
            elif type(self.discos[0][i]) is not bool:
                self._deallocate_help(pos=i, data=False)

    def _clean_trash(self):
        for i in self.trash:
            self._deallocate_help(pos=i, data=False)
            self.trash.remove(i)
            print(self.trash)

    """
        A partir de um `pointer` que conterá o indice do diretório anterior,
        captura o node_root presente nesse ponto e a partir dos indices
        presentes no seu `indexes` procurará o `node` em questão.
    """
    def find_node(self, node, pointer):
        node_root = self.discos[0][pointer]

        if len(node_root.indexes) > 0:
            for i in node_root.indexes:
                file = self.discos[0][i]
                if type(file) != bool and file.name == node:
                    return i
        return None
