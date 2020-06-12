import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import os
import time

from widgets import create_label, create_entry, create_button, \
create_file_chooser_dialog, create_combo_box, create_check_button

class MainWindow(Gtk.Window):
    grid = Gtk.Grid(column_spacing=12, row_spacing=12)

    location_entry = None
    output_type_combo_box = None
    shutdown_check_button = None

    location = ""
    output_type = ""
    shutdown = False


    def __init__(self):
        super(MainWindow, self).__init__()
        self.set_default_size(600, 800)
        self.set_title("Blender Overnight Renderer")
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.create_content()

    def create_content(self) -> None:
        location_label = create_label("Path to .blend file")
        self.location_entry = create_entry(False)
        self.location_entry.set_width_chars(30)
        location_button = create_button("Browse")
        location_button.connect("clicked", self.on_location_clicked)

        output_type_label = create_label("Choose an output type")
        output_types = ["Animation", "Single Frame"]
        self.output_type_combo_box = create_combo_box(output_types)

        shutdown_label = create_label("Shutdown after rendering is finished")
        self.shutdown_check_button = create_check_button()

        render_button = create_button("Render")
        render_button.connect("clicked", self.on_render_clicked)

        self.add(self.grid)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_valign(Gtk.Align.CENTER)
        self.grid.attach(location_label, 0, 0, 1, 1)
        self.grid.attach(self.location_entry, 1, 0, 1, 1)
        self.grid.attach(location_button, 2, 0, 1, 1)
        self.grid.attach(output_type_label, 0, 1, 1, 1)
        self.grid.attach(self.output_type_combo_box, 1, 1, 1, 1)
        self.grid.attach(shutdown_label, 0, 2, 1, 1)
        self.grid.attach(self.shutdown_check_button, 1, 2, 1, 1)
        self.grid.attach(render_button, 0, 3, 2, 1)

    def on_location_clicked(self, button: Gtk.Button) -> None:
        file_chooser_dialog = create_file_chooser_dialog(self)

        self.add_filters(file_chooser_dialog)

        response = file_chooser_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.location_entry.set_text(file_chooser_dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            pass

        file_chooser_dialog.destroy()

    def add_filters(self, dialog: Gtk.FileChooserDialog) -> None:
        filter_blend = Gtk.FileFilter()
        filter_blend.set_name(".blend files")
        filter_blend.add_pattern("*.blend")
        filter_blend.add_pattern("*.blend1")
        dialog.add_filter(filter_blend)

    def on_render_clicked(self, button: Gtk.Button) -> None:
        self.location = self.location_entry.get_text()
        output_type_iter = self.output_type_combo_box.get_active_iter()
        if output_type_iter is not None:
            model = self.output_type_combo_box.get_model()
            self.output_type = model[output_type_iter][0]
        self.shutdown = self.shutdown_check_button.get_active()
        self.render()

    def render(self) -> None:
        os.chdir(os.path.dirname(self.location))
        if self.output_type == "Animation":
            print("Rendering animation of {}".format(self.location))
            os.system("blender -b {} -a".format(os.path.basename(self.location)))
        elif self.output_type == "Single Frame":
            print("Rendering frame 1 of {}".format(self.location))
            os.system("blender -b {} -f 1".format(os.path.basename(self.location)))

        print("Rendering complete!")
        if self.shutdown:
            os.system("notify-send 'Rendering {} complete. Shutting down in 30 seconds'".format(self.location))
            time.sleep(30)
            print("Shutting down...")
            os.system("poweroff")
        else:
            os.system("notify-send 'Rendering {} complete.'".format(self.location))


main_window = MainWindow()
main_window.connect("delete-event", Gtk.main_quit)
main_window.show_all()
Gtk.main()
