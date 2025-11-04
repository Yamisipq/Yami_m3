import json
import os
from rich.console import Console
from rich.table import Table

INVENTARIO_FILE = 'inventario.json'
console = Console()  # Inicializa la consola de rich


def cargar_inventario():
    """Carga el inventario desde el archivo JSON."""
    if not os.path.exists(INVENTARIO_FILE):
        return []
    try:
        with open(INVENTARIO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        console.print(
            "[bold yellow]Advertencia:[/bold yellow] Archivo de inventario vacío o inválido. Iniciando con inventario vacío.")
        return []
    except Exception as e:
        console.print(f"[bold red]Error al cargar inventario:[/bold red] {e}")
        return []


def guardar_inventario(inventario):
    """Guarda el inventario actual al archivo JSON."""
    try:
        with open(INVENTARIO_FILE, 'w', encoding='utf-8') as f:
            json.dump(inventario, f, ensure_ascii=False, indent=4)
        console.print("[bold green]Éxito:[/bold green] Inventario guardado correctamente.")
    except Exception as e:
        console.print(f"[bold red]Error al guardar inventario:[/bold red] {e}")




def agregar_producto(inventario):
    """Agrega un nuevo producto o actualiza la cantidad si ya existe."""
    nombre = input("Ingrese el nombre del producto: ").strip().capitalize()

    producto_existente = next((p for p in inventario if p['nombre'] == nombre), None)

    try:
        cantidad = int(input("Ingrese la cantidad a agregar: "))
        precio = float(input("Ingrese el precio unitario: "))
    except ValueError:
        console.print("[bold red]Error:[/bold red] Cantidad o precio inválido. Operación cancelada.")
        return

    if producto_existente:
        producto_existente['cantidad'] += cantidad
        producto_existente['precio'] = precio  # Se actualiza el precio
        console.print(f"[bold blue]Actualizado:[/bold blue] Cantidad de {nombre} aumentada.")
    else:
        inventario.append({
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio
        })
        console.print(f"[bold green]Agregado:[/bold green] Producto {nombre} añadido al inventario.")

    guardar_inventario(inventario)  # Punto 2: Guardar tras modificación


def realizar_venta(inventario):
    """Reduce la cantidad de un producto por venta."""
    nombre = input("Ingrese el nombre del producto a vender: ").strip().capitalize()
    producto = next((p for p in inventario if p['nombre'] == nombre), None)

    if not producto:
        console.print("[bold red]Error:[/bold red] Producto no encontrado.")
        return

    try:
        cantidad_venta = int(input(f"Cantidad de {nombre} a vender (Actual: {producto['cantidad']}): "))
    except ValueError:
        console.print("[bold red]Error:[/bold red] Cantidad inválida. Operación cancelada.")
        return

    if cantidad_venta <= 0:
        console.print("[bold yellow]Advertencia:[/bold yellow] La cantidad a vender debe ser positiva.")
    elif cantidad_venta > producto['cantidad']:
        console.print("[bold red]Error:[/bold red] No hay suficiente stock. Venta cancelada.")
    else:
        producto['cantidad'] -= cantidad_venta
        console.print(f"[bold green]Venta realizada:[/bold green] {cantidad_venta} unidades de {nombre} vendidas.")

        if producto['cantidad'] == 0:
            inventario.remove(producto)
            console.print(f"[bold yellow]Aviso:[/bold yellow] Producto {nombre} agotado y retirado del inventario.")

        guardar_inventario(inventario)

def mostrar_inventario(inventario):
    """Muestra el inventario en formato de tabla usando la librería rich."""
    if not inventario:
        console.print("[bold magenta]El inventario está vacío.[/bold magenta]")
        return

    table = Table(title="Inventario Actual", show_header=True, header_style="bold green")

    table.add_column("Nombre", justify="left")
    table.add_column("Cantidad", justify="center")
    table.add_column("Precio Unitario", justify="right")
    table.add_column("Valor Total", justify="right")

    total_inventario = 0

    for producto in inventario:
        valor_total_producto = producto['cantidad'] * producto['precio']
        total_inventario += valor_total_producto

        cantidad_str = str(producto['cantidad'])
        precio_str = f"${producto['precio']:.2f}"
        total_str = f"${valor_total_producto:.2f}"

        table.add_row(
            producto['nombre'],
            cantidad_str,
            precio_str,
            total_str
        )

    table.add_section()
    table.add_row(
        "[bold white]TOTAL INVENTARIO[/bold white]",
        "",
        "",
        f"[bold underline red]${total_inventario:.2f}[/bold underline red]"
    )

    # Imprimir la tabla en la consola
    console.print(table)


# --- Función Principal (Menú) ---

def main():
    inventario = cargar_inventario()  # Punto 1: Cargar al iniciar

    while True:
        console.print("\n[bold]*** GESTOR DE INVENTARIO ***[/bold]")
        console.print("1. Mostrar Inventario")
        console.print("2. Agregar Producto")
        console.print("3. Realizar Venta")
        console.print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            mostrar_inventario(inventario)
        elif opcion == '2':
            agregar_producto(inventario)
        elif opcion == '3':
            realizar_venta(inventario)
        elif opcion == '4':
            console.print("[bold green]Saliendo del programa. ¡Hasta pronto![/bold green]")
            break
        else:
            console.print("[bold red]Opción no válida.[/bold red] Intente de nuevo.")


if __name__ == "__main__":
    main()