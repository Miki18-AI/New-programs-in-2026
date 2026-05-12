import os
import platform
import tkinter as tk
from tkinter import messagebox as mb

def clear_yandex_history():
    """Функция, которая вызывается при нажатии на кнопку."""
    
    # 1. Определяем пути к файлам
    if platform.system() == "Windows":
        base_path = os.path.expanduser('~') + r'\AppData\Local\Yandex\YandexBrowser\User Data\Default'
    elif platform.system() == "Darwin": # macOS
        base_path = os.path.expanduser('~') + '/Library/Application Support/Yandex/YandexBrowser/Default'
    else:
        mb.showerror("Ошибка", "Ваша операционная система пока не поддерживается.")
        return

    history_path = os.path.join(base_path, 'History')
    journal_path = os.path.join(base_path, 'History-journal')
    
    files_to_delete = [history_path, journal_path]
    
    deleted_something = False
    is_browser_open = False

    # 2. Пытаемся удалить
    for path in files_to_delete:
        if os.path.exists(path):
            try:
                os.remove(path)
                deleted_something = True
            except PermissionError:
                is_browser_open = True
            except Exception as e:
                mb.showerror("Непредвиденная ошибка", f"Ошибка: {e}")
                return

    # 3. Выводим результат в виде всплывающего окна
    if is_browser_open:
        mb.showwarning(
            "Браузер открыт!", 
            "Не удалось удалить файлы.\n\nПожалуйста, полностью закройте Яндекс Браузер и нажмите кнопку еще раз."
        )
    elif deleted_something:
        mb.showinfo("Успех", "История Яндекс Браузера успешно удалена!")
    else:
        mb.showinfo("Информация", "История уже чиста. Файлы для удаления не найдены.")

# === Создание графического интерфейса ===

# Создаем главное окно
root = tk.Tk()
root.title("Очистка Яндекса")
root.geometry("350x150") # Размер окна
root.resizable(False, False) # Запрещаем менять размер окна

# Создаем надпись (инструкцию)
label = tk.Label(root, text="Перед очисткой убедитесь, что браузер закрыт.", pady=10)
label.pack()

# Создаем большую красную кнопку
clean_button = tk.Button(
    root, 
    text="УДАЛИТЬ ИСТОРИЮ", 
    font=("Arial", 12, "bold"), 
    bg="#ffcccc", 
    fg="red",
    width=20,
    height=2,
    command=clear_yandex_history
)
clean_button.pack(pady=10)

# Запускаем программу
if __name__ == "__main__":
    root.mainloop()