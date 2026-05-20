"""Generador de reportes de conciliación."""

import pandas as pd
from typing import List, Dict
from datetime import datetime
from src.utils.helpers import Ayudantes


class GeneradorReportes:
    """Genera reportes de conciliación bancaria."""

    @staticmethod
    def generar_reporte_conciliacion(resumen: Dict, conciliaciones: List[Dict], discrepancias: List[Dict]) -> Dict:
        """Genera reporte completo de conciliación."""
        return {
            "fecha_generacion": datetime.now(),
            "resumen": resumen,
            "conciliaciones": pd.DataFrame(conciliaciones),
            "discrepancias": pd.DataFrame(discrepancias),
            "estadisticas": GeneradorReportes._calcular_estadisticas(conciliaciones, discrepancias),
        }

    @staticmethod
    def _calcular_estadisticas(conciliaciones: List[Dict], discrepancias: List[Dict]) -> Dict:
        """Calcula estadísticas del reporte."""
        puntuaciones = [c.get("puntuacion", 0) for c in conciliaciones]
        
        return {
            "total_conciliaciones": len(conciliaciones),
            "total_discrepancias": len(discrepancias),
            "puntuacion_promedio": sum(puntuaciones) / len(puntuaciones) if puntuaciones else 0,
            "puntuacion_minima": min(puntuaciones) if puntuaciones else 0,
            "puntuacion_maxima": max(puntuaciones) if puntuaciones else 0,
            "tasa_exito": (len(conciliaciones) / (len(conciliaciones) + len(discrepancias))) * 100 if (len(conciliaciones) + len(discrepancias)) > 0 else 0,
        }

    @staticmethod
    def generar_reporte_pagos(pagos: List[Dict]) -> pd.DataFrame:
        """Genera reporte de pagos."""
        df = pd.DataFrame(pagos)
        
        if not df.empty:
            df["monto_formateado"] = df["monto"].apply(Ayudantes.formatear_monto)
            df["estado_traducido"] = df["estado"].map({
                "pendiente": "Pendiente",
                "procesado": "Procesado",
                "confirmado": "Confirmado",
                "rechazado": "Rechazado",
                "devuelto": "Devuelto",
            })
        
        return df

    @staticmethod
    def generar_reporte_cuadre_sii(transacciones: pd.DataFrame, registros_sii: pd.DataFrame) -> Dict:
        """Genera reporte de cuadre con SII."""
        total_banco = Ayudantes.parsear_monto(transacciones["monto"].sum())
        total_sii = Ayudantes.parsear_monto(registros_sii["monto_total"].sum())
        diferencia = total_banco - total_sii
        
        return {
            "total_banco": total_banco,
            "total_sii": total_sii,
            "diferencia": diferencia,
            "diferencia_formateada": Ayudantes.formatear_monto(diferencia),
            "porcentaje_diferencia": (diferencia / max(total_banco, total_sii)) * 100 if max(total_banco, total_sii) > 0 else 0,
            "fecha_reporte": datetime.now(),
            "estado_cuadre": "Cuadrado" if abs(diferencia) < 1 else "Descuadrado",
        }
