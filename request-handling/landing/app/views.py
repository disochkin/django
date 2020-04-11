from collections import Counter

import request as request
from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing_type = request.GET.get('from-landing')
    counter_click[from_landing_type] += 1
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    landing_type = request.GET.get('ab-test-arg')
    counter_show[landing_type] += 1
    if landing_type == 'original':
        return render_to_response('landing.html')
    else:
        return render_to_response('landing_alternate.html')


def safe_div(x,y):
    if y == 0:
        return 0
    return x / y


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    test_conversion = safe_div(counter_click["test"], counter_show["test"])
    original_conversion = safe_div(counter_click["original"], counter_show["original"])
    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
