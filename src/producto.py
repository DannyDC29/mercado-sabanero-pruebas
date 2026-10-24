class Producto:
    def __init__(self, id_prod: str, nombre: str, precio: int, tarifa_iva: float):
        self.id_prod = id_prod
        self.nombre = nombre
        self.precio = precio
        self.tarifa_iva = tarifa_iva