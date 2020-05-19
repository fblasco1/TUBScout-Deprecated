nuevosquintetos = [[11353,11355,11356,11358,11351],[11353,11355,11356,11358,11359],[11353,11355,11356,11358,11359],[11353,11355,11356,11358,11352],[11353,11355,11356,11358,11351]]
listaquintetos  = []
aux = []

for quinteto in nuevosquintetos:
    elemento       = (quinteto,nuevosquintetos.count(quinteto))
    if listaquintetos == []:
        aux.append(quinteto)
        listaquintetos.append(elemento)
    else:
        if quinteto in aux:
            print("Quinteto ya esta")
        else:
            aux.append(quinteto)
            listaquintetos.append(elemento)

print(listaquintetos)


