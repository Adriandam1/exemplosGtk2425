
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo con Gtk Notebook")

        cartafol = Gtk.Notebook()

        paxina1 = Gtk.Box()
        paxina1.set_border_width(10)
        paxina1.add (Gtk.Label (label = "Páxina 1"))
        cartafol.append_page(paxina1, Gtk.Label ("Título pax1"))

        paxina2 = Gtk.Box()
        paxina2.set_border_width(10)
        paxina2.add(Gtk.Label ("Páxina con imaxe de título"))
        cartafol.append_page(
            paxina2, Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU))


        self.add(cartafol)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()