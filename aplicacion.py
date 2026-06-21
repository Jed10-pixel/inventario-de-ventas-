from flask import Flask, render_template, request, redirect
from datetime import datetime
import os

aplicacion = Flask(__name__)
ARCHIVO_VENTAS = os.path.pathsep.join([os.path.dirname(__file__), "ventas_trendy_web.txt"])

def guardar_venta(producto, cantidad, precio, total):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{fecha_hora} | Producto: {producto} | Cant.: {cantidad} | Precio U: ${precio:.2f} | Total: ${total:.2f}\n"
    with open(ARCHIVO_VENTAS, "a", encoding="utf-8") as archivo:
        archivo.write(linea)

def obtener_ventas():
    if not os.path.exists(ARCHIVO_VENTAS):
        return []
    with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo.readlines()][::-1]

@aplicacion.route('/')
def hogar():
    return render_template('inicio.html')

@aplicacion.route('/ventas', methods=['GET', 'POST'])
def indice():
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
    return render_template('indice.html', ventas=lista_ventas, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    aplicacion.run(host='0.0.0.0', port=port)
