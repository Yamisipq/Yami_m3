import pytest
import json
from unittest.mock import patch, mock_open, MagicMock

import persis_json as gi


@pytest.fixture
def inventario_mock_data():
    """Retorna un inventario de prueba para usar en los tests."""
    return [
        {'nombre': 'Manzana', 'cantidad': 100, 'precio': 0.5},
        {'nombre': 'Pera', 'cantidad': 50, 'precio': 0.75}
    ]


@pytest.fixture(autouse=True)
def mock_console_print():
    """Mockea console.print y console.rule globalmente para evitar output real."""
    with patch('gestor_inventario.console.print') as mock_print, \
            patch('gestor_inventario.console.rule'):
        yield mock_print



@patch('os.path.exists', return_value=False)
def test_cargar_inventario_no_existe(mock_exists):
    """Prueba que devuelve [] si el archivo no existe."""
    inventario = gi.cargar_inventario()
    assert inventario == []


@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='[{"nombre": "Leche", "cantidad": 10, "precio": 2.5}]')
def test_cargar_inventario_exitoso(mock_open, mock_exists):
    """Prueba la carga exitosa de un JSON válido."""
    inventario = gi.cargar_inventario()
    assert inventario == [{'nombre': 'Leche', 'cantidad': 10, 'precio': 2.5}]


@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='[inválido')
def test_cargar_inventario_json_invalido(mock_open, mock_exists, mock_console_print):
    """Prueba que maneja JSONDecodeError y alerta al usuario."""
    with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0)):
        inventario = gi.cargar_inventario()
        assert inventario == []
        mock_console_print.assert_called_once()
        assert "Archivo de inventario vacío o inválido" in mock_console_print.call_args[0][0]



@patch('builtins.open', new_callable=mock_open)
@patch('json.dump')
def test_guardar_inventario_exitoso(mock_dump, mock_open, mock_console_print, inventario_mock_data):
    """Prueba que el inventario se guarda correctamente en JSON."""
    gi.guardar_inventario(inventario_mock_data)

    mock_open.assert_called_once_with(gi.INVENTARIO_FILE, 'w', encoding='utf-8')

    mock_dump.assert_called_once_with(
        inventario_mock_data,
        mock_open(),
        ensure_ascii=False,
        indent=4
    )
    mock_console_print.assert_called_once()
    assert "[bold green]Éxito:[/bold green] Inventario guardado correctamente." in mock_console_print.call_args[0][0]



@patch('gestor_inventario.guardar_inventario')
def test_agregar_producto_nuevo_exitoso(mock_guardar, monkeypatch, inventario_mock_data):
    """Prueba la adición de un nuevo producto con datos válidos."""
    user_inputs = iter(['Chocolate', '50', '3.50'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    inventario = inventario_mock_data[:]
    gi.agregar_producto(inventario)

    assert len(inventario) == 3
    producto_nuevo = inventario[-1]
    assert producto_nuevo['nombre'] == 'Chocolate'
    assert producto_nuevo['cantidad'] == 50
    assert producto_nuevo['precio'] == 3.5
    mock_guardar.assert_called_once()


@patch('gestor_inventario.guardar_inventario')
def test_agregar_producto_existente_actualiza(mock_guardar, monkeypatch, inventario_mock_data):
    """Prueba la actualización de cantidad y precio de un producto existente."""
    user_inputs = iter(['Manzana', '20', '0.60'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    inventario = inventario_mock_data[:]
    gi.agregar_producto(inventario)

    producto_actualizado = inventario[0]
    assert producto_actualizado['cantidad'] == 120
    assert producto_actualizado['precio'] == 0.60
    mock_guardar.assert_called_once()



@patch('gestor_inventario.guardar_inventario')
def test_realizar_venta_exitosa_parcial(mock_guardar, monkeypatch, inventario_mock_data):
    """Prueba una venta parcial exitosa."""
    user_inputs = iter(['Manzana', '10'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    inventario = inventario_mock_data[:]
    gi.realizar_venta(inventario)

    producto = inventario[0]
    assert producto['nombre'] == 'Manzana'
    assert producto['cantidad'] == 90
    assert len(inventario) == 2
    mock_guardar.assert_called_once()


@patch('gestor_inventario.guardar_inventario')
def test_realizar_venta_existosa_agota_stock(mock_guardar, monkeypatch, inventario_mock_data):
    """Prueba una venta que agota el stock y elimina el producto."""
    user_inputs = iter(['Pera', '50'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    inventario = inventario_mock_data[:]
    gi.realizar_venta(inventario)

    assert len(inventario) == 1
    assert inventario[0]['nombre'] == 'Manzana'
    mock_guardar.assert_called_once()


def test_realizar_venta_stock_insuficiente(monkeypatch, inventario_mock_data, mock_console_print):
    """Prueba la cancelación por falta de stock."""
    user_inputs = iter(['Manzana', '101'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    inventario = inventario_mock_data[:]
    gi.realizar_venta(inventario)

    assert inventario[0]['cantidad'] == 100
    assert "No hay suficiente stock" in mock_console_print.call_args[0][0]



@patch('generador_reporte.Table')
def test_mostrar_inventario_vacio(mock_table_class, inventario_mock_data, mock_console_print):
    """Prueba el mensaje si el inventario está vacío."""
    gi.mostrar_inventario([])
    mock_console_print.assert_called_once()
    assert "[bold magenta]El inventario está vacío.[/bold magenta]" in mock_console_print.call_args[0][0]
    mock_table_class.assert_not_called()


@patch('generador_reporte.Table')
def test_mostrar_inventario_calculo_total(mock_table_class, inventario_mock_data, mock_console_print):
    """Prueba que la tabla se construye correctamente y calcula el total."""

    mock_table_instance = MagicMock()
    mock_table_class.return_value = mock_table_instance

    gi.mostrar_inventario(inventario_mock_data)


    mock_table_instance.add_row.assert_any_call('Manzana', '100', '$0.50', '$50.00')
    mock_table_instance.add_row.assert_any_call('Pera', '50', '$0.75', '$37.50')

    mock_table_instance.add_row.assert_any_call(
        "[bold white]TOTAL INVENTARIO[/bold white]",
        "",
        "",
        "[bold underline red]$87.50[/bold underline red]"
    )

    mock_console_print.assert_called_once_with(mock_table_instance)