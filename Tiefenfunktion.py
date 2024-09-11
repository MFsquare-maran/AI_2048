import matplotlib.pyplot as plt
import math

# Definiere die Funktion
def f(x):
    
    #y = int(math.exp((x-2) / 5.9)+1.5)
    y= int((x/2)+0.5)
    if y <=0:
        return 1
    
    return y

# Initialisiere Listen für x- und y-Werte
x_values = []
y_values = []

# Verwende eine for-Schleife, um die Werte zu berechnen
for x in range(0, 16):  # Bereich von -10 bis 10
    x_values.append(x)
    y_values.append(f(x))

# Plot die Funktion
plt.plot(x_values, y_values, label=r'$f(x) = e^{\frac{x-2}{7}}$')

# Beschrifte die Achsen
plt.xlabel('Anzahl Zahlen')
plt.ylabel('Tiefe')

# Füge einen Titel hinzu
plt.title(r'Plot von $f(x) = e^{\frac{x-2}{7}}$')

# Zeige die Legende
plt.legend()

# Zeige den Plot
plt.grid(True)
plt.show()
