from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from rembg import remove

class BackgroundRemoverApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Removedor de Fundo de Imagem")
        self.master.geometry("800x600")
        
        self.original_image = None
        self.processed_image_pil = None

        # Estilos
        style = ttk.Style()
        style.configure("TButton", padding=10, font=("Arial", 12))
        
        # Frames
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=20)
        self.image_frame = tk.Frame(master)
        self.image_frame.pack(pady=20)
        self.action_frame = tk.Frame(master)
        self.action_frame.pack(pady=20)
        self.status_frame = tk.Frame(master)
        self.status_frame.pack(pady=20)
        
        # Widgets
        self.select_button = ttk.Button(self.input_frame, text="Selecionar Imagem", command=self.select_image)
        self.select_button.pack(side=tk.LEFT, padx=10)
        
        self.remove_button = ttk.Button(self.action_frame, text="Remover Fundo", command=self.remove_background, state=tk.DISABLED)
        self.remove_button.pack(side=tk.LEFT, padx=10)
        
        self.save_button = ttk.Button(self.action_frame, text="Salvar Imagem", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=10)
        
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()
        
        self.status_label = tk.Label(self.status_frame, text="")
        self.status_label.pack()

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.original_image = self.original_image.convert('RGB')  # Ensure it is in RGB format
            self.display_thumbnail(self.original_image)
            self.remove_button['state'] = 'normal'
            self.status_label.config(text="Imagem carregada com sucesso!")

    def display_thumbnail(self, image):
        thumbnail = image.copy()
        thumbnail.thumbnail((300, 300), Image.Resampling.LANCZOS)  # Updated resampling method
        display_image = ImageTk.PhotoImage(thumbnail)
        self.image_label.config(image=display_image)
        self.image_label.image = display_image  # Maintain reference

    def remove_background(self):
        if self.original_image:
            self.remove_button['state'] = 'disabled'
            with BytesIO() as input_io:
                self.original_image.save(input_io, format='PNG')
                input_io.seek(0)  # Reset the stream to start
                result_bytes = remove(input_io.read())

            self.processed_image_pil = Image.open(BytesIO(result_bytes))
            self.display_thumbnail(self.processed_image_pil)
            self.save_button['state'] = 'normal'
            self.status_label.config(text="Fundo removido!")
            self.remove_button['state'] = 'normal'

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.processed_image_pil.save(file_path)
            messagebox.showinfo("Sucesso", "Imagem salva com sucesso em: " + file_path)
            self.status_label.config(text="Imagem salva com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()

