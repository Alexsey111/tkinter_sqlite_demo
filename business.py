import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def init_db():
    conn = sqlite3.connect('business_orders.db')  # Подключение к базе данных
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        order_details TEXT NOT NULL,
        status TEXT NOT NULL)
    ''')  # Создание таблицы, если ее нет
    conn.commit()
    conn.close()

def add_order():
    conn = sqlite3.connect('business_orders.db')  # Подключение к базе данных
    cur = conn.cursor()
    # Добавление новой записи в таблицу
    cur.execute(
        "INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
        (customer_name_entry.get(), order_details_entry.get())
    )
    conn.commit()  # Сохранение изменений в базе данных
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    view_orders()  # Обновление таблицы
    conn.close()

def view_orders():
    for i in tree.get_children():
        tree.delete(i)
    conn = sqlite3.connect('business_orders.db')  # Подключение к базе данных
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)  # Заполнение Treeview данными
    conn.close()

def complete_order():
    selected_item = tree.selection()
    if selected_item:
        order_id = tree.item(selected_item[0])['values'][0]
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status = 'Завершен' WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning('Предупреждение', 'Выберите заказ для завершения')


app = tk.Tk()
app.title('Система управления заказами')

tk.Label(app, text='Имя клиента').pack()
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

tk.Label(app, text='Детали заказа').pack()
order_details_entry = tk.Entry(app)
order_details_entry.pack()

add_button = tk.Button(app, text='Добавить заказ', command=add_order)
add_button.pack()

compile_button = tk.Button(app, text='Завершить заказ', command=complete_order)
compile_button.pack()

columns = ('id', 'customer_name', 'order_details', 'status')
tree = ttk.Treeview(app, columns=columns, show='headings')
for column in columns:
    tree.heading(column, text=column)
tree.pack()

init_db()  # Инициализация базы данных
view_orders()  # Предварительный просмотр заказов для заполнения таблицы

app.mainloop()  # Запуск основного цикла приложения