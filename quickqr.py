
import sys
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import io
import getpass
import platform

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class QRCodeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QuickQR Generator")
        self.geometry("500x620")
        self.iconbitmap(resource_path("icon.ico"))

        self.fg_color = "#000000"
        self.bg_color = "#ffffff"
        self.preview_visible = False

        self.default_save_path = self.get_default_save_path()
        os.makedirs(self.default_save_path, exist_ok=True)

        self.build_ui()

    def get_default_save_path(self):
        user = getpass.getuser()
        if platform.system() == "Windows":
            return os.path.join("C:/Users", user, "Documents", "QuickQR")
        else:
            return os.path.expanduser("~/Documents/QuickQR")

    def build_ui(self):
        def label(text):
            return ctk.CTkLabel(self, text=text, text_color="white", font=("Arial", 11, "bold"))

        label("Data to encode:").pack(pady=(15, 0))
        self.data_entry = ctk.CTkEntry(self, placeholder_text="e.g., https://...", width=400)
        self.data_entry.pack(pady=5)

        label("Filename (e.g., qr.png):").pack(pady=(15, 0))
        self.filename_entry = ctk.CTkEntry(self, placeholder_text="qr.png", width=400)
        self.filename_entry.pack(pady=5)

        label("Save Location:").pack(pady=(15, 0))
        path_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.path_entry = ctk.CTkEntry(path_frame, width=280)
        self.path_entry.insert(0, self.default_save_path)
        browse_btn = ctk.CTkButton(path_frame, text="Browse", command=self.browse_folder, width=100, fg_color="#f8b400", text_color="black")
        self.path_entry.pack(side="left", padx=5)
        browse_btn.pack(side="left")
        path_frame.pack(pady=5)

        label("Colors:").pack(pady=(15, 0))
        color_frame = ctk.CTkFrame(self)
        color_frame.pack(pady=5)

        self.fg_display = ctk.CTkLabel(color_frame, text="Pattern", text_color=self.fg_color)
        self.bg_display = ctk.CTkLabel(color_frame, text="Background", text_color=self.bg_color)

        fg_btn = ctk.CTkButton(color_frame, text="Pattern Color", command=self.pick_fg, fg_color="#f8b400", text_color="black")
        bg_btn = ctk.CTkButton(color_frame, text="Background Color", command=self.pick_bg, fg_color="#f8b400", text_color="black")

        fg_btn.grid(row=0, column=0, padx=10)
        self.fg_display.grid(row=0, column=1, padx=5)
        bg_btn.grid(row=1, column=0, padx=10, pady=5)
        self.bg_display.grid(row=1, column=1, padx=5)

        self.qr_canvas = ctk.CTkLabel(self, text="")
        self.qr_canvas.pack(pady=10)
        self.qr_canvas.pack_forget()

        generate_btn = ctk.CTkButton(self, text="Generate & Save QR", command=self.generate_qr, fg_color="#f8b400", text_color="black", width=250)
        generate_btn.pack(pady=20)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def pick_fg(self):
        from tkinter.colorchooser import askcolor
        color = askcolor(title="Pick pattern color")[1]
        if color and color != self.bg_color:
            self.fg_color = color
            self.fg_display.configure(text_color=color)
            self.update_preview()

    def pick_bg(self):
        from tkinter.colorchooser import askcolor
        color = askcolor(title="Pick background color")[1]
        if color and color != self.fg_color:
            self.bg_color = color
            self.bg_display.configure(text_color=color)
            self.update_preview()

    def generate_qr_img(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color=self.fg_color, back_color=self.bg_color)

    def update_preview(self):
        data = self.data_entry.get()
        if not data:
            return
        img = self.generate_qr_img(data)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        preview_img = Image.open(buffer).resize((200, 200))
        tk_img = ImageTk.PhotoImage(preview_img)
        self.qr_canvas.configure(image=tk_img)
        self.qr_canvas.image = tk_img
        if not self.preview_visible:
            self.qr_canvas.pack(pady=10)
            self.preview_visible = True

    def generate_qr(self):
        data = self.data_entry.get()
        filename = self.filename_entry.get().strip()
        path = self.path_entry.get().strip()

        if not data or not filename or not path:
            messagebox.showerror("Error", "All fields are required.")
            return
        if self.bg_color == self.fg_color:
            messagebox.showerror("Error", "Background and pattern colors cannot be the same.")
            return

        img = self.generate_qr_img(data)

        os.makedirs(path, exist_ok=True)
        if not filename.endswith(".png"):
            filename += ".png"
        save_path = os.path.join(path, filename)

        img.save(save_path)
        self.update_preview()
        messagebox.showinfo("Saved", f"QR Code saved at:\n{save_path}")

if __name__ == "__main__":
    app = QRCodeApp()
    app.mainloop()
