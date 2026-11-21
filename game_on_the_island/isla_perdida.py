import time
import threading


#---ESTADO DEL JUEGO---#
juego_activo = True
volver_jugar = True
parpadeando = True
escena = "campamento"
helicoptero_registrado = False
oficinas_registradas = False

#---ESTADO DEL JUGADOR---#
estado_jugador = {
    "VIDA": 100, "COMIDA": 100,
    "ENERGIA": 100, "AGUA": 100
}

#---TIEMPO EN EL JUEGO---#
dia = 1
horas = 8

#---INVENTARIO Y SU LIMITE---#
inventario = {}
LIMITE_BASE = 12        # espacios que puedes cargar sin mochila
LIMITE_MOCHILA = 20     # espacios con la Mochila Militar (la mochila no ocupa espacio)

#---ITEMS DEL JUEGO---#
# Objetos que se pueden usar: lo que recuperan (o quitan) a tus estadisticas
consumibles = {
    "Cocos": {"COMIDA": 30, "AGUA": 15},
    "Bayas": {"COMIDA": 15, "AGUA": 5},
    "Pez Cocinado": {"COMIDA": 30, "VIDA": 15},
    "Comida en Lata": {"COMIDA": 25, "ENERGIA": 10},
    "Agua en Botella": {"AGUA": 35},
    "Botiquin de Emergencia": {"VIDA": 40},
    "Venda": {"VIDA": 20},
    "Pez": {"COMIDA": 10, "VIDA": -20},      # crudo: te enfermas de Bacterias
}

#---RECETAS PARA CRAFTEAR---#
recetas = {
    "Cuerda": {"ingredientes": {"Fibras": 2}, "uso": "sirve para armar la Balsa"},
    "Lanza": {"ingredientes": {"Palos": 2, "Piedras": 1, "Fibras": 1}, "uso": "pescas 2 Peces en vez de 1"},
    "Venda": {"ingredientes": {"Hojas": 2, "Fibras": 1}, "uso": "cura 20 de vida"},
    "Balsa": {"ingredientes": {"Madera": 3, "Cuerda": 2}, "uso": "te permite escapar por el mar"},
}


#---ESTADISTICAS DEL JUGADOR---#
def estadisticas_jugador(STATS, CANTIDAD):
    global juego_activo
    if not juego_activo:
        return

    estado_jugador[STATS] = estado_jugador[STATS] + CANTIDAD

#---SE CONTROLAN LAS ESTADISTICAS---#
    if estado_jugador[STATS] > 100:
        estado_jugador[STATS] = 100
    elif estado_jugador[STATS] < 0:
        estado_jugador[STATS] = 0

    if estado_jugador["VIDA"] <= 0:
        print("=== FINAL MALO: HAS MUERTO POR TUS HERIDAS ===")
        juego_activo = False

    elif estado_jugador["COMIDA"] <= 0:
        print("=== FINAL MALO: HAS MUERTO POR FALTA DE COMIDA ===")
        juego_activo = False

    elif estado_jugador["ENERGIA"] <= 0:
        print("=== FINAL MALO: TE DESPLOMASTE Y NO PUDISTE LEVANTARTE, TE DIO SED Y HAMBRE ===")
        juego_activo = False

    elif estado_jugador["AGUA"] <= 0:
        print("=== FINAL MALO: HAS MUERTO POR FALTA DE SED ===")
        juego_activo = False


#---CAMINAR GASTA ENERGIA, COMIDA Y AGUA (con el Mapa gastas menos)---#
def caminar():
    if "Mapa" in inventario:
        estadisticas_jugador("ENERGIA", -10)
        estadisticas_jugador("COMIDA", -5)
        estadisticas_jugador("AGUA", -10)
    else:
        estadisticas_jugador("ENERGIA", -15)
        estadisticas_jugador("COMIDA", -10)
        estadisticas_jugador("AGUA", -15)


#---PASAR EL TIEMPO---#
def pasar_tiempo(horas_transcurridas):
    global dia, horas
    horas += horas_transcurridas

