import dearpygui.dearpygui as dpg
import sys
import json
import urllib
import urllib.request


class Convertor:

    def __init__(self):
        self.__default_value_first = "Доллар США"
        self.__default_value_second = "Российский рубль"
        self.__volume = 1
        self.__valute = {}
        self.__names_cur = []
        self.__nominal = {}
        self.__names_cur = [i.strip() for i in open("Currency names").readlines()]
        self.__cur_short = [i.strip() for i in open("Currency names short").readlines()]
        self.__result = 0

    def update_result(self, *args, **kwargs):
        self.__result = str(round(self.__volume * self.__valute.get(self.__default_value_first) /
                            self.__valute.get(self.__default_value_second), 2))
        dpg.set_value("text", self.__result)
    def input_int_callback(self, sender, app_data, *args, **kwargs):
        self.__volume = app_data
        sys.stdout.write(str(app_data))
        self.update_result()

    def update_default_value(self, sender, *args, **kwargs):
        if sender == 1:
            self.__default_value_first = dpg.get_value(sender)
        else:
            self.__default_value_second = dpg.get_value(sender)
        self.update_result()


    def swap_combos(self, *args, **kwargs):
        combo1_value = dpg.get_value(1)
        combo2_value = dpg.get_value(2)

        dpg.set_value(1, combo2_value)
        dpg.set_value(2, combo1_value)

        self.update_default_value(1)
        self.update_default_value(2)
        self.update_result()

    def get_response(self, url, *args, **kwargs):
        oper_url = urllib.request.urlopen(url)
        json_data = ""
        if oper_url.getcode() == 200:
            data = oper_url.read()
            json_data = json.loads(data)
        else:
            print("Error receiving data", oper_url.getcode())
        return json_data


    def update_data(self, *args, **kwargs):
        file_json = self.get_response("https://www.cbr-xml-daily.ru/daily_json.js")

        for i in range(44):
            if i == 28:
                self.__nominal[self.__names_cur[i]] = 1
                self.__valute[self.__names_cur[i]] = 1
                continue
            self.__nominal[self.__names_cur[i]] = file_json["Valute"][self.__cur_short[i]]["Nominal"]
            self.__valute[self.__names_cur[i]] = file_json["Valute"][self.__cur_short[i]]["Value"] / self.__nominal[self.__names_cur[i]]
        self.update_result()
    def get_result(self):
        return self.__result
    def get_names_cur(self):
        return self.__names_cur
    def get_default_value_first(self):
        return self.__default_value_first
    def get_default_value_second(self):
        return self.__default_value_second
def convertor():

    dpg.create_context()

    dpg.create_viewport(title='test', width=750, height=300)

    with dpg.font_registry():
        with dpg.font("RobotoCondensed-Bold.ttf", 20, default_font=True, tag="Default font"):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    test = Convertor()
    width, height, channels, data = dpg.load_image("swap.png")
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")
    with dpg.window(width=800, height=400, tag="Primary Window"):
        dpg.add_text(str(test.get_result()), pos=(395, 130), tag="text")
        test.update_data()
        dpg.add_text(
            "Привет! Добро пожаловать в наш конвертер валют. "
            "\nЗдесь вы можете легко и удобно выполнять обмен валюты и получать актуальные курсы обмена. "
            "\nВыберите валюты для конвертации и введите сумму, и мы позаботимся о остальном.")
        dpg.add_combo(items=test.get_names_cur(), callback=test.update_default_value, width=353,
                      default_value=test.get_default_value_first(), tag=1, pos=(0, 100))

        dpg.add_image_button(label="swap", callback=test.swap_combos, pos=(360, 100), texture_tag="texture_tag",
                             height=20, width=20)

        dpg.add_combo(items=test.get_names_cur(), callback=test.update_default_value, width=353, pos=(395, 100),
                      default_value=test.get_default_value_second(), tag=2)

        dpg.add_input_int(step=0, callback=test.input_int_callback, default_value=1, width=353, pos=(0, 130), max_value=2 ** 32)

    dpg.bind_font("Default font")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    convertor()
