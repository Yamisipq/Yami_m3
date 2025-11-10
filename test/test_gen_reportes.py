import pytest
import json
from unittest.mock import patch, mock_open, MagicMock

import gene_reportes as gr


@pytest.fixture
def mock_estudiantes_data():
    """Datos CSV de estudiantes simulados."""
    return [
        {"id": "1", "nombre": "Ana López", "email": "ana@test.com"},
        {"id": "2", "nombre": "Juan Pérez", "email": "juan@test.com"},
        {"id": "3", "nombre": "María García", "email": "maria@test.com"},
    ]


@pytest.fixture
def mock_cursos_data():
    """Datos JSON de cursos simulados."""
    return [
        {"nombre_curso": "Python Básico", "estudiantes_ids": [1, 2]},
        {"nombre_curso": "Estructuras de Datos", "estudiantes_ids": [1, 3]},
        {"nombre_curso": "Web Development", "estudiantes_ids": [5, 6]},
    ]



@patch('builtins.open', new_callable=mock_open)
@patch('generador_reporte.console.print')
def test_leer_csv_file_not_found(mock_print, mock_file):
    """Prueba que leer_csv maneje FileNotFoundError correctamente."""
    mock_file.side_effect = FileNotFoundError
    resultado = gr.leer_csv("no_existe.csv")
    assert resultado == []
    mock_print.assert_called_once()
    assert "[red]El archivo 'no_existe.csv' no fue encontrado.[/red]" in mock_print.call_args[0][0]


@patch('builtins.open', new_callable=mock_open)
@patch('generador_reporte.console.print')
def test_leer_json_json_decode_error(mock_print, mock_file):
    """Prueba que leer_json maneje JSONDecodeError (JSON inválido)."""
    mock_file.read.return_value = '{"clave": "valor"'
    with patch('json.load', side_effect=json.decoder.JSONDecodeError('msg', 'doc', 1)):
        resultado = gr.leer_json("invalido.json")

    assert resultado == []
    mock_print.assert_called_once()
    assert "[red]El archivo 'invalido.json' no es un archivo JSON válido.[/red]" in mock_print.call_args[0][0]


def test_leer_csv_exitoso(mock_estudiantes_data):
    """Prueba la lectura exitosa de un CSV y la conversión de 'id' a int."""

    csv_content = "id,nombre,email\n1,Ana López,ana@test.com\n2,Juan Pérez,juan@test.com"

    with patch('builtins.open', mock_open(read_data=csv_content)):
        resultado = gr.leer_csv(gr.ESTUDIANTES_FILE)

        assert len(resultado) == 2
        assert resultado[0]['nombre'] == "Ana López"
        assert resultado[0]['id'] == 1
        assert isinstance(resultado[0]['id'], int)



@patch('generador_reporte.leer_csv', return_value=[])
@patch('generador_reporte.leer_json', return_value=[])
@patch('generador_reporte.console.print')
@patch('generador_reporte.mostrar_reporte')
@patch('builtins.open')
def test_generar_reporte_no_data(mock_open, mock_mostrar, mock_print, mock_json, mock_csv):
    """Prueba que si no hay datos de entrada, el reporte no se genere."""
    gr.generar_reporte()
    mock_print.assert_called_once()
    assert "[red]No hay datos para generar el reporte.[/red]" in mock_print.call_args[0][0]
    mock_mostrar.assert_not_called()
    mock_open.assert_not_called()


@patch('generador_reporte.leer_csv')
@patch('generador_reporte.leer_json')
@patch('generador_reporte.mostrar_reporte')
@patch('generador_reporte.console.print')
@patch('builtins.open', new_callable=mock_open)
def test_generar_reporte_exitoso(mock_file, mock_print, mock_json, mock_csv, mock_estudiantes_data,
                                 mock_cursos_data):
    """Prueba la lógica de asignación y el contenido final del reporte."""
    mock_csv.return_value = mock_estudiantes_data
    mock_json.return_value = mock_cursos_data

    gr.generar_reporte()

    mock_file.assert_called_with(gr.REPORTE_FILE, mode='w', encoding='utf-8')

    handle = mock_file()
    escrito = handle.write.call_args[0][0]

    assert "REPORTE DE ASIGNACIÓN DE CURSOS" in escrito
    assert "[1] Estudiante: Ana López" in escrito
    assert "- Python Básico" in escrito
    assert "- Estructuras de Datos" in escrito
    assert "[2] Estudiante: Juan Pérez" in escrito
    assert "Cursos Asignados:\n- Python Básico" in escrito
    assert "[3] Estudiante: María García" in escrito
    assert "Cursos Asignados:\n- Estructuras de Datos" in escrito


    mock_csv.return_value.append({"id": 4, "nombre": "Sin Cursos", "email": "sc@test.com"})
    gr.generar_reporte()
    escrito_nuevo = mock_file().write.call_args[0][0]
    assert "[4] Estudiante: Sin Cursos" in escrito_nuevo
    assert "No tiene cursos asignados." in escrito_nuevo

    mock_print.assert_any_call("[green]Reporte generado[/green]")



@patch('generador_reporte.console.print')
@patch('generador_reporte.Text')
def test_mostrar_reporte_llamadas_rich(mock_text_class, mock_print):
    """Prueba que mostrar_reporte llame correctamente a Text y resalte los patrones."""

    mock_text_instance = MagicMock()
    mock_text_class.return_value = mock_text_instance

    contenido_ejemplo = "REPORTE DE ASIGNACIÓN\n[1] Estudiante: Ana\nCursos Asignados:\n- Curso Uno"

    gr.mostrar_reporte(contenido_ejemplo)

    mock_text_class.assert_called_once_with(contenido_ejemplo)

    assert mock_text_instance.highlight_regex.call_count == 3

    mock_text_instance.highlight_regex.assert_any_call(
        r"\[\d+\] Estudiante: .*", "bold yellow"
    )
    mock_text_instance.highlight_regex.assert_any_call(
        r"- .*", "green"
    )


    mock_print.assert_any_call(mock_text_instance)
    mock_print.assert_any_call("[bold cyan]FIN DE PREVISUALIZACIÓN[/bold cyan]", console=gr.console.rule.return_value)