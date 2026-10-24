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