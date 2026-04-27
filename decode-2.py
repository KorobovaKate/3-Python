from PIL import Image

# Функция берёт текстовый файл и превращает его в список координат, понятный Python
def load_keys(filename):
    keys = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('(') and line.endswith(')'):
                # Убираем скобки и разделяем по запятой
                coords = line.replace('(', '').replace(')', '').split(',')
                x = int(coords[0].strip())
                y = int(coords[1].strip())
                keys.append((x, y))
    return keys

def decode_message(image_path, keys_path):

    # Загружаем изображение
    try:
        img = Image.open(image_path)
        print(f"\nИзображение загружено: {image_path}")
    except FileNotFoundError:
        print(f"Ошибка: файл {image_path} не найден!")
        return None
    
    # Загружаем ключи
    try:
        keys = load_keys(keys_path)
        print(f"\nКлючи загружены: {keys_path}")
    except FileNotFoundError:
        print(f"Ошибка: файл {keys_path} не найден!")
        return None
    
    # Декодируем сообщение
    print(f"\nДекодирование сообщения:")
    message = []
    
    for i, (x, y) in enumerate(keys, 1):
        try:
            # Проверка на выход за границы
            if x >= img.size[0] or y >= img.size[1]:
                continue
            
            # Читаем пиксель
            pixel = img.getpixel((x, y))
            
            # Берём зеленый канал
            green_channel = pixel[1]
            
            # Преобразуем в символ
            char = chr(green_channel) #Превращает число (код ASCII) в символ
            message.append(char)
            
            # Выводим первые 5 символов для отладки
            if i <= 5:
                # Используем repr для безопасного вывода любых символов
                print(f"   Пиксель {i}: ({x}, {y}) | Синий канал: {green_channel:3d} | Символ: {repr(char)}")
            
        except Exception as e:
            continue
    
    # Формируем итоговое сообщение
    final_message = ''.join(message)
    
    print(f"\nРаскодированное сообщение:")
    print("-" * 60)
    print(final_message)
    print("-" * 60)
    

# Главная программа
if __name__ == "__main__":
    image_file = "encoded_new15.png"
    keys_file = "keys15.txt"
    
    decode_message(image_file, keys_file)