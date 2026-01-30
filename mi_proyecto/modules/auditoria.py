"""
Módulo de auditoría y logs
Registra todas las actividades del sistema
"""

import os
import json
from datetime import datetime

DIR_LOGS = "logs/"

def crear_directorio_logs():
    """Crea el directorio de logs si no existe"""
    os.makedirs(DIR_LOGS, exist_ok=True)

def obtener_archivo_log():
    """Obtiene el nombre del archivo log del día actual"""
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DIR_LOGS, f"auditoria_{fecha_actual}.log")

def registrar_log(usuario, accion, descripcion):
    """Registra una entrada en el log de auditoría"""
    crear_directorio_logs()
    
    entrada = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": usuario,
        "accion": accion,
        "descripcion": descripcion
    }
    
    archivo_log = obtener_archivo_log()
    
    # Cargar logs existentes o crear nuevo
    logs = []
    if os.path.exists(archivo_log):
        try:
            with open(archivo_log, 'r', encoding='utf-8') as f:
                # Leer todas las líneas como JSON
                for linea in f:
                    linea = linea.strip()
                    if linea:
                        logs.append(json.loads(linea))
        except:
            logs = []
    
    # Agregar nueva entrada
    logs.append(entrada)
    
    # Guardar en formato JSON línea por línea
    with open(archivo_log, 'w', encoding='utf-8') as f:
        for log in logs:
            f.write(json.dumps(log, ensure_ascii=False) + '\n')

def mostrar_logs():
    """Muestra los logs de auditoría (solo administrador)"""
    print("\n--- LOGS DE AUDITORÍA ---")
    
    crear_directorio_logs()
    
    # Listar archivos de log disponibles
    archivos_log = sorted([f for f in os.listdir(DIR_LOGS) if f.endswith('.log')])
    
    if not archivos_log:
        print("No hay archivos de log disponibles")
        return
    
    print("\nArchivos de log disponibles:")
    for i, archivo in enumerate(archivos_log[-5:], 1):  # Mostrar últimos 5
        print(f"{i}. {archivo}")
    
    try:
        seleccion = int(input("\nSeleccione archivo (número) o 0 para hoy: ").strip())
        
        if seleccion == 0:
            archivo_log = obtener_archivo_log()
        else:
            if 1 <= seleccion <= len(archivos_log):
                archivo_log = os.path.join(DIR_LOGS, archivos_log[-seleccion])
            else:
                print("Selección inválida")
                return
    except ValueError:
        archivo_log = obtener_archivo_log()
    
    # Mostrar contenido del log
    if os.path.exists(archivo_log):
        print(f"\nContenido de {os.path.basename(archivo_log)}:")
        print("-" * 100)
        print(f"{'Fecha/Hora':20} {'Usuario':15} {'Acción':20} {'Descripción':40}")
        print("-" * 100)
        
        try:
            with open(archivo_log, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    if linea:
                        log = json.loads(linea)
                        print(f"{log.get('timestamp', '')[:20]:20} {log.get('usuario', '')[:15]:15} "
                              f"{log.get('accion', '')[:20]:20} {log.get('descripcion', '')[:40]:40}")
        except:
            print("Error al leer el archivo de log")
    else:
        print(f"El archivo {archivo_log} no existe")