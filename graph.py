import plotly.graph_objects as go
from flask import Flask, render_template
import random

app = Flask(__name__)

# Генерация случайных данных для графика
def generate_data():
    x = list(range(10))
    y = [random.randint(1, 10) for _ in range(10)]
    return x, y

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для обновления графика
@app.route('/update_graph')
def update_graph():
    # Генерация новых данных
    x, y = generate_data()
    
    # Создание графика
    fig = go.Figure(data=go.Scatter(x=x, y=y))
    
    # Конвертация графика в HTML
    graph_html = fig.to_html(full_html=False)
    
    return graph_html

if __name__ == '__main__':
    app.run(debug=True)