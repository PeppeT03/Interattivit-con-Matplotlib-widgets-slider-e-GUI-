# --------------------------------------------------
# IMPORTAZIONE DELLE LIBRERIE
# --------------------------------------------------
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib

# Impostiamo il backend per utilizzare Matplotlib dentro Tkinter
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --------------------------------------------------
# PREPARAZIONE DEI DATI
# --------------------------------------------------

# Generiamo 1000 punti tra 0 e 2π
t = np.linspace(0, 2*np.pi, 1000)


# --------------------------------------------------
# FUNZIONI PER GENERARE LE CURVE
# --------------------------------------------------

# Generiamo una curva sinusoidale
def make_sin(A, f):
    return A * np.sin(f * t)


# Generiamo una curva cosinusoidale
def make_cos(A, f):
    return A * np.cos(f * t)


# Generiamo una curva con rumore casuale
def make_noise(A, f):
    rng = np.random.default_rng(123)

    return A * (
        rng.normal(scale=0.5, size=t.shape)
        + 0.2*np.sin(f*t)
    )


# --------------------------------------------------
# CREAZIONE DELLA CLASSE PRINCIPALE
# --------------------------------------------------

class PlotApp:

    def __init__(self, root):

        # Conserviamo il riferimento alla finestra principale
        self.root = root

        # Impostiamo il titolo della finestra
        root.title("Plotter Tkinter")


        # --------------------------------------------------
        # CONTENITORE DEI CONTROLLI
        # --------------------------------------------------

        # Creiamo un contenitore nella parte superiore
        ctrl = ttk.Frame(root)

        # Posizioniamo il contenitore
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)


        # --------------------------------------------------
        # SLIDER AMPIEZZA
        # --------------------------------------------------

        # Etichetta dello slider
        ttk.Label(ctrl, text="Ampiezza").grid(
            row=0, column=0, sticky="w"
        )

        # Variabile che conserva l'ampiezza
        self.amp_var = tk.DoubleVar(value=1.0)

        # Creiamo lo slider
        amp_scale = ttk.Scale(
            ctrl,
            from_=0.0,
            to=2.0,
            orient="horizontal",
            variable=self.amp_var,
            command=lambda _: self.update_plot()
        )

        # Posizioniamo lo slider
        amp_scale.grid(
            row=0, column=1, sticky="ew", padx=5
        )


        # --------------------------------------------------
        # SLIDER FREQUENZA
        # --------------------------------------------------

        # Etichetta dello slider
        ttk.Label(ctrl, text="Frequenza").grid(
            row=1, column=0, sticky="w"
        )

        # Variabile che conserva la frequenza
        self.freq_var = tk.DoubleVar(value=1.0)

        # Creiamo lo slider
        freq_scale = ttk.Scale(
            ctrl,
            from_=0.1,
            to=5.0,
            orient="horizontal",
            variable=self.freq_var,
            command=lambda _: self.update_plot()
        )

        # Posizioniamo lo slider
        freq_scale.grid(
            row=1, column=1, sticky="ew", padx=5
        )


        # --------------------------------------------------
        # CHECKBOX PER LE CURVE
        # --------------------------------------------------

        # Creiamo un contenitore per le checkbox
        boxframe = ttk.Frame(ctrl)

        # Posizioniamo il contenitore accanto agli slider
        boxframe.grid(
            row=0, column=2, rowspan=2, padx=10
        )

        # Variabili che conservano lo stato delle checkbox
        self.show_sin = tk.IntVar(value=1)
        self.show_cos = tk.IntVar(value=0)
        self.show_noise = tk.IntVar(value=0)

        # Checkbox per il seno
        ttk.Checkbutton(
            boxframe,
            text="Sin",
            variable=self.show_sin,
            command=self.update_plot
        ).pack(anchor="w")

        # Checkbox per il coseno
        ttk.Checkbutton(
            boxframe,
            text="Cos",
            variable=self.show_cos,
            command=self.update_plot
        ).pack(anchor="w")

        # Checkbox per il rumore
        ttk.Checkbutton(
            boxframe,
            text="Noise",
            variable=self.show_noise,
            command=self.update_plot
        ).pack(anchor="w")


        # --------------------------------------------------
        # PULSANTI
        # --------------------------------------------------

        # Creiamo un contenitore per i pulsanti
        btnframe = ttk.Frame(ctrl)

        # Posizioniamo il contenitore
        btnframe.grid(
            row=0, column=3, rowspan=2, padx=5
        )

        # Pulsante Reset
        ttk.Button(
            btnframe,
            text="Reset",
            command=self.reset
        ).pack(fill="x", pady=2)

        # Pulsante Salva PNG
        ttk.Button(
            btnframe,
            text="Salva PNG",
            command=self.save_png
        ).pack(fill="x", pady=2)

        # Pulsante Esci
        ttk.Button(
            btnframe,
            text="Esci",
            command=root.quit
        ).pack(fill="x", pady=2)


        # --------------------------------------------------
        # CREAZIONE DEL GRAFICO
        # --------------------------------------------------

        # Creiamo una figura Matplotlib
        self.fig = Figure(figsize=(7, 3))

        # Creiamo gli assi del grafico
        self.ax = self.fig.add_subplot(111)

        # Inseriamo Matplotlib dentro la finestra Tkinter
        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=root
        )

        # Posizioniamo il grafico nella finestra
        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=1
        )

        # Creiamo un dizionario per conservare le linee
        self.lines = {}

        # Disegniamo il grafico iniziale
        self.update_plot()


    # --------------------------------------------------
    # FUNZIONE DI AGGIORNAMENTO DEL GRAFICO
    # --------------------------------------------------

    def update_plot(self):

        # Recuperiamo i valori attuali degli slider
        A = self.amp_var.get()
        f = self.freq_var.get()

        # Puliamo il grafico precedente
        self.ax.clear()

        # Creiamo una lista per gli elementi della legenda
        legend_items = []


        # Se la checkbox Sin è selezionata
        if self.show_sin.get():

            # Generiamo i valori del seno
            y = make_sin(A, f)

            # Disegniamo la curva
            l1, = self.ax.plot(t, y, label="sin")

            # Conserviamo la linea nel dizionario
            self.lines["sin"] = l1

            # Aggiungiamo la linea alla legenda
            legend_items.append(l1)


        # Se la checkbox Cos è selezionata
        if self.show_cos.get():

            # Generiamo i valori del coseno
            y = make_cos(A, f)

            # Disegniamo la curva
            l2, = self.ax.plot(t, y, label="cos")

            # Conserviamo la linea
            self.lines["cos"] = l2

            # Aggiungiamo la linea alla legenda
            legend_items.append(l2)


        # Se la checkbox Noise è selezionata
        if self.show_noise.get():

            # Generiamo i valori del rumore
            y = make_noise(A, f)

            # Disegniamo la curva
            l3, = self.ax.plot(t, y, label="noise")

            # Conserviamo la linea
            self.lines["noise"] = l3

            # Aggiungiamo la linea alla legenda
            legend_items.append(l3)


        # Se abbiamo almeno una curva, mostriamo la legenda
        if legend_items:
            self.ax.legend()

        # Impostiamo i limiti verticali
        self.ax.set_ylim(-2.5, 2.5)

        # Inseriamo l'etichetta dell'asse X
        self.ax.set_xlabel("t")

        # Inseriamo il titolo
        self.ax.set_title("Dataset sintetici - legenda dinamica")

        # Aggiorniamo il grafico
        self.canvas.draw_idle()


    # --------------------------------------------------
    # FUNZIONE RESET
    # --------------------------------------------------

    def reset(self):

        # Ripristiniamo l'ampiezza iniziale
        self.amp_var.set(1.0)

        # Ripristiniamo la frequenza iniziale
        self.freq_var.set(1.0)

        # Attiviamo soltanto la curva del seno
        self.show_sin.set(1)
        self.show_cos.set(0)
        self.show_noise.set(0)

        # Aggiorniamo il grafico
        self.update_plot()


    # --------------------------------------------------
    # FUNZIONE SALVA PNG
    # --------------------------------------------------

    def save_png(self):

        # Apriamo una finestra per scegliere dove salvare il file
        fpath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG file", "*.png")],
            title="Salva grafico come..."
        )

        # Se è stato scelto un percorso
        if fpath:

            # Salviamo la figura
            self.fig.savefig(
                fpath,
                dpi=150,
                bbox_inches="tight"
            )

            # Mostriamo un messaggio di conferma
            messagebox.showinfo(
                "Salvataggio",
                f"Grafico salvato in:\n{fpath}"
            )


# --------------------------------------------------
# AVVIO DELL'APPLICAZIONE
# --------------------------------------------------

if __name__ == "__main__":

    # Creiamo la finestra principale
    root = tk.Tk()

    # Creiamo la nostra applicazione
    app = PlotApp(root)

    # Avviamo il ciclo principale della finestra
    root.mainloop()