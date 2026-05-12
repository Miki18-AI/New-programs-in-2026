import customtkinter as ctk

# Настройка главной темы
ctk.set_appearance_mode("dark")

class AsciiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ASCII Переводчик")
        self.geometry("500x400")
        self.configure(fg_color="#2b1640") # Главный темно-фиолетовый фон
        self.resizable(False, False)

        # Цвета для дизайна
        self.btn_color = "#8a2be2"       
        self.btn_hover = "#9b42f5"       
        self.bg_color = "#2b1640"        
        self.entry_color = "#41235a"     

        # --- СОЗДАЕМ СТРАНИЦЫ (ФРЕЙМЫ) ---
        self.menu_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.encode_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.decode_frame = ctk.CTkFrame(self, fg_color=self.bg_color)

        self.setup_menu_page()
        self.setup_encode_page()
        self.setup_decode_page()

        # Показываем главное меню при запуске
        self.show_page(self.menu_frame)

    # --- СИСТЕМА АНИМИРОВАННЫХ УВЕДОМЛЕНИЙ (TOAST) ---
    def show_toast(self, message, color):
        # Если старое уведомление еще висит, удаляем его
        if hasattr(self, "toast_frame") and self.toast_frame.winfo_exists():
            self.toast_frame.destroy()

        # Создаем плашку. bg_color="transparent" убирает черные артефакты по углам!
        self.toast_frame = ctk.CTkFrame(self, fg_color=color, corner_radius=15, bg_color="transparent")
        self.toast_label = ctk.CTkLabel(self.toast_frame, text=message, text_color="white", font=("Segoe UI", 14, "bold"))
        self.toast_label.pack(padx=20, pady=10)

        # Ставим плашку за пределами окна (снизу)
        self.toast_y = 450
        self.toast_frame.place(relx=0.5, y=self.toast_y, anchor="center")
        
        # Запускаем анимацию выезда
        self.animate_toast_in()

    def animate_toast_in(self):
        if hasattr(self, "toast_frame") and self.toast_frame.winfo_exists():
            target_y = 340
            if self.toast_y > target_y:
                # EASE-OUT: Вычисляем шаг как 20% от оставшегося расстояния.
                # Из-за этого плашка вылетает быстро, а в конце плавно тормозит.
                step = (self.toast_y - target_y) * 0.2
                if step < 1: step = 1 # Минимальный шаг
                
                self.toast_y -= step
                self.toast_frame.place(relx=0.5, y=self.toast_y, anchor="center")
                self.after(15, self.animate_toast_in)
            else:
                # Ждем 2 секунды и прячем
                self.after(2000, self.animate_toast_out)

    def animate_toast_out(self):
        if hasattr(self, "toast_frame") and self.toast_frame.winfo_exists():
            target_y = 450
            if self.toast_y < target_y:
                # EASE-IN: Плавно уезжает обратно вниз
                step = (target_y - self.toast_y) * 0.15 
                if step < 1: step = 1
                
                self.toast_y += step
                self.toast_frame.place(relx=0.5, y=self.toast_y, anchor="center")
                self.after(15, self.animate_toast_out)
            else:
                self.toast_frame.destroy()

    # --- ЛОГИКА ПЕРЕХОДА МЕЖДУ СТРАНИЦАМИ ---
    def show_page(self, page_frame):
        self.menu_frame.pack_forget()
        self.encode_frame.pack_forget()
        self.decode_frame.pack_forget()
        page_frame.pack(fill="both", expand=True)

    # --- СТРАНИЦА: ГЛАВНОЕ МЕНЮ ---
    def setup_menu_page(self):
        title = ctk.CTkLabel(self.menu_frame, text="Главное меню", font=("Segoe UI", 24, "bold"), text_color="white")
        title.pack(pady=(50, 30))

        btn_encode = ctk.CTkButton(self.menu_frame, text="Кодировать (Текст -> ASCII)", 
                                   command=lambda: self.show_page(self.encode_frame),
                                   fg_color=self.btn_color, hover_color=self.btn_hover, corner_radius=15, height=40)
        btn_encode.pack(pady=10, padx=50, fill="x")

        btn_decode = ctk.CTkButton(self.menu_frame, text="Раскодировать (ASCII -> Текст)", 
                                   command=lambda: self.show_page(self.decode_frame),
                                   fg_color=self.btn_color, hover_color=self.btn_hover, corner_radius=15, height=40)
        btn_decode.pack(pady=10, padx=50, fill="x")

        btn_exit = ctk.CTkButton(self.menu_frame, text="Выход", 
                                 command=self.destroy,
                                 fg_color="#d63031", hover_color="#ff7675", corner_radius=15, height=40)
        btn_exit.pack(pady=(30, 0), padx=100, fill="x")

    # --- СТРАНИЦА: КОДИРОВАНИЕ ---
    def setup_encode_page(self):
        label = ctk.CTkLabel(self.encode_frame, text="Введите текст для кодирования:", 
                             font=("Segoe UI", 16), text_color="white")
        label.pack(pady=(20, 10))

        self.enc_entry = ctk.CTkEntry(self.encode_frame, fg_color=self.entry_color, text_color="white", 
                                      border_color=self.btn_color, corner_radius=10, height=40)
        self.enc_entry.pack(pady=10, padx=20, fill="x")

        btn_run = ctk.CTkButton(self.encode_frame, text="Кодировать", command=self.do_encode,
                                fg_color=self.btn_color, hover_color=self.btn_hover, corner_radius=15, height=40)
        btn_run.pack(pady=10)

        self.enc_output = ctk.CTkTextbox(self.encode_frame, height=100, fg_color=self.entry_color, 
                                         text_color="white", border_color=self.btn_color, corner_radius=10)
        self.enc_output.pack(pady=10, padx=20, fill="x")

        bottom_frame = ctk.CTkFrame(self.encode_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=10)

        btn_copy = ctk.CTkButton(bottom_frame, text="Скопировать", command=lambda: self.copy_to_clipboard(self.enc_output),
                                 fg_color="#00b894", hover_color="#55efc4", corner_radius=15)
        btn_copy.pack(side="left", expand=True, padx=5)

        btn_back = ctk.CTkButton(bottom_frame, text="В меню", command=lambda: self.show_page(self.menu_frame),
                                 fg_color="#636e72", hover_color="#b2bec3", corner_radius=15)
        btn_back.pack(side="right", expand=True, padx=5)

    # --- СТРАНИЦА: РАСКОДИРОВАНИЕ ---
    def setup_decode_page(self):
        label = ctk.CTkLabel(self.decode_frame, text="Введите ASCII коды (через пробел):", 
                             font=("Segoe UI", 16), text_color="white")
        label.pack(pady=(20, 10))

        self.dec_entry = ctk.CTkEntry(self.decode_frame, fg_color=self.entry_color, text_color="white", 
                                      border_color=self.btn_color, corner_radius=10, height=40)
        self.dec_entry.pack(pady=10, padx=20, fill="x")

        btn_run = ctk.CTkButton(self.decode_frame, text="Раскодировать", command=self.do_decode,
                                fg_color=self.btn_color, hover_color=self.btn_hover, corner_radius=15, height=40)
        btn_run.pack(pady=10)

        self.dec_output = ctk.CTkTextbox(self.decode_frame, height=100, fg_color=self.entry_color, 
                                         text_color="white", border_color=self.btn_color, corner_radius=10)
        self.dec_output.pack(pady=10, padx=20, fill="x")

        bottom_frame = ctk.CTkFrame(self.decode_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=10)

        btn_copy = ctk.CTkButton(bottom_frame, text="Скопировать", command=lambda: self.copy_to_clipboard(self.dec_output),
                                 fg_color="#00b894", hover_color="#55efc4", corner_radius=15)
        btn_copy.pack(side="left", expand=True, padx=5)

        btn_back = ctk.CTkButton(bottom_frame, text="В меню", command=lambda: self.show_page(self.menu_frame),
                                 fg_color="#636e72", hover_color="#b2bec3", corner_radius=15)
        btn_back.pack(side="right", expand=True, padx=5)

    # --- РАБОЧИЕ ФУНКЦИИ ---
    def do_encode(self):
        text = self.enc_entry.get()
        if not text:
            self.show_toast("Введите текст!", "#d63031") 
            return
            
        ascii_codes = " ".join(str(ord(c)) for c in text)
        self.enc_output.delete("1.0", "end")
        self.enc_output.insert("end", ascii_codes)

    def do_decode(self):
        text = self.dec_entry.get()
        if not text:
            self.show_toast("Введите коды!", "#d63031")
            return
            
        try:
            chars = [chr(int(code)) for code in text.split()]
            result = "".join(chars)
            self.dec_output.delete("1.0", "end")
            self.dec_output.insert("end", result)
        except ValueError:
            self.show_toast("Ошибка: только числа через пробел!", "#d63031")

    def copy_to_clipboard(self, textbox):
        # Копирование теперь надежно отправляет данные в буфер обмена системы
        text = textbox.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update() # Принудительно обновляем буфер
            self.show_toast("Скопировано в буфер обмена!", "#00b894")
        else:
            self.show_toast("Нет текста для копирования!", "#d63031")

# Запуск программы
if __name__ == "__main__":
    app = AsciiApp()
    app.mainloop()