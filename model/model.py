import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        self.grafo=nx.DiGraph()
        self.dizionario_sales={}
        self.lista_sales=[]

    def get_date_range(self):
        return DAO.get_date_range()

    def crea_grafo(self, category_id, data_inizio, data_fine):
        self.grafo=nx.DiGraph()
        self.crea_nodi(category_id)
        self.get_sales(data_inizio, data_fine)

        """
        for product_id, num_vendite in self.lista_sales:
            nodo_u=self.dizionario_sales[product_id]
            nodo_v=self.dizionario_sales[product_id+1]
            peso=nodo_u.num_vendite+nodo_v.num_vendite
            if nodo_u.num_vendite > nodo_v.num_vendite:
                self.grafo.add_edge(nodo_u,nodo_v, weight=peso)
            elif nodo_v.num_vendite > nodo_u.num_vendite:
                self.grafo.add_edge(nodo_v,nodo_u, weight=peso)
        """
        sold_nodes = []
        for p in self.grafo.nodes:
            vendite = self.dizionario_sales.get(p.id, 0)
            if vendite > 0:
                sold_nodes.append(p)
        for i in range(len(sold_nodes)):
            for j in range(i+1, len(sold_nodes)):
                u=sold_nodes[i]
                v=sold_nodes[j]

                sales_u=self.dizionario_sales[u.id]
                sales_v=self.dizionario_sales[v.id]
                peso=sales_u+sales_v

                if sales_u>sales_v:
                    self.grafo.add_edge(u, v, weight=peso)
                elif sales_u<sales_v:
                    self.grafo.add_edge(v, u, weight=peso)
                elif sales_u==sales_v:
                    self.grafo.add_edge(u, v, weight=peso)
                    self.grafo.add_edge(v, u, weight=peso)


    def get_sales(self, data_inizio, data_fine):
        sales=DAO.read_sales(data_inizio, data_fine)
        self.lista_sales=sales
        for product_id, num_vendite in self.lista_sales:
            self.dizionario_sales[product_id]=num_vendite
        return self.lista_sales


    def crea_nodi(self, category_id):
        lista_nodi=DAO.get_nodes(category_id)
        for nodi in lista_nodi:
            self.grafo.add_node(nodi)

    def top_5(self):
        scores=[]
        for n in self.grafo.nodes:
            somma_out=sum(data["weight"] for u, v, data in self.grafo.out_edges(n, data=True))
            somma_in=sum(data["weight"] for u, v, data in self.grafo.in_edges(n, data=True))
            score=somma_out-somma_in
            scores.append((n, score, somma_out, somma_in))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:5]