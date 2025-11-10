import os
from rich.console import Console
from rich.table import Table

ARCHIVO_TAREAS = "tareas.txt"
console = Console()

def ver_tareas() -> list[str]:
    """Lee todas las tareas del archivo y las devuelve como lista."""
    if not os.path.exists(ARCHIVO_TAREAS):
        # Si el archivo no existe, se crea vacío
        open(ARCHIVO_TAREAS, "w", encoding="utf-8").close()
        return []

    try:
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as f:
            tareas = [linea.strip() for linea in f if linea.strip()]
        return tareas
    except IOError as e:
        console.print(f"[red]Error al leer el archivo: {e}[/red]")
        return []

def agregar_tarea(tarea: str) -> None:
    """Agrega una nueva tarea al archivo, validando duplicados."""
    tarea = tarea.strip()
    if not tarea:
        console.print("[red]La tarea no puede estar vacía.[/red]")
        return

    tareas = ver_tareas()
    if tarea in tareas:
        console.print(f"[yellow]La tarea '{tarea}' ya existe en la lista.[/yellow]")
        return

    try:
        with open(ARCHIVO_TAREAS, "a", encoding="utf-8") as f:
            f.write(tarea + "\n")
        console.print(f"[green]Tarea '{tarea}' agregada correctamente.[/green]")
    except IOError as e:
        console.print(f"[red]Error al escribir en el archivo: {e}[/red]")

def eliminar_tarea(indice: int) -> None:
    """Elimina una tarea por su número."""
    tareas = ver_tareas()
    if not tareas:
        console.print("[yellow]No hay tareas para eliminar.[/yellow]")
        return

    if indice < 1 or indice > len(tareas):
        console.print("[red]Número de tarea inválido.[/red]")
        return

    tarea_a_eliminar = tareas[indice - 1]
    confirmacion = input(f"¿Está seguro de eliminar '{tarea_a_eliminar}'? (s/n): ").strip().lower()
    if confirmacion != "s":
        console.print("[cyan]Operación cancelada.[/cyan]")
        return

    del tareas[indice - 1]
    try:
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as f:
            for t in tareas:
                f.write(t + "\n")
        console.print(f"[green]Tarea '{tarea_a_eliminar}' eliminada correctamente.[/green]")
    except IOError as e:
        console.print(f"[red]Error al actualizar el archivo: {e}[/red]")

def mostrar_tareas(tareas: list[str]) -> None:
    """Muestra las tareas en una tabla usando rich."""
    if not tareas:
        console.print("[yellow]No hay tareas registradas.[/yellow]")
        return

    tabla = Table(title=" Lista de Tareas")
    tabla.add_column("N°", justify="right", style="cyan", no_wrap=True)
    tabla.add_column("Tarea", style="white")

    for i, tarea in enumerate(tareas, start=1):
        tabla.add_row(str(i), tarea)

    console.print(tabla)

def menu() -> None:
    console.print("\n[bold cyan]--- MENÚ DE GESTIÓN DE TAREAS ---[/bold cyan]")
    console.print("1. Mostrar todas las tareas")
    console.print("2. Agregar una nueva tarea")
    console.print("3. Eliminar una tarea")
    console.print("4. Salir")

def main():
    while True:
        menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            tareas = ver_tareas()
            mostrar_tareas(tareas)
        elif opcion == "2":
            tarea = input("Ingrese la nueva tarea: ").strip()
            agregar_tarea(tarea)
        elif opcion == "3":
            tareas = ver_tareas()
            mostrar_tareas(tareas)
            if tareas:
                try:
                    indice = int(input("Ingrese el número de la tarea a eliminar: ").strip())
                    eliminar_tarea(indice)
                except ValueError:
                    console.print("[red]Debe ingresar un número válido.[/red]")
        elif opcion == "4":
            console.print("[cyan]Saliendo del programa...[/cyan]")
            break
        else:
            console.print("[red]Opción no válida. Intente nuevamente.[/red]")

if __name__ == "__main__":
    main()
