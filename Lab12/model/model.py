import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodi = []
        self._idMap = {}

    def build_graph(self, year, country):
        self._grafo.clear()
        self._nodi = DAO.get_nodi(country)

        for r in self._nodi:
            self._idMap[r.Retailer_code] = r

        self._grafo.add_nodes_from(self._nodi)

        archi = DAO.get_archi(year, country)
        for g1, g2, peso in archi:
            self._grafo.add_edge(self._idMap[g1], self._idMap[g2], weight = peso)


    def get_volume_vendita(self):

        risultati = []

        nodi = list(self._grafo.nodes)

        for nodo in nodi:
            somma = 0
            lista_archi = self._grafo.edges(nodo, data=True)

            for arco in lista_archi:
                nodo1 = arco[0]
                nodo2 = arco[1]
                attributi = arco[2]
                peso = attributi['weight']
                somma += peso

            risultati.append((nodo, somma))
        risultati.sort(key=lambda x:x[1], reverse=True)

        return risultati

    def trova_ciclo_massimo(self, N):
        self.best_path = []
        self.best_weight = 0

        for nodo in self._grafo.nodes:
            self._cerca([nodo], N, 0)

        return self.best_path, self.best_weight


    def _cerca(self, parziale, N, peso):

        if len(parziale) == N+1:
            if parziale[0] == parziale[-1] and peso > self.best_weight:
                self.best_weight = peso
                self.best_path = list(parziale)
            return


        ultimo = parziale[-1]

        for vicino in self._grafo.neighbors(ultimo):
            if vicino == parziale[0] and len(parziale) == N:
                self._cerca(parziale + [vicino], N, peso + self._grafo[ultimo][vicino]['weight'])
            elif vicino not in parziale:
                self._cerca(parziale + [vicino], N, peso + self._grafo[ultimo][vicino]['weight'])



    def getDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

