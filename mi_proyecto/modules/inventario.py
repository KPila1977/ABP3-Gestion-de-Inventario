"""
Módulo de gestión de inventario y stock
Maneja control de stock, alertas y procesamiento de pedidos
"""

import json
import os
from datetime import datetime, timedelta
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import auditoria

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

def mostrar_inventario():
    """Muestra todo el inventario"""
    print("\n--- INVENTARIO COMPLETO ---")
    
    productos_list = cargar_productos()
    
    if not productos_list:
        print("No hay productos en inventario")
        return
    
    # Ordenar por ubicación
    productos_list.sort(key=lambda x: x.get("ubicacion", ""))
    
    print("\n" + "="*120)
    print(f"{'Código':10} {'Descripción':25} {'Cantidad':12} {'Ubicación':15} {'Lote':10} {'Vencimiento':12} {'Stock Min':10} {'Proveedor':20}")
    print("="*120)
    
    total_productos = 0
    total_valor = 0
    
    for prod in productos_list:
        cantidad = prod.get("cantidad", 0)
        unidad = prod.get("unidad", "unidad")
        
        # Calcular si está bajo stock mínimo
        stock_min = prod.get("stock_minimo", 0)
        estado_stock = ""
        if cantidad <= stock_min:
            estado_stock = "⚠ BAJO"
        elif cantidad <= stock_min * 1.5:
            estado_stock = "⚠ ATENCIÓN"
        
        cantidad_str = f"{cantidad} {unidad}"
        
        print(f"{prod.get('codigo', ''):10} {prod.get('descripcion', '')[:25]:25} {cantidad_str:12} "
              f"{prod.get('ubicacion', ''):15} {prod.get('lote', '')[:10]:10} "
              f"{prod.get('fecha_vencimiento', '')[:12]:12} {stock_min:10} "
              f"{prod.get('proveedor', '')[:20]:20} {estado_stock}")
        
        total_productos += 1
        total_valor += cantidad
    
    print("="*120)
    print(f"Total productos: {total_productos}")
    print(f"Total ítems en stock: {total_valor}")

def mostrar_stock_critico():
    """Muestra productos con stock crítico (para supervisor)"""
    print("\n--- STOCK CRÍTICO ---")
    
    productos_list = cargar_productos()
    criticos = []
    
    for prod in productos_list:
        cantidad = prod.get("cantidad", 0)
        stock_min = prod.get("stock_minimo", 0)
        
        if cantidad <= stock_min:
            criticos.append(prod)
    
    if not criticos:
        print("No hay productos con stock crítico")
        return
    
    print(f"\nSe encontraron {len(criticos)} producto(s) con stock crítico:")
    print("-" * 90)
    print(f"{'Descripción':30} {'Stock Actual':15} {'Stock Mínimo':15} {'Diferencia':15} {'Ubicación':15}")
    print("-" * 90)
    
    for prod in criticos:
        cantidad = prod.get("cantidad", 0)
        stock_min = prod.get("stock_minimo", 0)
        diferencia = cantidad - stock_min
        
        print(f"{prod.get('descripcion', '')[:30]:30} {cantidad:15} {stock_min:15} {diferencia:15} {prod.get('ubicacion', '')[:15]:15}")

def mostrar_productos_por_vencer():
    """Muestra productos próximos a vencer (para supervisor)"""
    print("\n--- PRODUCTOS POR VENCER ---")
    
    dias_alerta = 30  # Alertar 30 días antes
    fecha_hoy = datetime.now()
    fecha_limite = fecha_hoy + timedelta(days=dias_alerta)
    
    productos_list = cargar_productos()
    por_vencer = []
    
    for prod in productos_list:
        fecha_vencimiento_str = prod.get("fecha_vencimiento", "")
        if fecha_vencimiento_str:
            try:
                fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d")
                if fecha_vencimiento <= fecha_limite:
                    dias_restantes = (fecha_vencimiento - fecha_hoy).days
                    prod["dias_restantes"] = dias_restantes
                    por_vencer.append(prod)
            except ValueError:
                continue
    
    if not por_vencer:
        print(f"No hay productos por vencer en los próximos {dias_alerta} días")
        return
    
    # Ordenar por fecha de vencimiento
    por_vencer.sort(key=lambda x: x.get("dias_restantes", 999))
    
    print(f"\nSe encontraron {len(por_vencer)} producto(s) por vencer:")
    print("-" * 100)
    print(f"{'Descripción':30} {'Lote':15} {'Vencimiento':15} {'Días Restantes':15} {'Cantidad':15} {'Ubicación':15}")
    print("-" * 100)
    
    for prod in por_vencer:
        dias = prod.get("dias_restantes", 0)
        estado = "⚠ VENCIDO" if dias < 0 else f"⚠ {dias} días"
        
        print(f"{prod.get('descripcion', '')[:30]:30} {prod.get('lote', '')[:15]:15} "
              f"{prod.get('fecha_vencimiento', '')[:15]:15} {estado:15} "
              f"{prod.get('cantidad', 0):15} {prod.get('ubicacion', '')[:15]:15}")

