clave = input("Ingresa una contraseña: ")

mayuscula = False
minuscula = False
numero = False
especial = False

for letra in clave:
    if letra.isupper():
        mayuscula = True
    elif letra.islower():
        minuscula = True
    elif letra.isdigit():
        numero = True
    else:
        especial = True

errores = []
if len(clave) < 8:
    errores.append("Debe tener al menos 8 caracteres")
if not mayuscula:
    errores.append("Debe tener al menos una letra mayuscula")
if not minuscula:
    errores.append("Debe tener al menos una letra minuscula")
if not numero:
    errores.append("Debe tener al menos un numero")
if not especial:
    errores.append("Debe tener al menos un caracter especial")

if len(errores) == 0:
    print("Contraseña valida")
else:
    print("Contraseña no valida:")
    for error in errores:
        print("-", error)
