#---EL DECORADOR---#
def agente_d(funcion):
    def espia(*args, **kwargs):
        print(f"[INFORME]: ¡Agente D infiltrando al objetivo '{funcion.__name__}'!")
        print(f"[INTELIGENCIA]: Equipamiento táctico (args) detectado: {args}")
        print(f"[INTELIGENCIA]: Documentos secretos (kwargs) recuperados: {kwargs}")

        resultado = funcion(*args, **kwargs)

        print(f"[EXTRACCIÓN]: ¡Misión cumplida! El objetivo ha revelado el secreto: {resultado!r}")
        return resultado
    return espia


#---FUNCIONES OBJETIVO---#
@agente_d
def desactivar_bomba(codigo, tiempo_restante):
    return "Bomba desactivada con éxito."


@agente_d
def sumar(a, b):
    return a + b


@agente_d
def crear_identidad(**datos):
    return f"Identidad creada: {datos['nombre']}"


#---OPERACIONES EN CAMPO---#
desactivar_bomba("código-azul", tiempo_restante=30)
print("")
sumar(2, 3)
print("")
crear_identidad(nombre="Bond", codigo=7)
