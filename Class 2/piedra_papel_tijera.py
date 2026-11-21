import random

opciones = ("piedra", "papel", "tijera")
bot = random.choice(opciones)
tu = input("Elige entre piedra, papel, tijera: ").lower()
print("El bot eligio:", bot)

if tu not in opciones:
    print("Opcion no valida")
elif tu == bot:
    print("Empate")
elif tu == "piedra" and bot == "tijera":
    print("Ganaste")
elif tu == "papel" and bot == "piedra":
    print("Ganaste")
elif tu == "tijera" and bot == "papel":
    print("Ganaste")
else:
    print("Perdiste")
