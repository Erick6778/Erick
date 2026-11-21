caminos = [
    (2, "Casa_Sol", "Casa_Arriba_Izq"),
    (2, "Casa_Arriba_Izq", "Casa_Centro"),
    (2, "Casa_Arriba_Der", "Casa_Centro"),
    (3, "Casa_Sol", "Casa_Avion"),
    (3, "Casa_Arriba_Izq", "Casa_Arriba_Der"),
    (3, "Casa_Arriba_Izq", "Casa_Avion"),
    (3, "Casa_Arriba_Der", "Casa_Derecha"),
    (3, "Casa_Derecha", "Casa_Bici"),
    (3, "Casa_Avion", "Casa_Bus"),
    (3, "Casa_Centro", "Casa_Bus"),
    (3, "Casa_Centro", "Casa_Puente"),
    (3, "Casa_Bus", "Casa_Puente"),
    (3, "Casa_Puente", "Casa_Bici"),
    (4, "Casa_Derecha", "Casa_Centro"),
    (4, "Casa_Centro", "Casa_Bici"),
    (4, "Casa_Avion", "Casa_Esquina_Izq"),
    (4, "Casa_Bus", "Casa_Esquina_Izq"),
    (4, "Casa_Esquina_Izq", "Casa_Puente"),
]

caminos.sort()

grupos = {}
for costo, u, v in caminos:
    grupos[u] = u
    grupos[v] = v

def buscar_grupo(casa):
    while grupos[casa] != casa:
        casa = grupos[casa]
    return casa

ruta_optima = []
costo_total = 0

for costo, casa1, casa2 in caminos:
    g1 = buscar_grupo(casa1)
    g2 = buscar_grupo(casa2)

    if g1 != g2:
        grupos[g1] = g2
        ruta_optima.append((casa1, casa2, costo))
        costo_total += costo

print("Caminos a pavimentar:")
for c1, c2, costo in ruta_optima:
    print(f" - {c1} <--> {c2} ({costo} cuadros)")

print(f"\nTotal de cuadros pavimentados: {costo_total}")