# Si la hora llega a 24 pasara al siguiente dia.
    if horas >= 24:
        dia += 1
        horas = horas - 24
        print("................................")


#---INVENTARIO---#
def limite_inventario():
    if "Mochila Militar" in inventario:
        return LIMITE_MOCHILA
    return LIMITE_BASE


def espacios_usados():
    total = 0
    for item in inventario:
        if item != "Mochila Militar":
            total += inventario[item]
    return total


#---ITEMS AGREGADO AL INVENTARIO AVISO---#
def agregar_items(ITEM, CANTIDAD):
    if ITEM == "Mochila Militar":
        libre = CANTIDAD
    else:
        libre = max(0, limite_inventario() - espacios_usados())

    entra = min(CANTIDAD, libre)
    if entra > 0:
        inventario[ITEM] = inventario.get(ITEM, 0) + entra
        print(f"  + {ITEM} x{entra}")
    if entra < CANTIDAD:
        print(f"  Inventario lleno: no puedes llevar {ITEM} x{CANTIDAD - entra}")
    return entra


def quitar_items(ITEM, CANTIDAD):
    inventario[ITEM] = inventario[ITEM] - CANTIDAD
    if inventario[ITEM] <= 0:
        del inventario[ITEM]


#---ITEMS---#
def usar_items():
    # Devuelve True si usaste algo, False si no paso nada, None si cancelaste
    if len(inventario) == 0:
        print("Tu inventario esta Vacio")
        return False

    lista = list(inventario)
    print("Objetos en tu inventario:")
    for i, item in enumerate(lista, start=1):
        print(f"{i}. {item} x{inventario[item]}")
    print("0. Volver")
    eleccion = input("Elige un objeto: ")

    if not eleccion.isdigit():
        print("Opción no válida.")
        return False
    numero = int(eleccion)
    if numero == 0:
        return None
    if numero > len(lista):
        print("Opción no válida.")
        return False

    item = lista[numero - 1]
    print(f"{item}:")
    print("1. Usar")
    print("2. Tirar uno")
    print("0. Cancelar")
    accion = input("Elige una opcion: ")

    if accion == "1":
        if item not in consumibles:
            print(f"No puedes usar {item} ahora: lo necesitarás en el momento justo.")
            return False
        if item == "Pez":
            print("Comes el Pez CRUDO. Te enfermas de Bacterias...")
        else:
            print(f"Usas {item}.")
        quitar_items(item, 1)
        efectos = []
        for stat, valor in consumibles[item].items():
            efectos.append(f"{stat} {valor:+d}")
        print("  (" + ", ".join(efectos) + ")")
        for stat, valor in consumibles[item].items():
            estadisticas_jugador(stat, valor)
        return True

    elif accion == "2":
        if item == "Mochila Militar":
            print("No puedes tirar la Mochila Militar.")
            return False
        quitar_items(item, 1)
        print(f"Tiras {item} x1.")
        return False

    elif accion == "0":
        return None

    print("Opción no válida.")
    return False


#---CRAFTEO---#
def craftear():
    # Devuelve True si crafteaste algo, False si no paso nada, None si cancelaste
    nombres = list(recetas)
    print("¿Qué quieres craftear?")
    for i, nombre in enumerate(nombres, start=1):
        pedido = []
        for item, cantidad in recetas[nombre]["ingredientes"].items():
            pedido.append(f"{item} x{cantidad}")
        print(f"{i}. {nombre} ({', '.join(pedido)}) - {recetas[nombre]['uso']}")
    print("0. Volver")
    eleccion = input("Elige una receta: ")

    if not eleccion.isdigit():
        print("Opción no válida.")
        return False
    numero = int(eleccion)
    if numero == 0:
        return None
    if numero > len(nombres):
        print("Opción no válida.")
        return False

    nombre = nombres[numero - 1]
    ingredientes = recetas[nombre]["ingredientes"]

    faltan = []
    for item, cantidad in ingredientes.items():
        if inventario.get(item, 0) < cantidad:
            faltan.append(f"{item} x{cantidad - inventario.get(item, 0)}")
    if len(faltan) > 0:
        print("Te faltan materiales: " + ", ".join(faltan))
        return False

    for item, cantidad in ingredientes.items():
        quitar_items(item, cantidad)
    print(f"¡Crafteaste {nombre}!")
    agregar_items(nombre, 1)
    return True


