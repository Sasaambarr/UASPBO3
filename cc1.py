import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import mysql.connector

class CatatanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catatanku")
        self.root.configure(bg="#FFB6C1")
        self.aplikasi_dimulai = False
        self.tampilkan_tombol_mulai()
        self.entri_cari_tanggal = None
        self.tombol_cari = None
        self.inisialisasi_tombol_cari()
        

    def tampilkan_tombol_mulai(self):
        tombol_mulai = tk.Button(self.root, text="Mulai", command=self.mulai_aplikasi, bg="#FFE4E1", fg="black", font=("Arial", 16))
        tombol_mulai.config(height=1, width=15, padx=25, pady=10)
        self.root.geometry("600x400")

        lebar_jendela = self.root.winfo_reqwidth()
        tinggi_jendela = self.root.winfo_reqheight()
        x = (lebar_jendela - tombol_mulai.winfo_reqwidth()) / 8
        y = (tinggi_jendela - tombol_mulai.winfo_reqheight()) / 8
        tombol_mulai.place(x=x, y=y)
        tombol_mulai.pack(pady=150)

    def mulai_aplikasi(self):
        if not self.aplikasi_dimulai:
            self.aplikasi_dimulai = True
            self.root.pack_slaves()[0].destroy()
            self.tampilkan_selamat_datang()

    def tampilkan_selamat_datang(self):
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Selamat Mencatat")
        welcome_window.configure(bg="#FFB6C1")
        welcome_label = tk.Label(welcome_window, text="Hai Selamat Datang di Aplikasi Catatanku!", bg="#FFB6C1", fg="black", font=("Arial", 20))
        welcome_label.pack(padx=20, pady=50)
        close_button = tk.Button(welcome_window, text="Mulai Catat", command=lambda: [welcome_window.destroy(), self.tampilkan_halaman_catatan()], bg="#FFE4E1", fg="black")
        close_button.pack(pady=20)

    def tampilkan_halaman_catatan(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Tanggal", "Judul", "Isi"), show="headings", style="Custom.Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tanggal", text="Tanggal")
        self.tree.heading("Judul", text="Judul")
        self.tree.heading("Isi", text="Isi")
        self.tree.pack(padx=10, pady=10)

        self.root.style = ttk.Style()
        self.root.style.theme_use("default")
        self.root.style.map("Custom.Treeview", background=[("selected", "#007ACC")])
        self.root.style.configure("Custom.Treeview", background="#FFFFFF", foreground="#000000", font=("Arial", 10))
        self.tree.tag_configure('Tanggal', background='#964B00')
        self.tree.tag_configure('Judul', background='#B22222')

        frame_tombol = tk.Frame(self.root, bg="#FFB6C1")
        frame_tombol.pack()
        tombol_tambah = tk.Button(frame_tombol, text="Tambah Catatan", command=self.tambah_catatan_gui, bg="#FFE4E1", fg="black")
        tombol_tambah.pack(side=tk.LEFT, padx=5, pady=10)
        tombol_buka = tk.Button(frame_tombol, text="Buka Catatan", command=self.buka_catatan, bg="#FFE4E1", fg="black")
        tombol_buka.pack(side=tk.LEFT, padx=5, pady=10)
        tombol_hapus = tk.Button(frame_tombol, text="Hapus Catatan", command=self.hapus_catatan, bg="#FFE4E1", fg="black")
        tombol_hapus.pack(side=tk.LEFT, padx=5, pady=10)
        tombol_arsip = tk.Button(frame_tombol, text="Arsipkan Catatan", command=self.arsipkan_catatan, bg="#FFE4E1", fg="black")
        tombol_arsip.pack(side=tk.LEFT, padx=5, pady=10)
        tombol_buka_arsip = tk.Button(frame_tombol, text="Buka Arsip", command=self.buka_arsip, bg="#FFE4E1", fg="black")
        tombol_buka_arsip.pack(side=tk.LEFT, padx=5, pady=10)
        tombol_edit = tk.Button(frame_tombol, text="Edit Catatan", command=self.edit_catatan_gui, bg="#FFE4E1", fg="black")
        tombol_edit.pack(side=tk.LEFT, padx=5, pady=10)

        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='apk_catatan'
            )
            self.cursor = self.conn.cursor()
            print("Connected to MySQL")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        self.tampilkan_catatan_dari_database()

    def tampilkan_catatan_dari_database(self):
        query = "SELECT id, tanggal, judul, isi FROM catatan"
        self.cursor.execute(query)
        hasil_query = self.cursor.fetchall()

        for catatan in hasil_query:
            self.tree.insert("", "end", values=catatan)

    def tambah_catatan(self, judul, isi):
        tanggal_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO catatan (tanggal, judul, isi) VALUES (%s, %s, %s)"
        values = (tanggal_sekarang, judul, isi)
        self.cursor.execute(query, values)
        self.conn.commit()

        id_catatan_baru = self.cursor.lastrowid

        self.tree.insert("", "end", values=(id_catatan_baru, tanggal_sekarang, judul, isi))

    def tambah_catatan_gui(self):
        jendela_tambah = tk.Toplevel(self.root)
        jendela_tambah.title("Tambah Catatan")
        jendela_tambah.configure(bg="#FFB6C1")

        label_judul = tk.Label(jendela_tambah, text="Judul:", bg="#FFB6C1", fg="black")
        label_judul.grid(row=0, column=0, padx=20, pady=10)
        entri_judul = tk.Entry(jendela_tambah)
        entri_judul.grid(row=0, column=1, padx=20, pady=5)
        label_isi = tk.Label(jendela_tambah, text="Isi:", bg="#FFB6C1", fg="black")
        label_isi.grid(row=1, column=0, padx=10, pady=5)
        entri_isi = scrolledtext.ScrolledText(jendela_tambah, wrap=tk.WORD, width=30, height=10)
        entri_isi.grid(row=1, column=1, padx=10, pady=5)

        tombol_simpan = tk.Button(jendela_tambah, text="Simpan", command=lambda: self.simpan_catatan(entri_judul.get(), entri_isi.get("1.0", tk.END), jendela_tambah), bg="#FFE4E1", fg="black")
        tombol_simpan.grid(row=2, columnspan=2, pady=10)

    def simpan_catatan(self, judul, isi, jendela):
        self.tambah_catatan(judul, isi)
        jendela.destroy()

    def hapus_catatan(self):
        item_terpilih = self.tree.selection()

        for item in item_terpilih:
            id_catatan = self.tree.item(item, "values")[0]
            self.tree.delete(item)
            self.hapus_catatan_dari_database(id_catatan)

    def hapus_catatan_dari_database(self, id_catatan):
        query = "DELETE FROM catatan WHERE id = %s"
        self.cursor.execute(query, (id_catatan,))
        self.conn.commit()

    def buka_catatan(self):
        item_terpilih = self.tree.selection()

        if item_terpilih:
            item = self.tree.item(item_terpilih)
            id_catatan, tanggal, judul, isi = item["values"]
            jendela_buka = tk.Toplevel(self.root)
            jendela_buka.title(f"Buka Catatan - {judul}")
            jendela_buka.configure(bg="#FFB6C1")

            label_tanggal = tk.Label(jendela_buka, text=f"Tanggal: {tanggal}")
            label_tanggal.pack(pady=5)
            label_judul = tk.Label(jendela_buka, text=f"Judul: {judul}")
            label_judul.pack(pady=5)
            label_isi = tk.Label(jendela_buka, text="Isi:")
            label_isi.pack(pady=5)

            text_isi = scrolledtext.ScrolledText(jendela_buka, wrap=tk.WORD, width=30, height=10)
            text_isi.insert(tk.END, isi)
            text_isi.pack(pady=10)

    def edit_catatan_gui(self):
        item_terpilih = self.tree.selection()

        if item_terpilih:
            item = self.tree.item(item_terpilih)
            id_catatan, tanggal, judul, isi = item["values"]
            self.catatan_terpilih = {
                "item_terpilih": item_terpilih,
                "id_catatan": id_catatan,
                "tanggal": tanggal,
                "judul": judul,
                "isi": isi
            }
            jendela_edit = tk.Toplevel(self.root)
            jendela_edit.title("Edit Catatan")
            jendela_edit.configure(bg="#FFB6C1")

            label_judul = tk.Label(jendela_edit, text="Judul:", bg="#FFB6C1", fg="black")
            label_judul.grid(row=0, column=0, padx=10, pady=5)
            entri_judul = tk.Entry(jendela_edit)
            entri_judul.grid(row=0, column=1, padx=10, pady=5)
            entri_judul.insert(tk.END, self.catatan_terpilih["judul"])

            label_isi = tk.Label(jendela_edit, text="Isi:", bg="#FFB6C1", fg="black")
            label_isi.grid(row=1, column=0, padx=10, pady=5)
            entri_isi = scrolledtext.ScrolledText(jendela_edit, wrap=tk.WORD, width=30, height=10)
            entri_isi.grid(row=1, column=1, padx=10, pady=5)
            entri_isi.insert(tk.END, self.catatan_terpilih["isi"])

            tombol_simpan = tk.Button(jendela_edit, text="Simpan Perubahan", command=lambda: self.simpan_perubahan_catatan(entri_judul.get(), entri_isi.get("1.0", tk.END), jendela_edit), bg="#FFE4E1", fg="black")
            tombol_simpan.grid(row=2, columnspan=2, pady=10)

    def simpan_perubahan_catatan(self, judul, isi, jendela):
        id_catatan = self.catatan_terpilih["id_catatan"]
        self.tree.item(self.catatan_terpilih["item_terpilih"], values=(id_catatan, self.catatan_terpilih["tanggal"], judul, isi))
        self.catatan_terpilih = None

        query = "UPDATE catatan SET judul = %s, isi = %s WHERE id = %s"
        values = (judul, isi, id_catatan)
        self.cursor.execute(query, values)
        self.conn.commit()

        jendela.destroy()

    def arsipkan_catatan(self):
        item_terpilih = self.tree.selection()

        if item_terpilih:
            item = self.tree.item(item_terpilih)
            id_catatan, tanggal, judul, isi = item["values"]
            arsip_data = (id_catatan, tanggal, judul, isi)

            if not hasattr(self, 'arsip'):
                self.arsip = []
            self.arsip.append(arsip_data)
            self.tree.delete(item_terpilih)

            self.arsipkan_catatan_dari_database(id_catatan)

    def arsipkan_catatan_dari_database(self, id_catatan):
        query = "INSERT INTO arsip (id_catatan) VALUES (%s)"
        self.cursor.execute(query, (id_catatan,))
        self.conn.commit()

    def buka_arsip(self):
        if hasattr(self, 'arsip') and self.arsip:
            jendela_arsip = tk.Toplevel(self.root)
            jendela_arsip.title("Arsip Catatan")
            jendela_arsip.configure(bg="#FFB6C1")

            tree_arsip = ttk.Treeview(jendela_arsip, columns=("ID", "Tanggal", "Judul", "Isi"), show="headings")
            tree_arsip.heading("ID", text="ID")
            tree_arsip.heading("Tanggal", text="Tanggal")
            tree_arsip.heading("Judul", text="Judul")
            tree_arsip.heading("Isi", text="Isi")
            tree_arsip.pack(padx=10, pady=10)

            for arsip_data in self.arsip:
                tree_arsip.insert("", "end", values=arsip_data)

            tombol_kembalikan = tk.Button(jendela_arsip, text="Kembalikan", command=self.buka_dan_kembalikan, bg="#FFE4E1", fg="black")
            tombol_kembalikan.pack(pady=10)

            tree_arsip.bind("<Double-1>", self.buka_dan_kembalikan)

    def buka_dan_kembalikan(self, event=None):
        item_terpilih = self.tree.selection()

        if item_terpilih:
            item = self.tree.item(item_terpilih)
        id_catatan, tanggal, judul, isi = item["values"]

        # Periksa apakah item yang dipilih berasal dari arsip
        if hasattr(self, 'arsip'):
            for arsip_data in self.arsip:
                if arsip_data[0] == id_catatan:
                    self.tree.insert("", "end", values=arsip_data)
                    self.arsip.remove(arsip_data)
                    self.kembalikan_catatan_dari_database(id_catatan)
                    return

    def kembalikan_catatan_dari_database(self, id_catatan):
        query = "DELETE FROM arsip WHERE id_catatan = %s"
        try:
            self.cursor.execute(query, (id_catatan,))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def inisialisasi_tombol_cari(self):
        frame_cari = tk.Frame(self.root, bg="#FFB6C1")
        frame_cari.pack()

        label_cari_tanggal = tk.Label(frame_cari, text="Cari :", bg="#FFB6C1", fg="black")
        label_cari_tanggal.pack(side=tk.LEFT, padx=5, pady=10)

        self.entri_cari_tanggal = tk.Entry(frame_cari)
        self.entri_cari_tanggal.pack(side=tk.LEFT, padx=5, pady=10)

        self.tombol_cari = tk.Button(frame_cari, text="Cari", command=self.cari_catatan_tanggal, bg="#FFE4E1", fg="black")
        self.tombol_cari.pack(side=tk.LEFT, padx=5, pady=10)

    def cari_catatan_tanggal(self):
        tanggal_cari = self.entri_cari_tanggal.get()

        if tanggal_cari:
            query = "SELECT id, tanggal, judul, isi FROM catatan WHERE tanggal LIKE %s"
            self.cursor.execute(query, (f"%{tanggal_cari}%",))
            hasil_query = self.cursor.fetchall()

            # Bersihkan tree sebelum menampilkan hasil pencarian
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Tampilkan hasil pencarian
            for catatan in hasil_query:
                self.tree.insert("", "end", values=catatan)

if __name__ == "__main__":
    root = tk.Tk()
    app = CatatanApp(root)
    root.mainloop()