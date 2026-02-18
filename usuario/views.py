from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import auth, firestore
from proyecto_clase.firebase_config import initialize_firebase
from functools import wraps
import requests
import os

# Inicializar Firebase UNA SOLA VEZ
db = initialize_firebase()

# Inventario en memoria
inventario = []
contador_id = 1


# REGISTRO USUARIO FIREBASE
def registro_usuario(request):
    mensaje = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if db is None:
            return render(request, 'registros.html', {'mensaje': "❌ Error: No hay conexión con Firebase"})

        try:
            usuario = auth.create_user(email=email, password=password)

            db.collection('usuarios').document(usuario.uid).set({
                'email': email,
                'uid': usuario.uid,
                'rol': 'aprendiz',
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            mensaje = f"✅ Usuario registrado y guardado en DB: {usuario.uid}"

        except Exception as e:
            print(f"ERROR DETALLADO: {e}") 
            mensaje = f"❌ Error: {e}"

    return render(request, 'registros.html', {'mensaje': mensaje})

# DECORADOR LOGIN REQUIRED FIREBASE
def login_required_firebase(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if 'uid' not in request.session:
            messages.warning(request, "Debes iniciar sesión.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapped_view


# LOGIN 
def login_usuario(request):
    if 'uid' in request.session:
        return redirect('inicio')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        api_key = os.getenv('FIREBASE_WEB_API_KEY')

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if response.status_code == 200:
                request.session['uid'] = data['localId']
                request.session['email'] = data['email']
                request.session['id_token'] = data['idToken']

                messages.success(request, "Logeado exitosamente")
                return redirect('inicio')
            else:
                messages.error(request, "Credenciales inválidas")

        except Exception:
            messages.error(request, "Error de conexión")

    return render(request, 'login.html')


# LOGOUT
def cerrar_sesion(request):
    request.session.flush()
    messages.success(request, "Sesión cerrada")
    return redirect('login')


# INICIO 
@login_required_firebase
def inicio(request):
    return render(request, "inicio.html", {"inventario": inventario})


# PERFIL USUARIO FIRESTORE 
@login_required_firebase
def perfil(request):
    uid = request.session.get('uid')
    datos_usuario = {}

    try:
        doc = db.collection('usuarios').document(uid).get()

        if doc.exists:
            datos_usuario = doc.to_dict()
            datos_usuario['total_productos'] = len(inventario)
        else:
            datos_usuario = {
                'email': request.session.get('email'),
                'uid': uid,
                'rol': 'Operador',
                'total_productos': len(inventario)
            }

    except Exception as e:
        messages.error(request, f"Error BD: {e}")

    return render(request, 'perfil.html', {'datos_usuario': datos_usuario})


# REGISTRO PRODUCTO FIRESTORE
@login_required_firebase
def registro_producto(request):
    mensaje = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        usuario_uid = request.session.get('uid') # Obtenemos el ID del usuario actual

        try:
            # Se crea la colección 'productos' y se guarda el producto vinculado al usuario
            db.collection('productos').add({
                'nombre': nombre,
                'precio': float(precio),
                'stock': int(stock),
                'usuario_id': usuario_uid,
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            mensaje = "✅ Producto guardado en Firebase correctamente"

        except Exception as e:
            mensaje = f"❌ Error: {e}"

    return render(request, 'registro_productos.html', {'mensaje': mensaje})


# CRUD INVENTARIO MEMORIA
def inventario_lista(request):
    return render(request, "inventario/lista.html", {"inventario": inventario})


def inventario_crear(request):
    global contador_id

    if request.method == "POST":
        producto = {
            "id": contador_id,
            "nombre": request.POST["nombre"],
            "precio": request.POST["precio"],
            "cantidad": request.POST["cantidad"],
        }

        inventario.append(producto)
        contador_id += 1
        return redirect("inventario_lista")

    return render(request, "inventario/form.html")


def inventario_editar(request, id):
    producto = next((p for p in inventario if p["id"] == id), None)

    if not producto:
        messages.error(request, "Producto no encontrado")
        return redirect("inventario_lista")

    if request.method == "POST":
        producto["nombre"] = request.POST["nombre"]
        producto["precio"] = request.POST["precio"]
        producto["cantidad"] = request.POST["cantidad"]
        return redirect("inventario_lista")

    return render(request, "inventario/form.html", {"producto": producto})


def inventario_eliminar(request, id):
    global inventario
    inventario = [p for p in inventario if p["id"] != id]
    return redirect("inventario_lista")