import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

class DuasFiestras:
    def __init__(self):
        self.temporizacion = None
        builder = Gtk.Builder()
        builder.add_from_file("interfaceGladeDuasFiestras.glade")
        wndFiestraPrincipal = builder.get_object("wndFiestraPrincipal")

        sinais = { "on_wndFiestraPrincipal_destroy": Gtk.main_quit,

                   }
        builder.connect_signals(sinais)


    def on_wndFiestraPrincipal_destroy(self):
        Gtk.main_quit()


if __name__ == "__main__":
    DuasFiestras()
    Gtk.main()






























