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
        # CA2: Validar rango de unidades
        if cantidad <= 0 or cantidad > 50:
            raise ValueError("Error: La cantidad a agregar debe estar entre 1 y 50 unidades.")

        # Consultar stock mediante el mock
        stock_disponible = self.servicio_inventario.obtener_stock(producto.id_prod)
        
        cantidad_actual = self.items[producto.id_prod].cantidad if producto.id_prod in self.items else 0
        
        # CA3: Validar si excede el stock
        if (cantidad_actual + cantidad) > stock_disponible:
            raise ValueError("Error: El stock es insuficiente.")

        # CA4: Sumar cantidades si ya existe
        if producto.id_prod in self.items:
            self.items[producto.id_prod].cantidad += cantidad
        else:
            self.items[producto.id_prod] = ItemCarrito(producto, cantidad)

    def liquidar_compra(self, municipio: str) -> dict:
        subtotal = sum(item.producto.precio * item.cantidad for item in self.items.values())

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