#!/usr/bin/env python3
import os
import shutil
import sys
import threading
import time
import tempfile
from pathlib import Path


def move_files_and_cleanup():
    """Основная логика перемещения файлов"""
    script_path = Path(__file__).absolute()
    script_dir = script_path.parent
    parent_dir = script_dir.parent

    print(f"Выполняю скрипт: {script_path}")

    # 1. Перемещаем app_test
    app_test_src = script_dir / 'app_test'
    app_test_dst = parent_dir / 'app_test'

    if app_test_src.exists():
        if app_test_dst.exists():
            print(f"Удаляю существующую папку: {app_test_dst}")
            shutil.rmtree(app_test_dst)
        shutil.move(str(app_test_src), str(app_test_dst))
        print(f"✓ Папка app_test перемещена")

    # 2. Перемещаем manage.py
    manage_src = script_dir / 'manage.py'
    manage_dst = parent_dir / 'manage.py'

    if manage_src.exists():
        if manage_dst.exists():
            print(f"Удаляю существующий файл: {manage_dst}")
            os.remove(manage_dst)
        shutil.move(str(manage_src), str(manage_dst))
        print(f"✓ Файл manage.py перемещён")

    # 3. Удаляем всё в текущей директории, кроме этого скрипта
    for item in script_dir.iterdir():
        if item.absolute() != script_path:
            try:
                if item.is_file():
                    os.remove(item)
                    print(f"Удалён файл: {item.name}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    print(f"Удалена папка: {item.name}")
            except Exception as e:
                print(f"Не удалось удалить {item}: {e}")

    return script_path


def self_delete(script_path):
    """Функция для самоудаления скрипта"""
    try:
        # Ждем немного, чтобы основной процесс завершился
        time.sleep(1)

        if sys.platform == "win32":
            # Windows
            import subprocess
            # Создаем командный файл для удаления
            cmd = f'''
            @echo off
            timeout /t 2 /nobreak >nul
            del /f /q "{script_path}"
            '''

            with tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.cmd',
                    delete=False,
                    encoding='utf-8'
            ) as cmd_file:
                cmd_path = cmd_file.name
                cmd_file.write(cmd)

            # Запускаем и не ждем завершения
            subprocess.Popen(
                ['cmd', '/c', cmd_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

        else:
            # Linux/Mac
            os.remove(script_path)
            print(f"Скрипт {script_path} удалён")

    except Exception as e:
        print(f"Не удалось удалить скрипт: {e}")


if __name__ == "__main__":
    try:
        # Выполняем основную логику
        script_path = move_files_and_cleanup()

        print("\n✓ Все операции выполнены успешно!")
        print("Скрипт будет удалён через 2 секунды...")

        # Запускаем самоудаление в отдельном потоке
        if sys.platform == "win32":
            # В Windows нужно использовать отдельный процесс
            import subprocess

            # Создаем простой Python скрипт для удаления
            delete_code = f'''
import os
import time
import sys
time.sleep(2)
try:
    os.remove(r"{script_path}")
    print("Скрипт удалён")
except:
    pass
sys.exit(0)
            '''

            with tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.py',
                    delete=False,
                    encoding='utf-8'
            ) as delete_script:
                delete_path = delete_script.name
                delete_script.write(delete_code)

            # Запускаем удаление в фоне
            subprocess.Popen(
                [sys.executable, delete_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )

        else:
            # В Unix-системах можно удалить сразу
            import threading

            threading.Thread(target=self_delete, args=(script_path,), daemon=True).start()

    except Exception as e:
        print(f"✗ Ошибка при выполнении: {e}")
        sys.exit(1)