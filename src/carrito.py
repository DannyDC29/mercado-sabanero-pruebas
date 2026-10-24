# src/carrito.py
class ItemCarrito:
    def __init__(self, producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad

class Carrito:
    def __init__(self, servicio_inventario=None):
        self.items = {}
        self.servicio_inventario = servicio_inventario

    def agregar_producto(self, producto, cantidad: int):
        stock_disponible = self.servicio_inventario.obtener_stock(producto.id_prod)
        if cantidad <= stock_disponible:
            self.items[producto.id_prod] = ItemCarrito(producto, cantidad)

    def liquidar_compra(self, municipio: str) -> dict:
        # 1. Calcular subtotal
        subtotal = sum(item.producto.precio * item.cantidad for item in self.items.values())

        # 2. Aplicar reglas de descuento por volumen (HU-03)
        if subtotal >= 500000:
            porcentaje_descuento = 0.10
        elif subtotal >= 200000:
            porcentaje_descuento = 0.05
        else:
            porcentaje_descuento = 0.0

        monto_descuento = round(subtotal * porcentaje_descuento)

        return {
            "subtotal": subtotal,
            "descuento": monto_descuento
        }