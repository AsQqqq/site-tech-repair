from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import qrcode, uuid


class GeneratedReceipt:
    def __init__(self, date_start: str, time_start: str, date_end: str, time_end: str, amount_expenced: str, amount_income: str, total_amount: str):
        # Устанавливаем параметры для печати
        width_mm = 79   # Ширина чека в мм
        dpi = 203  # Разрешение принтера (точек на дюйм)

        self.text = f"""
Доходы - {amount_income} руб.
Расходы - {amount_expenced} руб.\n
Итого - {total_amount} руб.
"""

        line_height = 30  # Выставляем высоту строки вручную
        text_height = 0  # Считаем высоту всего текста

        # Конвертируем мм в пиксели
        width_px = int(width_mm * dpi / 25.4)  # 25.4 мм в 1 дюйм

        # Создаем изображение белого фона с временной высотой
        height_px = 1000  # Начальная высота изображения, которую нужно будет пересчитать

        # Создаем изображение белого фона
        img = Image.new('RGB', (width_px, height_px), color=(255, 255, 255))

        # Инициализируем объект для рисования
        draw = ImageDraw.Draw(img)

        # Указываем путь к шрифтам, которые поддерживают кириллицу
        thin_font_path = "DejaVuSans-Oblique.ttf"  # Путь к тонкому шрифту



        header_font_size = 24  # Размер шрифта для заголовка
        font_size = 16  # Размер шрифта для основного текста
        bold_font = ImageFont.truetype(thin_font_path, header_font_size)
        thin_font = ImageFont.truetype(thin_font_path, font_size)  # Используем тонкий шрифт

        # Заголовок чека
        header = "Недельный чек"
        # Даты и времени
        date_time_info = f"С {date_start} / {time_start} По {date_end} / {time_end}"
        # Айди чека
        uuid_ = f"Номер - {str(self.generate_uuid())}"

        # Рисуем заголовок и дату
        y = 10  # Начальная высота текста
        header_bbox = draw.textbbox((0, 0), header, font=bold_font)  # Получаем границы заголовка
        header_width = header_bbox[2] - header_bbox[0]  # Ширина заголовка
        draw.text(((width_px - header_width) // 2, y), header, font=bold_font, fill=(0, 0, 0))  # Центрируем заголовок
        y += header_bbox[3] - header_bbox[1] + 15  # Отступ после заголовка (добавлен отступ в 15 пикселей)

        uuid__bbox = draw.textbbox((0, 0), uuid_, font=thin_font)  # Получаем границы заголовка
        uuid__width = uuid__bbox[2] - uuid__bbox[0]  # Ширина заголовка
        draw.text(((width_px - uuid__width) // 2, y), uuid_, font=thin_font, fill=(0, 0, 0))  # Центрируем заголовок
        y += line_height + 10  # Отступ после айди
        
        date_time_info_bbox = draw.textbbox((0, 0), date_time_info, font=thin_font)  # Получаем границы заголовка
        date_time_info_width = date_time_info_bbox[2] - date_time_info_bbox[0]  # Ширина заголовка
        draw.text(((width_px - date_time_info_width) // 2, y), date_time_info, font=thin_font, fill=(0, 0, 0))  # Центрируем заголовок
        y += line_height + 10  # Отступ после айди

        # Добавляем горизонтальную полосу
        draw.line((10, y, width_px - 10, y), fill=(0, 0, 0), width=2)
        y += 10  # Отступ после полосы

        # Рисуем основную информацию о тратах и доходах
        for line in self.text.split('\n'):
            draw.text((10, y), line, font=thin_font, fill=(0, 0, 0))  # Легкий цвет текста
            y += line_height
            text_height += line_height

        # Добавляем горизонтальную полосу
        draw.line((10, y, width_px - 10, y), fill=(0, 0, 0), width=2)
        y += 10  # Отступ после полосы

        # Генерация QR-кода
        qr_data = "https://repair-31.ru/"
        qr = qrcode.make(qr_data)
        qr = qr.convert('RGB')

        # Размеры QR-кода (вычисление динамически в зависимости от контента)
        qr_size = 200  # Размер QR-кода увеличен, можно динамически изменять
        qr = qr.resize((qr_size, qr_size))

        # Вставляем QR-код в изображение
        qr_x = (width_px - qr_size) // 2
        qr_y = y  # Начальная позиция для QR-кода, сразу после ссылки
        img.paste(qr, (qr_x, qr_y))

        # Обновляем высоту изображения в зависимости от содержимого
        height_px = y + qr_size + 10  # Отступ от QR-кода

        # Пересоздаем изображение с правильной высотой
        img = Image.new('RGB', (width_px, height_px), color=(255, 255, 255))  # Создаем новое изображение с правильной высотой
        draw = ImageDraw.Draw(img)  # Повторно инициализируем объект для рисования

        # Повторно рисуем заголовок, дату, основной текст, полосу, ссылку и QR-код
        y = 10  # Начальная высота текста
        header_bbox = draw.textbbox((0, 0), header, font=bold_font)  # Получаем границы заголовка
        header_width = header_bbox[2] - header_bbox[0]  # Ширина заголовка
        draw.text(((width_px - header_width) // 2, y), header, font=bold_font, fill=(0, 0, 0))  # Центрируем заголовок
        y += header_bbox[3] - header_bbox[1] + 15  # Отступ после заголовка (добавлен отступ в 15 пикселей)
        
        uuid__bbox = draw.textbbox((0, 0), uuid_, font=thin_font)  # Получаем границы заголовка
        uuid__width = uuid__bbox[2] - uuid__bbox[0]  # Ширина заголовка
        draw.text(((width_px - uuid__width) // 2, y), uuid_, font=thin_font, fill=(0, 0, 0))  # Центрируем заголовок
        y += line_height + 10  # Отступ после айди
        
        date_time_info_bbox = draw.textbbox((0, 0), date_time_info, font=thin_font)  # Получаем границы заголовка
        date_time_info_width = date_time_info_bbox[2] - date_time_info_bbox[0]  # Ширина заголовка
        draw.text(((width_px - date_time_info_width) // 2, y), date_time_info, font=thin_font, fill=(0, 0, 0))  # Центрируем заголовок
        y += line_height + 10  # Отступ после даты


        # Добавляем горизонтальную полосу
        draw.line((10, y, width_px - 10, y), fill=(0, 0, 0), width=2)
        y += 10  # Отступ после полосы

        # Рисуем основную информацию о тратах и доходах
        for line in self.text.split('\n'):
            draw.text((10, y), line, font=thin_font, fill=(0, 0, 0))
            y += line_height

        # Добавляем горизонтальную полосу
        draw.line((10, y, width_px - 10, y), fill=(0, 0, 0), width=2)
        y += 10  # Отступ после полосы

        # Вставляем QR-код в изображение
        img.paste(qr, (qr_x, qr_y))

        # Сохраняем картинку
        img.save("check_with_qr.png", "PNG")

    def generate_uuid(self):
        return uuid.uuid4()
    

if __name__ == "__main__":
    date_start = "01.01.2025"
    time_start = "23:53"

    date_end = datetime.now().strftime("%d.%m.%Y")
    time_end = datetime.now().strftime("%H:%M")

    amount_expenced = 3000
    amount_income = 150000
    total_amount = amount_income - amount_expenced

    receipt = GeneratedReceipt(date_start, time_start, date_end, time_end, amount_expenced, amount_income, total_amount)