from datetime import datetime

from kivy.lang import Builder
from kivy.properties import ListProperty, OptionProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import BaseDialog

Builder.load_string(
    """
<MDLabeltitle2@MDLabel>:
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    halign: "center"
    vlighn: "center"
    fon_style: "H5"
<MDLabeltitle@MDLabel>
    theme_text_color: "Primary"
    halign: "center"
    vlighn: "center"
    fon_style: "Caption"
<ButtonBase>
    size_hint_y: None
    height: dp(40)
    MDLabel:
        id: value
        text: root.text
        theme_text_color: "Primary"
        halign: "center"
        vlighn: "center"
<AKDatePicker>:
    size_hint: None, None
    size:
        (dp(302), dp(450)) \
        if root.theme_cls.device_orientation == "portrait" \
        else (dp(450), dp(350))
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba:  0/255, 106/255, 240/255, .4
            RoundedRectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: 0/255, 106/255, 240/255, .4
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius:[(10.0, 10.0), (10.0, 10.0), (0, 0), (0, 0)]
            MDLabeltitle2:
                text: root._year_title
                markup: True
            MDLabeltitle2:
                text: root._month_title
                markup: True
            MDLabeltitle2:
                text: root._day_title
                markup: True
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: 0/255, 106/255, 240/255, .4
                Rectangle:
                    size: self.size
                    pos: self.pos
            MDLabeltitle:
                markup: True
                font_size: 20
                text: "[color=#ffffff]Год[/color]"
            MDLabeltitle:
                markup: True
                font_size: 20
                text: "[color=#ffffff]Месяц[/color]"
            MDLabeltitle:
                markup: True
                font_size: 20
                text: "[color=#ffffff]День[/color]"
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0/255, 106/255, 240/255, .4
                Rectangle:
                    size: self.size
                    pos: self.pos
            ScrollView:
                MDBoxLayout:
                    id: year_view
                    orientation: "vertical"
                    adaptive_height: True
            ScrollView:
                MDBoxLayout:
                    id: month_view
                    orientation: "vertical"
                    adaptive_height: True
            ScrollView:
                MDBoxLayout:
                    id: day_view
                    orientation: "vertical"
                    adaptive_height: True
        BoxLayout:
            size_hint_y: None
            height: dp(40)
            padding: [dp(10), 0]
            spacing: dp(10)
            md_bg_color: 0/255, 106/255, 240/255, .4
            canvas.before:
                Color:
                    rgba: 0/255, 106/255, 240/255, .4
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [(0.0, 10.0), (0.0, 10.0), (10, 10), (10, 10)]
            MDFlatButton:
                text: '[color=#ffffff]Отмена[/color]'
                markup: True
                font_size:20
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.cancel()
            MDFlatButton:
                text: '[color=#ffffff]Выбрать[/color]'
                markup: True
                font_size:20
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root._choose()
"""
)


class AKDatePicker(BaseDialog, ThemableBehavior):

    year_range = ListProperty([1930, 2021])
    month_type = OptionProperty("string", options=["string", "int"])
    _day_title = StringProperty("-")
    _month_title = StringProperty("-")
    _year_title = StringProperty("-")

    def __init__(self, callback=None, **kwargs):
        super(AKDatePicker, self).__init__(**kwargs)
        self.month_dic = {
            "1": "Янаварь",
            "2": "Февраль",
            "3": "Март",
            "4": "Апрель",
            "5": "Май",
            "6": "Июнь",
            "7": "Июль",
            "8": "Август",
            "9": "Сентябрь",
            "10": "Октябрь",
            "11": "Ноябрь",
            "12": "Декабрь",
        }

        self.callback = callback
        for x in reversed(range(self.year_range[0], self.year_range[1])):
            self.ids.year_view.add_widget(
                MDFillRoundFlatButton(text="%d" % x, on_release=self._set_year, md_bg_color=(1,1,1,0), size_hint=(1,1), font_size= 20)
            )
        for x in reversed(range(1, 13)):
            if self.month_type == "string":
                month = self.month_dic[str(x)]
            else:
                month = str(x)

            self.ids.month_view.add_widget(
               MDFillRoundFlatButton(text=month, on_release=self._set_month,md_bg_color=(1,1,1,0), size_hint=(1,1), font_size= 20)
            )
        for x in reversed(range(1, 32)):
            self.ids.day_view.add_widget(
                MDFillRoundFlatButton(text="%d" % x, on_release=self._set_day,md_bg_color=(1,1,1,0), size_hint=(1,1), font_size= 20)
            )

    def _set_day(self, instance):
        self._day_title = instance.text

    def _set_month(self, instance):
        self._month_title = instance.text

    def _set_year(self, instance):
        self._year_title = instance.text

    def on_dismiss(self):
        self._year_title = "-"
        self._month_title = "-"
        self._day_title = "-"
        return

    def _choose(self):
        if not self.callback:
            return False

        if self.month_type == "string":
            for k, v in self.month_dic.items():
                if v == self._month_title:
                    self._month_title = k
                    break

        try:
            date = datetime(
                int(self._year_title),
                int(self._month_title),
                int(self._day_title),
            )
        except BaseException:
            date = False

        self.callback(date)
        self.cancel()

    def cancel(self):
        self.dismiss()


class ButtonBase(RectangularRippleBehavior, ButtonBehavior, BoxLayout):
    text = StringProperty()