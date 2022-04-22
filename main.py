from kivy.config import Config
#Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 350)
Config.set('graphics', 'height', 640)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from database import Costs, Orders, WeeklyOrders


class Container(FloatLayout):

    def display(self):
        self.ord_input.text = Costs().select_ord_cost()
        self.pos_input.text = Costs().select_pos_cost()
        return self.ord_input.text, self.pos_input.text

    def ord_cost_input(self):
        self.ord_input.foreground_color = .0, .87, .12, 1
        return self.ord_input.text

    def pos_cost_input(self):
        self.pos_input.foreground_color = .0, .87, .12, 1
        return self.pos_input.text

    def ord_and_pos(self):
        try:
            self.cost_tpl = (float(self.ord_cost_input()),
                         float(self.pos_cost_input()))
            Costs().delete_costs()
            Costs().update_costs(self.cost_tpl)
        except ValueError:
            pass

    def input_order(self):
        Orders().select_orders(float(self.ord_input.text),
                             float(self.pos_input.text),
                             int(self.last_ord_input.text))
        self.last_ord_input.text = ''

    def output_order(self):
        ord = Orders().select_orders_today()[1]
        pos = Orders().select_orders_today()[2]
        date = Orders().select_orders_today()[3]
        inc = Orders().select_orders_today()[4]
        self.today_output.text = f'\n  Сегодня, {date},\n  вами собрано ' \
                                 f'{ord} ' \
                                 f'заказов.\n' \
                                 f'  {pos} позиций.\n  Ваш доход составляет' \
                                 f' {inc} руб.'
        WeeklyOrders().update_weekly_orders()
        return self.today_output.text

    def output_weekly_orders(self):
        past = ''
        for row in WeeklyOrders().select_weekly_orders():
            past += f'  С {row[3]} по {row[4]}   {row[1]} заказов,\n  ' \
                   f'{row[2]} позиций. Заработано {row[5]}\n\n'
        return past

    def reset_today(self):
        Orders().delete_orders_today()


class MyApp(App):
    def build(self):
        return Container()


if __name__ == "__main__":
    Costs().create_costs()
    Orders().create_orders()
    WeeklyOrders().create_weekly_orders()
    MyApp().run()
