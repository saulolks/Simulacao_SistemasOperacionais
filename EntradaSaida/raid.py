from helpers.so import OS


if __name__ == '__main__':

    info = "\nuser@os:~"
    text = info + "r/$ "
    command = ""
    opsystem = OS(memory_size=20)

    while command != "exit":
        command = input(text)

        inputs = command.split(" ")

        if (len(inputs) == 1 and inputs[0] != "ls" and inputs[0] != "info"
            and inputs[0] != "currinfo" and inputs[0] != "help"):
            print("Comando executado de forma incompleta.")
            continue

        if inputs[0] == "cd":
            text = info + opsystem.cd(inputs[1]) + "$ "
        elif inputs[0] == "ls":
            opsystem.ls()
        elif inputs[0] == "mkdir":
            opsystem.mkdir(inputs[1])
        elif inputs[0] == "rm":
            opsystem.rm(inputs[1])
        elif inputs[0] == "info":
            if len(inputs) > 1:
                print(opsystem.info(node=inputs[1]))
            else:
                print(opsystem.info())
        elif inputs[0] == "currinfo":
            print(opsystem.currinfo())
        elif inputs[0] == "touch":
            opsystem.touch(inputs[1], inputs[2])
        elif inputs[0] == "help":
            print(opsystem.help())
        else:
            print("Informe um comando válido.")

