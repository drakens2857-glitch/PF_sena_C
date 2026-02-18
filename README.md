
# 📦 PF_sena_C

**Sistema de Inventario de Mercancía con Django y Firebase**

## Descripción del proyecto

Nuestro proyecto consiste en un **sistema de inventario de mercancía** diseñado para cualquier tipo de persona o empresa, con el objetivo de **facilitar la gestión de productos y pedidos** de manera organizada, segura y eficiente.

El sistema permite:

* Registro de usuarios.
* Inicio y cierre de sesión.
* Gestión de inventario (crear, editar, listar y eliminar productos).
* Control de acceso mediante autenticación.

Como tecnologías principales utilizamos:

* **Django** como framework backend.
* **Firebase** como sistema de autenticación y base de datos.

---

## 🛠️ Entorno virtual

Para iniciar el proyecto, se creó un entorno virtual con el siguiente comando:

```bash
py -m venv venv
```

Esto permite aislar las dependencias del proyecto y evitar conflictos con otras instalaciones.

---

## 🔥 Firebase

Primero se creó una cuenta en Firebase y luego se configuró un proyecto con **Authentication y Firestore**.

Desde Firebase se obtuvo:

* El **SDK de administración**.
* Las **credenciales (keys y tokens)** necesarias para la conexión.

Posteriormente se instalaron las librerías necesarias:

* `firebase-admin`
* `requests`

Estas permiten la comunicación entre Django y Firebase.

---

## 🔐 Variables de entorno (.env)

Se configuraron las variables de entorno con las claves de Firebase, necesarias para el funcionamiento de la autenticación mediante API REST.

Estas claves permiten:

* Validar usuarios.
* Generar tokens.
* Mantener sesiones seguras.

---

## 💻 Codificación del sistema

Se implementaron las vistas principales del sistema, tales como:

* Registro de usuario.
* Inicio de sesión.
* Dashboard.
* CRUD del inventario.

Cada vista cumple una función específica dentro del flujo del sistema.

---

## 📥 Importaciones

Las importaciones permiten usar herramientas externas necesarias para el funcionamiento del proyecto:

```python
from django.shortcuts import render, redirect  
from django.contrib import messages  
from firebase_admin import auth, firestore  
from proyecto_clase.firebase_config import initialize_firebase  
from functools import wraps  
import requests  
import os  
```

Estas se encargan de:

* Renderizar vistas.
* Manejar mensajes al usuario.
* Conectarse con Firebase.
* Proteger rutas.
* Hacer peticiones HTTP.

---

## 👤 Registro de usuario

Esta función permite crear nuevos usuarios en el sistema.
Los datos se guardan tanto en **Firebase Authentication** como en **Firestore**.

```python
db.collection('perfiles').document(usuario.uid).set({
    'email': email,
    'uid': usuario.uid,
    'rol': 'aprendiz',
    'fecha_registro': firestore.SERVER_TIMESTAMP
})
```

Esto permite mantener un perfil completo de cada usuario.

---

## 🔒 Seguridad de login

Se implementó un decorador que valida si el usuario ha iniciado sesión antes de acceder a cualquier vista protegida.

```python
def login_required_firebase(view_func):
```

Si no existe sesión activa, el sistema redirige automáticamente al login.

---

## 🔑 Login de usuario

El usuario ingresa con su correo y contraseña.
El sistema valida los datos directamente con Firebase mediante su API REST.

```python
def login_usuario(request):
```

Si las credenciales son correctas, se guardan en la sesión:

* UID
* Email
* Token

---

## 🚪 Cerrar sesión

Permite cerrar la sesión actual eliminando todos los datos almacenados en la sesión.

```python
def cerrar_sesion(request):
```

Esto protege la información del usuario y evita accesos no autorizados.

---

## 🏠 Vista inicio

Esta vista solo es accesible si el usuario está autenticado.

```python
@login_required_firebase  
def inicio(request):
```

Muestra el inventario disponible.

---

## 📊 Dashboard

Muestra la información del usuario desde Firestore.

```python
db.collection('perfiles').document(uid).get()
```

Si no existe un perfil, se genera uno temporal para pruebas.

---

## 📦 Inventario en memoria

El inventario se maneja temporalmente en memoria:

```python
inventario = []  
contador_id = 1  
```

---

## 📋 Listar productos

Envía todos los productos del inventario al HTML.

```python
def inventario_lista(request):
```

---

## ➕ Crear producto

Permite agregar nuevos productos al inventario.

```python
def inventario_crear(request):
```

Cada producto se guarda con un ID único:

```python
producto = {
    "id": contador_id,
    "nombre": ...
}
```

---

## ✏️ Editar producto

Busca un producto por su ID y permite modificar sus datos.

```python
def inventario_editar(request, id):
```

Búsqueda del producto:

```python
next((p for p in inventario if p["id"] == id), None)
```

---

## 🗑️ Eliminar producto

Filtra la lista y elimina el producto seleccionado.

```python
def inventario_eliminar(request, id):
```

```python
inventario = [p for p in inventario if p["id"] != id]
```

---

# 🔁 Return

Utilizamos la instrucción return para indicarle al sistema qué debe devolver al usuario como respuesta.
Esta palabra clave se encuentra especificada en varias partes del proyecto, ya que es fundamental para que el sistema sepa a qué vista debe redireccionar o qué página debe mostrar en cada situación.

En Django, return cumple un papel esencial, ya que sin él no sería posible mostrar información en pantalla, ni realizar redirecciones entre vistas.

---

## 🧠 Conclusión

Este proyecto implementa un **sistema real de inventario**, aplicando conceptos profesionales como:

* Autenticación externa.
* Control de sesiones.
* CRUD completo.
* Separación de responsabilidades.
* Seguridad de rutas.
