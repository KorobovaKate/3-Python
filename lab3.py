from PIL import Image

def load_keys(filename):
    keys = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('(') and line.endswith(')'):
                    # Убираем скобки и разбиваем по запятой
                    coords = line.replace('(', '').replace(')', '').split(',')
                    x = int(coords[0].strip())
                    y = int(coords[1].strip())
                    keys.append((x, y))
    except FileNotFoundError:
        print(f" Файл ключей '{filename}' не найден!")
    return keys

#1.1: Декодирование в синем канале
def decode_blue(image_path, keys_path):
    print("-" * 60)
    print("Задание 1.1: Декодирование исходного изображения")

    
    try:
        img = Image.open(image_path)
        keys = load_keys(keys_path)
        if not keys: return
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return

    message = []
    print(f"\nЧтение из синего канала (B)...")
    
    for i, (x, y) in enumerate(keys):
        if x >= img.width or y >= img.height:
            continue
        
        pixel = img.getpixel((x, y))
        blue_val = pixel[2] # Индекс 2 = Blue
        
        message.append(chr(blue_val))
        
        if i < 5:
            print(f"   Пиксель {i+1}: ({x}, {y}) -> B={blue_val} -> '{chr(blue_val)}'")

    final_msg = "".join(message)
    print(f"\nРезультат: '{final_msg}'")

#1.2: Кодирование в зеленый канал
def encode_green(image_path, keys_path, message, output_path):
    print("\n" + "-" * 60)
    print("Задание 1.2: Кодирование сообщения")

    try:
        img = Image.open(image_path)
        pixels = img.load()
        keys = load_keys(keys_path)
        if not keys: return False
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return False

    if len(message) > len(keys):
        print(f"Ошибка: Сообщение слишком длинное ({len(message)}), максимум {len(keys)} символов.")
        return False

    print(f"\nСообщение: \"{message}\"")

    if message:
        first_char = message[0]
        ascii_val = ord(first_char)
        binary_val = f"{ascii_val:08b}"
        print(f"\na)Биты первого символа '{first_char}':")
        print(f"   ASCII код: {ascii_val}")
        print(f"   Двоичный вид: {binary_val}")

    # 1.2.b и 1.2.c: Изменение пикселей
    print(f"\nИзменение пикселей:")
    print("-" * 60)
    
    for i, (x, y) in enumerate(keys):
        if x >= img.width or y >= img.height:
            continue
        
        current_pixel = pixels[x, y]
        new_pixel_list = list(current_pixel)
        
        if i < len(message):
            char_code = ord(message[i])
            new_pixel_list[1] = char_code
            pixels[x, y] = tuple(new_pixel_list)
            
            if i < 3:
                print(f"  Символ '{message[i]}' (ASCII={char_code}):")
                print(f"    Координаты: ({x}, {y})")
                print(f"    Исходный: {current_pixel} (G={current_pixel[1]})")
                print(f"    Новый:    {tuple(new_pixel_list)} (G={char_code})")
                print("-" * 60)
        
        # Если символы кончились - очищаем конец пробелами
        else:
            new_pixel_list[1] = 32 # 32 = ASCII пробел
            pixels[x, y] = tuple(new_pixel_list)

    try:
        img.save(output_path)
        return True
    except Exception as e:
        print(f" Ошибка сохранения: {e}")
        return False

#Проверка декодирование
def decode_green_check(image_path, keys_path):
    print("\n" + "-" * 60)
    print("Декодирование из закодированного файла")
    
    try:
        img = Image.open(image_path)
        keys = load_keys(keys_path)
        if not keys: return
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    message = []
    print(f"Чтение из зеленого канала (G)...")

    for i, (x, y) in enumerate(keys):
        if x >= img.width or y >= img.height:
            continue
        
        pixel = img.getpixel((x, y))
        green_val = pixel[1]
        message.append(chr(green_val))

    final_msg = "".join(message).rstrip()
    print(f"\nРезультат проверки: '{final_msg}'")


def main():
    # Файлы
    source_img = "new15.png"
    keys_file = "keys15.txt"
    encoded_img = "new15.png"

    # 1. Выполняем задание 1.1
    decode_blue(source_img, keys_file)

    # 2. Выполняем задание 1.2
    user_msg = input("\nВведите сообщение для кодирования: ")
    
    if user_msg:
        success = encode_green(source_img, keys_file, user_msg, encoded_img)
        
        # 3. Если закодировалось успешно - сразу проверяем
        if success:
            decode_green_check(encoded_img, keys_file)
    else:
        print("Сообщение пустое. Кодирование пропущено.")

if __name__ == "__main__":
    main()