def procesar_pedido(usuario):
    """Procesa salida de pedidos"""
    print("\n--- PROCESAMIENTO DE PEDIDO ---")
    
    productos_list = cargar_productos()
    
    if not productos_list:
        print("No hay productos en inventario")
        return
    
    # Crear nuevo pedido
    pedido = {
        "numero": f"PED-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": usuario,
        "items": [],
        "estado": "En proceso"
    }
    
    continuar = True
    
    while continuar:
        print("\n--- AGREGAR PRODUCTO AL PEDIDO ---")
        
        # Buscar producto
        busqueda = input("Buscar producto (código o descripción): ").strip().lower()
        resultados = []
        
        for prod in productos_list:
            if busqueda in prod.get("codigo", "").lower() or \
               busqueda in prod.get("descripcion", "").lower():
                resultados.append(prod)
        
        if not resultados:
            print("No se encontraron productos")
            continuar = input("\n¿Buscar otro producto? (S/N): ").strip().upper() == "S"
            continue
        
        # Mostrar resultados
        print(f"\nSe encontraron {len(resultados)} producto(s):")
        for i, prod in enumerate(resultados):
            print(f"{i+1}. {prod['descripcion']} - Stock: {prod['cantidad']} {prod['unidad']} - Ubicación: {prod['ubicacion']}")
        
        try:
            seleccion = int(input("\nSeleccione producto (número): ")) - 1
            if 0 <= seleccion < len(resultados):
                producto = resultados[seleccion]
                
                print(f"\nProducto seleccionado: {producto['descripcion']}")
                print(f"Stock disponible: {producto['cantidad']} {producto['unidad']}")
                
                cantidad_pedido = float(input(f"Cantidad requerida ({producto['unidad']}): "))
                
                if cantidad_pedido <= producto['cantidad']:
                    # Agregar al pedido
                    item = {
                        "codigo": producto["codigo"],
                        "descripcion": producto["descripcion"],
                        "cantidad": cantidad_pedido,
                        "unidad": producto["unidad"],
                        "lote": producto["lote"],
                        "ubicacion": producto["ubicacion"]
                    }
                    
                    pedido["items"].append(item)
                    
                    print(f"Producto agregado al pedido. Total items: {len(pedido['items'])}")
                else:
                    print(f"Stock insuficiente. Solo hay {producto['cantidad']} {producto['unidad']} disponibles")
            
            else:
                print("Selección inválida")
        
        except ValueError:
            print("Entrada inválida")
        
        continuar = input("\n¿Agregar otro producto al pedido? (S/N): ").strip().upper() == "S"
    
    if pedido["items"]:
        print("\n--- RESUMEN DEL PEDIDO ---")
        print(f"Número de pedido: {pedido['numero']}")
        print(f"Fecha: {pedido['fecha']}")
        print(f"Total items: {len(pedido['items'])}")
        
        print("\nDetalle del pedido:")
        print("-" * 80)
        for i, item in enumerate(pedido["items"], 1):
            print(f"{i}. {item['descripcion']} - {item['cantidad']} {item['unidad']} - Lote: {item['lote']}")
        
        confirmar = input("\n¿Confirmar y procesar pedido? (S/N): ").strip().upper()
        
        if confirmar == "S":
            # Actualizar inventario
            for item in pedido["items"]:
                for prod in productos_list:
                    if prod["codigo"] == item["codigo"] and prod["lote"] == item["lote"]:
                        prod["cantidad"] -= item["cantidad"]
                        
                        # Registrar movimiento
                        if "movimientos" not in prod:
                            prod["movimientos"] = []
                        
                        movimiento = {
                            "tipo": "Salida pedido",
                            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cantidad": item["cantidad"],
                            "usuario": usuario,
                            "pedido": pedido["numero"]
                        }
                        
                        prod["movimientos"].append(movimiento)
                        break
            
            # Guardar cambios
            guardar_productos(productos_list)
            
            # Generar impresión (simulada)
            print("\n" + "="*50)
            print("COMPROBANTE DE SALIDA")
            print("="*50)
            print(f"Pedido: {pedido['numero']}")
            print(f"Fecha: {pedido['fecha']}")
            print(f"Usuario: {usuario}")
            print("="*50)
            for item in pedido["items"]:
                print(f"{item['descripcion'][:30]:30} {item['cantidad']:8} {item['unidad']:10} {item['lote']:10}")
            print("="*50)
            
            pedido["estado"] = "Completado"
            print(f"\n¡Pedido {pedido['numero']} procesado exitosamente!")
            
            # Registrar en auditoría
            auditoria.registrar_log(usuario, "PROCESAR_PEDIDO", f"Pedido {pedido['numero']} procesado")
        else:
            print("Pedido cancelado")
    else:
        print("Pedido vacío. No se procesó nada.")

