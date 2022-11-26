from ag import Selecao
from ag_cod_binaria import main


def fit(x: float) -> float: return 1/((x-3)**2+0.1)+1/((x-2)**2+0.05)+2


main('funcao-letra-a-roleta', Selecao.ROLETA, -2, 8, fit, fit, 50)
main('funcao-letra-a-torneio', Selecao.TORNEIO, -2, 8, fit, fit, 50)
