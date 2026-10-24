# src/carrito.py
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

    def liquidar_compra(self, municipio: str) -> dict:
        subtotal = sum(item.producto.precio * item.cantidad for item in self.items.values())

        # Descuento por Volumen (HU-03)
        pct_volumen = 0.10 if subtotal >= 500000 else (0.05 if subtotal >= 200000 else 0.0)

        # Descuento por Cupón (HU-04)
        pct_cupon = 0.10 if self.cupon_aplicado == "SABANERO10" and subtotal >= 50000 else 0.0

        # CA4: Se aplica únicamente el mayor entre ambos descuentos (no se suman)
        pct_descuento_final = max(pct_volumen, pct_cupon)
        monto_descuento = round(subtotal * pct_descuento_final)

        return {
            "subtotal": subtotal,
            "descuento": monto_descuento
        }