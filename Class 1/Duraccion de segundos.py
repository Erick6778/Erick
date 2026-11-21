horas = float(input("Ingrese el numero (hora): "))
minutos = float(input("Ingrese el numero (minutos): "))
segundos = float(input("Ingrese el numero (segundos): "))

total_segundos = (horas * 3600) + (minutos * 60) + segundos
print("La duracion total en segundos es:", total_segundos)