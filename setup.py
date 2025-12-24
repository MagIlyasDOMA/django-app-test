import os
from pathlib import Path

CODE = f'''#!/usr/bin/env python3
import os, shutil, sys
from pathlib import Path


def delete_script():
    """Функция для удаления скрипта"""
    try:
        script_path = os.path.abspath(sys.argv[0])
        if os.path.exists(script_path):
            os.remove(script_path)
            print(f"Скрипт удален: {{script_path}}")
    except Exception as e:
        print(f"Ошибка при удалении: {{e}}")


def main():
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    project_dir = Path('{__file__.replace("\\", "/")}').resolve().parent

    # 1. Перемещаем app_test
    app_test_src = project_dir / 'app_test'
    app_test_dst = project_dir.parent / 'app_test'

    if app_test_src.exists():
        if app_test_dst.exists():
            shutil.rmtree(app_test_dst)
        shutil.move(str(app_test_src), str(app_test_dst))
        print("✅ Папка app_test перемещена")

    # 2. Перемещаем manage.py
    manage_src = project_dir / 'manage.py'
    manage_dst = project_dir.parent / 'manage.py'

    if manage_src.exists():
        if manage_dst.exists():
            os.remove(manage_dst)
        shutil.move(str(manage_src), str(manage_dst))
        print("✅ Файл manage.py перемещён")

    # 3. Добавляем в .gitignore
    gitignore_path = script_dir / '.gitignore'
    if gitignore_path.exists():
        with open(gitignore_path, "a+", encoding='utf-8') as f:
            content = f.read()
            if content and not content.endswith('\\n'):
                f.write('\\n')
            if 'app_test' not in content:
                f.write('/app_test/\\n')
            if 'manage.py' not in content:
                f.write('manage.py\\n')

    print("\\n✅ Все операции выполнены успешно!")

    try:
        shutil.rmtree(project_dir)
        print("\\n✅ Папка удалена")
    except Exception as e:
        print(f"\\n❌ Не удалось удалить папку: {{e}}")


if __name__ == "__main__":
    main()
    delete_script()
'''


def main():
    parent_dir = Path(__file__).resolve().parent.parent
    script_path = parent_dir / 'djt_setup.py'

    # Записываем скрипт с правильной кодировкой
    with open(script_path, 'w', encoding='utf-8') as script:
        script.write(CODE)

    os.chdir(parent_dir)
    os.system(f'python "{script_path}"')


if __name__ == '__main__':
    main()