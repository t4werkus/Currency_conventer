import dearpygui.dearpygui as dpg
import sys
import json
import urllib
import urllib.request


class Convertor:

    def __init__(self):
        self.default_value_first = "Доллар США"
        self.default_value_second = "Российский рубль"
        self.volume = 1
        self.valute = {}
        self.names_cur = []
        self.nominal = {}
        self.names_cur = [i.strip() for i in open("Currency names").readlines()]
        self.cur_short = [i.strip() for i in open("Currency names short").readlines()]
        self.result = 0

    def update_result(self, *args, **kwargs):
        self.result = str(round(self.volume * self.valute.get(self.default_value_first) /
                            self.valute.get(self.default_value_second), 2))
        dpg.set_value("text", self.result)
    def input_int_callback(self, sender, app_data, *args, **kwargs):
        self.volume = app_data
        sys.stdout.write(str(app_data))
        self.update_result()

    def update_default_value(self, sender, *args, **kwargs):
        if sender == 1:
            self.default_value_first = dpg.get_value(sender)
        else:
            self.default_value_second = dpg.get_value(sender)
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
                self.nominal[self.names_cur[i]] = 1
                self.valute[self.names_cur[i]] = 1
                continue
            self.nominal[self.names_cur[i]] = file_json["Valute"][self.cur_short[i]]["Nominal"]
            self.valute[self.names_cur[i]] = file_json["Valute"][self.cur_short[i]]["Value"] / self.nominal[self.names_cur[i]]
        self.update_result()
def convertor():

    dpg.create_context()

    dpg.create_viewport(title='test', width=750, height=300)

    with dpg.font_registry():
        with dpg.font("RobotoCondensed-Bold.ttf", 20, default_font=True, tag="Default font"):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    test = Convertor()
    width, height, channels, data = dpg.load_image("icon-font icon-flipper-24 icon-font--size_medium")
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")
    with dpg.window(width=800, height=400, tag="Primary Window"):
        dpg.add_text(str(test.result), pos=(395, 130), tag="text")
        test.update_data()
        dpg.add_text(
            "Привет! Добро пожаловать в наш конвертер валют. "
            "\nЗдесь вы можете легко и удобно выполнять обмен валюты и получать актуальные курсы обмена. "
            "\nВыберите валюты для конвертации и введите сумму, и мы позаботимся о остальном.")
        dpg.add_combo(items=test.names_cur, callback=test.update_default_value, width=353,
                      default_value=test.default_value_first, tag=1, pos=(0, 100))

        dpg.add_image_button(label="swap", callback=test.swap_combos, pos=(360, 100), texture_tag="texture_tag",
                             height=20, width=20)

        dpg.add_combo(items=test.names_cur, callback=test.update_default_value, width=353, pos=(395, 100),
                      default_value=test.default_value_second, tag=2)

        dpg.add_input_int(step=0, callback=test.input_int_callback, default_value=1, width=353, pos=(0, 130), max_value=2 ** 32)
        #dpg.add_button(label="Конвертировать", callback=test.button_callback, pos=(0, 210))

        #dpg.add_text(str(test.result), pos=(395, 150), id="text")
    dpg.bind_font("Default font")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    convertor()
