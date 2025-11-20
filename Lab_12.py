import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, save, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Bright6

def generate_sales_data(rows=100):
    """
    Генерує тестовий набір даних про продажі.
    Повертає pandas DataFrame.
    """
    np.random.seed(42)
    categories = ['Electronics', 'Clothing', 'Home', 'Garden', 'Toys', 'Sports']
    
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=rows, freq='3D'),
        'Category': np.random.choice(categories, rows),
        'Sales': np.random.randint(100, 1000, rows),
        'Profit': np.random.randint(10, 300, rows)
    }
    df = pd.DataFrame(data)
    # Сортування за датою для коректного відображення лінійного графіка
    df = df.sort_values('Date')
    return df

def create_dashboard(df):
    """
    Створює інтерактивні графіки на основі переданого DataFrame.
    Повертає об'єкт layout бібліотеки Bokeh.
    """
    # Підготовка джерела даних для Bokeh
    source = ColumnDataSource(df)

    # Графік 1: Динаміка продажів
    # Налаштування інтерактивних підказок
    TOOLTIPS = [
        ("Дата", "@Date{%F}"),
        ("Продажі", "$@Sales"),
        ("Категорія", "@Category")
    ]

    p_line = figure(title="Динаміка продажів за часом", x_axis_type="datetime", 
                    width=800, height=350, tooltips=TOOLTIPS)
    
    # Форматування підказок дати
    p_line.hover.formatters = {'@Date': 'datetime'}

    p_line.line(x='Date', y='Sales', source=source, line_width=2, color="navy", legend_label="Trend")
    p_line.scatter(x='Date', y='Sales', source=source, size=5, color="orange")
    
    p_line.title.text_font_size = '14pt'
    p_line.xaxis.axis_label = "Дата"
    p_line.yaxis.axis_label = "Сума продажів ($)"

    # Графік 2: Продажі за категоріями (Bar Chart)
    # Агрегація даних для другого графіка
    df_grouped = df.groupby('Category')['Sales'].sum().reset_index()
    source_grouped = ColumnDataSource(df_grouped)
    
    categories_list = df_grouped['Category'].tolist()

    p_bar = figure(x_range=categories_list, title="Загальні продажі за категоріями",
                   width=800, height=350, toolbar_location=None, tools="")

    p_bar.vbar(x='Category', top='Sales', width=0.5, source=source_grouped,
               line_color='white', 
               fill_color=factor_cmap('Category', palette=Bright6, factors=categories_list))

    p_bar.xgrid.grid_line_color = None
    p_bar.y_range.start = 0
    p_bar.yaxis.axis_label = "Загальний обсяг ($)"

    # Компонування графіків у стовпчик
    layout = column(p_line, p_bar)
    return layout

def save_report(layout, filename):
    """
    Зберігає макет у файл.
    """
    output_file(filename)
    save(layout)

def main():
    """
    Головна функція програми. Керує діалогом з користувачем та потоком даних.
    """
    print("Генератор аналітичного звіту (Bokeh)")
    
    try:
        # Взаємодія з користувачем
        user_filename = input("Введіть назву файлу для збереження (наприклад, report): ").strip()
        
        if not user_filename:
            raise ValueError("Ім'я файлу не може бути порожнім.")
        
        if not user_filename.endswith(".html"):
            user_filename += ".html"

        print("1.Генерація даних...")
        df = generate_sales_data()
        
        print("2.Створення візуалізацій...")
        dashboard_layout = create_dashboard(df)
        
        print(f"3.Збереження у файл '{user_filename}'...")
        save_report(dashboard_layout, user_filename)
        
        print(f"Успішно! Відкрийте файл {user_filename} у браузері для перегляду.")
        
        # Опціонально: спробувати відкрити файл автоматично (працює не у всіх середовищах)
        # show(dashboard_layout)

    except ValueError as ve:
        print(f"Помилка вводу: {ve}")
    except OSError as oe:
        print(f"Помилка доступу до файлової системи: {oe}")
    except Exception as e:
        print(f"Виникла неочікувана помилка: {e}")

if __name__ == "__main__":
    main()