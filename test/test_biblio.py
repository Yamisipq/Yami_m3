import pytest
from biblioteca import (
    buscar_libro_por_id,
    prestar_libro,
    devolver_libro,
    guardar_biblioteca
)



@pytest.fixture
def catalogo_inicial():
    """Proporciona un catálogo de prueba."""
    return [
        {"libro_id": "001", "titulo": "Cien Años de Soledad", "autor": "García Márquez", "prestado_a": None},
        {"libro_id": "002", "titulo": "1984", "autor": "George Orwell", "prestado_a": "Juan Pérez"},
    ]


@pytest.fixture
def mock_biblioteca(tmp_path, monkeypatch, catalogo_inicial):
    """Simula el archivo JSON en un directorio temporal."""
    archivo = tmp_path / "biblioteca_test.json"


    monkeypatch.setattr("biblioteca.BIBLIOTECA_JSON", archivo)

    guardar_biblioteca(catalogo_inicial)
    return archivo



def test_buscar_libro_por_id_existente(catalogo_inicial):
    """Test: Buscar libro existente."""
    libro = buscar_libro_por_id(catalogo_inicial, "001")
    assert libro is not None
    assert libro["titulo"] == "Cien Años de Soledad"


def test_prestar_libro_exitoso(mock_biblioteca):
    """Test: Prestar libro disponible (usando el archivo mock)."""
    resultado = prestar_libro("001", "Ana García")
    assert resultado is True


def test_devolver_libro_exitoso(mock_biblioteca):
    """Test: Devolver libro que ya estaba prestado (usando el archivo mock)."""
    resultado = devolver_libro("002")
    assert resultado is True


def test_prestar_libro_ya_prestado(mock_biblioteca):
    """Test: Intentar prestar libro que ya tiene un prestatario."""
    resultado = prestar_libro("002", "Nuevo Prestatario")
    assert resultado is False