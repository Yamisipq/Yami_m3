import pytest
import os
import csv
from unittest.mock import patch, mock_open, MagicMock

import datos_csv as ge



@pytest.fixture(autouse=True)
def mock_console_print():
    """Mockea console.print para evitar output real en los tests."""
    with patch('gestor_estudiantes.console.print') as mock_print:
        yield mock_print



@patch('os.path.exists', return_value=False)
@patch('builtins.open', new_callable=mock_open)
@patch('csv.writer')
def test_inicializar_archivo_crea_con_encabezados(mock_writer_class, mock_open, mock_exists, mock_console_print):
    """Prueba que el archivo se crea con encabezados si no existe."""
    ge.inicializar_archivo()


    mock_open.assert_called_once_with(ge.ARCHIVO_CSV, "w", newline="", encoding="utf-8")


    mock_writer_instance = mock_writer_class.return_value
    mock_writer_instance.writerow.assert_called_once_with(["nombre", "edad", "calificacion"])

    assert "creado exitosamente" in mock_console_print.call_args[0][0]


@patch('os.path.exists', return_value=True)
def test_inicializar_archivo_no_hace_nada_si_existe(mock_exists, mock_open):
    """Prueba que no se intenta crear/escribir si el archivo ya existe."""
    ge.inicializar_archivo()
    mock_open.assert_not_called()



@patch('builtins.input', side_effect=['', '25', '8.5'])
def test_agregar_estudiante_nombre_vacio(mock_input, mock_console_print):
    """Prueba la validación de nombre vacío."""
    ge.agregar_estudiante()
    assert "[red]El nombre no puede estar vacío.[/red]" in mock_console_print.call_args[0][0]


@patch('builtins.input', side_effect=['Carlos', 'veinte', '8.5'])
def test_agregar_estudiante_edad_invalida(mock_input, mock_console_print):
    """Prueba la validación de edad no numérica."""
    ge.agregar_estudiante()
    assert "[red]Edad y calificación deben ser valores numéricos.[/red]" in mock_console_print.call_args[0][0]


@patch('builtins.input', side_effect=['Elena', '22', '9.0'])
@patch('builtins.open', new_callable=mock_open)
@patch('csv.writer')
def test_agregar_estudiante_exitoso(mock_writer_class, mock_open, mock_input, mock_console_print):
    """Prueba la adición exitosa de un estudiante al CSV."""
    ge.agregar_estudiante()

    mock_open.assert_called_once_with(ge.ARCHIVO_CSV, "a", newline="", encoding="utf-8")

    mock_writer_instance = mock_writer_class.return_value
    mock_writer_instance.writerow.assert_called_once_with(['Elena', 22, 9.0])

    assert "Estudiante 'Elena' agregado correctamente." in mock_console_print.call_args[0][0]



@patch('builtins.open', new_callable=mock_open)
def test_analizar_calificaciones_archivo_vacio(mock_open):
    """Prueba que maneja un archivo vacío (solo encabezados)."""
    mock_open.return_value.read.return_value = 'nombre,edad,calificacion\n'

    with patch('csv.DictReader', return_value=[]):
        resultados = ge.analizar_calificaciones("test.csv")
        assert resultados == {"promedio": None, "max": None, "min": None}


def test_analizar_calificaciones_calculo_exitoso(mock_console_print):
    """Prueba el cálculo correcto de promedio, max y min."""
    csv_data = [
        {'nombre': 'A', 'edad': '20', 'calificacion': '8.0'},
        {'nombre': 'B', 'edad': '21', 'calificacion': '9.0'},
        {'nombre': 'C', 'edad': '19', 'calificacion': '7.0'},
        {'nombre': 'D', 'edad': '20', 'calificacion': 'invalido'},
    ]

    with patch('builtins.open', new_callable=mock_open) as mock_file:
        with patch('csv.DictReader', return_value=csv_data) as mock_reader:
            mock_reader.fieldnames = ["nombre", "edad", "calificacion"]

            resultados = ge.analizar_calificaciones("test.csv")

            assert resultados["promedio"] == pytest.approx(8.0)
            assert resultados["max"] == 9.0
            assert resultados["min"] == 7.0

            mock_console_print.assert_called_once()
            assert "Valor no numérico ignorado: 'invalido'" in mock_console_print.call_args[0][0]



@patch('generador_reporte.Table')
def test_mostrar_resultados_sin_datos(mock_table_class, mock_console_print):
    """Prueba que maneja el caso donde no hay resultados válidos."""
    resultados = {"promedio": None, "max": None, "min": None}
    ge.mostrar_resultados(resultados)
    mock_console_print.assert_called_once()
    assert "No hay datos para mostrar." in mock_console_print.call_args[0][0]
    mock_table_class.assert_not_called()


@patch('generador_reporte.Table')
def test_mostrar_resultados_tabla_correcta(mock_table_class, mock_console_print):
    """Prueba que la tabla se construye y se imprime con formato."""
    resultados = {"promedio": 8.123, "max": 9.5, "min": 6.0}

    mock_table_instance = MagicMock()
    mock_table_class.return_value = mock_table_instance

    ge.mostrar_resultados(resultados)

    mock_table_instance.add_row.assert_any_call("Promedio", "8.12")
    mock_table_instance.add_row.assert_any_call("Máximo", "9.50")
    mock_table_instance.add_row.assert_any_call("Mínimo", "6.00")

    mock_console_print.assert_called_once_with(mock_table_instance)
