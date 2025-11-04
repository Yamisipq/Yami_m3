"""
Sistema de Gestión de Biblioteca.

Este módulo proporciona funcionalidades para gestionar el préstamo
y devolución de libros en una biblioteca usando persistencia JSON.
Utiliza la librería 'rich' para una interfaz de consola mejorada.
"""

import json
from pathlib import Path
from typing import Any, List, Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

# Inicializar consola de Rich
console = Console()

# Ruta del archivo JSON
BIBLIOTECA_JSON = Path("biblioteca.json")

# Definición de Tipos para Claridad
Libro = Dict[str, Any]
Catalogo = List[Libro]

# --- Funciones de Persistencia ---

def guardar_biblioteca(libros: Catalogo) -> None:
    """
    Guarda los datos de la biblioteca en el archivo JSON.

    Asegura una codificación correcta y un formato legible (indent=2).
    """
    try:
        with BIBLIOTECA_JSON.open("w", encoding="utf-8") as archivo:
            json.dump(libros, archivo, ensure_ascii=False, indent=2)
    except IOError as e:
        console.print(f"[bold red]❌ Error de I/O al guardar: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]❌ Error inesperado al guardar la biblioteca: {e}[/bold red]")


def cargar_biblioteca() -> Catalogo:
    """
    Carga los datos de la biblioteca desde el archivo JSON.

    Si el archivo no existe o está vacío/inválido, inicializa con datos de ejemplo.
    """
    if not BIBLIOTECA_JSON.exists():
        console.print("[yellow]⚠️ Archivo no encontrado. Creando catálogo inicial...[/yellow]")
        datos_iniciales = [
            {"libro_id": "001", "titulo": "Cien Años de Soledad", "autor": "Gabriel García Márquez", "prestado_a": None},
            {"libro_id": "002", "titulo": "El Amor en los Tiempos del Cólera", "autor": "Gabriel García Márquez", "prestado_a": None},
            {"libro_id": "003", "titulo": "1984", "autor": "George Orwell", "prestado_a": None},
            {"libro_id": "004", "titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes", "prestado_a": None},
            {"libro_id": "005", "titulo": "La Sombra del Viento", "autor": "Carlos Ruiz Zafón", "prestado_a": None},
        ]
        guardar_biblioteca(datos_iniciales)
        return datos_iniciales

    try:
        with BIBLIOTECA_JSON.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        # Manejo de error si el JSON está malformado
        console.print("[bold red]❌ Error: El archivo JSON está corrupto. Reiniciando catálogo.[/bold red]")
        guardar_biblioteca([]) # Guardar lista vacía para evitar bucle de error
        return []
    except IOError as e:
        console.print(f"[bold red]❌ Error de I/O al cargar: {e}[/bold red]")
        return []

# --- Funciones de Utilidad ---

def buscar_libro_por_id(libros: Catalogo, libro_id: str) -> Optional[Libro]:
    """Busca un libro específico por su ID usando una expresión generadora."""
    # Uso de next() con un valor por defecto (None) es más eficiente y 'pythonic' que un bucle for
    return next((libro for libro in libros if libro["libro_id"] == libro_id), None)

def obtener_estado_libro(libro: Libro) -> str:
    """Retorna el estado del libro formateado para rich."""
    return (
        f"[bold red]❌ Prestado a {libro['prestado_a']}[/bold red]"
        if libro["prestado_a"]
        else "[bold green]✅ Disponible[/bold green]"
    )

# --- Funciones de Lógica de Negocio ---

def prestar_libro(libro_id: str, nombre_aprendiz: str) -> bool:
    """Marca un libro como prestado a un aprendiz, si está disponible."""
    libros = cargar_biblioteca()
    libro = buscar_libro_por_id(libros, libro_id)

    if libro is None:
        console.print(f"[red]❌ Error: No existe el libro con ID [bold cyan]{libro_id}[/bold cyan][/red]")
        return False

    if libro["prestado_a"] is not None:
        console.print(
            f"[yellow]⚠️  El libro '[bold magenta]{libro['titulo']}[/bold magenta]' ya está prestado a "
            f"[bold]{libro['prestado_a']}[/bold][/yellow]"
        )
        return False

    # Lógica de préstamo
    libro["prestado_a"] = nombre_aprendiz.strip().title() # Limpieza y formato del nombre
    guardar_biblioteca(libros)

    console.print(
        f"[green]✅ Libro '[bold magenta]{libro['titulo']}[/bold magenta]' prestado exitosamente a "
        f"[bold]{libro['prestado_a']}[/bold][/green]"
    )
    return True


