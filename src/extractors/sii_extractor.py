"""Extractor de datos desde archivos del SII."""

import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime


class ExtractorSII:
    """Extrae registros de compra-venta del SII desde archivos Excel."""

    def __init__(self):
        self.datos_extraidos = []
        self.tipo_registro = None  # "compras" o "ventas"

    def extraer(self, ruta_archivo: str, tipo_registro: str = "compras", nombre_hoja: Optional[str] = None) -> List[Dict]:
        """Extrae registros del SII de un archivo Excel."""
        self.datos_extraidos = []
        self.tipo_registro = tipo_registro
        
        try:
            # Leer archivo
            archivo_excel = pd.ExcelFile(ruta_archivo)
            
            # Detectar hoja si no se proporciona
            if nombre_hoja is None:
                nombre_hoja = self._detectar_hoja_sii(archivo_excel.sheet_names, tipo_registro)
            
            if nombre_hoja is None:
                nombre_hoja = archivo_excel.sheet_names[0]
            
            # Leer datos
            df = pd.read_excel(ruta_archivo, sheet_name=nombre_hoja)
            
            # Limpiar
            df = self._limpiar_dataframe(df)
            
            # Normalizar columnas para SII
            df = self._normalizar_columnas_sii(df)
            
            # Convertir a lista de diccionarios
            self.datos_extraidos = df.to_dict(orient="records")
            
            return self.datos_extraidos
        
        except Exception as e:
            print(f"Error extrayendo SII: {str(e)}")
            return []

    def _detectar_hoja_sii(self, nombres_hojas: List[str], tipo: str) -> Optional[str]:
        """Detecta la hoja del SII basada en el tipo."""
        palabras_compras = ["compras", "purchase", "purchases", "proveedores"]
        palabras_ventas = ["ventas", "sales", "revenue", "clientes"]
        
        palabras_objetivo = palabras_compras if tipo == "compras" else palabras_ventas
        
        for hoja in nombres_hojas:
            hoja_lower = hoja.lower()
            for palabra in palabras_objetivo:
                if palabra in hoja_lower:
                    return hoja
        
        return None

    def _limpiar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia el DataFrame del SII."""
        # Remover filas vacías
        df = df.dropna(how="all")
        
        # Normalizar nombres de columnas
        df.columns = df.columns.str.strip().str.lower()
        
        # Convertir fechas
        columnas_fecha = [col for col in df.columns if "fecha" in col]
        for col in columnas_fecha:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
        
        # Convertir montos a float
        columnas_monto = [col for col in df.columns if "monto" in col or "total" in col or "neto" in col or "iva" in col]
        for col in columnas_monto:
            try:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            except:
                pass
        
        return df

    def _normalizar_columnas_sii(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza nombres de columnas para estándar SII."""
        mapeo_columnas = {
            "fecha": ["fecha", "date"],
            "rut_proveedor": ["rut", "rut proveedor", "rut_proveedor"],
            "razon_social": ["razón social", "razon social", "proveedor", "nombre"],
            "monto_neto": ["neto", "monto neto", "monto_neto"],
            "iva": ["iva", "monto iva", "monto_iva"],
            "monto_total": ["total", "monto total", "monto_total"],
            "tipo_documento": ["tipo", "tipo documento", "tipo_documento"],
            "numero_documento": ["número", "numero", "folio", "numero_documento"],
        }
        
        nuevas_columnas = {}
        for columna_actual in df.columns:
            for nombre_estandar, sinonimos in mapeo_columnas.items():
                if columna_actual in sinonimos:
                    nuevas_columnas[columna_actual] = nombre_estandar
                    break
        
        if nuevas_columnas:
            df = df.rename(columns=nuevas_columnas)
        
        return df

    def obtener_dataframe(self) -> pd.DataFrame:
        """Retorna los datos extraídos como DataFrame."""
        return pd.DataFrame(self.datos_extraidos)
