import tkinter as tk
from PIL import Image, ImageTk, ImageDraw


def on_button_click():
    print("Кнопка нажата!")
def make_circle_image(image):
    # Создаем маску
    mask = Image.new("L", (image.size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)

    # Применяем маску к изображению
    output = Image.new("RGBA", image.size)
    output.paste(image, (0, 0), mask)
    return output


# Создаем главное окно
root = tk.Tk()
root.title("Круглая кнопка с изображением")

# Устанавливаем размер окна
root.geometry("800x600")

# Загружаем квадратное изображение
image = Image.open("backgroundButton.jpeg")  # Замените на имя вашего изображения
image = image.resize((120, 120), Image.LANCZOS)  # Изменяем размер изображения
circle_image = make_circle_image(image)  # Применяем функцию для создания круглого изображения
photo = ImageTk.PhotoImage(circle_image)

# Создаем canvas для круглой кнопки
canvas = tk.Canvas(root, width=800, height=600, bg="lightblue", highlightthickness=0)
canvas.pack()

# Вычисляем координаты для круга
radius = 60
x1, y1 = (400 - radius), (300 - radius)
x2, y2 = (400 + radius), (300 + radius)

# Рисуем круг с заливкой
canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")

# Добавляем круглое изображение в центр круга
canvas.create_image(400, 300, image=photo)

# Создаем текст под кнопкой
label = tk.Label(root, text="Кнопка", font=("Arial", 14, "bold"))
label.place(x=400, y=380, anchor='center')  # Центрирование текста под кнопкой

# Привязываем щелчок мыши к функции
canvas.bind("<Button-1>", lambda event: on_button_click())  # Клик по canvas вызывает функцию


root.mainloop()