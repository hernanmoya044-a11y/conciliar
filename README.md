# Aplicación de Conciliación Bancaria

Sistema automatizado de conciliación bancaria que permite lectura de extractos en PDF y Excel, conciliación automática de transacciones y cuadre con registros de compra-venta del SII.

## 🎯 Características Principales

- 📄 **Lectura de Extractos**: Importación automática desde PDF y archivos Excel
- 💰 **Conciliación Automática**: Matching inteligente por monto, fecha y concepto
- 👥 **Gestión de Pagos**: Seguimiento de pagos a clientes y proveedores
- 📊 **Cuadre SII**: Comparación automática con registros de compra-venta del SII
- 📈 **Reportes Detallados**: Auditoría completa de conciliaciones
- 🔍 **Búsqueda Fuzzy**: Coincidencia aproximada de conceptos

## 📋 Requisitos

- Python 3.8+
- pip

## 🚀 Instalación

```bash
git clone https://github.com/hernanmoya044-a11y/conciliar.git
cd conciliar
pip install -r requirements.txt
```

## 💻 Uso

```bash
streamlit run app.py
```

Luego abre tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
conciliar/
├── README.md
├── requirements.txt
├── config.py
├── app.py
├── src/
│   ├── __init__.py
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py
│   │   ├── excel_extractor.py
│   │   └── sii_extractor.py
│   ├── reconciliation/
│   │   ├── __init__.py
│   │   ├── matcher.py
│   │   ├── reconciler.py
│   │   └── comparator.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── db.py
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   └── exporters.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── helpers.py
├── data/
│   ├── samples/
│   └── uploads/
└── tests/
    ├── __init__.py
    └── test_reconciliation.py
```

## 🔧 Tecnologías

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Base de Datos**: SQLite
- **Datos**: Pandas, NumPy
- **PDF**: PyPDF2, pdfplumber
- **Excel**: openpyxl, pandas
- **Matching**: difflib, fuzzywuzzy

## 📖 Guía de Uso

### 1. Cargar Extractos Bancarios
- Ve a la sección "Cargar Datos"
- Sube un archivo PDF o Excel con el extracto bancario
- El sistema extraerá automáticamente las transacciones

### 2. Cargar Registros SII
- Sube el archivo Excel con los registros de compra-venta del SII
- Selecciona el tipo (compras o ventas)

### 3. Ejecutar Conciliación
- Haz clic en "Conciliar Automáticamente"
- El sistema hará matching de transacciones
- Revisa los resultados y resuelve discrepancias manualmente si es necesario

### 4. Revisar Pagos
- Accede a "Gestión de Pagos"
- Visualiza pagos a clientes y proveedores
- Actualiza estados de pago

### 5. Generar Reportes
- Usa la sección "Reportes"
- Descarga cuadres y auditoría en Excel

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo licencia MIT.

## 📧 Contacto

Creado por hernanmoya044-a11y
