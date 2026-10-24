# tests/test_hu04_cupones.py
import pytest
from unittest.mock import MagicMock
from src.producto import Producto
from src.carrito import Carrito

def test_aplicar_cupon_sabanero10_exitoso():
    # CA1: Aplicar SABANERO10 con subtotal >= $50.000 otorga 10% de descuento
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10
    carrito = Carrito(servicio_inventario=mock_inv)
    prod = Producto("P01", "Licuadora", 100000, 0.0)
    carrito.agregar_producto(prod, 1)
    
    carrito.aplicar_cupon("SABANERO10")
    res = carrito.liquidar_compra("Sincelejo")
    assert res["descuento"] == 10000


def test_cupon_sabanero10_subtotal_insuficiente_lanza_excepcion():
    # CA1: Rechazar SABANERO10 si el subtotal es menor a $50.000
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10
    carrito = Carrito(servicio_inventario=mock_inv)
    prod = Producto("P01", "Café", 40000, 0.0)
    carrito.agregar_producto(prod, 1)
    
    with pytest.raises(ValueError, match="Error: Subtotal insuficiente para aplicar el cupón SABANERO10."):
        carrito.aplicar_cupon("SABANERO10")


def test_cupon_inexistente_o_vencido_lanza_excepcion():
    # CA3: Rechazar cupones no reconocidos o vencidos
    mock_inv = MagicMock()
    carrito = Carrito(servicio_inventario=mock_inv)
    with pytest.raises(ValueError, match="Error: Cupón inexistente o vencido."):
        carrito.aplicar_cupon("CUPON_FALSO")


def test_cupon_sabanero10_y_descuento_volumen_no_se_suman():
    # CA4: Si hay descuento por volumen (10%) y cupón SABANERO10 (10%), se aplica solo el mayor (no se suman a 20%)
    mock_inv = MagicMock()
    mock_inv.obtener_stock.return_value = 10
    carrito = Carrito(servicio_inventario=mock_inv)
    prod = Producto("P01", "TV", 600000, 0.0)
    carrito.agregar_producto(prod, 1)
    
    carrito.aplicar_cupon("SABANERO10")
    res = carrito.liquidar_compra("Sincelejo")
    assert res["descuento"] == 60000  # 10% de $600.000 ($60.000, no $120.000)