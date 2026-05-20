"""Orquestador principal de conciliación bancaria."""

import pandas as pd
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from src.reconciliation.matcher import Matcher
from src.utils.helpers import Ayudantes


class Conciliador:
    """Orquesta el proceso completo de conciliación."""

    def __init__(self, tolerancia_dias: int = 3, tolerancia_monto: float = 0.01, min_fuzzy_score: int = 80):
        self.matcher = Matcher(tolerancia_dias, tolerancia_monto, min_fuzzy_score)
        self.transacciones_bancarias = []
        self.registros_sii = []
        self.conciliaciones = []
        self.discrepancias = []

    def cargar_datos(self, transacciones_bancarias: pd.DataFrame, registros_sii: pd.DataFrame):
        """Carga los datos a conciliar."""
        self.transacciones_bancarias = transacciones_bancarias.to_dict(orient="records")
        self.registros_sii = registros_sii.to_dict(orient="records")

    def conciliar_automaticamente(self) -> Dict:
        """Ejecuta conciliación automática."""
        self.conciliaciones = []
        self.discrepancias = []
        
        registros_conciliados = set()
        
        # Para cada transacción bancaria, buscar coincidencia en SII
        for idx, transaccion in enumerate(self.transacciones_bancarias):
            # Filtrar registros SII no conciliados
            candidatos = [
                reg for i, reg in enumerate(self.registros_sii)
                if i not in registros_conciliados
            ]
            
            coincidencia = self.matcher.encontrar_coincidencia(transaccion, candidatos)
            
            if coincidencia:
                registro_sii, puntuacion = coincidencia
                idx_sii = self.registros_sii.index(registro_sii)
                registros_conciliados.add(idx_sii)
                
                conciliacion = {
                    "id_transaccion": idx,
                    "id_registro_sii": idx_sii,
                    "transaccion": transaccion,
                    "registro_sii": registro_sii,
                    "puntuacion": puntuacion,
                    "estado": "conciliada" if puntuacion >= 95 else "parcial",
                    "fecha_conciliacion": datetime.now(),
                }
                self.conciliaciones.append(conciliacion)
            else:
                discrepancia = {
                    "id_transaccion": idx,
                    "transaccion": transaccion,
                    "motivo": "Sin coincidencia encontrada",
                    "fecha_deteccion": datetime.now(),
                }
                self.discrepancias.append(discrepancia)
        
        # Detectar registros SII sin conciliar
        for idx, registro in enumerate(self.registros_sii):
            if idx not in registros_conciliados:
                discrepancia = {
                    "id_registro_sii": idx,
                    "registro_sii": registro,
                    "motivo": "Registro SII sin coincidencia bancaria",
                    "fecha_deteccion": datetime.now(),
                }
                self.discrepancias.append(discrepancia)
        
        return self._generar_resumen()

    def _generar_resumen(self) -> Dict:
        """Genera resumen de resultados de conciliación."""
        total_transacciones = len(self.transacciones_bancarias)
        total_registros_sii = len(self.registros_sii)
        conciliadas_ok = len([c for c in self.conciliaciones if c["estado"] == "conciliada"])
        conciliadas_parcial = len([c for c in self.conciliaciones if c["estado"] == "parcial"])
        
        return {
            "fecha_conciliacion": datetime.now(),
            "total_transacciones_bancarias": total_transacciones,
            "total_registros_sii": total_registros_sii,
            "conciliaciones_exitosas": len(self.conciliaciones),
            "conciliadas_ok": conciliadas_ok,
            "conciliadas_parcial": conciliadas_parcial,
            "discrepancias": len(self.discrepancias),
            "tasa_conciliacion": (len(self.conciliaciones) / max(total_transacciones, 1)) * 100,
            "montos_conciliados": self._calcular_montos(),
        }

    def _calcular_montos(self) -> Dict:
        """Calcula estadísticas de montos."""
        montos_bancarios = [Ayudantes.parsear_monto(t.get("monto", 0)) for t in self.transacciones_bancarias]
        montos_sii = [Ayudantes.parsear_monto(r.get("monto_total", 0)) for r in self.registros_sii]
        
        return {
            "total_banco": sum(montos_bancarios),
            "total_sii": sum(montos_sii),
            "diferencia": sum(montos_bancarios) - sum(montos_sii),
        }

    def obtener_conciliaciones(self) -> pd.DataFrame:
        """Retorna conciliaciones como DataFrame."""
        return pd.DataFrame(self.conciliaciones)

    def obtener_discrepancias(self) -> pd.DataFrame:
        """Retorna discrepancias como DataFrame."""
        return pd.DataFrame(self.discrepancias)
