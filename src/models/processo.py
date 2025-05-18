import re

class Processo:
    """Classe para representar e validar um processo judicial."""
    
    def __init__(self, numero, tipo):
        self.numero = numero
        self.tipo = tipo.upper()
        
    @property
    def numero(self):
        return self._numero
        
    @numero.setter
    def numero(self, value):
        if not self.validar_numero(value):
            raise ValueError("Número de processo inválido. Deve conter exatamente 20 dígitos numéricos.")
        self._numero = value
    
    @property
    def tipo(self):
        return self._tipo
        
    @tipo.setter
    def tipo(self, value):
        if value not in ["TJ", "TRF"]:
            raise ValueError("Tipo de processo inválido. Deve ser 'TJ' ou 'TRF'.")
        self._tipo = value
    
    @staticmethod
    def validar_numero(numero):
        """Valida se o número do processo tem exatamente 20 dígitos numéricos."""
        padrao = re.compile(r'^\d{20}$')
        return bool(padrao.match(numero))