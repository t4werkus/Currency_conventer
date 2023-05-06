import sys


def convertor():
    f = open("Currncy 2023-03-04").readlines()  # считывание файла с ЦБ
    rus = open("Currency names").readlines()  # считывание доп. файла с названиями валют на русском языке, без него
    # поддержки русского языка нет
    valute = {}  # словарь, где будут храниться валюты и их курс
    nominal = {}  # словарь, где будет храниться номинал валют
    valut, valut1, count, volume = "0", "0", 0, - 1
    fl, fl1 = True, False  # флаги для русского языка
    sys.stdout.write("Дата: " + f[1][13:23] + "\n\n")  # вывод даты актуальности файла валют
    for i in range(12, 356, 9):
        nominal[rus[count]] = f[i - 2].count("1") * (10 ** f[i - 2].count("0"))  # заполнение словаря с номиналами валют
        valute[rus[count]] = float(float(f[i][-9:-2]) / float(nominal.get(rus[count])))  # заполнение цен валют за 1
        # единицу номинала
        count += 1
    while valut + "\n" not in rus:  # защита от "дурака". Не позволяет выйти из цикла пока не будет введена валюта с
        # сайта ЦБ
        valut = input("Введите первую валюту: ")
        if valut == "Российский рубль":  # курс валют сделан относительно российского рубля, поэтому нет смысла
            # переводить куда-то Российский рубль
            fl1 = True
            break
    while True:  # ввод объема валюты(выйти из цикла без ввода числа нельзя
        volume = input("Введите объем валюты: ")
        if volume.isdigit() and int(volume) > 0:
            volume = int(volume)
            break
    while valut1 + "\n" not in rus:  # ввод второй валюты(в нее мы переводим первую валюту).
        # Также стоит защита от не правильной валюты
        valut1 = input("Введите вторую валюту: ")
        if valut1 == "Российский рубль":  # если надо перевести в Российский рубль, то переводить не надо
            sys.stdout.write("\nобъем первой валюты: " + str(volume) + "\n" + "объем второй валюты: " + str(
                valute.get(valut + "\n") * volume))
            fl = False
            break
    if fl and not fl1:  # проверка вводился ли российский рубль или нет
        sys.stdout.write("\nИз " + valut + " в " + valut1 + "\n")
        sys.stdout.write("объем первой валюты: " + str(volume) + "\n" + "объем второй валюты: ")
        sys.stdout.write(str(round(valute.get(valut + "\n") * volume / valute.get(valut1 + "\n"), 2)))
    if fl1:  # проверка вводился ли российский рубль в первый раз
        sys.stdout.write("объем второй валюты: " + str(round(volume / valute.get(valut1 + "\n"), 2)))


if __name__ == '__main__':
    convertor()
