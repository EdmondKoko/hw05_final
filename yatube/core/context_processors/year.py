import datetime


def year(request):
    """Контекст-процессор,
    обавляющий текущий год на все страницы в переменную {{year}}."""
    return {
        'year': datetime.datetime.now().year
    }
