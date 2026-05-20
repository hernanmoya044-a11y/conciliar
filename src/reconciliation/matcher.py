"""Motor de matching para conciliación de transacciones."""

from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
from src.utils.validators import ValidadorDatos
from src.utils.helpers import Ayudantes


class Matcher:
    """Realiza matching entre transacciones bancarias y registros."""

    def __init__(self, tolerancia_dias: int = 3, tolerancia_monto: float = 0.01, min_fuzzy_score: int = 80):
        self.tolerancia_dias = tolerancia_dias
        self.tolerancia_monto = tolerancia_monto
        self.min_fuzzy_score = min_fuzzy_score
        self.coincidencias = []

    def encontrar_coincidencia(self, transaccion: Dict, candidatos: List[Dict]) -> Optional[Tuple[Dict, float]]:
        """Encuentra la mejor coincidencia para una transacción."""
        mejor_coincidencia = None
        mejor_puntuacion = 0
        
        for candidato in candidatos:
            puntuacion = self._calcular_puntuacion(transaccion, candidato)
            
            if puntuacion > mejor_puntuacion and puntuacion >= self.min_fuzzy_score:
                mejor_puntuacion = puntuacion
                mejor_coincidencia = candidato
        
        if mejor_coincidencia is not None:
            return mejor_coincidencia, mejor_puntuacion
        
        return None

    def _calcular_puntuacion(self, transaccion1: Dict, transaccion2: Dict) -> float:
        """Calcula puntuación de coincidencia entre dos transacciones."""
        puntuaciones = []
        pesos = []
        
        # Comparar fechas (peso: 30%)
        if "fecha" in transaccion1 and "fecha" in transaccion2:
            puntuacion_fecha = self._comparar_fechas(transaccion1["fecha"], transaccion2["fecha"])
            puntuaciones.append(puntuacion_fecha)
            pesos.append(0.3)
        
        # Comparar montos (peso: 40%)
        if "monto" in transaccion1 and "monto" in transaccion2:
            puntuacion_monto = self._comparar_montos(transaccion1["monto"], transaccion2["monto"])
            puntuaciones.append(puntuacion_monto)
            pesos.append(0.4)
        
        # Comparar conceptos (peso: 30%)
        if "concepto" in transaccion1 and "concepto" in transaccion2:
            puntuacion_concepto = self._comparar_conceptos(transaccion1["concepto"], transaccion2["concepto"])
            puntuaciones.append(puntuacion_concepto)
            pesos.append(0.3)
        
        if not puntuaciones:
            return 0
        
        # Calcular promedio ponderado
        puntuacion_total = sum(p * w for p, w in zip(puntuaciones, pesos)) / sum(pesos)
        
        return puntuacion_total

    def _comparar_fechas(self, fecha1, fecha2) -> float:
        """Compara dos fechas y retorna puntuación (0-100)."""
        try:
            f1 = Ayudantes.parsear_fecha(fecha1)
            f2 = Ayudantes.parsear_fecha(fecha2)
            
            if f1 is None or f2 is None:
                return 0
            
            diferencia = abs((f1 - f2).days)
            
            if diferencia == 0:
                return 100
            elif diferencia <= self.tolerancia_dias:
                return 100 - (diferencia * 20)
            else:
                return 0
        
        except Exception:
            return 0

    def _comparar_montos(self, monto1, monto2) -> float:
        """Compara dos montos y retorna puntuación (0-100)."""
        try:
            m1 = Ayudantes.parsear_monto(monto1)
            m2 = Ayudantes.parsear_monto(monto2)
            
            if m1 == 0 and m2 == 0:
                return 100
            
            if m1 == 0 or m2 == 0:
                return 0
            
            diferencia_porcentaje = abs(m1 - m2) / max(m1, m2)
            
            if diferencia_porcentaje == 0:
                return 100
            elif diferencia_porcentaje <= 0.01:
                return 100 - (diferencia_porcentaje * 1000)
            else:
                return 0
        
        except Exception:
            return 0

    def _comparar_conceptos(self, concepto1: str, concepto2: str) -> float:
        """Compara dos conceptos usando fuzzy matching (0-100)."""
        try:
            c1 = ValidadorDatos.normalizar_concepto(str(concepto1))
            c2 = ValidadorDatos.normalizar_concepto(str(concepto2))
            
            if c1 == "" or c2 == "":
                return 0
            
            puntuacion = fuzz.token_set_ratio(c1, c2)
            
            return puntuacion
        
        except Exception:
            return 0

    def encontrar_coincidencias_multiples(self, transaccion: Dict, candidatos: List[Dict], cantidad: int = 5) -> List[Tuple[Dict, float]]:
        """Encuentra múltiples coincidencias ordenadas por puntuación."""
        coincidencias = []
        
        for candidato in candidatos:
            puntuacion = self._calcular_puntuacion(transaccion, candidato)
            coincidencias.append((candidato, puntuacion))
        
        # Ordenar por puntuación descendente
        coincidencias.sort(key=lambda x: x[1], reverse=True)
        
        # Retornar top N
        return coincidencias[:cantidad]
