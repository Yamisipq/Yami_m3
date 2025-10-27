def crear_pfp(nombre: str, edad: int, *hobbies: str, **redes_sociales: str) -> str:

    hobbies_str = ", ".join(hobbies) if hobbies else "No especificados."

    redes_lista=[]

    if redes_sociales:
        for red,user in redes_sociales.items():
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
        print("El valor ingresado no puede ser un numero")

hobbies_list=[]

print("Enter para terminar dejando vacío")
while True:
    hobby = input(f"Ingresa tu hobby #{len(hobbies_list)+1}: ").strip()
    if not hobby:
        break
    hobbies_list.append(hobby)

redes_dict={}

print("Deja vacío y enter para terminar")
while True:
    red = input("Ingresa tu red: ")
    if not red:
        break

    user=input(f"Ingresa tu user para {red}: ").strip()
    if user:
        redes_dict[red]=user
    else:
        print("No user red ignored")

perfil_final=crear_pfp(
    nombre,
    edad,
    *hobbies_list,
    **redes_dict
)
print(perfil_final)