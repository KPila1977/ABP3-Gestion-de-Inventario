"""
Módulo de gestión de productos y mercancías
Maneja ingreso, salida y consulta de productos
"""

import json
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import re

ARCHIVO_PRODUCTOS = "data/productos.json"

def cargar_productos():
    """Carga productos desde archivo JSON"""
    if not os.path.exists(ARCHIVO_PRODUCTOS):
        return []
    
    try:
        with open(ARCHIVO_PRODUCTOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def guardar_productos(productos_list):
    """Guarda productos en archivo JSON"""
    os.makedirs(os.path.dirname(ARCHIVO_PRODUCTOS), exist_ok=True)
    with open(ARCHIVO_PRODUCTOS, 'w', encoding='utf-8') as f:
        json.dump(productos_list, f, indent=2, ensure_ascii=False)

def solicitar_fecha(mensaje):
    """Solicita una fecha y valida su formato"""
    while True:
        fecha_str = input(f"{mensaje} (YYYY-MM-DD): ").strip()
        for fmt in ("%Y-%m-%d", "%d-%m-%y", "%d/%m/%y", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                dt = datetime.strptime(fecha_str, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass
        print("Formato de fecha inválido. Intente nuevamente.")

def solicitar_float(mensaje):
    """Solicita un número decimal validado"""
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
            print("Valor inválido. Debe ser un número.")

def solicitar_int(mensaje):
    """Solicita un número entero validado"""
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Valor inválido. Debe ser un número entero.")

def ingresar_mercancia(usuario):
    """Proceso de ingreso de mercancías"""
    print("\n--- INGRESO DE MERCANCÍA ---")
    
    # Checklist de recepción (Simplificado)
    checklist = {}
    print("\nCHECKLIST DE RECEPCIÓN:")
    for item in ["Documento de entrega", "Documento de transporte", "Inspección visual"]:
        checklist[item] = input(f"{item} (S/N): ").strip().upper() == "S"
    
    observaciones = input("Observaciones: ").strip()
    
    # Estado de recepción
    print("\nESTADO DE RECEPCIÓN: 1. Conforme, 2. Conforme c/Obs, 3. Rechazo")
    opcion = input("Seleccione (1-3): ").strip()
    estado = {"1": "Conforme", "2": "Conforme c/Obs", "3": "Rechazo"}.get(opcion, "Conforme")
    
    # Datos generales
    print("\n--- DATOS DE DOCUMENTO ---")
    num_documento = input("N° documento: ").strip()
    fecha_documento = solicitar_fecha("Fecha documento")
    proveedor = input("Proveedor: ").strip()
    
    productos = []
    continuar = True
    
    while continuar:
        print(f"\n--- PRODUCTO {len(productos) + 1} ---")
        
        producto = {
            "codigo": input("Código interno: ").strip(),
            "descripcion": input("Descripción: ").strip(),
            "unidad": input("Unidad (unidad/ml/gr): ").strip() or "unidad",
            "cantidad": solicitar_float("Cantidad: "),
            "marca": input("Marca: ").strip(),
            "fecha_elaboracion": solicitar_fecha("Fecha elaboración"),
            "fecha_vencimiento": solicitar_fecha("Fecha vencimiento"),
            "ubicacion": input("Ubicación en bodega: ").strip(),
            "lote": input("Número de lote: ").strip(),
            "stock_minimo": solicitar_int("Stock mínimo: "),
            "proveedor": proveedor,
            "guia_despacho": num_documento,
            "fecha_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "usuario_ingreso": usuario,
            "estado": estado,
            "observaciones": observaciones
        }
        
        # Campos opcionales
        producto["peligrosidad"] = input("Peligrosidad (opcional): ").strip()
        producto["temperatura"] = input("Temperatura (opcional): ").strip()
        
        productos.append(producto)
        continuar = input("\n¿Agregar otro producto? (S/N): ").strip().upper() == "S"
    
    # Guardar productos
    productos_existentes = cargar_productos()
    productos_existentes.extend(productos)
    guardar_productos(productos_existentes)
    
    print(f"\n¡{len(productos)} producto(s) ingresado(s) exitosamente!")
    print(f"Estado: {estado}")
    print(f"Guía de despacho: {num_documento}")

def recibir_mercancia(usuario):
    """Proceso de recepción de mercancía para bodeguero"""
    print("\n--- RECEPCIÓN DE MERCANCÍA ---")
    
    productos_list = cargar_productos()
    
    if not productos_list:
        print("No hay productos pendientes de recepción")
        return
    
    # Mostrar productos pendientes
    print("\nProductos pendientes de recepción:")
    for i, prod in enumerate(productos_list):
        if prod.get("estado_recepcion") != "Recibido":
            print(f"{i+1}. {prod['descripcion']} - Lote: {prod['lote']} - Estado: {prod.get('estado', 'Pendiente')}")
    
    try:
        seleccion = int(input("\nSeleccione producto a recibir (número): ")) - 1
        if 0 <= seleccion < len(productos_list):
            producto = productos_list[seleccion]
            
            print(f"\nRecibiendo: {producto['descripcion']}")
            print(f"Lote: {producto['lote']}")
            print(f"Proveedor: {producto['proveedor']}")
            
            # Confirmar recepción
            conforme = input("\n¿Recepción conforme? (S/N): ").strip().upper()
            observaciones = input("Observaciones: ").strip()
            
            productos_list[seleccion]["estado_recepcion"] = "Recibido" if conforme == "S" else "No conforme"
            productos_list[seleccion]["observaciones_recepcion"] = observaciones
            productos_list[seleccion]["fecha_recepcion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            productos_list[seleccion]["usuario_recepcion"] = usuario
            
            guardar_productos(productos_list)
            
            estado = "CONFORME" if conforme == "S" else "NO CONFORME"
            print(f"\nProducto marcado como {estado}")
        else:
            print("Selección inválida")
    except ValueError:
        print("Entrada inválida")

def consultar_producto():
    """Consulta si un producto está en bodega"""
    print("\n--- CONSULTA DE PRODUCTO ---")
    
    criterio = input("Buscar por (1. código, 2. descripción, 3. lote): ").strip()
    busqueda = input("Texto a buscar: ").strip().lower()
    
    productos_list = cargar_productos()
    resultados = []
    
    for prod in productos_list:
        if (criterio == "1" and busqueda in prod.get("codigo", "").lower()) or \
           (criterio == "2" and busqueda in prod.get("descripcion", "").lower()) or \
           (criterio == "3" and busqueda in prod.get("lote", "").lower()):
            resultados.append(prod)
    
    if resultados:
        print(f"\nSe encontraron {len(resultados)} resultado(s):")
        print("-" * 100)
        print(f"{'Código':10} {'Descripción':30} {'Cantidad':10} {'Ubicación':15} {'Lote':10} {'Vencimiento':12}")
        print("-" * 100)
        
        for prod in resultados:
            cantidad_str = f"{prod['cantidad']} {prod['unidad']}"
            print(f"{prod['codigo']:10} {prod['descripcion'][:30]:30} {cantidad_str:10} {prod['ubicacion']:15} {prod['lote']:10} {prod['fecha_vencimiento']:12}")
    else:
        print("No se encontraron productos con ese criterio")

def marcar_egreso(usuario):
    """Marca egresos de mercancías (para digitador)"""
    print("\n--- MARCADO DE EGRESOS ---")
    
    productos_list = cargar_productos()
    
    if not productos_list:
        print("No hay productos en inventario")
        return
    
    print("Seleccione producto para marcar egreso:")
    for i, prod in enumerate(productos_list):
        print(f"{i+1}. {prod['descripcion']} - Stock: {prod['cantidad']} {prod['unidad']}")
    
    try:
        seleccion = int(input("\nSelección: ")) - 1
        if 0 <= seleccion < len(productos_list):
            producto = productos_list[seleccion]
            
            print(f"\nProducto: {producto['descripcion']}")
            print(f"Stock actual: {producto['cantidad']} {producto['unidad']}")
            
            cantidad_egreso = float(input(f"Cantidad a egresar ({producto['unidad']}): "))
            
            if cantidad_egreso <= producto['cantidad']:
                # Registrar movimiento
                if "movimientos" not in producto:
                    producto["movimientos"] = []
                
                movimiento = {
                    "tipo": "Egreso",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "cantidad": cantidad_egreso,
                    "usuario": usuario,
                    "motivo": input("Motivo del egreso: ").strip()
                }
                
                producto["movimientos"].append(movimiento)
                producto["cantidad"] -= cantidad_egreso
                
                productos_list[seleccion] = producto
                guardar_productos(productos_list)
                
                print(f"\nEgreso registrado. Nuevo stock: {producto['cantidad']} {producto['unidad']}")
            else:
                print("Cantidad insuficiente en inventario")
        else:
            print("Selección inválida")
    except ValueError:
        print("Entrada inválida")