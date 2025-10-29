tasa_iva = 0.19

def cal_iva(precio_base: float) -> float:
    """
    Calcula y muestra el precio total con IVA aplicado.

    Utiliza la tasa de IVA global (`tasa_iva`) para calcular el precio final,
    mostrando en pantalla el valor total con el impuesto incluido.

    Args:
        precio_base (float): Precio base del producto sin IVA.

    Returns:
        float: Valor total con IVA incluido.

    """
    global tasa_iva
    calculado = precio_base * tasa_iva
    total = calculado + precio_base
    print(f"Precio con el iva a:{tasa_iva}, Valor: {total}")
    return total


def act_iva(n_tasa: float) -> float:
    """
    Actualiza la tasa de IVA global y muestra el nuevo valor total con la nueva tasa aplicada.

    Modifica la variable global `tasa_iva` y calcula el precio total con la nueva tasa,
    utilizando la variable global `precio_base`.

    Args:
        n_tasa (float): Nueva tasa de IVA en formato decimal (por ejemplo, 0.21).

    Returns:
        float: Valor total con el nuevo IVA incluido.

    """
    global tasa_iva
    tasa_iva = n_tasa
    c_n = tasa_iva * precio_base
    total = c_n + precio_base
    print(f"Precio con el nuevo iva a:{tasa_iva}, Valor: {total}")
    return total


# --- Ejecución principal del programa ---
precio_base = float(input("Ingrese precio base: "))
n_tasa = float(input("Ingrese en decimal la nueva tasa actual (ej. 0.19): "))

if __name__ == "__main__":
    cal_iva(precio_base)
    act_iva(n_tasa)