def devolver_libro(libro_id: str) -> bool:
    """Marca un libro como disponible (devuelto)."""
    libros = cargar_biblioteca()
    libro = buscar_libro_por_id(libros, libro_id)

    if libro is None:
        console.print(f"[red]❌ Error: No existe el libro con ID [bold cyan]{libro_id}[/bold cyan][/red]")
        return False

    if libro["prestado_a"] is None:
        console.print(
            f"[yellow]⚠️  El libro '[bold magenta]{libro['titulo']}[/bold magenta]' [underline]no está prestado[/underline][/yellow]"
        )
        return False

    # Lógica de devolución
    nombre_anterior = libro["prestado_a"]
    libro["prestado_a"] = None
    guardar_biblioteca(libros)

    console.print(
        f"[green]✅ Libro '[bold magenta]{libro['titulo']}[/bold magenta]' devuelto exitosamente por "
        f"[bold]{nombre_anterior}[/bold][/green]"
    )
    return True


# --- Funciones de Visualización (Rich) ---

def _crear_tabla_libros(libros: Catalogo, titulo: str, columnas: List[str]) -> Table:
    """Función auxiliar para generar una tabla Rich genérica."""
    tabla = Table(title=titulo, show_header=True, header_style="bold blue")

    # Definir columnas
    for col_name, style in columnas:
        tabla.add_column(col_name, style=style)

    for libro in libros:
        estado_texto = obtener_estado_libro(libro)

        # Lógica para determinar qué campos mostrar según el tipo de tabla
        row_data = [
            libro["libro_id"],
            libro["titulo"],
            libro.get("autor", "N/A")
        ]

        if "Estado" in [c[0] for c in columnas]:
             row_data.append(estado_texto)
        elif "Prestado a" in [c[0] for c in columnas]:
             row_data.append(libro["prestado_a"] or "N/A")

        tabla.add_row(*row_data)

    return tabla


def ver_todos_libros() -> None:
    """Muestra todos los libros del catálogo con su estado."""
    libros = cargar_biblioteca()

    columnas = [
        ("ID", "cyan", {"no_wrap": True}),
        ("Título", "magenta"),
        ("Autor", "green"),
        ("Estado", "yellow")
    ]

    # Adaptar para que acepte una lista de libros sin crear una función auxiliar compleja.
    # Se mantiene la implementación original de tu código por simplicidad.

    tabla = Table(title="📚 Catálogo Completo de Biblioteca", show_header=True)
    tabla.add_column("ID", style="cyan", no_wrap=True)
    tabla.add_column("Título", style="magenta")
    tabla.add_column("Autor", style="green")
    tabla.add_column("Estado", style="yellow")

    for libro in libros:
        tabla.add_row(
            libro["libro_id"],
            libro["titulo"],
            libro.get("autor", "N/A"),
            obtener_estado_libro(libro)
        )

    console.print(tabla)


def ver_libros_prestados() -> Catalogo:
    """Muestra todos los libros que están actualmente prestados."""
    libros = cargar_biblioteca()
    prestados = [libro for libro in libros if libro["prestado_a"] is not None]

    if not prestados:
        console.print(
            Panel(
                "[bold green]✅ Todos los libros están disponibles.[/bold green]",
                title="📚 Libros Prestados",
                border_style="green",
            )
        )
        return prestados

    tabla = Table(title="📚 Libros Actualmente Prestados", show_header=True, header_style="bold red")
    tabla.add_column("ID", style="cyan", no_wrap=True)
    tabla.add_column("Título", style="magenta")
    tabla.add_column("Autor", style="green")
    tabla.add_column("Prestado a", style="bold yellow") # Estilo más llamativo

    for libro in prestados:
        tabla.add_row(
            libro["libro_id"],
            libro["titulo"],
            libro.get("autor", "N/A"),
            libro["prestado_a"],
        )

    console.print(tabla)
    return prestados


