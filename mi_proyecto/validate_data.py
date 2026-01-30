
import json
import os
import sys
from datetime import datetime

DATA_DIR = "data"
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")
PRODUCTOS_FILE = os.path.join(DATA_DIR, "productos.json")

def validate_usuarios():
    print(f"Validating {USUARIOS_FILE}...")
    if not os.path.exists(USUARIOS_FILE):
        print("  File not found (OK - will be created).")
        return []

    try:
        with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("  [ERROR] Invalid JSON format.")
        return ["Invalid JSON in usuarios.json"]

    errors = []
    if not isinstance(data, dict):
         errors.append("Root must be a dictionary")
         return errors

    for user_id, user in data.items():
        if not isinstance(user, dict):
            errors.append(f"User {user_id} is not a dict")
            continue
        
        required_fields = ["id", "nombre", "rol", "contrasena"] 
        for field in required_fields:
            if field not in user:
                errors.append(f"User {user_id} missing field {field}")
        
        # Validate types
        if not isinstance(user.get("nombre"), str): errors.append(f"User {user_id} nombre not string")
    
    if not errors:
        print("  Usuarios valid.")
    return errors

def validate_productos():
    print(f"Validating {PRODUCTOS_FILE}...")
    if not os.path.exists(PRODUCTOS_FILE):
        print("  File not found (OK - will be created).")
        return []

    try:
        with open(PRODUCTOS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("  [ERROR] Invalid JSON format.")
        return ["Invalid JSON in productos.json"]

    errors = []
    if not isinstance(data, list):
         errors.append("Root must be a list")
         return errors

    for i, prod in enumerate(data):
        if not isinstance(prod, dict):
            errors.append(f"Item {i} is not a dict")
            continue
            
        required_fields = ["codigo", "descripcion", "cantidad", "unidad"]
        for field in required_fields:
            if field not in prod:
                errors.append(f"Product {i} missing field {field}")
        
        # Validate quantity is number
        qty = prod.get("cantidad")
        if not isinstance(qty, (int, float)):
            errors.append(f"Product {i} ({prod.get('descripcion')}) quantity is not number: {type(qty)}")

    if not errors:
        print("  Productos valid.")
    else:
        for e in errors:
            print(f"  [ERROR] {e}")

    return errors

def main():
    all_errors = []
    all_errors.extend(validate_usuarios())
    all_errors.extend(validate_productos())
    
    if all_errors:
        print("\nDATA CORRUPTION FOUND:")
        for e in all_errors:
            print(f"- {e}")
        sys.exit(1)
    else:
        print("\nNo data corruption found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
