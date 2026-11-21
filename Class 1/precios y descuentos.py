precio = float(input("precio: "))
descuento = float(input("descuento: "))
precio_final = precio - (precio * descuento / 100)
print("El precio final es:", precio_final)