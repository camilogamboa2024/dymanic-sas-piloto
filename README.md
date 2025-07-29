# 📦 Dymanic SAS – Gestión de Inventario, Ventas y Reportes

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

<!-- ¡Añade tu badge de CI/CD cuando subas el workflow! -->

> **Dymanic SAS** es una plataforma *SaaS* que integra **inventario**, **facturación** y **analítica** para micro‑y pequeñas empresas latinoamericanas. El objetivo es reducir hasta **40 %** del tiempo destinado al control de stock y **25 %** de los costos de reposición.

---

## ✨ Características principales

| Módulo         | Funcionalidades clave                                |
| -------------- | ---------------------------------------------------- |
| **Inventario** | CRUD de productos, categorías y movimientos de stock |
| **Ventas**     | Clientes, facturas, líneas de venta y resumen        |
| **Reportes**   | Productos más vendidos y rotación de inventario      |

---

## 🖥️ Stack tecnológico

* **Backend:** Python 3.11 · Django 4.2
* **Base de datos (dev):** SQLite 3 (por defecto)
* **Base de datos (prod):** PostgreSQL ≥ 12 *(opcional)*
* **Frontend:** Templates Django + HTMX
* **DevOps:** Git · GitHub Actions (tests & deploy) · Render (PaaS)

---

## 🚀 Instalación local rápida

> Probado en **Linux/macOS** y **Windows 10/11**.

### Requisitos previos

* Python 3.11+
* Git
* **(Opcional)** PostgreSQL si vas a usarlo en producción/staging

### 1 – Clona el repositorio

```bash
git clone https://github.com/camilogamboa2024/dymanic-sas.git
cd dymanic-sas
```

### 2 – Crea y activa un entorno virtual

| SO                     | Comando                                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------------------- |
| **Linux/macOS**        | `python3 -m venv venv && source venv/bin/activate`                                              |
| **Windows CMD**        | `python -m venv venv && venv\Scripts\activate.bat`                                              |
| **Windows PowerShell** | 1️⃣ `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`  2️⃣ `./venv/Scripts/Activate` |

> ⚠️ En Windows evita carpetas sincronizadas (p.ej. OneDrive) para reducir problemas de permisos.

### 3 – Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4 – Aplica migraciones y crea un superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5 – Arranca el servidor

```bash
python manage.py runserver
```

Visita `http://127.0.0.1:8000/` y ¡listo!

---

## ⚙️ Variables de entorno (`.env`)

Copia `.env.example` → `.env` y ajusta según tu entorno.

```dotenv
# 🔧 Entorno
debug=True
secret_key=pon_aqui_tu_clave
allowed_hosts=localhost,127.0.0.1

# 📊 Base de datos – solo si usarás PostgreSQL
ause_postgres=False
# USE_POSTGRES=True  # cámbialo a True en producción
# db_name=dymanic
# db_user=dymanic
# db_password=supersecret
# db_host=localhost
# db_port=5432
```

* `USE_POSTGRES=False` → **SQLite** (archivo `db.sqlite3` creado automáticamente).
* `USE_POSTGRES=True` + datos de conexión → **PostgreSQL**.

---

## 🛠️ Scripts y comandos útiles

| Acción                          | Comando                              |
| ------------------------------- | ------------------------------------ |
| Ejecutar tests (cuando existan) | `pytest`                             |
| Recolectar archivos estáticos   | `python manage.py collectstatic`     |
| Exportar backup (PostgreSQL)    | `pg_dump -Fc -f backup.dump dymanic` |

---

##  Despliegue en Render (ejemplo)

1. Crea un servicio «web service» de **Render → Django**.
2. Variables de entorno (panel » Environment): igual a tu `.env` de producción.
3. *Build command:*

   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```Windows PowerShell

1️⃣ Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass  2️⃣ ./venv/Scripts/Activate

4. *Start command:*

   ```bash
   gunicorn dymanic.wsgi:application --log-file -
   ```



---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.
