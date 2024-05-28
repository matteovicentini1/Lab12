import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idmap = {}
        self.ricor=[]
        self.costo=0



    def creagrafo(self,n):
        rivenditori = DAO.getRivenditori(n)
        self.grafo.add_nodes_from(rivenditori)
        for i in self.grafo.nodes:
            self.idmap[i.Retailer_code]=i

    def connessioni(self,n,y):
        for i in self.grafo.nodes:
            archi = DAO.getarchi(n, y, i.Retailer_code)
            for x, u, z in archi:
                if self.grafo.has_edge(self.idmap[x], self.idmap[u]):
                    continue
                else:
                    self.grafo.add_edge(self.idmap[x], self.idmap[u], weight=z)


    def getnodi(self):
        return len(self.grafo.nodes)

    def getarchi(self):
        return len(self.grafo.edges)

    def nazioni(self):
        return DAO.getCountry()

    def volumi(self):
        l=[]
        for i in self.grafo.nodes:
            somma=0
            for vic in self.grafo.neighbors(i):
                somma+= self.grafo[i][vic]['weight']
            l.append((i.Retailer_name,somma))
        ordinata = sorted(l , key=lambda x:x[1], reverse=True)
        return ordinata

    def percorso(self,numero):
        self.ricor=[]
        self.costo=0

        for i in self.grafo.nodes:
            self.ricorsione([i],numero,0,i)

        return self.ricor,self.costo




    def ricorsione(self,parziale,max,cos,start):
        if len(parziale) == max:
            if parziale[-1].Retailer_code == parziale[0].Retailer_code and self.costo<=cos:
                self.ricor=copy.deepcopy(parziale)
                self.costo=cos

        else:
            for i in self.grafo.neighbors(parziale[-1]):
                if i not in parziale[1:] and i.Retailer_code!=start.Retailer_code:
                    cos += self.grafo[parziale[-1]][i]['weight']
                    parziale.append(i)
                    self.ricorsione(parziale,max,cos,start)
                    parziale.pop()
                elif i not in parziale[1:] and i.Retailer_code==start.Retailer_code and len(parziale)==(max-1):
                    cos += self.grafo[parziale[-1]][i]['weight']
                    parziale.append(i)
                    self.ricorsione(parziale, max, cos,start)
                    parziale.pop()
