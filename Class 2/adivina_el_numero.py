import random

numero = random.randint(1, 100)
print("Adivina el numero entre 1 y 100")

while True:
    intento = input("Tu numero: ")
    if not intento.isdigit():
        print("Escribe un numero entero")
        continue
    intento = int(intento)

    if intento < numero:
        print("Mayor")
    elif intento > numero:
        print("Menor")
    else:
        print("Adivinaste el numero:", numero)
        break
