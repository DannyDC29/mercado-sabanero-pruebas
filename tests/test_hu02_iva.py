# tests/test_hu02_iva.py
import pytest
from unittest.mock import MagicMock
from src.producto import Producto
from src.carrito import Carrito

def test_calculo_iva_tarifas_sin_descuento():
    # HU-02 CA1: Calcular IVA para productos con tarifas 0%, 5% y 19%
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10
    carrito = Carrito(servicio_inventario=mock_inv)

    prod_iva_19 = Producto("P01", "Licuadora", 100000, 0.19)  # IVA $19.000
    prod_iva_5  = Producto("P02", "Café", 10000, 0.05)       # IVA $500
    prod_iva_0  = Producto("P03", "Arroz", 5000, 0.00)       # IVA $0

    carrito.agregar_producto(prod_iva_19, 1)
    carrito.agregar_producto(prod_iva_5, 1)
    carrito.agregar_producto(prod_iva_0, 1)

    res = carrito.liquidar_compra("Sincelejo")
    assert res["iva"] == 19500  # $19.000 + $500 + $0


def test_calculo_iva_con_descuento_aplicado():
    # HU-02 CA2: El IVA se calcula sobre el valor del producto con el descuento aplicado
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10
    carrito = Carrito(servicio_inventario=mock_inv)

    # Subtotal $200.000 -> Aplica 5% de descuento por volumen ($10.000 desc -> Base imponible = $190.000)
    prod = Producto("P01", "Electrodoméstico", 200000, 0.19)
    carrito.agregar_producto(prod, 1)

    res = carrito.liquidar_compra("Sincelejo")
    # Base $190.000 * 0.19 = $36.100 de IVA
    assert res["descuento"] == 10000
    assert res["iva"] == 36100