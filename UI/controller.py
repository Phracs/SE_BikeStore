from UI.view import View
from database.dao import DAO
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        category=int(self._view.dd_category.value)
        data_inizio=self._view.dp1.value
        data_fine=self._view.dp2.value
        self._model.crea_grafo(category, data_inizio, data_fine)
        self._view.txt_risultato.controls.append(ft.Text(f"{self._model.grafo}"))
        for u, v, data in self._model.grafo.edges(data=True):
            vendite= data["weight"]
            self._view.txt_risultato.controls.append(ft.Text(f"{u} -> {v}, Num vendite: {vendite}"))
        self._view.update()





    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO
        self._view.txt_risultato.controls.clear()
        top5 = self._model.top_5()
        for n, score, somma_out, somma_in in top5:
            self._view.txt_risultato.controls.append(ft.Text(f"{n}| {score}"))
        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO

    def populate_dd(self, dd):
        lista_categories= DAO.get_categories()
        for c in lista_categories:
            dd.options.append(ft.dropdown.Option(key=str(c.id), text=c.category_name))


