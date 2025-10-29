def crear_pfp(nombre: str, edad: int, *hobbies: str, **redes_sociales: str) -> str:
    """
    Crea un perfil de usuario con información básica, hobbies y redes sociales.

    Esta función genera un texto formateado que describe un perfil de usuario
    utilizando el nombre, edad, una lista variable de hobbies y redes sociales.

    Args:
        nombre (str): Nombre del usuario.
        edad (int): Edad del usuario.
        *hobbies (str): Lista opcional de hobbies o intereses del usuario.
        **redes_sociales (str): Diccionario opcional de redes sociales con el nombre
            de la red como clave y el usuario o handle como valor.

    Returns:
        str: Una cadena formateada con la información del perfil del usuario.

    """
    hobbies_str = ", ".join(hobbies) if hobbies else "No especificados."

    redes_lista = []

    if redes_sociales:
        for red, user in redes_sociales.items():
            redes_lista.append(f"-{red.capitalize()}: {user}")
        redes_str = "\n".join(redes_lista)
    else:
        redes_str = "No especificados."

    perfil = (f"Perfil de usuario\n"
              f"nombre: {nombre}\n"
              f"edad: {edad} años\n"
              f"hobbies: {hobbies_str}\n"
              f"redes sociales: {redes_str}")
    return perfil.strip()


nombre = input("Ingresa tu nombre: ")

while True:
    try:
        edad = int(input("Ingresa tu edad: "))
        break
    except ValueError:
        print("El valor ingresado no puede ser un número.")

hobbies_list = []

print("Presiona Enter sin escribir nada para terminar.")
while True:
    hobby = input(f"Ingresa tu hobby #{len(hobbies_list)+1}: ").strip()
    if not hobby:
        break
    hobbies_list.append(hobby)

redes_dict = {}

print("Presiona Enter sin escribir nada para terminar.")
while True:
    red = input("Ingresa tu red: ").strip()
    if not red:
        break

    user = input(f"Ingresa tu usuario para {red}: ").strip()
    if user:
        redes_dict[red] = user
    else:
        print("Usuario vacío, red ignorada.")

perfil_final = crear_pfp(
    nombre,
    edad,
    *hobbies_list,
    **redes_dict
)

print(perfil_final)
