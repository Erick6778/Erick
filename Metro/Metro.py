import unicodedata

metro_caracas = {
    "Linea1": {
        "Propatria": {"estaciones_siguientes": ["Perez Bonalde"], "tiempo_siguiente": 2},
        "Perez Bonalde": {"estaciones_siguientes": ["Plaza Sucre"], "tiempo_siguiente": 2},
        "Plaza Sucre": {"estaciones_siguientes": ["Gato Negro"], "tiempo_siguiente": 2},
        "Gato Negro": {"estaciones_siguientes": ["Agua Salud"], "tiempo_siguiente": 2},
        "Agua Salud": {"estaciones_siguientes": ["Caño Amarillo"], "tiempo_siguiente": 2},
        "Caño Amarillo": {"estaciones_siguientes": ["Capitolio"], "tiempo_siguiente": 2},

        #---Transferencia en "Capitolio" hacia "El Silencio" (Linea 2)---#
        "Capitolio": {"estaciones_siguientes": ["La Hoyada"], "tiempo_siguiente": 2},
        "La Hoyada": {"estaciones_siguientes": ["Parque Carabobo"], "tiempo_siguiente": 2},
        "Parque Carabobo": {"estaciones_siguientes": ["Bellas Artes"], "tiempo_siguiente": 2},
        "Bellas Artes": {"estaciones_siguientes": ["Colegio de Ingenieros"], "tiempo_siguiente": 2},
        "Colegio de Ingenieros": {"estaciones_siguientes": ["Plaza Venezuela"], "tiempo_siguiente": 2},

        #---Transferencia en "Plaza Venezuela" hacia Linea 3 y hacia "Zona Rental" (Linea 4)---#
        "Plaza Venezuela": {"estaciones_siguientes": ["Sabana Grande"], "tiempo_siguiente": 2},
        "Sabana Grande": {"estaciones_siguientes": ["Chacaito"], "tiempo_siguiente": 2},
        "Chacaito": {"estaciones_siguientes": ["Chacao"], "tiempo_siguiente": 2},
        "Chacao": {"estaciones_siguientes": ["Altamira"], "tiempo_siguiente": 2},
        "Altamira": {"estaciones_siguientes": ["Parque del Este"], "tiempo_siguiente": 2},

        "Parque del Este": {"estaciones_siguientes": ["Los Dos Caminos"], "tiempo_siguiente": 2},
        "Los Dos Caminos": {"estaciones_siguientes": ["Los Cortijos"], "tiempo_siguiente": 2},
        "Los Cortijos": {"estaciones_siguientes": ["La California"], "tiempo_siguiente": 2},
        "La California": {"estaciones_siguientes": ["Petare"], "tiempo_siguiente": 2},
        "Petare": {"estaciones_siguientes": ["Palo Verde"], "tiempo_siguiente": 2},
        "Palo Verde": {"estaciones_siguientes": [], "tiempo_siguiente": 0}
    },
    "Linea2": {
        "El Silencio": {"estaciones_siguientes": ["Capuchinos"], "tiempo_siguiente": 2},

        #---Transferencia en "Capuchinos" hacia Linea 4---#
        "Capuchinos": {"estaciones_siguientes": ["Maternidad"], "tiempo_siguiente": 2},
        "Maternidad": {"estaciones_siguientes": ["Artigas"], "tiempo_siguiente": 2},
        "Artigas": {"estaciones_siguientes": ["La Paz"], "tiempo_siguiente": 2},
        "La Paz": {"estaciones_siguientes": ["La Yaguara"], "tiempo_siguiente": 2},
        "La Yaguara": {"estaciones_siguientes": ["Carapita"], "tiempo_siguiente": 2},
        "Carapita": {"estaciones_siguientes": ["Antimano"], "tiempo_siguiente": 2},
        "Antimano": {"estaciones_siguientes": ["Mamera"], "tiempo_siguiente": 2},

        #---En "Mamera" la linea se divide en dos ramales---#
        "Mamera": {"estaciones_siguientes": ["Ruiz Pineda", "Caricuao"], "tiempo_siguiente": 2},

        #---Ramal hacia "Las Adjuntas"---#
        "Ruiz Pineda": {"estaciones_siguientes": ["Las Adjuntas"], "tiempo_siguiente": 2},
        "Las Adjuntas": {"estaciones_siguientes": [], "tiempo_siguiente": 0},

        #---Ramal hacia "Zoologico"---#
        "Caricuao": {"estaciones_siguientes": ["Zoologico"], "tiempo_siguiente": 2},
        "Zoologico": {"estaciones_siguientes": [], "tiempo_siguiente": 0}
    },
    "Linea3": {
        "Plaza Venezuela": {"estaciones_siguientes": ["Ciudad Universitaria"], "tiempo_siguiente": 2},
        "Ciudad Universitaria": {"estaciones_siguientes": ["Los Simbolos"], "tiempo_siguiente": 2},
        "Los Simbolos": {"estaciones_siguientes": ["La Bandera"], "tiempo_siguiente": 2},
        "La Bandera": {"estaciones_siguientes": ["El Valle"], "tiempo_siguiente": 2},
        "El Valle": {"estaciones_siguientes": ["Los Jardines"], "tiempo_siguiente": 2},
        "Los Jardines": {"estaciones_siguientes": ["Coche"], "tiempo_siguiente": 2},
        "Coche": {"estaciones_siguientes": ["Mercado"], "tiempo_siguiente": 2},
        "Mercado": {"estaciones_siguientes": ["La Rinconada"], "tiempo_siguiente": 2},
        "La Rinconada": {"estaciones_siguientes": [], "tiempo_siguiente": 0}
    },
    "Linea4": {
        "Capuchinos": {"estaciones_siguientes": ["Teatros"], "tiempo_siguiente": 2},
        "Teatros": {"estaciones_siguientes": ["Nuevo Circo"], "tiempo_siguiente": 2},
        "Nuevo Circo": {"estaciones_siguientes": ["Parque Central"], "tiempo_siguiente": 2},
        "Parque Central": {"estaciones_siguientes": ["Zona Rental"], "tiempo_siguiente": 2},

        #---"Zona Rental" conecta caminando con "Plaza Venezuela" (Linea 1 y 3)---#
        "Zona Rental": {"estaciones_siguientes": [], "tiempo_siguiente": 0}
    }
}

