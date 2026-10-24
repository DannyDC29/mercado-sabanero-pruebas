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