#---PAUSA PARA LEER---#
def pausa():
    if juego_activo:
        input("Presiona ENTER para continuar...")


#---MOTOR DE ESCRITURA---#
def write_slowly(text, speed=0.005):
    for letra in text:
        print(letra, end="", flush=True)
        time.sleep(speed)
    print()


#---ANIMACION DE PARPADEO---#
def animacion_parpadeo():
    time.sleep(0.5)
    while parpadeando:
        print("              (𝓮𝓷𝓽𝓮𝓻)", end="\r", flush=True)
        time.sleep(0.5)
        if not parpadeando:
            break
        print("                           ", end="\r", flush=True)
        time.sleep(0.4)


#---MENU DE COMIENZO DEL JUEGO---#
def menu_juego():
    global parpadeando
    print("====================================")
    print("      🚨 Matanceros: Site C 🚨      ")
    print("               JUGAR              ")

    hilo = threading.Thread(target=animacion_parpadeo)
    hilo.start()

    input()

    parpadeando = False
    hilo.join()
    print("              ")
    print("====================================")
    print("Iniciando Programa...")


menu_juego()

#---INTRODUCCION DEL JUEGO---#
write_slowly("Eres un investigador de InGen. La empresa te ha enviado en una expedición junto a otros cuatro científicos.")
write_slowly("La misión es analizar la costa y la selva de la Isla, la cual está confirmada como deshabitada desde 1949. Para el equipo es un hecho que allí no hay peligro, pues los únicos registros de presencia biológica pertenecen a Isla Nublar —escenario de las catástrofes de \"Jurassic Park\" y \"Jurassic World\"— e Isla Sorna (el Sitio B), donde InGen criaba a los dinosaurios antes de trasladarlos a Isla Nublar.")
write_slowly("A medida que nos acercamos a la isla, el ambiente se vuelve pesado. Una sensación extraña me oprime el pecho; el sol no alumbra con fuerza y el cielo luce de un gris apagado, como si nos estuviera advirtiendo que demos la vuelta y no pisemos este lugar. Ya sobrevolando la isla rumbo a la costa norte para establecer la base de operaciones, cuando la voz del piloto rompe el silencio con tono de pánico:")
write_slowly("—¡Estamos perdiendo potencia en los motores! No sé qué ocurre, pero parece que el helicóptero va a caer...")
write_slowly("Desperté confundido. Los asientos delanteros amortiguaron parte del impacto y me salvaron la vida. Logro ponerme de pie entre el humo, pero no hay rastro del piloto ni del resto del equipo. Al levantar la mirada, veo que el helicóptero quedó atrapado entre las gruesas lianas de un árbol gigantesco. De pronto, un escalofrío me recorre la espalda: siento claramente que algo, desde la oscuridad de la selva, me está mirando fijamente.")
print()


#---REINICIO DEL JUEGO---#
while volver_jugar:
    dia = 1
    horas = 8
    estado_jugador = {"VIDA": 100, "COMIDA": 100, "ENERGIA": 100, "AGUA": 100}
    inventario = {}
    helicoptero_registrado = False
    oficinas_registradas = False
    escena = "campamento"
    juego_activo = True

#---BUCLE PRINCIPAL---#
    while juego_activo:

#---ESTADISTICAS QUE SE MUESTRAN EN LA PANTALLA---#
        print(f"""
    | ❤️ :{estado_jugador['VIDA']}/100 | 🍖 :{estado_jugador['COMIDA']}/100 |
    | ⚡:{estado_jugador['ENERGIA']}/100 | 💧:{estado_jugador['AGUA']}/100 |""")

#---DIA Y HORA DEL JUEGO QUE SE MUESTRA EN LA PANTALLA---#
        print(f"         DIA: {dia}  | HORA: {horas}:00 ")

