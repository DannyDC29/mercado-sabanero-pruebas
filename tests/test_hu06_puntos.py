# tests/test_hu06_puntos.py
import pytest
from unittest.mock import MagicMock
from src.producto import Producto
from src.carrito import Carrito

def test_acumular_puntos_cliente_estandar():
    # HU-06 CA1: 1 punto por cada $1.000 completos (sin incluir el envío)
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10
    carrito = Carrito(servicio_inventario=mock_inv)

    # Subtotal $100.000 (sin IVA ni desc) + $8.000 envío = Total $108.000
    prod = Producto("P01", "Arroz", 100000, 0.0)
    carrito.agregar_producto(prod, 1)

    res = carrito.liquidar_compra(municipio="Sincelejo", categoria_cliente="ESTÁNDAR")
    # Puntos sobre $100.000 sin envío -> 100 puntos
    assert res["puntos"] == 100


def test_acumular_puntos_cliente_oro_recibe_doble():
    # HU-06 CA2: Cliente ORO recibe el doble de puntos
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10
    carrito = Carrito(servicio_inventario=mock_inv)

    prod = Producto("P01", "Arroz", 100000, 0.0)
    carrito.agregar_producto(prod, 1)

    res = carrito.liquidar_compra(municipio="Sincelejo", categoria_cliente="ORO")
    # Puntos base 100 * 2 = 200 puntos
    assert res["puntos"] == 200


def test_ejemplo_oficial_mercado_sabanero():
    # Ejemplo de verificación del taller (HU-06)
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 100
    carrito = Carrito(servicio_inventario=mock_inv)

    licuadora = Producto("P1", "Licuadora", 180000, 0.19)
    cafe      = Producto("P2", "Café", 15000, 0.05)
    arroz     = Producto("P3", "Arroz", 4500, 0.00)

    carrito.agregar_producto(licuadora, 1)
    carrito.agregar_producto(cafe, 2)
    carrito.agregar_producto(arroz, 4)

    res = carrito.liquidar_compra(municipio="Sincelejo", categoria_cliente="ESTÁNDAR")

    assert res["subtotal"] == 228000
    assert res["descuento"] == 11400
    assert res["iva"] == 33915
    assert res["envio"] == 0
    assert res["total"] == 250515
    assert res["puntos"] == 250