# src/cupones.py
class GestorCupones:
    CUPONES_VALIDOS = {"SABANERO10", "ENVIOGRATIS"}

    @staticmethod
    def validar_cupon(codigo: str):
        if codigo not in GestorCupones.CUPONES_VALIDOS:
            raise ValueError("Error: Cupón inexistente o vencido.")