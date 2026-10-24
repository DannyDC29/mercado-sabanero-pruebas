# tests/test_hu03_volumen.py
import pytest
from unittest.mock import MagicMock
from src.producto import Producto
from src.carrito import Carrito

# Prueba parametrizada para valores límite de HU-03 (CA1, CA2, CA3)
@pytest.mark.parametrize("subtotal_compra, descuento_esperado", [
    (199999, 0),       # CA1: Menor a $200.000 -> 0% descuento
    (200000, 10000),   # CA2: Desde $200.000 (5%) -> $10.000
    (499999, 25000),   # CA2: Justo antes de $500.000 (5%) -> $24.999.95 ~ $25.000
    (500000, 50000)    # CA3: Desde $500.000 (10%) -> $50.000
])
def test_descuento_por_volumen_limites(subtotal_compra, descuento_esperado):
    # Arrange
    mock_inventario = MagicMock()
    mock_inventario.obtener_stock.return_value = 100
    
    carrito = Carrito(servicio_inventario=mock_inventario)
    prod = Producto(id_prod="P_GENERICO", nombre="Producto Prueba", precio=subtotal_compra, tarifa_iva=0.0)
    carrito.agregar_producto(prod, 1)

    # Act (Llamada al método liquidar_compra que aún no existe)
    resultado = carrito.liquidar_compra(municipio="Sincelejo")

    # Assert
    assert resultado["descuento"] == descuento_esperado