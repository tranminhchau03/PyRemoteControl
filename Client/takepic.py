# takepic.py
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import ImageTk, Image
import io

#take screenshot
def take_picture(self, client):
    self.Screenshot = tk.Toplevel()
    self.Screenshot.title("PrintScreen")
    self.Screenshot.configure(bg="#FDF4F5")

    def receive_and_display_picture():
        try:
            client.sendall(bytes("TakePicture", "utf-8"))
        except:
            messagebox.showinfo("", "Lỗi kết nối ")
            return

        self.img_data = client.recv(40960000)  # Store the image data

        img = Image.open(io.BytesIO(self.img_data))  # Open image from data
        img = img.resize((850, 500))  # Resize the image
        img = ImageTk.PhotoImage(img)
        
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img  # Keep a reference to prevent garbage collection


    def save_picture():
        if self.img_data is None:
            messagebox.showinfo("", "Không có dữ liệu hình ảnh để lưu.")
            return

        try:
            fname = filedialog.asksaveasfilename(title=u'Lưu file', filetypes=[("PNG", ".png")])
            if fname.strip() != '':
                with open(fname + '.png', 'wb') as file:
                    file.write(self.img_data)
        except Exception as e:
            messagebox.showinfo("", "Lỗi khi lưu file: " + str(e))


    self.canvas = tk.Canvas(self.Screenshot, bg="white", width=850, height=500)
    self.canvas.grid(row=0, column=0, columnspan=2)  # Use columnspan to occupy both columns

    self.cap = tk.Button(self.Screenshot, text="Capture", bg="#FAF3F0", font="Helvetica 9 bold",
                         width=150, height=4, borderwidth=5, command=receive_and_display_picture,
                         bd=5, activebackground='#FFF3DA')
    self.cap.grid(row=1, column=0, padx=10, pady=10)  # Add padding for spacing

    # Empty label as a placeholder
    placeholder_label = tk.Label(self.Screenshot, text="", bg="#FDF4F5")
    placeholder_label.grid(row=1, column=1)

    self.Save = tk.Button(self.Screenshot, text="Save", bg="#FAF3F0", font="Helvetica 9 bold",
                          width=10, height=2, borderwidth=5, command=save_picture,
                          bd=5, activebackground='#FFF3DA')
    self.Save.grid(row=1, column=2, padx=10, pady=10)  # Add padding for spacing
