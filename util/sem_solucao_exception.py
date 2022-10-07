class SemSolucaoException(Exception):
    def __init__(self, message="Essa configuração de estado inicial e objetivo não possui solução."):
        super().__init__(message)
