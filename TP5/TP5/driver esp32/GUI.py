import serial
import threading
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SerialPlotter:
    """
    @class SerialPlotter
    @brief Lee datos de temperatura y humedad desde un puerto serial y almacena la variable seleccionada.
    """

    def __init__(self, port="/dev/ttyACM0", baudrate=9600):
        """
        @brief Constructor de la clase SerialPlotter.

        @param port Puerto serial al que está conectada la ESP32.
        @param baudrate Velocidad de transmisión en baudios.
        """
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.data = []         ///< Lista para almacenar los valores (temperatura o humedad).
        self.time = []         ///< Lista de tiempo correspondiente a cada lectura.
        self.index = 0         ///< Contador de muestras para el eje temporal.
        self.variable = "temperature"  ///< Variable activa: "temperature" o "humidity".

    def read_serial(self):
        """
        @brief Hilo que lee continuamente del puerto serial y actualiza los datos según la variable seleccionada.
        """
        while True:
            if self.ser.in_waiting:
                try:
                    line = self.ser.readline().decode().strip()
                    t, h = map(float, line.split(','))
                    if self.variable == "temperature":
                        self.data.append(t)
                    else:
                        self.data.append(h)
                    self.time.append(self.index)
                    self.index += 1
                except:
                    continue

    def reset_data(self):
        """
        @brief Resetea los datos de tiempo y valores, usado al cambiar de variable a graficar.
        """
        self.data.clear()
        self.time.clear()
        self.index = 0

class App:
    """
    @class App
    @brief Crea una interfaz gráfica en Tkinter que muestra una gráfica en tiempo real con datos del sensor DHT11.
    """

    def __init__(self, root, plotter):
        """
        @brief Constructor de la clase App.

        @param root Instancia principal de Tkinter.
        @param plotter Instancia de SerialPlotter para acceder a los datos seriales.
        """
        self.root = root
        self.plotter = plotter

        self.root.title("Monitor de Sensor DHT11 - ESP32")

        # Crear la figura y eje de la gráfica
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Botón para cambiar entre temperatura y humedad
        self.switch_button = ttk.Button(root, text="Switch to Humidity", command=self.switch_variable)
        self.switch_button.pack(pady=10)

        # Iniciar animación para refrescar la gráfica cada segundo
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000)

        # Iniciar hilo de lectura del puerto serial
        self.thread = threading.Thread(target=self.plotter.read_serial, daemon=True)
        self.thread.start()

    def switch_variable(self):
        """
        @brief Cambia entre graficar temperatura y humedad. Reinicia la gráfica.
        """
        if self.plotter.variable == "temperature":
            self.plotter.variable = "humidity"
            self.switch_button.config(text="Switch to Temperature")
        else:
            self.plotter.variable = "temperature"
            self.switch_button.config(text="Switch to Humidity")
        self.plotter.reset_data()

    def update_plot(self):
        """
        @brief Actualiza el gráfico con los nuevos datos cada intervalo.
        """
        self.ax.clear()
        self.ax.plot(self.plotter.time, self.plotter.data, label=self.plotter.variable.capitalize())
        self.ax.set_title(f"{self.plotter.variable.capitalize()} vs Time")
        self.ax.set_xlabel("Time (s)")

        # Etiqueta dinámica del eje Y según la variable seleccionada
        if self.plotter.variable == "temperature":
            self.ax.set_ylabel("Celsius (°C)")
        else:
            self.ax.set_ylabel("Percent (%)")

        self.ax.legend()
        self.ax.grid(True)


if __name__ == "__main__":
    """
    @brief Punto de entrada principal del programa.
    """
    port = "/dev/ttyACM0"
    plotter = SerialPlotter(port)
    root = tk.Tk()
    app = App(root, plotter)
    root.mainloop()
