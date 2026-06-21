from flask import Flask, render_template, request, redirect
from datetime import datetime
import os

app = Flask(__name__)
ARCHIVO_VENTAS = os.path.join(os.path.dirname(__file__), "ventas_trendy_web.txt")

def guardar_venta(producto, cantidad, precio, total):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{fecha_hora} | {producto} | Cant: {cantidad} | Precio U: ${precio:.2f} | Total: ${total:.2f}\n"
    with open(ARCHIVO_VENTAS, "a", encoding="utf-8") as archivo:
        archivo.write(linea)

def obtener_ventas():
    if not os.path.exists(ARCHIVO_VENTAS):
        return []
    with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as archivo:
        # Devolver en orden inverso para mostrar las ventas más recientes primero
        return [linea.strip() for linea in archivo.readlines()][::-1]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ventas', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        try:
            producto = request.form['producto'].strip().upper()
            cantidad = int(request.form['cantidad'])
            precio = float(request.form['precio'])
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que 0.")
            if precio < 0:
                raise ValueError("El precio no puede ser negativo.")
            total = cantidad * precio
            guardar_venta(producto, cantidad, precio, total)
            return redirect('/ventas')
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Error al guardar la venta: {e}"
    lista_ventas = obtener_ventas()
    return render_template('index.html', ventas=lista_ventas, error=error)

if __name__ == '__main__':
    app.run(debug=True)
