import csv
import os
from rich.console import Console
from rich.table import Table

console = Console()
ARCHIVO_CSV = "datos_e.csv"


def inicializar_archivo():
    """Crea el archivo CSV con encabezados si no existe."""
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["nombre", "edad", "calificacion"])
        console.print(f"[green]Archivo '{ARCHIVO_CSV}' creado exitosamente.[/green]")


def agregar_estudiante():
    """Permite ingresar un nuevo estudiante al CSV."""
    nombre = input("Ingrese el nombre del estudiante: ").strip()
    if not nombre:
        console.print("[red]El nombre no puede estar vacío.[/red]")
        return

    try:
        edad = int(input("Ingrese la edad: ").strip())
        calificacion = float(input("Ingrese la calificación: ").strip())
    except ValueError:
        console.print("[red]Edad y calificación deben ser valores numéricos.[/red]")
        return

    with open(ARCHIVO_CSV, "a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow([nombre, edad, calificacion])

    console.print(f"[green]Estudiante '{nombre}' agregado correctamente.[/green]")


def analizar_calificaciones(nombre_archivo: str) -> dict:
    """Analiza la columna 'calificacion' del CSV."""
    resultados = {"promedio": None, "max": None, "min": None}

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            if "calificacion" not in lector.fieldnames:
                console.print("[red]No se encontró la columna 'calificacion' en el archivo.[/red]")
                return resultados

            valores = []
            for fila in lector:
                valor = fila.get("calificacion", "").strip()
                if valor:
                    try:
                        valores.append(float(valor))
                    except ValueError:
                        console.print(f"[yellow]⚠ Valor no numérico ignorado: '{valor}'[/yellow]")

            if not valores:
                console.print("[red]No hay valores válidos en la columna 'calificacion'.[/red]")
                return resultados

            resultados["promedio"] = sum(valores) / len(valores)
            resultados["max"] = max(valores)
            resultados["min"] = min(valores)
            return resultados

    except FileNotFoundError:
        console.print(f"[red]El archivo '{nombre_archivo}' no existe.[/red]")
    except IOError as e:
        console.print(f"[red]Error al leer el archivo: {e}[/red]")

    return resultados


def mostrar_resultados(resultados: dict):
    """Muestra los resultados del análisis en una tabla con rich."""
    if not resultados["promedio"]:
        console.print("[yellow]⚠ No hay datos para mostrar.[/yellow]")
        return

    tabla = Table(title="Análisis de Calificaciones")
    tabla.add_column("Estadística", justify="left", style="bold cyan")
    tabla.add_column("Valor", justify="right", style="green")

    tabla.add_row("Promedio", f"{resultados['promedio']:.2f}")
    tabla.add_row("Máximo", f"{resultados['max']:.2f}")
    tabla.add_row("Mínimo", f"{resultados['min']:.2f}")

    console.print(tabla)

def main():
    inicializar_archivo()

    while True:
        console.print("\n[bold blue]--- MENÚ DE GESTIÓN DE ESTUDIANTES ---[/bold blue]")
        console.print("1. Agregar estudiante")
        console.print("2. Analizar calificaciones")
        console.print("3. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_estudiante()
        elif opcion == "2":
            resultados = analizar_calificaciones(ARCHIVO_CSV)
            if any(resultados.values()):
                mostrar_resultados(resultados)
        elif opcion == "3":
            console.print("[cyan]Saliendo del programa...[/cyan]")
            break
        else:
            console.print("[red]Opción no válida, intente nuevamente.[/red]")


if __name__ == "__main__":
    main()
