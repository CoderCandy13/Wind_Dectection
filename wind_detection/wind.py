import tkinter as tk
from tkinter import Button
import speech_recognition as sr
import pyttsx3
import random
import time
import math
import turtle

class WindInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wind Information")

        self.wind_info_label = tk.Label(root, text="Wind Information", font=("Arial", 20))
        self.wind_info_label.pack(pady=20)

        self.direction_label = tk.Label(root, text="", font=("Arial", 18))
        self.direction_label.pack(pady=20)

        self.speed_label = tk.Label(root, text="", font=("Arial", 18))
        self.speed_label.pack(pady=20)

        self.start_button = Button(root, text="Start Voice Recognition", command=self.start_voice_recognition)
        self.start_button.pack(pady=20)

        self.stop_button = Button(root, text="Stop Voice Recognition", command=self.stop_voice_recognition)
        self.stop_button.pack(pady=20)

        # Variables to store the last known alpha value and wind speed
        self.last_alpha_value = 45  # Initial static value
        self.last_wind_speed = 0.0  # Initial static value

        # Initialize pyttsx3
        self.engine = pyttsx3.init()

        # Initialize turtle for compass display
        self.compass_turtle = turtle.Turtle()
        self.draw_compass()

        # Flag to control voice recognition
        self.voice_recognition_active = False

    def get_wind_direction(self, alpha):
        if 0 <= alpha < 45:
            return 'North'
        elif 45 <= alpha < 135:
            return 'East'
        elif 135 <= alpha < 225:
            return 'South'
        elif 225 <= alpha < 315:
            return 'West'
        else:
            return 'North'

    def handle_orientation(self, alpha):
        wind_direction = self.get_wind_direction(alpha)
        message = f"The wind is currently coming from the {wind_direction}."
        self.direction_label.config(text=message)
        self.speak(message)
        self.update_compass_direction(alpha)

    def handle_wind_speed(self, wind_speed):
        message = f"The wind speed is currently {wind_speed:.2f} meters per second."
        self.speed_label.config(text=message)
        self.speak(message)

    def speak(self, message):
        # Use pyttsx3 for speech synthesis
        self.engine.say(message)
        self.engine.runAndWait()

    def start_voice_recognition(self):
        self.speak("Hey Yeoung Sil is here to help you")
        self.voice_recognition_active = True

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening... Say 'What is the direction of the wind', 'What is the speed of the wind', 'Stop', or 'Exit'")
            while self.voice_recognition_active:
                try:
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio).lower()
                    print(f"You said: {command}")

                    if 'what is the direction of the wind' in command:
                        self.handle_orientation(self.last_alpha_value)
                    elif 'what is the speed of the wind' in command:
                        self.handle_wind_speed(self.last_wind_speed)
                    elif 'stop' in command or 'exit' in command:
                        self.stop_voice_recognition()

                except sr.UnknownValueError:
                    print("Sorry, I could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")

    def stop_voice_recognition(self):
        self.speak("Stopping voice recognition.")
        self.voice_recognition_active = False

    def update_wind_data(self):
        # Simulate updating wind data (replace this with actual logic)
        self.last_alpha_value = random.uniform(0, 360)
        self.last_wind_speed = random.uniform(0, 10)

        # Update the GUI labels and compass
        self.handle_orientation(self.last_alpha_value)
        self.handle_wind_speed(self.last_wind_speed)

        # Schedule the next update after 5 seconds
        if self.voice_recognition_active:
            self.root.after(5000, self.update_wind_data)

    def draw_compass(self):
        # Draw a simple compass using turtle
        self.compass_turtle.speed(1)
        self.compass_turtle.penup()
        self.compass_turtle.goto(0, -150)
        self.compass_turtle.pendown()
        self.compass_turtle.circle(150)

        # Draw cardinal directions
        directions = ['N', 'E', 'S', 'W']
        for angle, direction in enumerate(directions):
            self.compass_turtle.penup()
            self.compass_turtle.goto(0, 0)
            self.compass_turtle.setheading(angle * 90)
            self.compass_turtle.forward(120)
            self.compass_turtle.pendown()
            self.compass_turtle.write(direction, align="center", font=("Arial", 12, "normal"))

    def update_compass_direction(self, alpha):
        # Update the compass needle based on wind direction
        self.compass_turtle.clear()
        self.draw_compass()

        self.compass_turtle.penup()
        self.compass_turtle.goto(0, 0)
        self.compass_turtle.setheading(-alpha)  # Negative because turtle's orientation is different
        self.compass_turtle.pendown()
        self.compass_turtle.forward(80)

if __name__ == "__main__":
    root = tk.Tk()
    app = WindInfoApp(root)
    
    # Schedule the periodic update of wind data
    root.after(5000, app.update_wind_data)

    root.mainloop()