def ordenar_mercancia():
    """Función para ordenar mercancía (bodeguero)"""
    print("\n--- ORDENAR MERCANCÍA ---")
    
    productos_list = cargar_productos()
    
    if not productos_list:
        print("No hay productos para ordenar")
        return
    
    # Mostrar productos desordenados (simulado)
    print("\nProductos que requieren reordenamiento:")
    for i, prod in enumerate(productos_list[:5]):  # Mostrar primeros 5
        print(f"{i+1}. {prod['descripcion']} en {prod['ubicacion']}")
    
    print("\nFuncionalidad de reordenamiento en desarrollo...")
    print("Por ahora, se recomienda:")
    print("1. Verificar etiquetas")
    print("2. Revisar fechas de vencimiento")
    print("3. Agrupar por tipo de producto")
    print("4. Actualizar ubicaciones en el sistema")

def revisar_stock():
    """Función para revisar stock (bodeguero)"""
    print("\n--- REVISIÓN DE STOCK ---")
    
    productos_list = cargar_productos()
    
    if not productos_list:
        print("No hay productos en inventario")
        return
    
    ubicacion = input("Ubicación a revisar (dejar vacío para todas): ").strip()
    
    productos_filtrados = []
    for prod in productos_list:
        if not ubicacion or ubicacion.lower() in prod.get("ubicacion", "").lower():
            productos_filtrados.append(prod)
    
    print(f"\nSe encontraron {len(productos_filtrados)} producto(s) en la ubicación:")
    
    for prod in productos_filtrados:
        print(f"- {prod['descripcion']}: {prod['cantidad']} {prod['unidad']} "
              f"(Mínimo: {prod.get('stock_minimo', 0)})")

def mostrar_reportes():
    """Muestra reportes consolidados del inventario"""
    print("\n--- REPORTES Y ESTADÍSTICAS ---")
    
    productos_list = cargar_productos()
    
    if not productos_list:
        print("No hay datos para generar reportes")
        return

    # Cálculos generales
    total_skus = len(productos_list)
    total_unidades = sum(prod.get("cantidad", 0) for prod in productos_list)
    
    # Stock crítico
    criticos = [p for p in productos_list if p.get("cantidad", 0) <= p.get("stock_minimo", 0)]
    
    # Por vencer (30 días)
    fecha_hoy = datetime.now()
    fecha_limite = fecha_hoy + timedelta(days=30)
    por_vencer = []
    
    def parse_date(date_str):
        for fmt in ("%Y-%m-%d", "%d-%m-%y", "%d/%m/%y", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                pass
        return None

    for prod in productos_list:
        if prod.get("fecha_vencimiento"):
            fv = parse_date(prod["fecha_vencimiento"])
            if fv and fv <= fecha_limite:
                por_vencer.append(prod)

    # Valorización (Simulada ya que no hay precio, usamos conteo por unidad)
    unidades_dist = {}
    for prod in productos_list:
        u = prod.get("unidad", "unidad")
        unidades_dist[u] = unidades_dist.get(u, 0) + prod.get("cantidad", 0)

    print(f"\nRESUMEN GENERAL")
    print("-" * 40)
    print(f"Total Productos (SKUs): {total_skus}")
    print(f"Total Ítems (Suma):     {total_unidades:g}")
    print(f"Productos Críticos:     {len(criticos)}")
    print(f"Productos por Vencer:   {len(por_vencer)}")
    
    print(f"\nDISTRIBUCIÓN POR UNIDAD")
    print("-" * 40)
    for u, cant in unidades_dist.items():
        print(f"- {u}: {cant:g}")
    
    print(f"\nALERTAS")
    print("-" * 40)
    if criticos:
        print(f"⚠ {len(criticos)} productos con stock bajo o nulo")
    if por_vencer:
        print(f"⚠ {len(por_vencer)} productos vencidos o próximos a vencer")
        
    if not criticos and not por_vencer:
        print("✓ Inventario saludable")

if __name__ == "__main__":
    # Test execution
    mostrar_reportes()