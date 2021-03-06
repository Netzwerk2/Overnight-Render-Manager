import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from typing import List, Optional, Union


class NumberEntry(Gtk.Entry):
    def __init__(self, min_number: Optional[int] = None):
        Gtk.Entry.__init__(self)
        self.min_number = min_number
        self.connect("changed", self.on_changed)

    def on_changed(self, *args) -> None:
        text = self.get_text().strip()
        self.set_text("".join([i for i in text if i in "0123456789"]))
        if self.min_number is not None:
            if text == "":
                text = str(self.min_number)
            if int(text) != 0 and int(text) < self.min_number:
                self.set_text(str(self.min_number))


def create_label(text: str) -> Gtk.Label:
    label = Gtk.Label(label=text)
    label.set_halign(Gtk.Align.START)
    return label


def create_entry(
    numbers_only: bool = True, min_number: Optional[int] = None
) -> Union[NumberEntry, Gtk.Entry]:
    if numbers_only:
        entry = NumberEntry(min_number)
    else:
        entry = Gtk.Entry()
    entry.set_width_chars(42)
    return entry


def create_file_chooser_button(
        self, dialog_title, action: Gtk.FileChooserAction,
    button: Gtk.ButtonsType, filter_blend: bool
) -> Gtk.FileChooserButton:
    file_chooser_dialog = create_file_chooser_dialog(
        self, dialog_title, action, button
    )
    if filter_blend:
        add_blend_filters(file_chooser_dialog)
    return Gtk.FileChooserButton(dialog=file_chooser_dialog)


def create_file_chooser_dialog(
        self, title: str, action: Gtk.FileChooserAction, button: Gtk.ButtonsType
) -> Gtk.FileChooserDialog:
    file_chooser_dialog = Gtk.FileChooserDialog(
        title,
        self,
        action,
        (
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            button,
            Gtk.ResponseType.OK
        )
    )
    return file_chooser_dialog


def add_blend_filters(dialog: Gtk.FileChooserDialog) -> None:
    filter_blend = Gtk.FileFilter()
    filter_blend.set_name(".blend files")
    filter_blend.add_pattern("*.blend")
    filter_blend.add_pattern("*.blend1")
    dialog.add_filter(filter_blend)


def create_combo_box(
    model: Optional[Gtk.TreeModel] = None, labels: Optional[List[str]] = None
) -> Gtk.ComboBox:
    if model is None:
        model = Gtk.ListStore(str)
    if labels is not None:
        for i in range(len(labels)):
            model.append([labels[i]])
    combo_box = Gtk.ComboBox.new_with_model(model)
    renderer_text = Gtk.CellRendererText()
    combo_box.pack_start(renderer_text, True)
    combo_box.add_attribute(renderer_text, "text", 0)
    combo_box.set_active(0)
    return combo_box


def create_check_button() -> Gtk.CheckButton:
    check_button = Gtk.CheckButton()
    return check_button


def create_tree_view(model: Gtk.ListStore, columns: List[str]) -> Gtk.TreeView:
    tree_view = Gtk.TreeView(model=model)
    for i, column in enumerate(columns):
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn(column, renderer_text, text=i)
        tree_view.append_column(column_text)
    return tree_view
