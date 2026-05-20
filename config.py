import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Rutas
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
SAMPLES_DIR = DATA_DIR / "samples"
DB_DIR = BASE_DIR / "database"

# Crear directorios si no existen
for directory in [DATA_DIR, UPLOADS_DIR, SAMPLES_DIR, DB_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DB_DIR}/conciliacion.db"
)

# Configuración de Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Conciliación Bancaria",
    "page_icon": "💰",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Configuración de Conciliación
CONCILIACION_CONFIG = {
    "tolerance_dias": 3,  # Tolerancia de días para matching
    "tolerance_monto": 0.01,  # Tolerancia de monto en pesos
    "min_fuzzy_score": 80,  # Score mínimo para fuzzy matching
    "max_resultados_busqueda": 10,
}

# Configuración de Extracción
EXTRACCION_CONFIG = {
    "pdf_dpi": 150,
    "excel_sheet_names": ["Movimientos", "Transacciones", "Movimientos bancarios"],
    "sii_sheet_names": ["Compras", "Ventas", "Registro"],
}

# Columnas esperadas
COLUMNAS_BANCARIAS = {
    "fecha": ["Fecha", "fecha", "Date", "date"],
    "monto": ["Monto", "monto", "Amount", "Valor", "valor"],
    "concepto": ["Concepto", "concepto", "Descripción", "descripcion", "Description"],
    "tipo": ["Tipo", "tipo", "Type", "Débito/Crédito"],
    "referencia": ["Referencia", "referencia", "Reference", "Número", "numero"],
}

COLUMNAS_SII = {
    "fecha": ["Fecha", "fecha"],
    "rut_proveedor": ["RUT Proveedor", "rut_proveedor", "RUT"],
    "razon_social": ["Razón Social", "razon_social", "Proveedor"],
    "monto_neto": ["Monto Neto", "monto_neto", "Neto"],
    "monto_iva": ["IVA", "iva", "Monto IVA"],
    "monto_total": ["Monto Total", "monto_total", "Total"],
    "tipo_documento": ["Tipo Documento", "tipo_documento"],
    "numero_documento": ["Número", "numero", "Folio"],
}

# Límites de archivo
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = {
    "pdf": [".pdf"],
    "excel": [".xlsx", ".xls", ".csv"],
}

# Configuración de Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    "rotation": "10 MB",
    "retention": "10 days",
}

# Estados de conciliación
ESTADOS_CONCILIACION = {
    "pendiente": "Pendiente",
    "conciliada": "Conciliada",
    "parcial": "Parcialmente Conciliada",
    "discrepancia": "Discrepancia",
    "manual": "Conciliación Manual",
}

# Estados de pago
ESTADOS_PAGO = {
    "pendiente": "Pendiente",
    "procesado": "Procesado",
    "confirmado": "Confirmado",
    "rechazado": "Rechazado",
    "devuelto": "Devuelto",
}
