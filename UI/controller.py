import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        nazioni = self._model.nazioni()
        for i in nazioni:
            self._view.ddcountry.options.append(ft.dropdown.Option(i))
        for i in range(2015,2019):
            self._view.ddyear.options.append(ft.dropdown.Option(str(i)))
        self._view.update_page()


    def handle_graph(self, e):
        if self._view.ddyear.value is None:
            self._view.create_alert('Inserire anno')
            return
        if self._view.ddcountry.value is None:
            self._view.create_alert('Inserire nazione')
            return
        anno = (self._view.ddyear.value)
        self._model.creagrafo(self._view.ddcountry.value)
        self._model.connessioni(self._view.ddcountry.value,anno)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'Grafico creato correttamente'))
        self._view.txt_result.controls.append(ft.Text(f'Nodi: {self._model.getnodi()}'))
        self._view.txt_result.controls.append(ft.Text(f'Archi: {self._model.getarchi()}'))
        self._view.btn_volume.disabled=False

        self._view.update_page()




    def handle_volume(self, e):
        lista = self._model.volumi()
        self._view.txt_result.controls.clear()
        for riv,peso in lista:
            self._view.txtOut2.controls.append(ft.Text(f'{riv} --> {peso}'))

        self._view.update_page()


    def handle_path(self, e):
        if self._view.txtN.value == '':
            self._view.create_alert('inserire lunghezza')
            return
        try:
            lunghezza = int(self._view.txtN.value)
            if lunghezza<2:
                self._view.create_alert('lunghezza troppo corta')
                return
            luis,peso=self._model.percorso(lunghezza)
            self._view.txtOut3.controls.append(ft.Text(f'Costo del percorso: {peso}'))
            for i in range(0,len(luis)-1):
                self._view.txtOut3.controls.append(ft.Text(f'{luis[i]} --> {luis[i+1]}'))
            self._view.update_page()

        except ValueError:
            self._view.create_alert('Inserire un numero')
