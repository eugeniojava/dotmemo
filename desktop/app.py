import logging
import tkinter as tk
from tkinter import messagebox

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
KEY_VALUE_STRING_SEPARATOR = "="


def format_key_value(key, value) -> str:
    return f"{key}{KEY_VALUE_STRING_SEPARATOR}{value}"


def create_master(title) -> tk.Tk:
    master = tk.Tk()
    master.title(title)
    # master.geometry("300x400")
    master.resizable(False, False)
    master.option_add("*font", "Consolas 12")
    return master


def create_key_label_and_entry(master) -> (tk.Entry, tk.Label):
    key_label = tk.Label(master, text="Key:")
    key_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    key_entry = tk.Entry(master)
    key_entry.grid(row=0, column=1, padx=5, pady=5)
    return key_label, key_entry


def create_value_label_and_entry(master) -> (tk.Entry, tk.Label):
    value_label = tk.Label(master, text="Value:")
    value_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    value_entry = tk.Entry(master)
    value_entry.grid(row=1, column=1, padx=5, pady=5)
    return value_label, value_entry


def create_add_button(master, add_key_value):
    add_button = tk.Button(master, text="Add", command=add_key_value)
    add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")


def create_filter_label_and_entry(master) -> (tk.Entry, tk.Label):
    filter_label = tk.Label(master, text="Filter:")
    filter_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    filter_entry = tk.Entry(master)
    filter_entry.grid(row=3, column=1, padx=5, pady=5, sticky="we")
    return filter_label, filter_entry


class App:
    def __init__(self, title):
        self.master = create_master(title)
        self.key_label, self.key_entry = create_key_label_and_entry(self.master)
        self.value_label, self.value_entry = create_value_label_and_entry(self.master)
        create_add_button(self.master, self.add_key_value)
        self.filter_label, self.filter_entry = create_filter_label_and_entry(self.master)
        self.data_map = {"password": "123456", "secret": "qwerty"}
        self.shown_data = tk.StringVar()
        self.shown_data.set([format_key_value(key, value) for key, value in self.data_map.items()])
        self.right_click_menu = tk.Menu(self.master, tearoff=False)
        self.right_click_menu.add_command(label="Copy key", command=self.copy_selected_key_from_listbox)
        self.right_click_menu.add_command(label="Copy value", command=self.copy_selected_value_from_listbox)
        self.right_click_menu.add_command(label="Copy key and value",
                                          command=self.copy_selected_key_and_value_from_listbox)
        self.data_listbox = tk.Listbox(self.master, listvariable=self.shown_data)
        self.data_listbox_scrollbar = tk.Scrollbar(self.master)
        self.data_listbox.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.data_listbox.bind("<Button-3>", self.handle_right_click)
        self.filter_entry.bind("<KeyRelease>", self.handle_key_release_event)

    def init(self):
        self.master.mainloop()

    def add_key_value(self):
        key = self.key_entry.get().strip()
        value = self.value_entry.get().strip()
        if key and len(key) > 0:
            if key in self.data_map:
                logger.info(f"Key '{key}' already exists")
                messagebox.showerror("Error", f"Key '{key}' already exists")
                self.key_entry.focus_set()
                return
            if value and len(value) > 0:
                self.data_map[key] = value
                logger.info(f"Added '{key}: {value}'")
                self.key_entry.delete(0, tk.END)
                self.value_entry.delete(0, tk.END)
                self.key_entry.focus_set()
                self.update_filtered_data()

    def update_filtered_data(self):
        to_filter_text = self.filter_entry.get().lower()
        filtered_data = [
            format_key_value(key, value) for key, value in self.data_map.items()
            if to_filter_text in key.lower()
        ]
        logger.info(f"Filtered '{'\', \''.join(filtered_data)}'")
        self.shown_data.set(filtered_data)

    def handle_key_release_event(self, event):
        self.update_filtered_data()

    def handle_right_click(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)

    def copy_selected_key_from_listbox(self):
        selected_item = self.data_listbox.get(self.data_listbox.curselection())
        logger.info(f"Selected '{selected_item}'")
        key = selected_item.split(KEY_VALUE_STRING_SEPARATOR)[0]
        self.master.clipboard_clear()
        self.master.clipboard_append(selected_item)
        logger.info(f"Key '{key}' copied to clipboard")

    def copy_selected_value_from_listbox(self):
        selected_item = self.data_listbox.get(self.data_listbox.curselection())
        logger.info(f"Selected '{selected_item}'")
        value = selected_item.split(KEY_VALUE_STRING_SEPARATOR)[1]
        self.master.clipboard_clear()
        self.master.clipboard_append(selected_item)
        logger.info(f"Value '{value}' copied to clipboard")

    def copy_selected_key_and_value_from_listbox(self):
        selected_item = self.data_listbox.get(self.data_listbox.curselection())
        logger.info(f"Selected '{selected_item}'")
        self.master.clipboard_clear()
        self.master.clipboard_append(selected_item)
        logger.info(f"Key and value '{selected_item}' copied to clipboard")
