# Alocação indexada
## Descrição do funcionamento

1. OS
2. Memória
3. I-Node

## 1. OS
### Atributos:
- `root`: dicionário que armazena todos os diretórios, não pode **jamais**
    apontar para outro caminho. Diretórios e arquivos contidos em `root` são 
    representados como:
    ```json
    "root" : {
        "diretorio": {
        },
        "arquivo": 1
    }
    ```
- `current`: dicionário que representa o diretório que usuário está no momento.
    Ele é variável, sempre muda quando o usuário faz uma operação de `cd`.
- `wayback`: armazena todo o caminho que o usuário está percorrendo para o
    sistema saber para qual diretório irá apontar quando o usuário realizar o
    comando `cd ..`. Exemplo:
    ```python
    print(wayback)
    >> "/root/exemplo/diretorios/"    
    ```
- `index_wayback`: armazena os índices de bloco que o usuário percorre, para caso
    o usuário queira retornar ao diretório anterior.
- `memory`: instância da classe memória que o OS irá salvar e excluir seus arquivos.
- `pointer`: posição do bloco do diretório que o usuário está apontando no momento.

## Métodos:
- `cd`: Esse método realiza a navegação entre os diretórios do sistema, podendo
    voltar um diretório ou avançar quantos quiser. A função checa se o comando
    é para retroceder, se sim, obtém o caminho salvo em `wayback`, divide as
    chaves pelo caractere *'/'* e parte do nó raiz (`root`) até a penúltima chave,
    ou seja, nó anterior. Caso a navegação seja para um diretório seguinte,
    o caminho passado é dividido pelo caractere *'/'* e a função utiliza os 
    valores como chave a partir do diretório atual (`current`).
- `mkdir`: cria um diretório dentro do diretório atual, instanciando um 
    dicionário e atribuindo ao dicionário corrente, pela chave recebida 
    como parâmetro.
- `ls`: lista todos os valores armazenados no dicionário corrente.
