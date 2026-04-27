from PIL import Image

def load_keys(filename):
    keys = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('(') and line.endswith(')'):
                coords = line.replace('(', '').replace(')', '').split(',')
                x = int(coords[0].strip())
                y = int(coords[1].strip())
                keys.append((x, y))
    return keys

# Кодируем сообщение в изображение
def encode_message(image_path, keys_path, message, output_path="encoded_new15.png"):

    # Загружаем изображение
    try:
        img = Image.open(image_path)
        pixels = img.load()
        width, height = img.size
        print(f"\nИзображение загружено: {image_path}")
    except FileNotFoundError:
        print(f"Ошибка: файл {image_path} не найден!")
        return False

    # Загружаем ключи
    try:
        keys = load_keys(keys_path)
        print(f"Ключи загружены: {keys_path}")
    except FileNotFoundError:
        print(f"Ошибка: файл {keys_path} не найден!")
        return False

    # Проверка длины сообщения
    if len(message) > len(keys):
        print(f"Ошибка: Сообщение слишком длинное ({len(message)} симв.), максимум {len(keys)}.")
        return False

    print(f"\nСообщение для кодирования: \"{message}\"")
    print(f"Длина: {len(message)} символов")

    # Требование a: Биты первого символа
    if len(message) > 0:
        first_char = message[0]
        first_byte_val = ord(first_char) #Функция ord() превращает символ в его ASCII-код
        first_byte_bin = f"{first_byte_val:08b}"
        
        print(f"\na) Биты первого символа '{first_char}':")
        print(f"   ASCII код: {first_byte_val}")
        print(f"   Двоичный вид: {first_byte_bin}")

    # Требования b и c: изменение пикселей 
    print(f"\nb) и c) Изменение пикселей:")
  
    for i in range(len(message)):
        x, y = keys[i]

        if x >= width or y >= height:
            continue
            
        original_pixel = pixels[x, y]
        new_pixel_list = list(original_pixel)
        original_green = new_pixel_list[1]
        char_code = ord(message[i])
        
        new_pixel_list[1] = char_code
        pixels[x, y] = tuple(new_pixel_list)
        
        # Выводим отладочную информацию для первых 3 символов
        if i < 3:
            print(f"Символ №{i+1}: '{message[i]}' (ASCII={char_code})")
            print(f"   Координата: ({x}, {y})")
            print(f"   Исходный пиксель: {original_pixel}  (G={original_green})")
            print(f"   Новый пиксель: {tuple(new_pixel_list)}  (G={char_code})")
            print("-" * 60)

    # Перезаписываем оставшиеся пиксели пробелами
    for i in range(len(message), len(keys)):
        x, y = keys[i]
        if x >= width or y >= height:
            continue
        new_pixel_list = list(pixels[x, y])
        new_pixel_list[1] = 32
        pixels[x, y] = tuple(new_pixel_list)

    # Сохраняем результат
    try:
        img.save(output_path)
        print(f"\nИзображение сохранено как: {output_path}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        return False

if __name__ == "__main__":
    image_file = "new15.png"
    keys_file = "keys15.txt"
    
    # Ввод сообщения пользователем
    test_message = input("\nВведите сообщение для кодирования: ")
    
    if not test_message:
        print("Сообщение не может быть пустым!")
    else:
        success = encode_message(image_file, keys_file, test_message)
        if success:
            print("\n Готово! Теперь запустите decode-2.py, чтобы проверить вывод.")