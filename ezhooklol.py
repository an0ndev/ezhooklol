import tkinter, tkinter.messagebox
from typing import Union, Optional, Dict

import requests

def post (*, base_webhook_url: str, title: Optional [str] = None, desc: Optional [str] = None, footer: Optional [str] = None, image_url: Optional [str] = None):
    embed = {}
    if title is not None: embed ["title"] = title
    if desc is not None: embed ["description"] = desc
    if footer is not None: embed ["footer"] = {"text": footer}
    if image_url is not None: embed ["image"] = {"url": image_url}
    resp = requests.post (base_webhook_url, params = {"wait": True}, json = {"embeds": [embed]})
    resp.raise_for_status ()

class HookUI:
    def __init__ (self):
        self.root = tkinter.Tk ()
        self.root.wm_title ("ezhooklol")

        self.url_label, self.url_box = self._make_label_and_entry ("Webhook URL", 0)
        self.title_label, self.title_box = self._make_label_and_entry ("Title", 1)
        self.desc_label, self.desc_box = self._make_label_and_entry ("Description", 2, True)
        self.footer_label, self.footer_box = self._make_label_and_entry ("Footer", 3)
        self.image_url_label, self.image_url_box = self._make_label_and_entry ("Image URL", 4)
        self.do_it_button = tkinter.Button (self.root, text = "do it", command = self._do_it)
        self.do_it_button.grid (row = 5, column = 0, columnspan = 2, sticky = "nesw")
    def run (self):
        self.root.mainloop ()
    def _make_label (self, text: str, row: int, col: int) -> tkinter.Label:
        new_label = tkinter.Label (self.root, text = text)
        new_label.grid (row = row, column = col, sticky = "nesw")
        return new_label
    def _make_entry (self, row: int, col: int, is_text: bool) -> Union [tkinter.Entry, tkinter.Text]:
        entry_class = tkinter.Text if is_text else tkinter.Entry
        new_entry = entry_class (self.root)
        new_entry.grid (row = row, column = col, sticky = "nesw")
        self.root.grid_rowconfigure (row, weight = 1)
        self.root.grid_columnconfigure (col, weight = 1)
        return new_entry
    def _make_label_and_entry (self, text: str, row: int, is_text: bool = False) -> (tkinter.Label, Union [tkinter.Entry, tkinter.Text]):
        return self._make_label (text = text, row = row, col = 0), self._make_entry (row = row, col = 1, is_text = is_text)
    @staticmethod
    def _get_values_from_boxes (*boxes: (str, Union [tkinter.Entry, tkinter.Text])) -> Dict [str, str]:
        values: Dict [str, str] = {}
        for box_name, box in boxes:
            value: Optional [str] = box.get ("1.0", tkinter.END) if isinstance (box, tkinter.Text) else box.get ()
            if value.strip () != "": values [box_name] = value
        return values
    def _do_it (self):
        values = self._get_values_from_boxes (("base_webhook_url", self.url_box), ("title", self.title_box), ("desc", self.desc_box), ("footer", self.footer_box), ("image_url", self.image_url_box))
        if "base_webhook_url" not in values:
            tkinter.messagebox.showerror ("ezhooklol", "you need a url bruh")
            return
        post (**values)

if __name__ == "__main__":
    HookUI ().run ()