#---MOSTRAR INVENTARIO---#
        print("------------------------------------------")
        print(f"           🎒 INVENTARIO: ({espacios_usados()}/{limite_inventario()})")
        if len(inventario) == 0:
            print("               (𝒱𝒶𝒸í𝑜)")
        else:
            for items, cantidad in inventario.items():
                print(items, "x", cantidad, end=" | ")
            print()
        print("------------------------------------------")
        print()

        #---CAMPAMENTO (PRIMERA DECISION)---#
        if escena == "campamento":
            print("Estás en el campamento junto a los restos del helicóptero. ¿Qué deseas hacer?")
            print("1. Registrar los restos del helicóptero - 2 horas")
            print("2. Buscar materiales en los alrededores (Madera, Fibras, Palos, Hojas, Piedras) - 2 horas")
            print("3. Ir al riachuelo a pescar o buscar Cocos - 2 horas")
            print("4. Usar el Encendedor para hacer fogata y cocinar - 1 hora")
            print("5. Usar objetos del inventario (comer, beber, curarte o tirar) - 1 hora")
            print("6. Craftear")
            print("7. Descansar - 3 horas")
            print("8. Avanzar hacia la selva profunda - 3 horas")
            if "Balsa" in inventario:
                print("9. Navegar hacia el mar en tu balsa (hacen falta fuerzas y agua)")
            opcion = input("Elige una opcion: ")

            if opcion == "1":
                print()
                if helicoptero_registrado:
                    print("Ya rescataste todo lo que se podía de los restos del helicóptero.")
                else:
                    print("Revisas los restos del helicóptero y rescatas lo que puedes, pero te cortas con los metales retorcidos.")
                    helicoptero_registrado = True
                    agregar_items("Mochila Militar", 1)
                    agregar_items("Machete", 1)
                    agregar_items("Encendedor", 1)
                    agregar_items("Botiquin de Emergencia", 1)
                    agregar_items("Linterna Tactica", 1)
                    agregar_items("Bengala de Mano", 1)
                    agregar_items("Comida en Lata", 2)
                    agregar_items("Agua en Botella", 2)
                    pasar_tiempo(2)
                    estadisticas_jugador("ENERGIA", -10)
                    estadisticas_jugador("VIDA", -25)
                pausa()

            elif opcion == "2":
                print()
                print("Recorres los alrededores y juntas materiales entre los árboles.")
                agregar_items("Madera", 1)
                agregar_items("Fibras", 2)
                agregar_items("Palos", 1)
                agregar_items("Hojas", 1)
                agregar_items("Piedras", 1)
                pasar_tiempo(2)
                estadisticas_jugador("ENERGIA", -10)
                estadisticas_jugador("COMIDA", -5)
                estadisticas_jugador("AGUA", -10)
                pausa()

            elif opcion == "3":
                print()
                print("Encuentras un riachuelo junto al campamento.")
                if "Lanza" in inventario:
                    print("Con tu Lanza pescas mucho mejor.")
                    agregar_items("Pez", 2)
                else:
                    agregar_items("Pez", 1)
                agregar_items("Cocos", 2)
                agregar_items("Bayas", 1)
                pasar_tiempo(2)
                estadisticas_jugador("ENERGIA", -10)
                estadisticas_jugador("COMIDA", -5)
                estadisticas_jugador("AGUA", -5)
                pausa()

            elif opcion == "4":
                print()
                if "Palos" in inventario and "Encendedor" in inventario:
                    print("Enciendes una fogata caliente.")
                    quitar_items("Palos", 1)
                    if "Pez" in inventario:
                        cantidad = inventario["Pez"]
                        print(f"Cocinaste {cantidad} Pez. ¡Ahora tienes Pez Cocinado!")
                        quitar_items("Pez", cantidad)
                        agregar_items("Pez Cocinado", cantidad)
                    else:
                        print("No tienes nada que cocinar, pero el fuego te reconforta.")
                    pasar_tiempo(1)
                else:
                    print("Te faltan Palos o el Encendedor para prender fuego.")
                pausa()

            elif opcion == "5":
                print()
                resultado = usar_items()
                if resultado:
                    pasar_tiempo(1)
                if resultado is not None:
                    pausa()

            elif opcion == "6":
                print()
                resultado = craftear()
                if resultado:
                    pasar_tiempo(1)
                    estadisticas_jugador("ENERGIA", -5)
                if resultado is not None:
                    pausa()

            elif opcion == "7":
                print()
                print("Descansas un rato junto al campamento y recuperas fuerzas.")
                pasar_tiempo(3)
                estadisticas_jugador("ENERGIA", 40)
                estadisticas_jugador("COMIDA", -5)
                estadisticas_jugador("AGUA", -10)
                pausa()

            elif opcion == "8":
                print()
                print("Te adentras en la selva siguiendo rastros de la instalación abandonada...")
                escena = "selva"
                pasar_tiempo(3)
                caminar()

            elif opcion == "9" and "Balsa" in inventario:
                print()
                print("Empujas tu balsa al mar y empiezas a remar hacia el horizonte...")
                if estado_jugador["ENERGIA"] >= 30 and estado_jugador["AGUA"] >= 30:
                    print("Tus brazos resisten el oleaje. Tras dos días remando, un barco pesquero te divisa y te rescata.")
                    print("=== FINAL BUENO: ESCAPASTE EN BALSA ===")
                else:
                    print("Estás demasiado débil y deshidratado para remar. Una ola gigante voltea la balsa...")
                    print("=== FINAL MALO: TE QUEDASTE SIN FUERZAS EN EL MAR ===")
                juego_activo = False

            else:
                print("Opción no válida.")

        elif escena == "selva":
            print("Llegas a un punto de la selva donde el camino se divide. ¿Qué haces?")
            if "Mapa" in inventario:
                print("(Según tu Mapa, el arroyo lleva hacia la costa y los rastros, a una instalación de InGen.)")
            print("1. Seguir el sonido de un arroyo - 2 horas")
            print("2. Seguir unos rastros hacia una instalación abandonada - 2 horas")
            print("3. Volver al campamento - 2 horas")
            opcion = input("Elige una opcion: ")

            if opcion == "1":
                escena = "arroyo"
                pasar_tiempo(2)
                caminar()
            elif opcion == "2":
                escena = "instalacion"
                pasar_tiempo(2)
                caminar()
            elif opcion == "3":
                print("Regresas al campamento junto al helicóptero.")
                escena = "campamento"
                pasar_tiempo(2)
                caminar()
            else:
                print("Opción no válida.")

        elif escena == "arroyo":
            print("Encuentras un arroyo de agua cristalina. ¿Qué haces?")
            print("1. Beber agua y descansar un rato junto al arroyo")
            print("2. Cruzar el arroyo por las piedras resbaladizas y seguir río arriba - 2 horas")
            if "Machete" in inventario:
                print("3. Usar el machete para abrirte paso hacia la costa")
            opcion = input("Elige una opcion: ")

            if opcion == "1":
                print()
                print("Te agachas a beber y de pronto escuchas chasquidos a tu alrededor.")
                print("Una manada de Velociraptors te rodeó sin hacer ruido...")
                print("=== FINAL MALO: LA MANADA DEL ARROYO ===")
                juego_activo = False
            elif opcion == "2":
                print("Te resbalas y la corriente te golpea contra las rocas, pero logras beber agua.")
                print("Sigues río arriba hasta que ves una estructura entre los árboles.")
                escena = "instalacion"
                pasar_tiempo(2)
                caminar()
                estadisticas_jugador("AGUA", 40)
                estadisticas_jugador("VIDA", -50)
            elif opcion == "3" and "Machete" in inventario:
                print()
                print("Con el machete abres un sendero entre la maleza hasta llegar a la costa.")
                print("Entre las rocas encuentras una lancha de rescate de InGen, la empujas al mar y escapas de la isla.")
                print("=== FINAL BUENO: ESCAPASTE EN LANCHA ===")
                juego_activo = False
            else:
                print("Opción no válida.")

        elif escena == "instalacion":
            print("Llegas a una estructura oxidada de InGen cubierta por la vegetación. ¿Qué haces?")
            print("1. Registrar los escritorios de las oficinas - 2 horas")
            print("2. Entrar al laboratorio principal - 1 hora")
            print("3. Volver al campamento - 3 horas")
            opcion = input("Elige una opcion: ")

            if opcion == "1":
                if oficinas_registradas:
                    print("Ya registraste todas las oficinas.")
                else:
                    print("Entre los vidrios rotos encuentras el Mapa de la isla y una Pistola de Bengala, pero te cortas las manos.")
                    oficinas_registradas = True
                    agregar_items("Mapa", 1)
                    agregar_items("Pistola de Bengala", 1)
                    pasar_tiempo(2)
                    estadisticas_jugador("VIDA", -25)
            elif opcion == "2":
                escena = "laboratorio"
                pasar_tiempo(1)
                caminar()
            elif opcion == "3":
                print("Regresas al campamento junto al helicóptero.")
                escena = "campamento"
                pasar_tiempo(3)
                caminar()
            else:
                print("Opción no válida.")

        elif escena == "laboratorio":
            print("Entras al laboratorio y lees un informe sobre el espécimen K-123.")
            print("De pronto escuchas un gruñido: en la pared ves el camuflaje de un Velociraptor.")
            print("Corres a un cuarto de control y cierras la puerta de metal justo a tiempo.")
            print("El Velociraptor golpea la puerta con furia... ¿Cómo te defiendes?")
            print("1. Usar la Pistola de Bengala o la Bengala de Mano")
            print("2. Pelear con el machete")
            print("3. Aguantar la puerta con tu peso")
            opcion = input("Elige una opcion: ")

            if opcion == "1":
                print()
                if "Pistola de Bengala" in inventario or "Bengala de Mano" in inventario:
                    print("Disparas la bengala. La luz intensa asusta al Velociraptor, que huye chillando hacia la selva.")
                    print("Logras llegar a la costa y eres rescatado.")
                    print("=== FINAL BUENO: SOBREVIVISTE A LA ISLA DE INGEN ===")
                else:
                    print("Buscas desesperadamente una bengala, pero no tienes ninguna.")
                    print("La puerta cae y el Velociraptor entra.")
                    print("=== FINAL MALO: CAÍSTE EN EL LABORATORIO ===")
                juego_activo = False
            elif opcion == "2":
                print()
                vida_minima = 50
                if "Linterna Tactica" in inventario:
                    vida_minima = 30
                    print("Con la Linterna Táctica ves el camuflaje del Velociraptor a tiempo y ganas ventaja.")
                if "Machete" in inventario and estado_jugador["VIDA"] >= vida_minima:
                    print("Logras herir al Velociraptor con el machete, pero quedas gravemente herido.")
                    print("Sales arrastrándote hacia la playa...")
                    print("=== FINAL BUENO: SUPERVIVIENTE HERIDO ===")
                elif "Machete" not in inventario:
                    print("No tienes ningún machete con el que defenderte.")
                    print("=== FINAL MALO: CAÍSTE EN EL LABORATORIO ===")
                else:
                    print("Estás demasiado herido para pelear: te falla el pulso y el Velociraptor se abalanza sobre ti.")
                    print("=== FINAL MALO: CAÍSTE EN EL LABORATORIO ===")
                juego_activo = False
            elif opcion == "3":
                print()
                print("La fuerza del dinosaurio rompe las bisagras de la puerta y te aplasta.")
                print("=== FINAL MALO: CAÍSTE EN EL LABORATORIO ===")
                juego_activo = False
            else:
                print("Opción no válida.")

#---VOLVER A JUGAR---#
    print()
    print("¿Quieres jugar otra vez?")
    print("1. Si, Reiniciar")
    print("2. No, Salir")
    respuesta = input("Elige una opcion: ")
    while respuesta not in ["1", "2"]:
        print("Opción inválida. Elige 1 o 2.")
        respuesta = input("Elige una opcion: ")

    if respuesta == "2":
        volver_jugar = False
        print()
        print("¡Gracias por jugar!")
