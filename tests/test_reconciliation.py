"""Tests para el módulo de conciliación."""

import pytest
import pandas as pd
from src.reconciliation.matcher import Matcher
from src.reconciliation.reconciler import Conciliador
from src.utils.validators import ValidadorDatos
from src.utils.helpers import Ayudantes


class TestValidadores:
    """Tests para validadores."""
    
    def test_validar_fecha_valida(self):
        """Test de fecha válida."""
        valido, msg = ValidadorDatos.validar_fecha("01/01/2024")
        assert valido is True
    
    def test_validar_fecha_invalida(self):
        """Test de fecha inválida."""
        valido, msg = ValidadorDatos.validar_fecha("99/99/9999")
        assert valido is False
    
    def test_validar_monto_positivo(self):
        """Test de monto positivo."""
        valido, msg = ValidadorDatos.validar_monto(1000)
        assert valido is True
    
    def test_validar_monto_negativo(self):
        """Test de monto negativo."""
        valido, msg = ValidadorDatos.validar_monto(-100)
        assert valido is False


class TestAyudantes:
    """Tests para funciones auxiliares."""
    
    def test_parsear_monto(self):
        """Test de parsing de monto."""
        assert Ayudantes.parsear_monto("$ 1.000,50") == 1000.5
        assert Ayudantes.parsear_monto("1000.50") == 1000.5
    
    def test_parsear_fecha(self):
        """Test de parsing de fecha."""
        fecha = Ayudantes.parsear_fecha("01/01/2024")
        assert fecha is not None
    
    def test_formatear_monto(self):
        """Test de formateo de monto."""
        resultado = Ayudantes.formatear_monto(1000.5)
        assert "1.000" in resultado or "1,000" in resultado


class TestMatcher:
    """Tests para el motor de matching."""
    
    def test_comparar_fechas_iguales(self):
        """Test de comparación de fechas iguales."""
        matcher = Matcher()
        puntuacion = matcher._comparar_fechas("01/01/2024", "01/01/2024")
        assert puntuacion == 100
    
    def test_comparar_montos_iguales(self):
        """Test de comparación de montos iguales."""
        matcher = Matcher()
        puntuacion = matcher._comparar_montos(1000, 1000)
        assert puntuacion == 100
    
    def test_encontrar_coincidencia(self):
        """Test de búsqueda de coincidencia."""
        matcher = Matcher()
        
        transaccion = {
            "fecha": "01/01/2024",
            "monto": 1000,
            "concepto": "Pago Factura"
        }
        
        candidatos = [
            {
                "fecha": "01/01/2024",
                "monto_total": 1000,
                "razon_social": "Pago de Factura"
            }
        ]
        
        coincidencia = matcher.encontrar_coincidencia(transaccion, candidatos)
        assert coincidencia is not None


class TestConciliador:
    """Tests para el conciliador."""
    
    def test_cargar_datos(self):
        """Test de carga de datos."""
        conciliador = Conciliador()
        
        df_banco = pd.DataFrame([
            {"fecha": "01/01/2024", "monto": 1000, "concepto": "Test"}
        ])
        
        df_sii = pd.DataFrame([
            {"fecha": "01/01/2024", "monto_total": 1000, "razon_social": "Test"}
        ])
        
        conciliador.cargar_datos(df_banco, df_sii)
        
        assert len(conciliador.transacciones_bancarias) == 1
        assert len(conciliador.registros_sii) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
