"""Extractor de datos desde archivos Excel."""

import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path


class ExtractorExcel:
    """Extrae transacciones bancarias desde archivos Excel."""

    def __init__(self):
        self.datos_extraidos = []
        self.nombre_hojas = []

    def extraer(self, ruta_archivo: str, nombre_hoja: Optional[str] = None) -> List[Dict]:
        """Extrae transacciones de un archivo Excel."""
        self.datos_extraidos = []
        
        try:
            # Leer todas las hojas para detectar estructura
            archivo_excel = pd.ExcelFile(ruta_archivo)
            self.nombre_hojas = archivo_excel.sheet_names
            
            # Determinar hoja a leer
            if nombre_hoja is None:
                nombre_hoja = self._detectar_hoja_movimientos()
            
            if nombre_hoja is None:
                # Si no se detecta, usar la primera hoja
                nombre_hoja = self.nombre_hojas[0]
            
            # Leer datos
            df = pd.read_excel(ruta_archivo, sheet_name=nombre_hoja)
            
            # Limpiar y normalizar
            df = self._limpiar_dataframe(df)
            
            # Convertir a lista de diccionarios
            self.datos_extraidos = df.to_dict(orient="records")
            
            return self.datos_extraidos
        
        except Exception as e:
            print(f"Error extrayendo Excel: {str(e)}")
            return []

    def _detectar_hoja_movimientos(self) -> Optional[str]:
        """Detecta automáticamente la hoja con movimientos bancarios."""
        palabras_clave = [
            "movimientos", "transacciones", "movimientos bancarios",
            "extracts", "transactions", "account", "extracto"
        ]
        
        for hoja in self.nombre_hojas:
            hoja_lower = hoja.lower()
            for palabra in palabras_clave:
                if palabra in hoja_lower:
                    return hoja
        
        return None

    def _limpiar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia y normaliza el DataFrame."""
        # Remover filas completamente vacías
        df = df.dropna(how="all")
        
        # Remover columnas completamente vacías
        df = df.dropna(axis=1, how="all")
        
        # Renombrar columnas al remover espacios en blanco
        df.columns = df.columns.str.strip()
        
        # Convertir fechas
        columnas_fecha = [col for col in df.columns if "fecha" in col.lower() or "date" in col.lower()]
        for col in columnas_fecha:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
        
        return df

    def obtener_dataframe(self) -> pd.DataFrame:
        """Retorna los datos extraídos como DataFrame."""
        return pd.DataFrame(self.datos_extraidos)
