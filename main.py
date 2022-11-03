from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class FirstScreen(Screen):
    def __init__(self,**kwargs):
        super(FirstScreen, self).__init__(**kwargs)    
        layout=BoxLayout(orientation="vertical",size_hint_y= None)
        layout.bind(minimum_height=layout.setter('height'))                
        for i in range(50):
                btn = Button(text="Button"+str(i),
                             id=str(i),
                             size_hint=(None, None),
                             on_press=self.Press_auth)               #<<<<<<<<<<<<<<<<           
                layout.add_widget(btn)
        root = ScrollView()
        root.add_widget(layout)
        self.add_widget(root)

    def Press_auth(self,instance):     
        print(str(instance))

class TestScreenManager(ScreenManager):
    def __init__(self,  **kwargs):
        super(TestScreenManager,  self).__init__(**kwargs)
        self.add_widget(FirstScreen())

class ExampleApp(App):
    def build(self):           
        return TestScreenManager()


app = ExampleApp()
app.run()