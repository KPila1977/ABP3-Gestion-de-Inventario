# Sistema de Gestión de Productos - ABP3

Sistema modular de gestión de productos desarrollado en Python, diseñado para una empresa de tecnología que busca automatizar sus procesos internos.

## Características Principales

### 1. Gestión de Usuarios con Roles
- **Administrador**: Acceso total al sistema
- **Supervisor**: Revisión de stock y análisis
- **Digitador**: Ingreso y marcado de egresos
- **Bodeguero**: Orden y recepción de mercancías
- **Usuario**: Consulta básica de productos

### 2. Validaciones de Datos
- RUN chileno con dígito verificador
- Email con formato válido
- Teléfono con código de país
- Datos en mayúsculas según requerimiento

### 3. Gestión de Mercancías
- Checklist de recepción
- Estados de recepción (Conforme/Disconforme/Rechazo)
- Datos completos del lote
- Control de fechas de elaboración y vencimiento

### 4. Control de Inventario
- Stock mínimo por producto
- Alertas de stock crítico
- Productos próximos a vencer
- Revisión y ordenamiento de bodega

### 5. Auditoría Completa
- Logs diarios de todas las actividades
- Registro de sesiones y movimientos
- Archivos .log organizados por fecha

## Estructura del Proyecto
mi_proyecto/
├── main.py # Punto de entrada principal
├── modules/ # Módulos del sistema
│ ├── init.py
│ ├── usuarios.py # Gestión de usuarios
│ ├── productos.py # Gestión de productos
│ ├── inventario.py # Control de inventario
│ ├── auditoria.py # Sistema de logs
│ └── utils.py # Utilidades generales
├── data/ # Datos persistentes (JSON)
│ ├── usuarios.json
│ └── productos.json
├── logs/ # Archivos de auditoría
│ └── auditoria_YYYY-MM-DD.log
└── README.md # Este archivo

El sistema incluye usuarios preconfigurados para pruebas:
ID	Rol	Usuario	Contraseña
admin001	Administrador	admin@empresa.cl	Admin123
super001	Supervisor	supervisor@empresa.cl	Super123
digit001	Digitador	digitador@empresa.cl	Digit123
bode001	Bodeguero	bodeguero@empresa.cl	Bode123
user001	Usuario	usuario@empresa.cl	User123

## Instalación y Uso

1. **Crear estructura de carpetas:**
   ```bash
   mkdir mi_proyecto
   cd mi_proyecto
   mkdir modules data logs
Copiar los archivos:

Colocar cada archivo .py en su carpeta correspondiente

Ejecutar el sistema:

bash
python main.py

