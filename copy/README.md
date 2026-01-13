# Backend - APC (Aplicación de Contabilidad Personal)

Este backend pertenece a una aplicación web de **gestión financiera personal**, pensada para **usuarios jóvenes** con **ingresos bajos** y **poca experiencia en gestión monetaria**.

El objetivo del backend es:

- gestionar usuarios
- almacenar ingresos
- calcular saldos y resúmenes
- permitir presupuestos sencillos
- ofrecer datos para estadísticas gráficas

Todo esto diseñado de forma **simple**, poniendo, por encima de todo, especial cuidado en la compresión del código.

---

## Herramientas

- **Python**
- **Flask** - framework para web, APIs, etc.
- **MySQL** - base de datos relacional
- **mysql-connector-python** - conectar Python y MySQL

## Estructura del backend del proyecto

backend/
|
|**app.py # Servidor Flask, donde se encuentra toda la lógica del backend
|**db.sql # Scripts de la creación de la base de datos y sus tablas
|\_\_README.md # Documentación del backend

## Base de datos

### Tablas principales

- `users` -> usuarios registrados
- `categories` -> categorías de ingresos y gastos
- `incomes` -> ingresos del usuario
- `expenses` -> gastos del usuario
- `budgets` -> presupuestos semanales o mensuales

Cada ingreso y gasto:

- pertenece a un usuario
- puede tener una categoría
- puede incluir una **nota identificativa**!SECTION
- tiene fecha y cantidad

## Pasos de ejecución del backend

1. - Crear la base de datos con los scripts del archivo **db.sql**
2. - Instalar mysql-connector-pyton
3. - Configurar la conexión a MySQL, ajustar la función **get_db** en **app.py**
4. - Ejecutar el servidor, **python3 /ruta del archivo/app.py**
