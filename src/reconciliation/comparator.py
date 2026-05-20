"""Comparador detallado para análisis de diferencias."""

import pandas as pd
from typing import List, Dict, Tuple
from src.utils.helpers import Ayudantes


class Comparador:
    """Compara transacciones para identificar discrepancias."""

    @staticmethod
    def comparar_montos(monto1: float, monto2: float, tolerancia: float = 0.01) -> Dict:
        """Compara detalladamente dos montos."""
        diferencia = abs(monto1 - monto2)
        porcentaje_diferencia = (diferencia / max(monto1, monto2)) * 100 if max(monto1, monto2) > 0 else 0
        
        return {
            "monto1": monto1,
            "monto2": monto2,
            "diferencia": diferencia,
            "porcentaje_diferencia": porcentaje_diferencia,
            "dentro_tolerancia": diferencia <= tolerancia,
            "tipo_diferencia": "exceso" if monto1 > monto2 else "defecto" if monto1 < monto2 else "igual",
        }

    @staticmethod
    def comparar_fechas(fecha1, fecha2, tolerancia_dias: int = 3) -> Dict:
        """Compara detalladamente dos fechas."""
        f1 = Ayudantes.parsear_fecha(fecha1)
        f2 = Ayudantes.parsear_fecha(fecha2)
        
        if f1 is None or f2 is None:
            return {"error": "Fechas no válidas"}
        
        diferencia_dias = abs((f1 - f2).days)
        
        return {
            "fecha1": f1,
            "fecha2": f2,
            "diferencia_dias": diferencia_dias,
            "dentro_tolerancia": diferencia_dias <= tolerancia_dias,
            "es_posterior": f1 > f2,
        }

    @staticmethod
    def generar_reporte_discrepancias(conciliaciones: List[Dict]) -> pd.DataFrame:
        """Genera reporte de discrepancias encontradas."""
        discrepancias = []
        
        for conc in conciliaciones:
            if conc["estado"] != "conciliada":
                trans = conc["transaccion"]
                sii = conc["registro_sii"]
                
                discrepancia = {
                    "fecha_transaccion": trans.get("fecha"),
                    "fecha_sii": sii.get("fecha"),
                    "monto_banco": Ayudantes.parsear_monto(trans.get("monto", 0)),
                    "monto_sii": Ayudantes.parsear_monto(sii.get("monto_total", 0)),
                    "concepto_banco": trans.get("concepto", ""),
                    "concepto_sii": sii.get("razon_social", ""),
                    "puntuacion_matching": conc["puntuacion"],
                    "tipo": "monto" if abs(Ayudantes.parsear_monto(trans.get("monto", 0)) - Ayudantes.parsear_monto(sii.get("monto_total", 0))) > 0 else "fecha" if trans.get("fecha") != sii.get("fecha") else "concepto",
                }
                discrepancias.append(discrepancia)
        
        return pd.DataFrame(discrepancias)

    @staticmethod
    def calcular_diferencias_totales(transacciones_banco: pd.DataFrame, registros_sii: pd.DataFrame) -> Dict:
        """Calcula diferencias totales entre banco y SII."""
        total_banco = Ayudantes.parsear_monto(transacciones_banco["monto"].sum())
        total_sii = Ayudantes.parsear_monto(registros_sii["monto_total"].sum())
        
        diferencia = total_banco - total_sii
        porcentaje = (diferencia / max(total_banco, total_sii)) * 100 if max(total_banco, total_sii) > 0 else 0
        
        return {
            "total_banco": total_banco,
            "total_sii": total_sii,
            "diferencia": diferencia,
            "porcentaje_diferencia": porcentaje,
            "cantidad_transacciones_banco": len(transacciones_banco),
            "cantidad_registros_sii": len(registros_sii),
        }