#---CONNECTIONS---#
transferencias = {
    ("Linea1", "Linea2"): ("Capitolio", "El Silencio"),
    ("Linea2", "Linea1"): ("El Silencio", "Capitolio"),
    ("Linea1", "Linea4"): ("Plaza Venezuela", "Zona Rental"),
    ("Linea4", "Linea1"): ("Zona Rental", "Plaza Venezuela"),
    ("Linea1", "Linea3"): ("Plaza Venezuela", "Plaza Venezuela"),
    ("Linea3", "Linea1"): ("Plaza Venezuela", "Plaza Venezuela"),
    ("Linea2", "Linea4"): ("Capuchinos", "Capuchinos"),
    ("Linea4", "Linea2"): ("Capuchinos", "Capuchinos"),
    ("Linea3", "Linea4"): ("Plaza Venezuela", "Zona Rental"),
    ("Linea4", "Linea3"): ("Zona Rental", "Plaza Venezuela")}

#---Tiempo que toma cada cambio de linea---#
TIEMPO_TRANSFERENCIA = 3


#---FUNCIONES DE LA ESTACION---#
def acentos(texto):
#---Quita acentos y convierte a minusculas---#
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " ".join(texto.lower().split())


#---Motor de Busquedad---#
def buscar_estacion(texto):

    todas = []
    for linea in metro_caracas:
        for estacion in metro_caracas[linea]:
            if estacion not in todas:
                todas.append(estacion)

    consulta = acentos(texto)
    if consulta == "":
        return []
    for estacion in todas:
        if acentos(estacion) == consulta:
            return [estacion]

    parecidas = []
    for estacion in todas:
        if consulta in acentos(estacion):
            parecidas.append(estacion)
    return sorted(parecidas)


#---RECORRIDO DENTRO DE UNA LINEA---#
def vecinos(linea, estacion):
    """Estaciones a las que se llega desde 'estacion' dentro de su linea (ida y vuelta)."""
    datos_linea = metro_caracas[linea]
    resultado = list(datos_linea[estacion]["estaciones_siguientes"])
    for otra in datos_linea:
        if estacion in datos_linea[otra]["estaciones_siguientes"]:
            resultado.append(otra)
    return resultado


def camino_en_linea(linea, origen, destino, recorrido=None):

    if recorrido is None:
        recorrido = [origen]
    if origen == destino:
        return recorrido
    for vecina in vecinos(linea, origen):
        if vecina not in recorrido:
            camino = camino_en_linea(linea, vecina, destino, recorrido + [vecina])
            if camino:
                return camino
    return None

