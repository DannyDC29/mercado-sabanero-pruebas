# tests/test_hu01_carrito.py
import pytest
from unittest.mock import MagicMock

# Aplicando patrón AAA (Arrange, Act, Assert)
def test_agregar_producto_cantidad_valida_exitoso():
    # Arrange: Preparar mock de inventario, carrito y producto
    mock_inventario = MagicMock()
    mock_inventario.obtener_stock.return_value = 20  # Stock suficiente
    
    # Importaciones (fallarán porque aún no existen las clases)
    from src.producto import Producto
    from src.carrito import Carrito

    carrito = Carrito(servicio_inventario=mock_inventario)
    producto = Producto(id_prod="P01", nombre="Arroz 1kg", precio=4500, tarifa_iva=0.0)

    # Act: Agregar 5 unidades (dentro del rango 1 a 50)
    carrito.agregar_producto(producto, 5)

    # Assert: Verificar que el producto quedó en el carrito
    assert "P01" in carrito.items
    assert carrito.items["P01"].cantidad == 5
# Pruebas adicionales para HU-01 (CA2, CA3, CA4)

def test_agregar_producto_cantidad_invalida_lanza_excepcion():
    # CA2: Excepción si la cantidad es 0 o mayor a 50
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 100
    from src.producto import Producto
    from src.carrito import Carrito

    carrito = Carrito(servicio_inventario=mock_inv)
    prod = Producto("P01", "Arroz", 4500, 0.0)

    # Probar con 0 unidades
    with pytest.raises(ValueError, match="Error: La cantidad a agregar debe estar entre 1 y 50 unidades."):
        carrito.agregar_producto(prod, 0)

    # Probar con 51 unidades
    with pytest.raises(ValueError, match="Error: La cantidad a agregar debe estar entre 1 y 50 unidades."):
        carrito.agregar_producto(prod, 51)


def test_agregar_producto_stock_insuficiente_lanza_excepcion():
    # CA3: Prueba con Doble de Prueba (Mock) para stock insuficiente
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 3  # Stock solo de 3 unidades
    from src.producto import Producto
    from src.carrito import Carrito

    carrito = Carrito(servicio_inventario=mock_inv)
    prod = Producto("P01", "Arroz", 4500, 0.0)

    with pytest.raises(ValueError, match="Error: El stock es insuficiente."):
        carrito.agregar_producto(prod, 5)  # Pide 5 habiendo solo 3


def test_agregar_producto_ya_existente_suma_cantidades():
    # CA4: Sumar cantidades si el producto ya está en el carrito
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 20
    from src.producto import Producto
    from src.carrito import Carrito

    carrito = Carrito(servicio_inventario=mock_inv)
    prod = Producto("P01", "Arroz", 4500, 0.0)

    carrito.agregar_producto(prod, 2)
    carrito.agregar_producto(prod, 3)

    assert carrito.items["P01"].cantidad == 5

