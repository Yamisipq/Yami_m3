import pytest
import arch_txt
from arch_txt import ver_tareas, agregar_tarea, eliminar_tarea


@pytest.fixture
def archivo_tareas_temp(tmp_path, monkeypatch):
    """Simula el archivo de tareas en un directorio temporal."""
    archivo = tmp_path / "tareas_test.txt"
    monkeypatch.setattr(arch_txt, "ARCHIVO_TAREAS", str(archivo))
    archivo.touch()
    return archivo



def test_ver_tareas_vacio(archivo_tareas_temp):
    """Test: Ver tareas cuando el archivo está vacío."""
    tareas = ver_tareas()
    assert tareas == []


def test_agregar_tarea(archivo_tareas_temp):
    """Test: Agregar nueva tarea y verificar su lectura."""
    agregar_tarea("Estudiar Python")
    tareas = ver_tareas()
    assert "Estudiar Python" in tareas


def test_agregar_tarea_duplicada(archivo_tareas_temp):
    """Test: No permitir tareas duplicadas."""
    agregar_tarea("Tarea 1")
    agregar_tarea("Tarea 1")
    tareas = ver_tareas()
    assert tareas.count("Tarea 1") == 1


def test_eliminar_tarea(archivo_tareas_temp, monkeypatch):
    """Test: Eliminar tarea existente, simulando confirmación de usuario."""
    agregar_tarea("Tarea a eliminar")
    agregar_tarea("Tarea a mantener")

    monkeypatch.setattr("builtins.input", lambda _: "s")
    eliminar_tarea(1)

    tareas = ver_tareas()
    assert "Tarea a eliminar" not in tareas
    assert "Tarea a mantener" in tareas