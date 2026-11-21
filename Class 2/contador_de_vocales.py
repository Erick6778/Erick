frase = input("Ingresa una frase: ").lower()
vocales = 0

for letra in frase:
    if letra in "aeiouáéíóú":
        vocales += 1

print("Cantidad de vocales:", vocales)
