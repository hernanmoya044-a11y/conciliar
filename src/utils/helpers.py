"""Funciones auxiliares generales."""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import re


class Ayudantes:
    """Clase con funciones auxiliares."""

    @staticmethod
    def parsear_fecha(fecha_str, formatos=None):
        """Intenta parsear una fecha con múltiples formatos."""
        if pd.isna(fecha_str):
            return None
        
        if isinstance(fecha_str, pd.Timestamp):
            return fecha_str.date()
        
        if formatos is None:
            formatos = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d.%m.%Y"]
        
        for fmt in formatos:
            try:
                return datetime.strptime(str(fecha_str), fmt).date()
            except (ValueError, TypeError):
                continue
        
        return None

    @staticmethod
    def parsear_monto(monto_str) -> float:
        """Convierte string de monto a float, removiendo símbolos."""
        if pd.isna(monto_str):
            return 0.0
        
        if isinstance(monto_str, (int, float)):
            return float(monto_str)
        
        # Remover símbolos de moneda y separadores
        monto_str = str(monto_str).strip()
        monto_str = re.sub(r"[^0-9.,-]", "", monto_str)
        
        # Detectar si usa coma como decimal
        if "," in monto_str and "." in monto_str:
            if monto_str.rindex(",") > monto_str.rindex("."):
                monto_str = monto_str.replace(".", "").replace(",", ".")
            else:
                monto_str = monto_str.replace(",", "")
        elif "," in monto_str:
            monto_str = monto_str.replace(",", ".")
        
        try:
            return float(monto_str)
        except ValueError:
            return 0.0

    @staticmethod
    def esta_dentro_rango_fechas(fecha: datetime.date, fecha_ref: datetime.date, dias: int = 3) -> bool:
        """Verifica si una fecha está dentro de un rango de días."""
        if fecha is None or fecha_ref is None:
            return False
        
        diferencia = abs((fecha - fecha_ref).days)
        return diferencia <= dias

    @staticmethod
    def esta_dentro_rango_monto(monto1: float, monto2: float, tolerancia: float = 0.01) -> bool:
        """Verifica si dos montos están dentro de tolerancia."""
        if monto1 is None or monto2 is None:
            return False
        
        diferencia = abs(monto1 - monto2)
        return diferencia <= tolerancia

    @staticmethod
    def extraer_numeros(texto: str) -> List[int]:
        """Extrae todos los números de un texto."""
        if not texto:
            return []
        return [int(num) for num in re.findall(r"\d+", str(texto))]

    @staticmethod
    def extraer_rut(texto: str) -> str:
        """Extrae RUT de un texto."""
        patron = r"\d{1,2}\.?\d{3}\.?\d{3}[-]?[0-9K]"
        coincidencias = re.findall(patron, texto)
        return coincidencias[0] if coincidencias else None

    @staticmethod
    def agrupar_por_fecha(transacciones: List[Dict], campo_fecha: str = "fecha") -> Dict:
        """Agrupa transacciones por fecha."""
        agrupadas = {}
        for transaccion in transacciones:
            fecha = transaccion.get(campo_fecha)
            if fecha not in agrupadas:
                agrupadas[fecha] = []
            agrupadas[fecha].append(transaccion)
        return agrupadas

    @staticmethod
    def agrupar_por_rango_monto(transacciones: List[Dict], rango: float = 1000, campo_monto: str = "monto") -> Dict:
        """Agrupa transacciones por rango de monto."""
        agrupadas = {}
        for transaccion in transacciones:
            monto = transaccion.get(campo_monto, 0)
            rango_clave = int(monto // rango)
            if rango_clave not in agrupadas:
                agrupadas[rango_clave] = []
            agrupadas[rango_clave].append(transaccion)
        return agrupadas

    @staticmethod
    def crear_resumen_estadistico(transacciones: List[Dict], campo_monto: str = "monto") -> Dict:
        """Crea resumen estadístico de transacciones."""
        if not transacciones:
            return {}
        
        montos = [t.get(campo_monto, 0) for t in transacciones]
        
        return {
            "total": sum(montos),
            "promedio": sum(montos) / len(montos),
            "maximo": max(montos),
            "minimo": min(montos),
            "cantidad": len(transacciones),
        }

    @staticmethod
    def formatear_monto(monto: float, moneda: str = "$") -> str:
        """Formatea monto como string con separadores."""
        return f"{moneda} {monto:,.2f}".replace(",", ".")
