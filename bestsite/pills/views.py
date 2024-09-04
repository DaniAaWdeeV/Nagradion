from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


from datetime import date, timedelta
from time import localtime



def index(request):
    # cur_date = date(2024, 8, 1)
    cur_date = date.today()
    test_date = date(2024, 7, 31)

    if cur_date < test_date:
        # raise DateError('Current date before the date we know pills')
        return HttpResponse("Ошибка: Обратный ход времени!")

    pills_onboard = (16 + 8 + 1) * 30 + 3  # Справедливо на 31.07.2024, в 31.07.2024 еще не принимал
    doza = 4

    reserve = timedelta(days=((pills_onboard - doza * (cur_date - test_date).days) // doza))

    expiration_date = cur_date + reserve

    return HttpResponse(f"На {cur_date} в наличии {pills_onboard - doza * abs(cur_date - test_date).days} таблеток, что соответсвует"
                        f" {(pills_onboard - doza * abs(cur_date - test_date).days) // doza} дням лечения. Таблетки закончатся {expiration_date}")
