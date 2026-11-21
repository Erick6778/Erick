filas = input("Cuantas filas quieres?: ")

if not filas.isdigit() or int(filas) == 0:
    print("Escribe un numero entero positivo")
else:
    filas = int(filas)
    for i in range(1, filas + 1):
        for j in range(1, i + 1):
            print(j, end=" ")
        print()