#---Tiempo entre estaciones---#
def tiempo_entre(linea, a, b):

    if b in metro_caracas[linea][a]["estaciones_siguientes"]:
        return metro_caracas[linea][a]["tiempo_siguiente"]
    return metro_caracas[linea][b]["tiempo_siguiente"]


def tiempo_total(tramos):

    total = 0
    for linea, estaciones in tramos:
        for i in range(len(estaciones) - 1):
            total += tiempo_entre(linea, estaciones[i], estaciones[i + 1])
    total += (len(tramos) - 1) * TIEMPO_TRANSFERENCIA
    return total


#---BUSQUEDA DE LA RUTA---#
def rutas_posibles(linea, estacion, destino, lineas_usadas, tramos):

    resultados = []


    if destino in metro_caracas[linea]:
        camino = camino_en_linea(linea, estacion, destino)
        resultados.append(tramos + [(linea, camino)])

    for (linea_a, linea_b), (salida, llegada) in transferencias.items():
        if linea_a == linea and linea_b not in lineas_usadas:
            camino = camino_en_linea(linea, estacion, salida)
            if camino:
                resultados += rutas_posibles(linea_b, llegada, destino,
                                             lineas_usadas + [linea_b],
                                             tramos + [(linea, camino)])
    return resultados


def buscar_ruta(origen, destino):

    posibles = []
    for linea in metro_caracas:
        if origen in metro_caracas[linea]:
            posibles += rutas_posibles(linea, origen, destino, [linea], [])

    mejor = None
    for tramos in posibles:
        valor = (tiempo_total(tramos), len(tramos) - 1)
        if mejor is None or valor < mejor[0]:
            mejor = (valor, tramos)
    return mejor[1], mejor[0][0]


#---MOSTRAR EL RESULTADO---#
def texto_de_ruta(tramos):
    partes = []
    for i, (linea, estaciones) in enumerate(tramos):
        if i > 0:
            partes.append("|TRANSFERENCIA|")
            if partes[-2] == estaciones[0]:
                estaciones = estaciones[1:]
        partes.extend(estaciones)
    return "  →  ".join(partes)


def mostrar_ruta(tramos, tiempo):
    num_estaciones = 0
    for linea, estaciones in tramos:
        num_estaciones += len(estaciones) - 1
    cantidad_cambios = len(tramos) - 1

    print(f"Numero de estaciones a pasar: {num_estaciones}")
    if cantidad_cambios > 0:
        plural = "s" if cantidad_cambios > 1 else ""
        print(f"Tiempo estimado de viaje: {tiempo} minutos (Incluye {cantidad_cambios} transferencia{plural})")
        print("Tu ruta tiene transferencia y es:")
    else:
        print(f"Tiempo estimado de viaje: {tiempo} minutos")
        print("Tu ruta es:")
    print(texto_de_ruta(tramos))

    print("")
    if cantidad_cambios == 0:
        print(f"Viaje directo por la {tramos[0][0]}, sin cambios de linea.")
    else:
        print(f"Empiezas en la {tramos[0][0]}.")
        for i in range(cantidad_cambios):
            linea_salida, estaciones_salida = tramos[i]
            linea_llegada, estaciones_llegada = tramos[i + 1]
            estacion_salida = estaciones_salida[-1]
            estacion_llegada = estaciones_llegada[0]
            if estacion_salida == estacion_llegada:
                print(f"¡Atencion! En {estacion_salida} cambia de {linea_salida} a {linea_llegada}.")
            else:
                print(f"¡Atencion! Sal de {estacion_salida} ({linea_salida}) y camina a "
                      f"{estacion_llegada} para tomar la {linea_llegada}.")


def pedir_estacion(mensaje):
    while True:
        texto = input(mensaje)
        coincidencias = buscar_estacion(texto)
        if len(coincidencias) == 1:
            return coincidencias[0]
        if not coincidencias:
            print("Estacion no valida. Intenta de nuevo.")
        else:
            print("Hay varias estaciones parecidas, se mas especifico:")
            for nombre in coincidencias:
                print(f"  - {nombre}")


#---PROGRAMA---#
print("")
print("       🚇BIENVENIDOS AL METRO DE CARACAS🚇          ")
print("")

O1 = pedir_estacion("Estacion de partida: ")
D2 = pedir_estacion("Ingrese la estación de destino: ")
print("")

if O1 == D2:
    print("Ya estas en tu destino.")
else:
    tramos, tiempo = buscar_ruta(O1, D2)
    mostrar_ruta(tramos, tiempo)
