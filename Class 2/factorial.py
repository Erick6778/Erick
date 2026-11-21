numero = input("Ingresa un numero entero no negativo: ")

if not numero.isdigit():
    print("Numero no valido")
else:
    numero = int(numero)
    resultado = 1
    for i in range(1, numero + 1):
        resultado = resultado * i
    print(f"El factorial de {numero} es {resultado}")
