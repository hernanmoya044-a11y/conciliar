"""Exportadores de reportes a diferentes formatos."""

import pandas as pd
from typing import Dict, Optional
from pathlib import Path
from datetime import datetime


class ExportadorReportes:
    """Exporta reportes a diferentes formatos."""

    @staticmethod
    def exportar_excel(reporte: Dict, ruta_salida: str):
        """Exporta reporte a archivo Excel."""
        try:
            with pd.ExcelWriter(ruta_salida, engine="openpyxl") as writer:
                # Hoja de resumen
                resumen_df = pd.DataFrame([reporte["resumen"]])
                resumen_df.to_excel(writer, sheet_name="Resumen", index=False)
                
                # Hoja de conciliaciones
                reporte["conciliaciones"].to_excel(writer, sheet_name="Conciliaciones", index=False)
                
                # Hoja de discrepancias
                reporte["discrepancias"].to_excel(writer, sheet_name="Discrepancias", index=False)
                
                # Hoja de estadísticas
                stats_df = pd.DataFrame([reporte["estadisticas"]])
                stats_df.to_excel(writer, sheet_name="Estadísticas", index=False)
            
            return True, f"Reporte exportado a {ruta_salida}"
        
        except Exception as e:
            return False, f"Error exportando reporte: {str(e)}"

    @staticmethod
    def exportar_csv(df: pd.DataFrame, ruta_salida: str) -> tuple:
        """Exporta DataFrame a CSV."""
        try:
            df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")
            return True, f"Archivo exportado a {ruta_salida}"
        except Exception as e:
            return False, f"Error exportando CSV: {str(e)}"

    @staticmethod
    def generar_nombre_archivo(prefijo: str = "reporte", extension: str = ".xlsx") -> str:
        """Genera nombre de archivo con timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefijo}_{timestamp}{extension}"
