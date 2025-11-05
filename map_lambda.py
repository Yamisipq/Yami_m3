def aplicar_descuento(productos: list, descuento: float = 0.1) -> list:
    """
    Aplica un descuento a una lista de productos y devuelve una lista
    con los precios finales después del descuento.

    Args:
        productos (list): Lista de diccionarios con las claves:
            - "nombre" (str): Nombre del producto.
            - "precio" (float): Precio original del producto.
        descuento (float, opcional): Porcentaje de descuento expresado en decimal.
            Por defecto es 0.1 (equivale al 10%).

    Returns:
        list: Lista con los precios de los productos luego de aplicar el descuento.
    """
    precios_descuento = list(map(lambda p: p["precio"] * (1 - descuento), productos))
    return precios_descuento

if __name__ == "__main__":
    productos = [
        {"nombre": "Camisa", "precio": 50000},
        {"nombre": "Pantalón", "precio": 80000},
        {"nombre": "Zapatos", "precio": 120000},
        {"nombre": "Chaqueta", "precio": 150000}
    ]

    precios_con_descuento = aplicar_descuento(productos, 0.1)
    print(precios_con_descuento)
