from pathlib import Path


def get_file_size(file_path):
    """
    Получить размер файла в удобном формате.

    Args:
        file_path: путь к файлу (str или Path)
        unit: 'B', 'KB', 'MB', 'GB', 'auto'

    Returns:
        tuple: (размер, единица_измерения)
    """

    path = Path(file_path)

    size_bytes = path.stat().st_size

    units = ["B", "KB", "MB", "GB", "TB"]

    # Автоматически выбираем подходящую единицу
    size = size_bytes
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return round(size, 2), units[unit_index]
