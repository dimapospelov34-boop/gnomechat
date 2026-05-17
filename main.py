import flet as ft

# Шаблон для писем в чате
class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

def main(page: ft.Page):
    page.title = "ГномЧат"
    page.theme_mode = ft.ThemeMode.DARK  # Брутальная темная тема под стать логотипу
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    
    # Ссылка на твою картинку, которая лежит в папке assets
    AVATAR_PATH = "/gnome_avatar.jpg" 

    # Обработчик входящих сообщений
    def on_message(message: Message):
        if message.message_type == "status":
            # Системный текст (кто-то зашел/вышел)
            chat.controls.append(ft.Text(message.text, italic=True, color=ft.Colors.RED_400, size=12))
        else:
            # Обычное сообщение от гнома
            chat.controls.append(
                ft.Row([
                    ft.CircleAvatar(content=ft.Text(message.user_name[:2].upper()), bgcolor=ft.Colors.RED_900),
                    ft.Column([
                        ft.Text(message.user_name, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_500),
                        ft.Text(message.text, selectable=True),
                    ], spacing=2)
                ], vertical_alignment=ft.CrossAxisAlignment.START)
            )
        page.update()  # Обновляем экран смартфона

    # Подключаем устройство к общей системе обмена сообщениями
    page.pubsub.subscribe(on_message)

    # Функция входа в чат
    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Имя гнома не может быть пустым!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            # Отправляем в чат статус, что гном на связи
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"⛏️ {join_user_name.value} спустился в шахту чата!", message_type="status"))
            page.add(chat_layout)

    # Поле ввода никнейма
    join_user_name = ft.TextField(label="Имя гнома в сети...", on_submit=join_chat_click, color=ft.Colors.WHITE)
    
    # Приветственное окно с твоим логотипом
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("ГномЧат: Убежище Братства", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
        content=ft.Column([
            ft.Image(src=AVATAR_PATH, width=150, height=150),  # Твой JPG логотип
            join_user_name
        ], width=300, height=220, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        actions=[ft.ElevatedButton(text="Войти в чат", on_click=join_chat_click, bgcolor=ft.Colors.RED_900, color=ft.Colors.WHITE)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    # Кнопка отправки текста
    def send_message_click(e):
        if new_message.value:
            user_name = page.session.get("user_name")
            page.pubsub.send_all(Message(user_name=user_name, text=new_message.value, message_type="chat"))
            new_message.value = ""
            new_message.focus()
            page.update()

    # Сетка интерфейса
    chat = ft.ListView(expand=True, spacing=15, auto_scroll=True)
    new_message = ft.TextField(hint_text="Написать гномам...", expand=True, on_submit=send_message_click, shift_enter=True)
    
    chat_layout = ft.Column([
        ft.Container(content=chat, expand=True, padding=10),
        ft.Row([new_message, ft.IconButton(icon=ft.Icons.SEND_ROUNDED, icon_color=ft.Colors.RED_900, on_click=send_message_click)])
    ], expand=True)

# Запускаем приложение и указываем папку с ресурсами
ft.app(target=main, assets_dir="assets")
