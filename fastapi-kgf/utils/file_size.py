from pathlib import Path

KB = 1024


def get_file_size(file_path: Path) -> str:
    """
    Получить размер файла в удобном формате.

    Args:
        file_path: путь к файлу (str или Path)

    Returns:
        str: размер
    """
    size_bytes = file_path.stat().st_size

    units = ["B", "KB", "MB", "GB", "TB"]

    # Автоматически выбираем подходящую единицу
    current_value: float = float(size_bytes)
    unit_index = 0

    while current_value >= KB and unit_index < len(units) - 1:
        current_value = current_value / KB  # Делим float
        unit_index += 1

    return f"{round(current_value, 2)} {units[unit_index]}"
