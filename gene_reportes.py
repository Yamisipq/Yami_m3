import csv
import json
import os
from rich.console import Console
from rich.text import Text

ESTUDIANTES_FILE = 'estudiantes.csv'
CURSOS_FILE = 'cursos.json'
REPORTE_FILE = 'reporte.txt'
console = Console()

def leer_csv(nombre_archivo):
    datos=[]

    try:
        with open(nombre_archivo,mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                row['id'] = int(row['id'])
                datos.append(row)
        return datos
    except FileNotFoundError:
        console.print(f"[red]El archivo '{nombre_archivo}' no fue encontrado.[/red]")
        return []
    except Exception as e:
        console.print(f"[red]Error al leer el archivo '{nombre_archivo}': {e}[/red]")
        return []

def leer_json(nombre_archivo):
    try:
        with open(nombre_archivo,mode='r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        console.print(f"[red]El archivo '{nombre_archivo}' no fue encontrado.[/red]")
        return []
    except json.decoder.JSONDecodeError:
        console.print(f"[red]El archivo '{nombre_archivo}' no es un archivo JSON válido.[/red]")
        return []
    except Exception as e:
        console.print(f"[red]Error al leer el archivo[red]")
        return []

def generar_reporte():

    estudiantes= leer_csv(ESTUDIANTES_FILE)
    cursos = leer_json(CURSOS_FILE)

    if not estudiantes or not cursos:
        console.print("[red]No hay datos para generar el reporte.[/red]")
        return

    estudiantes_dict = {estudiante['id']: estudiante['nombre'] for estudiante in estudiantes}

    lineas_reporte = []

    lineas_reporte.append("REPORTE DE ASIGNACIÓN DE CURSOS")

    estudiantes_cursos={}
    for id_estudiante in estudiantes_dict.keys():
        estudiantes_cursos[id_estudiante] = []

    for curso in cursos:
        nombre_curso = curso['nombre_curso']
        for id_estudiante in curso['estudiantes_ids']:
            if id_estudiante in estudiantes_cursos:
                estudiantes_cursos[id_estudiante].append(nombre_curso)

    for id_estudiante, nombre_estudiante in estudiantes_dict.items():
        cursos_asignados = estudiantes_cursos.get(id_estudiante, [])

        lineas_reporte.append(f"\n[{id_estudiante}] Estudiante: {nombre_estudiante}")
        lineas_reporte.append(f"Cursos Asignados:")
        if cursos_asignados:
            for curso in cursos_asignados:  # Esto itera sobre la lista de nombres. ¡Correcto!
                lineas_reporte.append(f"- {curso}")
        else:
            lineas_reporte.append("- No tiene cursos asignados.")
    reporte_contenido="\n".join(lineas_reporte)

    mostrar_reporte(reporte_contenido)

    try:
        with open(REPORTE_FILE, mode='w', encoding='utf-8') as f:
            f.write(reporte_contenido)
        console.print(f"[green]Reporte generado[/green]")
    except Exception as e:
        console.print(f"[red]Error al generar el reporte: {e}[/red]")


def mostrar_reporte(contenido):

    reporte_texto = Text(contenido)

    reporte_texto.highlight_regex(r"\[\d+\] Estudiante: .*", "bold yellow")
    reporte_texto.highlight_regex(r"Cursos tomados:", "bold magenta")
    reporte_texto.highlight_regex(r"- .*", "green")

    console.print(reporte_texto)
    console.rule("[bold cyan]FIN DE PREVISUALIZACIÓN[/bold cyan]")

if __name__ == "__main__":
    generar_reporte()