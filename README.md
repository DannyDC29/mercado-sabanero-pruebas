# Mercado Sabanero - Módulo de Liquidación y Carrito de Compras

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/Testing-pytest-green)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)
![TDD](https://img.shields.io/badge/Methodology-TDD%20(Red--Green--Refactor)-red)

Este repositorio contiene la implementación y el conjunto de pruebas unitarias automatizadas para el módulo de liquidación de compras y carrito del ecommerce **Mercado Sabanero** (Sincelejo, Sucre). 

---

## Integrantes del Equipo

* **Daniela Díaz Caro** - GitHub: [@DannyDC29](https://github.com/DannyDC29)
* **Estefanía Villalba Paternina** - GitHub: [@Niabonita](https://github.com/Niabonita)

**Docente:** Laudyt María Lambraño Pérez  
**Asignatura:** Electiva Profesional en Ingeniería del Software  
**Institución:** Corporación Universitaria del Caribe – CECAR  

## Declaración del Uso de Inteligencia Artificial

En el desarrollo de este proyecto se utilizó la herramienta de Inteligencia Artificial **Google Gemini** como soporte académico para:

* **Comparativa de Tecnologías:** Análisis comparativo entre diferentes lenguajes de programación (Java, C#, Python, JS) y frameworks de pruebas para seleccionar la pila tecnológica más eficiente para el proyecto (Python + `pytest`).
* **Comprensión de Conceptos:** Profundización en las prácticas de TDD (*Red-Green-Refactor*), patrón AAA (*Arrange-Act-Assert*), diseño de pruebas parametrizadas y aislamiento mediante dobles de prueba (*Mocks*).
* **Estructuración y Generación:** Apoyo en la estructuración de la documentación del proyecto, maquetación de informes técnicos y aceleración en la escritura de la lógica de negocio y casos de prueba.

---

## Tecnologías y Herramientas

* **Lenguaje de Programación:** Python 3.10+
* **Framework de Pruebas Unitarias:** `pytest`
* **Dobles de Prueba (Mocks):** `unittest.mock` (`MagicMock`)
* **Reporte de Cobertura:** `coverage.py` / `pytest-cov`
* **Control de Versiones:** Git y GitHub

---

## Estructura del Proyecto

```text
mercado-sabanero-pruebas/
│
├── src/
│   ├── __init__.py
│   ├── producto.py       # Modelo de producto (ID, nombre, precio, tarifa_iva)
│   ├── cupones.py        # Validación y gestión de cupones de descuento
│   └── carrito.py        # Lógica de negocio del carrito y liquidación
│
├── tests/
│   ├── __init__.py
│   ├── test_hu01_carrito.py   # Pruebas de agregación y límites de stock (con Mocks)
│   ├── test_hu02_iva.py       # Pruebas de cálculo de IVA sobre base con descuento
│   ├── test_hu03_volumen.py   # Pruebas parametrizadas de descuentos por volumen
│   ├── test_hu04_cupones.py   # Pruebas de cupones y regla de descuento mayor
│   ├── test_hu05_envio.py     # Pruebas de envío regional y fórmula del total
│   └── test_hu06_puntos.py    # Pruebas de acumulación de puntos y ejemplo integrado
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/DannyDC29/mercado-sabanero-pruebas.git
   cd mercado-sabanero-pruebas
   ```

2. **Crear y activar el entorno virtual:**
   * En Windows (PowerShell / Git Bash):
     ```bash
     python -m venv venv
     source venv/Scripts/activate
     ```
   * En Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecución de Pruebas Unitarias

Para ejecutar el conjunto completo de pruebas unitarias automatizadas:

```bash
py -m pytest -v
```

Para ejecutar las pruebas de una historia de usuario específica (ej. HU-01):
```bash
py -m pytest tests/test_hu01_carrito.py -v
```

---

## Reporte de Cobertura de Código

Para ejecutar las pruebas y generar la métrica de cobertura de código sobre la carpeta `src/`:

```bash
py -m pytest --cov=src --cov-report=term-missing --cov-report=html
```

* **Visualización en Navegador:** Abre el archivo `htmlcov/index.html` generado localmente para inspeccionar la cobertura línea por línea.

---

## Flujo de Trabajo TDD (Red - Green - Refactor)

El proyecto fue desarrollado aplicando la metodología **Desarrollo Guiado por Pruebas (TDD)**, reflejada en el historial de commits:

1. 🔴 **ROJO (`test:`):** Creación de la prueba unitaria automatizada que falla inicialmente.
2. 🟢 **VERDE (`feat:`):** Implementación del código de producción mínimo para satisfacer la prueba.
3. 🔵 **REFACTOR (`refactor:`):** Optimización del diseño y limpieza del código manteniendo la prueba en verde.

---

## Caso Integrado Oficial Verificado

El sistema incluye la verificación automatizada del caso de prueba de la guía oficial:

* **Cliente:** ESTÁNDAR en Sincelejo, sin cupón.
* **Carrito:**
  * 1 Licuadora de $180.000 (IVA 19%)
  * 2 Cafés de $15.000 (IVA 5%)
  * 4 Arroces de $4.500 (IVA 0%)
* **Resultados Verificados Exitosamente:**
  * **Subtotal:** $228.000
  * **Descuento (5% volumen):** $11.400
  * **IVA (base imponible reducida):** $33.915
  * **Costo de Envío:** $0 (envío gratis por suma de productos con IVA ≥ $150.000)
  * **Total a Pagar:** $250.515
  * **Puntos Acumulados:** 250 puntos
