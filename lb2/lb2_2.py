import os
import datetime
from PIL import Image, ImageFilter


INPUT_DIR = os.path.join("Lab2_Media", "data", "input")
OUTPUT_DIR = os.path.join("Lab2_Media", "data", "output")
LOG_FILE = os.path.join("Lab2_Media", "logs", "history.txt")


def log_action(filename, status):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{now}] Файл: {filename} | Фильтр: Unsharp Masking + Gamma | Статус: {status}\n"
    try:
        with open(LOG_FILE, 'a', encoding="UTF-8") as log:
            log.write(log_entry)
    except Exception as e:
        print(f"Не удалось записать лог: {e}")


def main():
    filename = input("Введите имя файла для обработки (например, image1.jpg или image2.png): ").strip()
    
    if not filename:
        print("Ошибка: Имя файла не может быть пустым.")
        return
        
    input_path = os.path.join(INPUT_DIR, filename)
    
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError
            
        if not os.access(input_path, os.R_OK):
            raise PermissionError
            
        print(f"Открытие файла {filename}")
        img = Image.open(input_path)
        img = img.convert("RGB")
        
        print("Применение повышения резкости (Unsharp Masking)")
        img = img.filter(ImageFilter.UnsharpMask(radius=5, percent=150, threshold=3))
        print("Применение гамма-коррекции")
        gamma = 2.2
        img = img.point(lambda i: int((i / 255.0) ** gamma * 255.0))
        
        output_path = os.path.join(OUTPUT_DIR, "result.jpg")
        img.save(output_path, "JPEG")
        print(f"Результат сохранен в {output_path}")

        log_action(filename, "Успешно")

    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        log_action(filename, "Ошибка: Файл не найден")
    
    except PermissionError:
        print(f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору")
        log_action(filename, "Ошибка доступа")
    
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        log_action(filename, "Ошибка обработки")

if __name__ == "__main__":
    main()

