# src/carrito.py
import math
from src.cupones import GestorCupones

class ItemCarrito:
    def __init__(self, producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad

class Carrito:
    def __init__(self, servicio_inventario=None):
        self.items = {}
        self.servicio_inventario = servicio_inventario
        self.cupon_aplicado = None

    def agregar_producto(self, producto, cantidad: int):
        if cantidad <= 0 or cantidad > 50:
            raise ValueError("Error: La cantidad a agregar debe estar entre 1 y 50 unidades.")

        stock_disponible = self.servicio_inventario.obtener_stock(producto.id_prod)
        cantidad_actual = self.items[producto.id_prod].cantidad if producto.id_prod in self.items else 0
        
        if (cantidad_actual + cantidad) > stock_disponible:
            raise ValueError("Error: El stock es insuficiente.")

        if producto.id_prod in self.items:
            self.items[producto.id_prod].cantidad += cantidad
        else:
            self.items[producto.id_prod] = ItemCarrito(producto, cantidad)

    def aplicar_cupon(self, codigo: str):
        GestorCupones.validar_cupon(codigo)
        subtotal = sum(item.producto.precio * item.cantidad for item in self.items.values())
        if codigo == "SABANERO10" and subtotal < 50000:
            raise ValueError("Error: Subtotal insuficiente para aplicar el cupón SABANERO10.")
        self.cupon_aplicado = codigo

    def liquidar_compra(self, municipio: str, categoria_cliente: str = "ESTÁNDAR") -> dict:
        # 1. Subtotal
        subtotal = sum(item.producto.precio * item.cantidad for item in self.items.values())

        # 2. Descuentos (HU-03 y HU-04)
        pct_volumen = 0.10 if subtotal >= 500000 else (0.05 if subtotal >= 200000 else 0.0)
        pct_cupon = 0.10 if self.cupon_aplicado == "SABANERO10" and subtotal >= 50000 else 0.0

        pct_descuento_final = max(pct_volumen, pct_cupon)
        monto_descuento = round(subtotal * pct_descuento_final)

        # 3. Cálculo de IVA con descuento aplicado (HU-02)
        total_iva = 0.0
        suma_base_productos_con_iva = 0
        for item in self.items.values():
            base_item = (item.producto.precio * item.cantidad) * (1 - pct_descuento_final)
            iva_item = base_item * item.producto.tarifa_iva
            total_iva += iva_item

            if item.producto.tarifa_iva > 0:
                suma_base_productos_con_iva += (item.producto.precio * item.cantidad)

        total_iva = round(total_iva)

        # 4. Cálculo de Envío (HU-05)
        if self.cupon_aplicado == "ENVIOGRATIS" or suma_base_productos_con_iva >= 150000:
            costo_envio = 0
        elif municipio.lower() == "sincelejo":
            costo_envio = 8000
        else:
            costo_envio = 15000

        # 5. Total General (HU-05 CA3)
        total_pagar = subtotal - monto_descuento + total_iva + costo_envio

        # 6. Puntos acumulados (HU-06)
        total_sin_envio = subtotal - monto_descuento + total_iva
        puntos_base = math.floor(total_sin_envio / 1000)
        puntos_finales = puntos_base * 2 if categoria_cliente.upper() == "ORO" else puntos_base

        return {
            "subtotal": subtotal,
            "descuento": monto_descuento,
            "iva": total_iva,
            "envio": costo_envio,
            "total": total_pagar,
            "puntos": puntos_finales
        }