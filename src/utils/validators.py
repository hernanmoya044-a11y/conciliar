"""Validadores de datos para la aplicación."""

import re
from datetime import datetime
from typing import Tuple, List


class ValidadorDatos:
    """Clase para validar datos bancarios y del SII."""

    @staticmethod
    def validar_fecha(fecha_str: str) -> Tuple[bool, str]:
        """Valida formato de fecha."""
        formatos = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]
        
        for fmt in formatos:
            try:
                datetime.strptime(fecha_str, fmt)
                return True, "Fecha válida"
            except ValueError:
                continue
        
        return False, f"Formato de fecha no reconocido: {fecha_str}"

    @staticmethod
    def validar_monto(monto) -> Tuple[bool, str]:
        """Valida que el monto sea numérico y positivo."""
        try:
            monto_float = float(monto)
            if monto_float < 0:
                return False, "El monto no puede ser negativo"
            return True, "Monto válido"
        except (ValueError, TypeError):
            return False, f"Monto inválido: {monto}"

    @staticmethod
    def validar_rut(rut: str) -> Tuple[bool, str]:
        """Valida RUT chileno."""
        rut = rut.replace(".", "").upper()
        
        if "-" not in rut:
            return False, "RUT debe contener guion"
        
        try:
            num, dv = rut.split("-")
            num = int(num)
            
            # Calcular dígito verificador
            s = 0
            m = 2
            for d in reversed(str(num)):
                s += int(d) * m
                m = m + 1 if m < 7 else 2
            
            dv_calculado = 11 - (s % 11)
            if dv_calculado == 11:
                dv_calculado = 0
            elif dv_calculado == 10:
                dv_calculado = "K"
            
            if str(dv_calculado) == dv:
                return True, "RUT válido"
            else:
                return False, "Dígito verificador incorrecto"
        except Exception as e:
            return False, f"Error validando RUT: {str(e)}"

    @staticmethod
    def validar_referencia_bancaria(referencia: str) -> Tuple[bool, str]:
        """Valida formato de referencia bancaria."""
        if not referencia or len(str(referencia).strip()) == 0:
            return False, "Referencia vacía"
        
        return True, "Referencia válida"

    @staticmethod
    def validar_concepto(concepto: str) -> Tuple[bool, str]:
        """Valida concepto/descripción de transacción."""
        if not concepto or len(str(concepto).strip()) == 0:
            return False, "Concepto vacío"
        
        if len(str(concepto)) > 500:
            return False, "Concepto muy largo (máx 500 caracteres)"
        
        return True, "Concepto válido"

    @staticmethod
    def limpiar_espacios(texto: str) -> str:
        """Limpia espacios en blanco excesivos."""
        if not isinstance(texto, str):
            return str(texto)
        return " ".join(texto.split())

    @staticmethod
    def normalizar_concepto(concepto: str) -> str:
        """Normaliza concepto para mejor matching."""
        concepto = ValidadorDatos.limpiar_espacios(concepto)
        concepto = concepto.upper()
        # Remover caracteres especiales
        concepto = re.sub(r"[^A-Z0-9 áéíóúñÁÉÍÓÚÑ]", "", concepto)
        return concepto
