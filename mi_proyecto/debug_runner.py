
import sys
import os
from unittest.mock import patch
from io import StringIO

# Add current directory to path
sys.path.append(os.getcwd())

import main

def run_test():
    # Inputs:
    # 1. Select "1" (Login)
    # 2. User "admin001"
    # 3. Pass "Admin123"
    # 4. Select "3" (Salir, inside admin menu - wait, admin menu option 3 is 'Gestionar pedidos', option 7 is 'Cerrar sesión')
    # Let's try 7 to logout from admin menu.
    # 5. Select "3" (Salir from main menu)
    
    # Check main.py menu options again:
    # Main menu: 1. Iniciar sesión, 2. Registrarse, 3. Salir
    # Admin menu: 7. Cerrar sesión
    
    inputs = [
        "1",           # Main menu: Login
        "admin001",    # User
        "Admin123",    # Pass
        "7",           # Admin menu: Logout
        "3"            # Main menu: Exit
    ]
    
    input_generator = (i for i in inputs)
    
    def mock_input(prompt=""):
        print(f"[MOCK INPUT] {prompt}", end='')
        try:
            val = next(input_generator)
            print(val)
            return val
        except StopIteration:
            raise EOFError("No more inputs")

    with patch('builtins.input', side_effect=mock_input):
        try:
            main.main()
            print("\n[TEST SUCCESS] Main executed successfully.")
        except Exception as e:
            print(f"\n[TEST FAILED] Exception: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    run_test()
