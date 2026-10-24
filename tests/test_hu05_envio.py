# tests/test_hu05_envio.py
import pytest
from unittest.mock import MagicMock
from src.producto import Producto
from src.carrito import Carrito

def test_costo_envio_sincelejo_y_otros_municipios():
    # HU-05 CA1: $8.000 en Sincelejo, $15.000 en otros municipios
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10

    # Test Sincelejo
    c1 = Carrito(servicio_inventario=mock_inv)
    c1.agregar_producto(Producto("P1", "Arroz", 10000, 0.0), 1)
    assert c1.liquidar_compra("Sincelejo")["envio"] == 8000

    # Test Corozal (Otro municipio)
    c2 = Carrito(servicio_inventario=mock_inv)
    c2.agregar_producto(Producto("P1", "Arroz", 10000, 0.0), 1)
    assert c2.liquidar_compra("Corozal")["envio"] == 15000


def test_envio_gratis_por_productos_con_iva_mayor_o_igual_150k():
    # HU-05 CA2: Si los productos con IVA suman $150.000 o más, el envío es gratis
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10
    carrito = Carrito(servicio_inventario=mock_inv)

    prod_con_iva = Producto("P1", "Licuadora", 150000, 0.19)
    carrito.agregar_producto(prod_con_iva, 1)

    res = carrito.liquidar_compra("Corozal")
    assert res["envio"] == 0


def test_formula_total_general():
    # HU-05 CA3: Total = Subtotal - Descuento + IVA + Envío
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10
    carrito = Carrito(servicio_inventario=mock_inv)

    prod = Producto("P1", "Licuadora", 100000, 0.19)  # IVA $19.000
    carrito.agregar_producto(prod, 1)

    res = carrito.liquidar_compra("Sincelejo")
    # Subtotal: 100.000 | Desc: 0 | IVA: 19.000 | Envío: 8.000 | Total: 127.000
    assert res["total"] == 100000 - 0 + 19000 + 8000