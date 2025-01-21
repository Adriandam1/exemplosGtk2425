from sys import orig_argv

import gi
from gi.repository.Gtk import Orientation

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ListBoxConDatos (Gtk.ListBoxRow):
    def __init__(self, dato):
        super().__init__()
        self.dato = dato
        self.add(Gtk.Label(label=dato))


class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo con Gtk ListBox")

        caixaP = Gtk.Box (orientation=Gtk.Orientation.VERTICAL, spacing=6)

        listBox = Gtk.ListBox()
        listBox.set_selection_mode(Gtk.SelectionMode.NONE)
        caixaP.pack_start(listBox,True, True,0)

        fila = Gtk.ListBoxRow()
        caixaH = Gtk.Box (orientation= Gtk.Orientation.HORIZONTAL, spacing = 50)
        fila.add(caixaH)
        caixaV = Gtk.Box (orientation = Gtk.Orientation.VERTICAL)
        caixaH.pack_start(caixaV, True, True, 0)

        lblEtiqueta1 = Gtk.Label ("Data e hora automática")
        lblEtiqueta2 = Gtk.Label ("Acceso a interrede")
        caixaV.pack_start(lblEtiqueta1, True, True, 0)
        caixaV.pack_start(lblEtiqueta2, True, True, 0)

        int = Gtk.Switch()
        int.props.valign = Gtk.Align.CENTER
        caixaH.pack_start(int, False, True, 0)
        listBox.add(fila)

        fila2 = Gtk.ListBoxRow()
        caixaH = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing= 50)
        fila2.add(caixaH)
        lblEtiqueta3 = Gtk.Label(label = "Permite actualización automática", xalign = 0)
        check = Gtk.CheckButton()
        caixaH.pack_start(lblEtiqueta3, True, True, 0)
        caixaH.pack_start(check, False, True, 0)
        listBox.add(fila2)

        listBox2 = Gtk.ListBox()
        elementos = "Unha frase longa para dividir".split()

        for palabra in elementos:
            listBox2.add(ListBoxConDatos(palabra))

        listBox2.set_sort_func(self.funcion_ordeacion)
        listBox2.set_filter_func(self.funcion_filtrado)
        listBox2.connect("row-activated", self.on_row_activated)
        caixaP.pack_start(listBox2, True, True, 0)


        self.add(caixaP)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_row_activated (self, listbox_widget, fila):
        print (fila.dato)

    def funcion_filtrado (self, fila):
        return False if fila.dato == "longa" else True

    def funcion_ordeacion (self, fila1, fila2):
        return fila1.dato.lower()<fila2.dato.lower()




if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()