# Importiamo le librerie necessarie
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# --------------------------------------------------
# PREPARAZIONE DEI DATI
# --------------------------------------------------

# Generiamo 1000 punti tra 0 e 2π
t = np.linspace(0, 2*np.pi, 1000)

# Impostiamo i valori iniziali di ampiezza e frequenza
amp0 = 1.0
freq0 = 1.0


# --------------------------------------------------
# CREAZIONE DEL GRAFICO
# --------------------------------------------------

# Creiamo la figura e gli assi
fig, ax = plt.subplots(figsize=(8, 4))

# Riserviamo spazio nella parte inferiore
# per inserire slider e pulsanti
plt.subplots_adjust(left=0.1, bottom=0.28)

# Disegniamo la curva iniziale del seno
# Conserviamo il riferimento alla linea in sin_line
sin_line, = ax.plot(
    t,
    amp0 * np.sin(freq0 * t),
    label="sin(t)"
)

# Impostiamo i limiti verticali del grafico
ax.set_ylim(-2.5, 2.5)

# Inseriamo il nome dell'asse X
ax.set_xlabel("t")

# Inseriamo il titolo del grafico
ax.set_title("Sinusoidale con Reset e Salva")

# Mostriamo la legenda
ax.legend()


# --------------------------------------------------
# SLIDER AMPIEZZA
# --------------------------------------------------

# Creiamo lo spazio per il primo slider
ax_amp = plt.axes([0.1, 0.16, 0.8, 0.03])

# Creiamo lo slider dell'ampiezza
# Valore minimo: 0
# Valore massimo: 2
# Valore iniziale: amp0
s_amp = Slider(
    ax_amp,
    "Ampiezza",
    0.0,
    2.0,
    valinit=amp0
)


# --------------------------------------------------
# SLIDER FREQUENZA
# --------------------------------------------------

# Creiamo lo spazio per il secondo slider
ax_freq = plt.axes([0.1, 0.12, 0.8, 0.03])

# Creiamo lo slider della frequenza
# Valore minimo: 0.1
# Valore massimo: 5
# Valore iniziale: freq0
s_freq = Slider(
    ax_freq,
    "Frequenza",
    0.1,
    5.0,
    valinit=freq0
)


# --------------------------------------------------
# FUNZIONE DI AGGIORNAMENTO
# --------------------------------------------------

def update(val):

    # Recuperiamo i valori attuali dei due slider
    A = s_amp.val
    f = s_freq.val

    # Aggiorniamo la curva del seno
    sin_line.set_ydata(A * np.sin(f * t))

    # Aggiorniamo il grafico senza ricrearlo
    fig.canvas.draw_idle()


# Colleghiamo entrambi gli slider alla funzione update
s_amp.on_changed(update)
s_freq.on_changed(update)


# --------------------------------------------------
# PULSANTE RESET
# --------------------------------------------------

# Creiamo lo spazio per il pulsante Reset
ax_reset = plt.axes([0.1, 0.04, 0.15, 0.05])

# Creiamo il pulsante
btn_reset = Button(ax_reset, "Reset")


# Funzione eseguita quando clicchiamo Reset
def reset(event):

    # Riportiamo lo slider dell'ampiezza al valore iniziale
    s_amp.reset()

    # Riportiamo lo slider della frequenza al valore iniziale
    s_freq.reset()

    # Aggiorniamo il grafico
    update(None)


# Colleghiamo il pulsante alla funzione reset
btn_reset.on_clicked(reset)


# --------------------------------------------------
# PULSANTE SALVA PNG
# --------------------------------------------------

# Creiamo lo spazio per il pulsante Salva PNG
ax_save = plt.axes([0.32, 0.04, 0.15, 0.05])

# Creiamo il pulsante
btn_save = Button(ax_save, "Salva PNG")


# Funzione eseguita quando clicchiamo Salva PNG
def save_png(event):

    # Definiamo il nome del file
    filename = "esercizio2.png"

    # Salviamo la figura in formato PNG
    # dpi=150 imposta la risoluzione
    # bbox_inches="tight" riduce gli spazi bianchi
    fig.savefig(filename, dpi=150, bbox_inches="tight")

    # Comunichiamo il nome del file salvato
    print(f"Grafico salvato in: {filename}")


# Colleghiamo il pulsante alla funzione save_png
btn_save.on_clicked(save_png)


# --------------------------------------------------
# VISUALIZZAZIONE
# --------------------------------------------------

# Mostriamo il grafico interattivo
plt.show()