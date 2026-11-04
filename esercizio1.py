
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons

# --------------------------------------------------
# PREPARAZIONE DEI DATI
# --------------------------------------------------

# Generiamo 1000 punti tra 0 e 2π
t = np.linspace(0, 2*np.pi, 1000)

# Impostiamo i valori iniziali
amp0 = 1.0
freq0 = 1.0


# --------------------------------------------------
# CREAZIONE DEL GRAFICO
# --------------------------------------------------

# Creiamo figura e assi
fig, ax = plt.subplots(figsize=(11, 6))

# Sistemiamo lo spazio per grafico, checkbox e slider
fig.subplots_adjust(
    left=0.25,
    right=0.98,
    bottom=0.28,
    top=0.90
)

# Disegniamo inizialmente la curva del seno
# Conserviamo il riferimento alla linea in sin_line
sin_line, = ax.plot(
    t,
    amp0 * np.sin(freq0 * t),
    label="sin(t)"
)

# Creiamo la curva del coseno, inizialmente nascosta
cos_line, = ax.plot(
    t,
    amp0 * np.cos(freq0 * t),
    label="cos(t)",
    visible=False
)

# Impostiamo i limiti verticali
ax.set_ylim(-2.5, 2.5)

# Inseriamo il nome dell'asse orizzontale
ax.set_xlabel("t")

# Inseriamo il titolo
ax.set_title("Sinusoidale con ampiezza e frequenza variabili")

# Mostriamo la legenda
ax.legend([sin_line], ["sin(t)"], loc="upper right")


# --------------------------------------------------
# SLIDER AMPIEZZA
# --------------------------------------------------

# Creiamo lo spazio del primo slider
ax_amp = plt.axes([0.28, 0.17, 0.68, 0.03])

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

# Creiamo lo spazio del secondo slider
ax_freq = plt.axes([0.28, 0.09, 0.68, 0.03])

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

    # Aggiorniamo la curva del coseno
    cos_line.set_ydata(A * np.cos(f * t))

    # Aggiorniamo il grafico senza ricrearlo
    fig.canvas.draw_idle()


# Colleghiamo entrambi gli slider alla funzione update
s_amp.on_changed(update)
s_freq.on_changed(update)


# --------------------------------------------------
# CHECKBOX PER IL COSENO
# --------------------------------------------------

# Creiamo uno spazio separato a sinistra del grafico
rax = plt.axes([0.04, 0.45, 0.16, 0.12])

# Creiamo la checkbox, inizialmente non selezionata
check = CheckButtons(
    rax,
    ["coseno"],
    [False]
)


# --------------------------------------------------
# FUNZIONE PER MOSTRARE/NASCONDERE IL COSENO
# --------------------------------------------------

def toggle(label):

    # Mostriamo o nascondiamo il coseno
    cos_line.set_visible(not cos_line.get_visible())

    # Se il coseno è visibile, mostriamo entrambe le curve
    if cos_line.get_visible():
        ax.legend([sin_line, cos_line], ["sin(t)", "cos(t)"])

    # Altrimenti mostriamo soltanto il seno
    else:
        ax.legend([sin_line], ["sin(t)"])

    # Aggiorniamo il grafico
    fig.canvas.draw_idle()


# Colleghiamo la checkbox alla funzione toggle
check.on_clicked(toggle)


# --------------------------------------------------
# SALVATAGGIO E VISUALIZZAZIONE
# --------------------------------------------------

# Salviamo il grafico in PNG
fig.savefig(
    "esercizio1.png",
    dpi=300,
    bbox_inches="tight"
)

# Mostriamo il grafico interattivo
plt.show()
