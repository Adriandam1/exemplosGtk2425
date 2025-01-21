
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo con Gtk Grid")

        maia = Gtk.Grid()

        boton1 = Gtk.Button(label="Boton 1")
        boton2 = Gtk.Button(label="Boton 2")
        boton3 = Gtk.Button(label="Boton 3")
        boton4 = Gtk.Button(label="Boton 4")
        boton5 = Gtk.Button(label="Boton 5")
        boton6 = Gtk.Button(label="Boton 6")
        boton7 = Gtk.Button(label="Boton 7")
        boton8 = Gtk.Button(label="Boton 8")
        boton9 = Gtk.Button(label="Boton 9")
        boton10 = Gtk.Button(label="Boton 10")
        boton11 = Gtk.Button(label="Boton 11")
        boton12 = Gtk.Button(label="Boton 12")

        maia.add (boton1)
        maia.attach (boton2,left=1, top=0, width=2, height=1)
        maia.attach_next_to (boton3, boton1, Gtk.PositionType.BOTTOM,1, 2)
        maia.attach_next_to (boton4, boton2, Gtk.PositionType.BOTTOM, 2, 1)
        maia.attach_next_to (boton5, boton4, Gtk.PositionType.BOTTOM, 1,1)
        maia.attach_next_to (boton6, boton5, Gtk.PositionType.RIGHT, 1, 1)
        maia.attach_next_to (boton7, boton3, Gtk.PositionType.BOTTOM, 3, 1)
        maia.attach_next_to (boton8, boton7, Gtk.PositionType.BOTTOM, 2, 1)
        maia.attach_next_to (boton9, boton8, Gtk.PositionType.BOTTOM, 1, 1)
        maia.attach_next_to (boton10, boton9, Gtk.PositionType.RIGHT, 1, 1)
        maia.attach_next_to (boton11, boton9, Gtk.PositionType.BOTTOM, 2, 1)
        maia.attach_next_to (boton12, boton8, Gtk.PositionType.RIGHT, 1, 3)



        self.add(maia)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_btnSaudo_clicked (self, boton, cadroTexto, etiqueta):
        etiqueta.set_text("Ola " + cadroTexto.get_text())

    def on_txtSaudo_activated (self, cadroTexto, etiqueta):
        etiqueta.set_text("Ola " +cadroTexto.get_text())



if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()