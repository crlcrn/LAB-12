import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):

        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(f'{i}'))

        nazione = DAO.getAllNation()
        for n in nazione:
            self._view.ddcountry.options.append(ft.dropdown.Option(f'{n}'))

        self._view.update_page()


    def handle_graph(self, e):

        year = self._view.ddyear.value
        country = self._view.ddcountry.value

        self._model.build_graph(year, country)

        Nnodes, Nedges = self._model.getDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {Nnodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {Nedges}"))
        self._view.update_page()

    def handle_volume(self, e):
        self._view.txt_result.controls.clear()

        volume = self._model.get_volume_vendita()

        self._view.txt_result.controls.append(ft.Text("Volume di vendita per retailer:"))

        for coppia in volume:
            retailer = coppia[0]
            valore = coppia[1]

            self._view.txt_result.controls.append(
                ft.Text(f"{retailer.Retailer_name}: {valore}")
            )

        self._view.update_page()

    def handle_path(self, e):
        N = int(self._view.txtN.value)
        percorso, peso_totale = self._model.trova_ciclo_massimo(N)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Peso totale ciclo: {peso_totale}"))

        for i in range(len(percorso) - 1):
            r1 = percorso[i]
            r2 = percorso[i + 1]
            peso_arco = self._model._grafo[r1][r2]['weight']
            self._view.txt_result.controls.append(
                ft.Text(f"{r1.Retailer_name} —> {r2.Retailer_name} : {peso_arco}")
            )

        self._view.update_page()
