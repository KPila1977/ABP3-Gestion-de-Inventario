"""
Módulo de gestión de usuarios
Maneja registro, validación, login y recuperación de usuarios
"""

import json
import re
import os
from datetime import datetime

ARCHIVO_USUARIOS = "data/usuarios.json"

def validar_run(run):
    """Valida el RUN chileno con algoritmo de dígito verificador"""
    run = run.replace(".", "").replace("-", "").upper()
    
    if not re.match(r'^\d{7,8}[0-9K]$', run):
        return False
    
    cuerpo = run[:-1]
    dv = run[-1]
    
    # Algoritmo de dígito verificador
    suma = 0
    multiplo = 2
    
    for i in range(len(cuerpo)-1, -1, -1):
        suma += int(cuerpo[i]) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2
    
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    
    return dv == dv_calculado

def validar_email(email):
    """Valida formato de email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_telefono(telefono):
    """Valida formato de teléfono con código de país"""
    patron = r'^\+?[1-9]\d{1,14}$'
    return re.match(patron, telefono) is not None

def capitalizar_nombre(nombre):
    """Convierte a mayúsculas según requerimiento"""
    return nombre.upper()

def cargar_usuarios():
    """Carga usuarios desde archivo JSON"""
    if not os.path.exists(ARCHIVO_USUARIOS):
        return {}
    
    try:
        with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def guardar_usuarios(usuarios_dict):
    """Guarda usuarios en archivo JSON"""
    os.makedirs(os.path.dirname(ARCHIVO_USUARIOS), exist_ok=True)
    with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios_dict, f, indent=2, ensure_ascii=False)

def registrar_usuario():
    """Registra un nuevo usuario con validaciones"""
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    
    # Validación de datos
    nombre = input("Nombre: ").strip()
    while not nombre:
        print("El nombre es obligatorio")
        nombre = input("Nombre: ").strip()
    nombre = capitalizar_nombre(nombre)
    
    apellido_paterno = input("Apellido paterno: ").strip()
    while not apellido_paterno:
        print("El apellido paterno es obligatorio")
        apellido_paterno = input("Apellido paterno: ").strip()
    apellido_paterno = capitalizar_nombre(apellido_paterno)
    
    apellido_materno = input("Apellido materno: ").strip()
    apellido_materno = capitalizar_nombre(apellido_materno)
    
    run = input("RUN (sin dígito verificador): ").strip()
    while not validar_run(run + "0"):  # Validar con dígito temporal
        print("RUN inválido")
        run = input("RUN (sin dígito verificador): ").strip()
    
    email = input("Email: ").strip()
    while not validar_email(email):
        print("Email inválido")
        email = input("Email: ").strip()
    
    telefono = input("Teléfono (con código de país): ").strip()
    while not validar_telefono(telefono):
        print("Teléfono inválido")
        telefono = input("Teléfono (con código de país): ").strip()
    
    # Roles disponibles
    print("\nRoles disponibles:")
    roles = ["Administrador", "Supervisor", "Digitador", "Bodeguero", "Usuario"]
    for i, rol in enumerate(roles, 1):
        print(f"{i}. {rol}")
    
    rol_idx = int(input("Seleccione rol (1-5): ")) - 1
    rol = roles[rol_idx] if 0 <= rol_idx < len(roles) else "Usuario"
    
    # Contraseña por defecto
    contrasena_default = "Password123"
    
    # Crear usuario
    usuarios_dict = cargar_usuarios()
    usuario_id = f"user_{len(usuarios_dict) + 1:03d}"
    
    usuarios_dict[usuario_id] = {
        "id": usuario_id,
        "nombre": nombre,
        "apellido_paterno": apellido_paterno,
        "apellido_materno": apellido_materno,
        "run": run,
        "email": email,
        "telefono": telefono,
        "rol": rol,
        "contrasena": contrasena_default,  # En producción, usar hash
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "activo": True
    }
    
    guardar_usuarios(usuarios_dict)
    print(f"\nUsuario registrado exitosamente!")
    print(f"ID de usuario: {usuario_id}")
    print(f"Contraseña temporal: {contrasena_default}")
    print("Debe cambiar la contraseña en el primer inicio de sesión")
    
    # Enviar correo de verificación (simulado)
    print(f"[SIMULACIÓN] Correo de verificación enviado a {email}")
    print(f"[SIMULACIÓN] SMS con código enviado a {telefono}")

def iniciar_sesion():
    """Inicia sesión de usuario"""
    print("\n--- INICIO DE SESIÓN ---")
    
    usuarios_dict = cargar_usuarios()
    
    intentos = 0
    max_intentos = 3
    
    while intentos < max_intentos:
        usuario_id = input("ID de usuario: ").strip()
        contrasena = input("Contraseña: ").strip()
        
        # Buscar usuario
        for user_id, user_data in usuarios_dict.items():
            if (user_id == usuario_id or user_data.get("email") == usuario_id) and \
               user_data["contrasena"] == contrasena and \
               user_data.get("activo", True):
                
                print(f"\n¡Bienvenido(a) {user_data['nombre']} {user_data['apellido_paterno']}!")
                print(f"Rol: {user_data['rol']}")
                
                # Cambiar contraseña si es la primera vez
                if contrasena == "Password123":
                    cambiar_contrasena(usuario_id)
                
                return usuario_id, user_data["rol"]
        
        intentos += 1
        print(f"Credenciales incorrectas. Intentos restantes: {max_intentos - intentos}")
    
    print("Demasiados intentos fallidos. Contacte al administrador.")
    return None, None

def cambiar_contrasena(usuario_id):
    """Permite al usuario cambiar su contraseña"""
    print("\n--- CAMBIO DE CONTRASEÑA OBLIGATORIO ---")
    print("Debe cambiar su contraseña por defecto")
    
    usuarios_dict = cargar_usuarios()
    
    if usuario_id not in usuarios_dict:
        return
    
    nueva_contrasena = input("Nueva contraseña: ").strip()
    confirmar = input("Confirmar contraseña: ").strip()
    
    if nueva_contrasena == confirmar and len(nueva_contrasena) >= 6:
        usuarios_dict[usuario_id]["contrasena"] = nueva_contrasena
        guardar_usuarios(usuarios_dict)
        print("Contraseña cambiada exitosamente")
    else:
        print("Las contraseñas no coinciden o son demasiado cortas")

def gestionar_usuarios():
    """Gestión de usuarios (solo administrador)"""
    print("\n--- GESTIÓN DE USUARIOS ---")
    usuarios_dict = cargar_usuarios()
    
    print(f"\nTotal de usuarios: {len(usuarios_dict)}")
    print("\nLista de usuarios:")
    print("-" * 80)
    print(f"{'ID':10} {'Nombre':20} {'Email':25} {'Rol':15} {'Activo':6}")
    print("-" * 80)
    
    for user_id, user_data in usuarios_dict.items():
        nombre_completo = f"{user_data['nombre']} {user_data['apellido_paterno'][0]}."
        print(f"{user_id:10} {nombre_completo:20} {user_data['email'][:25]:25} {user_data['rol']:15} {'Sí' if user_data.get('activo', True) else 'No':6}")
    
    print("\nOpciones:")
    print("1. Activar/Desactivar usuario")
    print("2. Cambiar rol")
    print("3. Volver")
    
    opcion = input("\nSeleccione opción: ").strip()
    
    if opcion == "1":
        user_id = input("ID del usuario: ").strip()
        if user_id in usuarios_dict:
            usuarios_dict[user_id]["activo"] = not usuarios_dict[user_id].get("activo", True)
            guardar_usuarios(usuarios_dict)
            estado = "activado" if usuarios_dict[user_id]["activo"] else "desactivado"
            print(f"Usuario {user_id} {estado}")
    
    elif opcion == "2":
        user_id = input("ID del usuario: ").strip()
        if user_id in usuarios_dict:
            print("Roles disponibles: Administrador, Supervisor, Digitador, Bodeguero, Usuario")
            nuevo_rol = input("Nuevo rol: ").strip()
            if nuevo_rol in ["Administrador", "Supervisor", "Digitador", "Bodeguero", "Usuario"]:
                usuarios_dict[user_id]["rol"] = nuevo_rol
                guardar_usuarios(usuarios_dict)
                print(f"Rol cambiado a {nuevo_rol}")
            else:
                print("Rol no válido")

def crear_usuarios_prueba():
    """Crea usuarios de prueba para validación del sistema"""
    usuarios_dict = cargar_usuarios()
    
    # Solo crear si no existen
    if usuarios_dict:
        return
    
    usuarios_prueba = {
        "admin001": {
            "id": "admin001",
            "nombre": "ADMIN",
            "apellido_paterno": "SISTEMA",
            "apellido_materno": "",
            "run": "12345678",
            "email": "admin@empresa.cl",
            "telefono": "+56912345678",
            "rol": "Administrador",
            "contrasena": "Admin123",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activo": True
        },
        "super001": {
            "id": "super001",
            "nombre": "SUPERVISOR",
            "apellido_paterno": "PRUEBA",
            "apellido_materno": "",
            "run": "87654321",
            "email": "supervisor@empresa.cl",
            "telefono": "+56987654321",
            "rol": "Supervisor",
            "contrasena": "Super123",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activo": True
        },
        "digit001": {
            "id": "digit001",
            "nombre": "DIGITADOR",
            "apellido_paterno": "PRUEBA",
            "apellido_materno": "",
            "run": "11222333",
            "email": "digitador@empresa.cl",
            "telefono": "+56911222333",
            "rol": "Digitador",
            "contrasena": "Digit123",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activo": True
        },
        "bode001": {
            "id": "bode001",
            "nombre": "BODEGUERO",
            "apellido_paterno": "PRUEBA",
            "apellido_materno": "",
            "run": "44555666",
            "email": "bodeguero@empresa.cl",
            "telefono": "+56944555666",
            "rol": "Bodeguero",
            "contrasena": "Bode123",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activo": True
        },
        "user001": {
            "id": "user001",
            "nombre": "USUARIO",
            "apellido_paterno": "PRUEBA",
            "apellido_materno": "",
            "run": "77888999",
            "email": "usuario@empresa.cl",
            "telefono": "+56977888999",
            "rol": "Usuario",
            "contrasena": "User123",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "activo": True
        }
    }
    
    guardar_usuarios(usuarios_prueba)
    print("Usuarios de prueba creados exitosamente")