base_de_datos_de_dinosaurios = [("Tiranosaurio", "Rex", "Carnivoro", "Cretacico", "La mordedura del T-rex tenia una presión de casi 6 toneladas de fuerza, suficiente para triturar los huesos de sus presas por completo y hacer que explotaran desde el interior mientras se los tragaba "),
                                ("Triceratops", "Horridus", "Herbivoro", "Cretacico", "Los tres cuernos del Triceratops no eran solo de hueso macizo; estaban cubiertos de queratina (el mismo material de tus uñas) lo que los hacia super afilados y resistentes para apuñalar a los T-rex que intentaban cazarlos "),
                                ("Spinosaurus", "Aegyptiacus", "Carnivoro", "Cretacico", "En el cine los ponen a pelear al Spinosaurus y al Tiranosaurio Rex pero el Spinosaurus vivió unos 30 millones de años antes que el T-rex y pasaba la mayor parte de su tiempo cazando bajo el agua "),
                                ("Stegosaurus", "Stenops", "Herbivoro", "Jurasico", "Nosotros los humanos modernos estamos mas cerca del Tiranosaurio Rex (66 millones de años) y el T-rex esta unos 84 millones de años del Stegosaurio "),
                                ("Quetzalcoatlus", "Northropi", "Carnivoro", "Cretacico", "El Quetzalcoatlus fue el animal volador mas grande de todos los tiempos; tenia la misma altura que una jirafa moderna y sus alas extendidas medían 11 metros lo mismo que un avion privado "),
                                ("Velociraptor", "Antirrhopus", "Carnivoro", "Cretacico", "El Velociraptor real no tenía la piel de lagarto como nos lo muestran las películas sino que estaba completamente cubierto de plumas como un ave moderna y apenas tenía el tamaño de un pavo grande o un lobo pequeño "),
                                ("Brachiosaurus", "Altithorax", "Herbivoro", "Jurasico", "El Brachiosaurus tenia las patas delanteras mas largas que las traseras, como una jirafa gigante, y con su cuello podia alzar la cabeza a unos 12 metros del suelo, casi la altura de un edificio de cuatro pisos "),
                                ("Dilophosaurus", "Wetherilli", "Carnivoro", "Jurasico", "En la pelicula el Dilophosaurus escupe veneno y abre un collar alrededor del cuello pero no existe ninguna evidencia fosil de que hiciera eso, y ademas el real era mucho mas grande: medía unos 7 metros de largo y no el tamaño de un perro como en el cine "),
                                ("Gallimimus", "Bullatus", "Omnivoro", "Cretacico", "El nombre Gallimimus significa imitador de gallina, y se calcula que podia correr a unos 50 kilometros por hora, mas rapido que cualquier persona, lo que le servia para escapar de los depredadores ")]


#---Quita acentos, espacios y mayusculas para comparar lo que escribe el usuario---#
def limpiar(texto):
    texto = texto.strip().lower()
    return texto.translate(str.maketrans("áéíóú", "aeiou"))


#---Muestra los datos de un dinosaurio---#
def mostrar_dinosaurio(dino):
    print(f"Nombre: {dino[0]}, Especie: {dino[1]}, Dieta: {dino[2]}, Periodo: {dino[3]}")


#---Busqueda por nombre---#
def informacion_dinosaurio(base_de_datos, nombre_dinosaurio):
    encontrado = "no"

    for dino in base_de_datos:
        if limpiar(dino[0]) == limpiar(nombre_dinosaurio):
            mostrar_dinosaurio(dino)
            encontrado = "si"
            break

    if encontrado == "no":
        print("Dinosaurio no encontrado.")
        return None
    return dino


#---Busqueda por dieta---#
def dinosaurios_por_dieta(base_de_datos, dieta):
    cantidad = 0

    for dino in base_de_datos:
        if limpiar(dino[2]) == limpiar(dieta):
            mostrar_dinosaurio(dino)
            cantidad += 1

    if cantidad == 0:
        print("No hay dinosaurios con esa dieta.")


#---Busqueda por periodo---#
def dinosaurios_por_periodo(base_de_datos, periodo):
    cantidad = 0

    for dino in base_de_datos:
        if limpiar(dino[3]) == limpiar(periodo):
            mostrar_dinosaurio(dino)
            cantidad += 1

    if cantidad == 0:
        print("No hay dinosaurios de ese periodo.")


#---PROGRAMA---#
print("Como quieres buscar?")
print("1. Por nombre")
print("2. Por dieta")
print("3. Por periodo")
opcion = input("")

while opcion not in ("1", "2", "3"):
    print("Opcion no valida. Elige 1, 2 o 3.")
    opcion = input("")
print("")

if opcion == "1":
    print("Ingrese el nombre del Dinosaurio que deseas saber sus datos.")
    buscador = input("")
    print("")
    dino_encontrado = informacion_dinosaurio(base_de_datos_de_dinosaurios, buscador)

    if dino_encontrado is not None:
        print("")
        print("Quieres Saber un dato curioso del", dino_encontrado[0])
        print("si/no")
        dato_curioso = limpiar(input(""))
        if dato_curioso == "si":
            print("dato Curioso:", dino_encontrado[4])
        elif dato_curioso == "no":
            print("Ok, hasta pronto.")
        else:
            print("Respuesta no valida, hasta pronto.")

elif opcion == "2":
    print("Ingrese la dieta que deseas buscar (Carnivoro, Herbivoro u Omnivoro).")
    dieta = input("")
    print("")
    dinosaurios_por_dieta(base_de_datos_de_dinosaurios, dieta)

elif opcion == "3":
    print("Ingrese el periodo que deseas buscar (Cretacico, Jurasico o Triasico).")
    periodo = input("")
    print("")
    dinosaurios_por_periodo(base_de_datos_de_dinosaurios, periodo)
