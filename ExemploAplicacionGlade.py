import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

class Aplicacion:
    def __init__(self):
        self.temporizacion = None
        builder = Gtk.Builder()
        builder.add_from_file("interfaceGladeEntry.glade")
        wndFiestra = builder.get_object("wndFiestraPrincipal")
        self.txtTexto = builder.get_object("txtTexto")
        self.txtTexto.set_invisible_char("~")
        sinais = { "on_wndFiestraPrincipal_destroy": Gtk.main_quit,
                   "on_chkEditable_toggled": self.on_chkEditable_toggled,
                   "on_chkVisible_toggled": self.on_chkVisible_toggled,
                   "on_chkIcona_toggled": self.on_chkIcona_toggled,
                   "on_chkPulso_toggled": self.on_chkPulso_toggled
                   }
        builder.connect_signals(sinais)


    def on_wndFiestraPrincipal_destroy(self):
        Gtk.main_quit()

    def on_chkEditable_toggled(self, boton):
        pulsado = boton.get_active()

        self.txtTexto.set_editable(pulsado)

    def on_chkVisible_toggled(self, boton):
        self.txtTexto.set_visibility (boton.get_active())

    def on_chkIcona_toggled(self, boton):
        if boton.get_active():
            nome_icona = "system-search-symbolic"
        else:
            nome_icona = None
        self.txtTexto.set_icon_from_icon_name (Gtk.EntryIconPosition.PRIMARY, nome_icona)

    def on_chkPulso_toggled(self, boton):
        if boton.get_active():
            self.txtTexto.set_progress_pulse_step(0.2)
            self.temporizacion = GLib.timeout_add(300, self.do_pulso)

    def do_pulso(self):
        self.txtTexto.progress_pulse()
        return True

if __name__ == "__main__":
    Aplicacion()
    Gtk.main()






























