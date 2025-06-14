from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from coach_agent import get_workout_plan
from nutritionist_agent import get_meal_plan
from user_profile import load_user_profile, save_user_profile, user_profile_exists
from screens_coach_screen import CoachScreen
from screens_nutritionist_screen import NutritionistScreen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from functools import partial

# Set window color
Window.clearcolor = get_color_from_hex("#1A1A1A")

# Custom styles
COLORS = {
    'background': "#1A1A1A",  # Dark background
    'panel': "#252525",       # Slightly lighter panels
    'accent': "#00A6ED",      # Electric blue
    'accent2': "#FF3D00",     # Warning orange
    'text': "#E0E0E0",        # Light gray text
    'success': "#00C853",     # Success green
    'button': "#303030",      # Button background
    'input_bg': "#2A2A2A",    # Input background
}

class StylizedButton(Button):
    def __init__(self, **kwargs):
        super(StylizedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex(COLORS['button'])
        self.color = get_color_from_hex(COLORS['text'])
        self.bold = True
        self.border = (0, 0, 0, 0)
        
        # Bind hover effects
        self.bind(on_press=partial(self.on_button_state, 'down'))
        self.bind(on_release=partial(self.on_button_state, 'normal'))

    def on_button_state(self, state, instance):
        if state == 'down':
            self.background_color = get_color_from_hex(COLORS['accent'])
        else:
            self.background_color = get_color_from_hex(COLORS['button'])

class StylizedTextInput(TextInput):
    def __init__(self, **kwargs):
        super(StylizedTextInput, self).__init__(**kwargs)
        self.background_color = get_color_from_hex(COLORS['input_bg'])
        self.foreground_color = get_color_from_hex(COLORS['text'])
        self.cursor_color = get_color_from_hex(COLORS['accent'])
        self.padding = [15, 10]
        self.font_size = '16sp'

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        # Main dark panel
        with self.canvas.before:
            Color(*get_color_from_hex(COLORS['panel']))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        # Title
        title = Label(
            text="[b]Fitness App[/b]",
            markup=True,
            size_hint_y=None,
            height=60,
            font_size='24sp',
            color=get_color_from_hex(COLORS['accent'])
        )
        layout.add_widget(title)

        # Subtitle
        subtitle = Label(
            text="Enter Your Profile Details",
            size_hint_y=None,
            height=30,
            font_size='16sp',
            color=get_color_from_hex(COLORS['text'])
        )
        layout.add_widget(subtitle)

        # Input fields with tactical styling
        self.name_input = StylizedTextInput(hint_text='Name', multiline=False, size_hint_y=None, height=45)
        self.age_input = StylizedTextInput(hint_text='Age', multiline=False, input_filter='int', size_hint_y=None, height=45)
        self.gender_input = StylizedTextInput(hint_text='Gender (M/F/Other)', multiline=False, size_hint_y=None, height=45)
        self.weight_input = StylizedTextInput(hint_text='Weight (kg)', multiline=False, input_filter='float', size_hint_y=None, height=45)
        self.height_input = StylizedTextInput(hint_text='Height (cm)', multiline=False, input_filter='float', size_hint_y=None, height=45)
        self.exp_input = StylizedTextInput(hint_text='Experience Level (Beginner/Intermediate/Advanced)', multiline=False, size_hint_y=None, height=45)

        for input_field in [self.name_input, self.age_input, self.gender_input, 
                          self.weight_input, self.height_input, self.exp_input]:
            layout.add_widget(input_field)

        save_btn = StylizedButton(
            text="Save & Continue",
            size_hint_y=None,
            height=50,
            background_color=get_color_from_hex(COLORS['accent'])
        )
        save_btn.bind(on_press=self.save_and_continue)
        layout.add_widget(save_btn)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def save_and_continue(self, instance):
        user_data = {
            "name": self.name_input.text.strip(),
            "age": self.age_input.text.strip(),
            "gender": self.gender_input.text.strip(),
            "weight": self.weight_input.text.strip(),
            "height": self.height_input.text.strip(),
            "experience_level": self.exp_input.text.strip(),
        }
        if all(user_data.values()):
            save_user_profile(user_data)
            self.manager.get_screen('home').load_user_data()
            self.manager.current = 'home'
        else:
            instance.text = "Please fill all fields!"
            from kivy.clock import Clock
            def reset_text(dt):
                instance.text = "Save & Continue"
            Clock.schedule_once(reset_text, 2)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        # Main dark panel
        with self.canvas.before:
            Color(*get_color_from_hex(COLORS['panel']))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Top bar with options button and centered title
        top_bar = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        # Left section for options button
        left_section = BoxLayout(size_hint_x=0.2)
        options_btn = StylizedButton(
            text="Options",
            size_hint_x=None,
            width=100,
            background_color=get_color_from_hex(COLORS['button'])
        )
        options_btn.bind(on_press=self.go_to_options)
        left_section.add_widget(options_btn)
        
        # Center section for title
        title = Label(
            text="[b]Fitness App[/b]",
            markup=True,
            font_size='20sp',
            color=get_color_from_hex(COLORS['accent']),
            size_hint_x=0.6,
            halign='center',
            valign='middle'
        )
        title.bind(size=lambda *_: setattr(title, 'text_size', title.size))
        
        # Right section for balance
        right_section = BoxLayout(size_hint_x=0.2)
        
        # Add all sections to top bar
        top_bar.add_widget(left_section)
        top_bar.add_widget(title)
        top_bar.add_widget(right_section)
        
        self.layout.add_widget(top_bar)

        # Profile panel
        profile_panel = BoxLayout(orientation='vertical', size_hint_y=None, height=220, 
                                padding=15, spacing=8)
        with profile_panel.canvas.before:
            Color(*get_color_from_hex(COLORS['button']))
            self.profile_rect = RoundedRectangle(pos=profile_panel.pos, 
                                               size=profile_panel.size, radius=[10])
        profile_panel.bind(size=self._update_profile_rect, pos=self._update_profile_rect)

        # Profile labels
        self.labels_box = BoxLayout(orientation='vertical', spacing=5)
        self.name_label = Label(text="", size_hint_y=None, height=30, halign='left')
        self.age_label = Label(text="", size_hint_y=None, height=30, halign='left')
        self.gender_label = Label(text="", size_hint_y=None, height=30, halign='left')
        self.weight_label = Label(text="", size_hint_y=None, height=30, halign='left')
        self.height_label = Label(text="", size_hint_y=None, height=30, halign='left')
        self.exp_label = Label(text="", size_hint_y=None, height=30, halign='left')

        for label in [self.name_label, self.age_label, self.gender_label,
                     self.weight_label, self.height_label, self.exp_label]:
            label.bind(size=self._update_label_width)
            self.labels_box.add_widget(label)

        profile_panel.add_widget(self.labels_box)
        self.layout.add_widget(profile_panel)

        # Goals input
        self.goals_input = StylizedTextInput(
            hint_text="Enter your goals or other info here...",
            multiline=True,
            size_hint_y=0.4
        )
        self.layout.add_widget(self.goals_input)

        # Action buttons
        btn_box = BoxLayout(size_hint_y=None, height=50, spacing=20)
        coach_btn = StylizedButton(
            text='Ask Coach',
            background_color=get_color_from_hex(COLORS['accent'])
        )
        coach_btn.bind(on_press=self.go_to_coach)
        
        nutrition_btn = StylizedButton(
            text='Ask Nutritionist',
            background_color=get_color_from_hex(COLORS['accent2'])
        )
        nutrition_btn.bind(on_press=self.go_to_nutrition)
        
        btn_box.add_widget(coach_btn)
        btn_box.add_widget(nutrition_btn)
        self.layout.add_widget(btn_box)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_profile_rect(self, instance, value):
        self.profile_rect.pos = instance.pos
        self.profile_rect.size = instance.size

    def _update_label_width(self, instance, value):
        instance.text_size = (instance.width, None)

    def load_user_data(self):
        profile = load_user_profile()
        if profile:
            self.name_label.text = f"[color={COLORS['accent']}][b]Name:[/b][/color] {profile.get('name', '')}"
            self.age_label.text = f"[color={COLORS['accent']}][b]Age:[/b][/color] {profile.get('age', '')}"
            self.gender_label.text = f"[color={COLORS['accent']}][b]Gender:[/b][/color] {profile.get('gender', '')}"
            self.weight_label.text = f"[color={COLORS['accent']}][b]Weight:[/b][/color] {profile.get('weight', '')} kg"
            self.height_label.text = f"[color={COLORS['accent']}][b]Height:[/b][/color] {profile.get('height', '')} cm"
            self.exp_label.text = f"[color={COLORS['accent']}][b]Experience Level:[/b][/color] {profile.get('experience_level', '')}"

            for lbl in [self.name_label, self.age_label, self.gender_label,
                       self.weight_label, self.height_label, self.exp_label]:
                lbl.markup = True
                lbl.color = get_color_from_hex(COLORS['text'])

            self.goals_input.text = profile.get("goals", "")

    def go_to_coach(self, instance):
        self.manager.current = 'coach'

    def go_to_nutrition(self, instance):
        self.manager.current = 'nutrition'

    def go_to_options(self, instance):
        self.manager.current = 'edit_profile'


class EditProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(EditProfileScreen, self).__init__(**kwargs)
        
        # Main dark panel
        with self.canvas.before:
            Color(*get_color_from_hex(COLORS['panel']))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        # Title
        title = Label(
            text="[b]Edit Profile[/b]",
            markup=True,
            size_hint_y=None,
            height=50,
            font_size='20sp',
            color=get_color_from_hex(COLORS['accent'])
        )
        layout.add_widget(title)

        # Input fields
        self.name_input = StylizedTextInput(hint_text='Name', multiline=False, size_hint_y=None, height=45)
        self.age_input = StylizedTextInput(hint_text='Age', multiline=False, input_filter='int', size_hint_y=None, height=45)
        self.gender_input = StylizedTextInput(hint_text='Gender (M/F/Other)', multiline=False, size_hint_y=None, height=45)
        self.weight_input = StylizedTextInput(hint_text='Weight (kg)', multiline=False, input_filter='float', size_hint_y=None, height=45)
        self.height_input = StylizedTextInput(hint_text='Height (cm)', multiline=False, input_filter='float', size_hint_y=None, height=45)
        self.exp_input = StylizedTextInput(hint_text='Experience Level (Beginner/Intermediate/Advanced)', multiline=False, size_hint_y=None, height=45)

        for input_field in [self.name_input, self.age_input, self.gender_input,
                          self.weight_input, self.height_input, self.exp_input]:
            layout.add_widget(input_field)

        # Button box
        btn_box = BoxLayout(size_hint_y=None, height=50, spacing=20)
        
        cancel_btn = StylizedButton(
            text="Cancel",
            background_color=get_color_from_hex(COLORS['button'])
        )
        cancel_btn.bind(on_press=self.cancel_edit)

        save_btn = StylizedButton(
            text="Save Changes",
            background_color=get_color_from_hex(COLORS['accent'])
        )
        save_btn.bind(on_press=self.save_changes)

        btn_box.add_widget(cancel_btn)
        btn_box.add_widget(save_btn)
        layout.add_widget(btn_box)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_pre_enter(self):
        profile = load_user_profile()
        if profile:
            self.name_input.text = profile.get('name', '')
            self.age_input.text = str(profile.get('age', ''))
            self.gender_input.text = profile.get('gender', '')
            self.weight_input.text = str(profile.get('weight', ''))
            self.height_input.text = str(profile.get('height', ''))
            self.exp_input.text = profile.get('experience_level', '')

    def save_changes(self, instance):
        user_data = {
            "name": self.name_input.text.strip(),
            "age": self.age_input.text.strip(),
            "gender": self.gender_input.text.strip(),
            "weight": self.weight_input.text.strip(),
            "height": self.height_input.text.strip(),
            "experience_level": self.exp_input.text.strip(),
        }
        if all(user_data.values()):
            save_user_profile(user_data)
            # Instantly update home screen
            home_screen = self.manager.get_screen('home')
            home_screen.load_user_data()
            
            # Update AI agents' context
            coach_screen = self.manager.get_screen('coach')
            nutritionist_screen = self.manager.get_screen('nutrition')
            coach_screen.update_user_context(user_data)
            nutritionist_screen.update_user_context(user_data)
            
            self.manager.current = 'home'
        else:
            instance.text = "Please fill all fields!"
            from kivy.clock import Clock
            def reset_text(dt):
                instance.text = "Save Changes"
            Clock.schedule_once(reset_text, 2)

    def cancel_edit(self, instance):
        self.manager.current = 'home'


class FitnessApp(App):
    def build(self):
        # Use FadeTransition for a more polished look
        sm = ScreenManager(transition=FadeTransition())

        if user_profile_exists():
            home = HomeScreen(name='home')
            sm.add_widget(home)
            sm.add_widget(CoachScreen(name='coach'))
            sm.add_widget(NutritionistScreen(name='nutrition'))
            sm.add_widget(EditProfileScreen(name='edit_profile'))
            home.load_user_data()
            sm.current = 'home'
        else:
            sm.add_widget(LoginScreen(name='login'))
            sm.add_widget(HomeScreen(name='home'))
            sm.add_widget(CoachScreen(name='coach'))
            sm.add_widget(NutritionistScreen(name='nutrition'))
            sm.add_widget(EditProfileScreen(name='edit_profile'))
            sm.current = 'login'

        return sm


if __name__ == '__main__':
    FitnessApp().run()