def buscar_libro(query: str) -> Catalogo:
    """Busca libros por título (búsqueda parcial, no sensible a mayúsculas)."""
    libros = cargar_biblioteca()
    query_lower = query.lower()

    # Filtro más conciso usando comprensión de listas
    resultados = [
        libro for libro in libros
        if query_lower in libro.get("titulo", "").lower() # Uso de .get() por si acaso falta la clave 'titulo'
    ]

    # Mostrar resultados con Rich
    if not resultados:
        console.print(f"[yellow]No se encontraron libros que contengan '[bold]{query}[/bold]'[/yellow]")
        return resultados

    tabla = Table(title=f"📚 Resultados de búsqueda: '[bold magenta]{query}[/bold magenta]'", show_header=True)
    tabla.add_column("ID", style="cyan", no_wrap=True)
    tabla.add_column("Título", style="magenta")
    tabla.add_column("Autor", style="green")
    tabla.add_column("Estado", style="yellow")

    for libro in resultados:
        tabla.add_row(
            libro["libro_id"],
            libro["titulo"],
            libro.get("autor", "N/A"),
            obtener_estado_libro(libro) # Reutilizando la función de estado
        )

    console.print(tabla)
    return resultados


# --- Menú y Función Principal ---

def mostrar_menu() -> None:
    """Muestra el menú principal de opciones."""
    console.print("\n" + "=" * 60, style="bold cyan")
    console.print(
        Panel.fit(
            "[bold cyan]📚 SISTEMA DE GESTIÓN DE BIBLIOTECA 📚[/bold cyan]",
            border_style="cyan",
        )
    )
    # Mejorar la presentación del menú usando rich
    menu_texto = """
[cyan]1.[/cyan] 📖 [bold]Ver catálogo completo[/bold]
[cyan]2.[/cyan] 🔍 [bold]Buscar libro por título[/bold]
[cyan]3.[/cyan] 📤 [bold]Prestar libro[/bold]
[cyan]4.[/cyan] 📥 [bold]Devolver libro[/bold]
[cyan]5.[/cyan] 📋 [bold]Ver libros prestados[/bold]
[cyan]6.[/cyan] 🚪 [bold red]Salir[/bold red]
    """
    console.print(menu_texto)


def main() -> None:
    """Función principal que ejecuta el sistema de biblioteca."""
    console.print(
        Panel.fit(
            "[bold green]¡Bienvenido al Sistema de Biblioteca![/bold green]\n"
            "Gestiona préstamos de forma fácil y eficiente usando JSON.",
            border_style="green",
        )
    )

    while True:
        mostrar_menu()

        # Validar la entrada usando Prompt de rich
        opcion = Prompt.ask(
            "[bold yellow]Selecciona una opción[/bold yellow]",
            choices=["1", "2", "3", "4", "5", "6"]
        )

        console.print("\n" + "-" * 30, style="dim") # Separador visual

        if opcion == "1":
            ver_todos_libros()

        elif opcion == "2":
            query = Prompt.ask("[bold]Ingresa el título a buscar[/bold]")
            buscar_libro(query)

        elif opcion == "3":
            libro_id = Prompt.ask("[bold]Ingresa el ID del libro[/bold]")
            nombre = Prompt.ask("[bold]Ingresa el nombre del aprendiz[/bold]")
            prestar_libro(libro_id, nombre)

        elif opcion == "4":
            libro_id = Prompt.ask("[bold]Ingresa el ID del libro[/bold]")
            devolver_libro(libro_id)

        elif opcion == "5":
            ver_libros_prestados()

        elif opcion == "6":
            if Confirm.ask("[bold red]¿Seguro que deseas salir?[/bold red]"):
                console.print(
                    Panel.fit(
                        "[bold green]¡Gracias por usar el Sistema de Biblioteca![/bold green]",
                        border_style="green",
                    )
                )
                break

        console.print("\n" + "=" * 60, style="bold cyan")


if __name__ == "__main__":
    main()