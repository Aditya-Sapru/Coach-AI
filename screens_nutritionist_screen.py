# screens/nutritionist_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from nutritionist_agent import send_to_nutritionist, get_meal_plan, clear_conversation
from user_profile import load_user_profile
from kivy.graphics import Color, RoundedRectangle
import fpdf
import os

class NutritionistScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_history = []
        self.setup_ui()
        self.user_context = None
        self.update_user_context()

    def update_user_context(self, user_data=None):
        if user_data is None:
            user_data = load_user_profile()
        
        if user_data:
            self.user_context = f"""You are a professional nutritionist. Your client's details are:
            Name: {user_data['name']}
            Age: {user_data['age']}
            Gender: {user_data['gender']}
            Weight: {user_data['weight']} kg
            Height: {user_data['height']} cm
            Experience Level: {user_data['experience_level']}
            
            Provide personalized nutrition advice based on these details. Focus on healthy, sustainable eating habits."""
            
            # If there's an active conversation, add a system message about the profile update
            if self.chat_history:
                self.chat_history.append({
                    'role': 'system',
                    'content': 'User profile has been updated. Adjusting nutrition advice accordingly.'
                })

    def get_nutrition_response(self, user_message):
        if self.user_context:
            # Include the user context in the conversation
            messages = [{'role': 'system', 'content': self.user_context}]
            messages.extend(self.chat_history)
            messages.append({'role': 'user', 'content': user_message})
            
            response = get_meal_plan(messages)
            return response
        return "Please set up your profile first."

    def setup_ui(self):
        # Main layout
        self.layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(5))

        # Top button bar
        self.button_bar = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(5),
            padding=dp(5)
        )

        # Back button
        self.back_btn = Button(
            text="Back",
            size_hint_x=0.3,
            background_color=get_color_from_hex("#9E9E9E"),
            background_normal=''
        )
        self.back_btn.bind(on_press=self.go_back)

        # Export to PDF button
        self.export_btn = Button(
            text="Export Meal Plan",
            size_hint_x=0.7,
            background_color=get_color_from_hex("#4CAF50"),
            background_normal='',
            disabled=True
        )
        self.export_btn.bind(on_press=self.export_to_pdf)

        self.button_bar.add_widget(self.back_btn)
        self.button_bar.add_widget(self.export_btn)
        self.layout.add_widget(self.button_bar)

        # Scrollable chat area
        self.scroll = ScrollView(size_hint=(1, 0.88))
        self.chat_container = GridLayout(
            cols=1, 
            size_hint_y=None, 
            spacing=dp(10), 
            padding=(dp(10), dp(10))
        )
        self.chat_container.bind(minimum_height=self.chat_container.setter('height'))
        self.scroll.add_widget(self.chat_container)

        # Bottom input area
        self.input_area = BoxLayout(
            size_hint=(1, 0.12), 
            spacing=dp(5), 
            padding=(dp(5), 0)
        )
        
        # Text input with better styling
        self.user_input = TextInput(
            hint_text="Ask your nutritionist...",
            multiline=False,
            size_hint=(0.75, 1),
            padding=(dp(10), dp(10)),
            background_color=(0.95, 0.95, 0.95, 1),
            cursor_color=(0, 0, 0, 1),
            font_size=dp(16)
        )
        
        # Send button with better styling
        self.send_btn = Button(
            text="Send",
            size_hint=(0.25, 1),
            background_color=(0.2, 0.6, 1, 1),
            background_normal=''
        )

        # Bind events
        self.send_btn.bind(on_press=self.handle_user_input)
        self.user_input.bind(on_text_validate=self.handle_user_input)
        
        # Add widgets to input area
        self.input_area.add_widget(self.user_input)
        self.input_area.add_widget(self.send_btn)

        # Add main components to layout
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.input_area)
        
        # Generate Plan button (initially hidden)
        self.plan_btn = Button(
            text="Generate Meal Plan",
            size_hint=(1, None),
            height=0,
            background_color=(0.2, 0.8, 0.2, 1),
            background_normal=''
        )
        self.plan_btn.bind(on_press=self.generate_plan)
        self.layout.add_widget(self.plan_btn)

        self.add_widget(self.layout)

        # Typing indicator
        self.typing_label = None
        
        # Store meal plan
        self.current_plan = None

        # Welcome message
        Clock.schedule_once(lambda dt: self.add_chat_message(
            "Hi! I'm your AI nutritionist. I'll help you create a personalized meal plan "
            "that aligns with your fitness goals. Let's start by discussing your dietary "
            "preferences and restrictions. Are you vegetarian, vegan, or do you eat everything?",
            sender="Nutritionist"
        ), 0.5)

    def add_chat_message(self, message, sender=""):
        # Configure bubble appearance based on sender
        bubble_color = (0.9, 0.9, 0.9, 1) if sender == "Nutritionist" else (0.7, 0.9, 1, 1)
        align = 'left' if sender == "Nutritionist" else 'right'
        prefix = "[b]Nutritionist:[/b]\n" if sender == "Nutritionist" else "[b]You:[/b]\n"
        
        # Create message bubble
        label = Label(
            text=prefix + message,
            size_hint_y=None,
            halign=align,
            valign='top',
            padding=(dp(10), dp(10)),
            markup=True,
            color=(0, 0, 0, 1),
            text_size=(self.width * 0.9, None)
        )

        # Handle text wrapping and sizing
        def update_text_size(*args):
            label.text_size = (self.scroll.width * 0.8, None)
            label.texture_update()
            label.size = label.texture_size
            label.pos = (dp(10), 0) if sender == "Nutritionist" else (self.scroll.width - label.width - dp(10), 0)

            # Update bubble background
            with label.canvas.before:
                label.canvas.before.clear()
                Color(*bubble_color)
                RoundedRectangle(
                    pos=label.pos,
                    size=label.size,
                    radius=[dp(15)]
                )

        label.bind(width=update_text_size)
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1] + dp(20)))
        self.scroll.bind(width=update_text_size)

        # Add message to chat
        self.chat_container.add_widget(label)
        
        # Scroll to bottom
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0))

    def show_typing_indicator(self):
        if not self.typing_label:
            self.typing_label = Label(
                text="[i]Nutritionist is typing...[/i]",
                size_hint_y=None,
                halign='left',
                markup=True,
                height=dp(30),
                color=(0.5, 0.5, 0.5, 1)
            )
            self.chat_container.add_widget(self.typing_label)
            Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0))

    def hide_typing_indicator(self):
        if self.typing_label and self.typing_label in self.chat_container.children:
            self.chat_container.remove_widget(self.typing_label)
            self.typing_label = None

    def handle_user_input(self, instance):
        message = self.user_input.text.strip()
        if not message:
            return

        # Clear input
        self.user_input.text = ""
        
        # Add user message to chat
        self.add_chat_message(message, sender="You")

        # Show typing indicator
        self.show_typing_indicator()

        # Process message and get response
        def get_response(dt):
            response = self.get_nutrition_response(message)
            self.hide_typing_indicator()
            self.add_chat_message(response, sender="Nutritionist")

            # Check if ready to generate plan
            if "ready to generate" in response.lower():
                self.plan_btn.height = dp(50)
                self.plan_btn.disabled = False
            
        Clock.schedule_once(get_response, 1)

    def generate_plan(self, instance):
        self.show_typing_indicator()
        user_data = load_user_profile()
        
        def create_plan(dt):
            plan = get_meal_plan(user_data)
            self.hide_typing_indicator()
            self.add_chat_message(plan, sender="Nutritionist")
            self.plan_btn.disabled = True
            self.plan_btn.height = 0
            self.current_plan = plan
            self.export_btn.disabled = False
            
        Clock.schedule_once(create_plan, 1)

    def export_to_pdf(self, instance):
        if not self.current_plan:
            return

        # Create PDF
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="Your Personalized Meal Plan", ln=1, align='C')
        
        # Add user info
        pdf.set_font("Arial", size=12)
        user_data = load_user_profile()
        pdf.cell(200, 10, txt=f"Name: {user_data.get('name', '')}", ln=1, align='L')
        pdf.cell(200, 10, txt=f"Age: {user_data.get('age', '')}", ln=1, align='L')
        pdf.cell(200, 10, txt=f"Experience Level: {user_data.get('experience_level', '')}", ln=1, align='L')
        
        # Add meal plan content
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=self.current_plan)
        
        # Save PDF
        if not os.path.exists('exports'):
            os.makedirs('exports')
        pdf_path = os.path.join('exports', f'meal_plan_{user_data.get("name", "user")}.pdf')
        pdf.output(pdf_path)
        
        # Show confirmation message
        self.add_chat_message(
            f"Your meal plan has been exported to: {pdf_path}",
            sender="Nutritionist"
        )

    def go_back(self, instance):
        self.manager.current = 'home'

    def on_leave(self):
        # Keep conversation history
        pass 