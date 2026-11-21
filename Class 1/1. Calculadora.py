print("Calculadora")
print("Deseas: " \
"1. Suma " \

"2. Resta " \

"3. Multiplicación " \

"4. División")

opcion = input("Elige una opcion del 1-4 ")
numero1 = int(input("Ingrese un numero: "))
numero2 = int(input("Ingrese un numero: "))
if opcion == "1":
 print("Resultado:", numero1 + numero2)
elif opcion == "2":
 print("Resultado:", numero1 - numero2)
elif opcion == "3":
 print("Resultado:", numero1 * numero2)
elif opcion == "4":
 print("Resultado:", numero1 / numero2)
else:
 print("Error! Debes elegir de 1-4 para que funcione")
