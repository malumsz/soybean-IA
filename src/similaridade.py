import util.crud as crud
import heapq 

class Similaridade: 
    def __init__(self, novoCaso):
        self.pesos = [3,7,1,2,7,7,7,8,1,3,8,7,8,7,6,7,7,8,6,8,8,8,5,6,8,8,7,7,8,1,3,8,8,7,4]
        self.tabela_similaridade = [[0,1,2,3], [0,1,2,3], [0,1,2,3], [0,1,2,3,4,5,6], [0,1], [0,1,2,3], [0,1], [0,1,2,3], [0,1,2], [0,1], [0,1,2], [0,1], [0,1,2], [0,1], [0,1,2], [0,1,2], [0,1,2], [0,1], [0,1], [0,1], [0,1], [0,1], [0,1], [0,1,2], [0,1,2], [0,1], [0,1], [0,1], [0,1], [0,1,2], [0,1,2], [0,1], [0,1], [0,1,2,3], [0,1,2]]
        self.crud = crud.CRUD()
        self.novo_caso = novoCaso
        self.similaridade_geral = self.calculo_todos_casos()
        self.casos = self.get_todos_casos()

    def calculo_similaridade(self, novo_caso, caso):
        caso_valores = caso[2:]

        similaridade = [0] * (len(caso_valores))
        similaridade_global = 0
        
        for i in range(len(caso_valores)):
            #cálculo da similaridade circular para data
            if i == 3:
                if novo_caso[i] is None or caso_valores[i] is None:
                    similaridade[i] = 0
                    continue
                if novo_caso[i] == caso_valores[i]:
                    similaridade[i] = 1
                    continue
                if abs(novo_caso[i] - caso_valores[i]) < abs(novo_caso[i] - (caso_valores[i] + 12)):
                    similaridade[i] = 1 - abs(novo_caso[i] - caso_valores[i]) / (self.tabela_similaridade[i][-1] - self.tabela_similaridade[i][0])
                    #print(similaridade[i], "entrou aqui")
                    continue
                else:
                    similaridade[i] = 1 - abs(novo_caso[i] - (caso_valores[i] + 12)) / (self.tabela_similaridade[i][-1] - self.tabela_similaridade[i][0])
                    #print(similaridade[i], "entrou aqui 2")
                    continue
            elif caso_valores[i] is None or novo_caso[i] is None:
                similaridade[i] = 0
                continue
            elif novo_caso[i] == caso_valores[i]:
                similaridade[i] = 1
                continue
            else:
                similaridade[i] = 1 - (abs(novo_caso[i] - caso_valores[i])/((self.tabela_similaridade[i][-1]) - (self.tabela_similaridade[i][0]))) 
                continue
        
        #print(similaridade)
        for i in range(len(similaridade)):
            similaridade_global = similaridade_global + similaridade[i] * self.pesos[i]    
        similaridade_global = similaridade_global / sum(self.pesos) * 100
        return round(similaridade_global, 2)

    def calculo_todos_casos(self):
        similaridade_geral = []
        
        self.crud.conectar()
        casos = self.crud.read()
        self.crud.desconectar()

        for caso in casos:
            similaridade_geral.append(self.calculo_similaridade(self.novo_caso, caso))
        return similaridade_geral

    def get_maiores_valores(self, n):
        #indices_maiores = heapq.nlargest(n, range(len(self.similaridade_geral)), key=lambda i: self.similaridade_geral[i])
        valores_maiores = heapq.nlargest(n, self.calculo_todos_casos())
        return valores_maiores #, indices_maiores
    
    def get_indices_maiores_valores(self, n):
        indices_maiores = heapq.nlargest(n, range(len(self.similaridade_geral)), key=lambda i: self.similaridade_geral[i])
        return indices_maiores

    def get_todos_casos(self):
        self.crud.conectar()
        casos = self.crud.read()
        self.crud.desconectar()
        return casos
