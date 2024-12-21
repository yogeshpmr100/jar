import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import pyautogui
import time
from urllib.parse import quote

class Jarvis:
    def __init__(self):
        print("Starting Jarvis...")
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.setup_voice()
        self.is_active = True
        self.current_path = "C:\\"  # Default starting path
        self.current_items = []

    def setup_voice(self):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 175)

    def speak(self, text):
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("\nListening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=7)
                print("Processing...")
                command = self.recognizer.recognize_google(audio, language='en-US')
                print(f"You said: {command}")
                return command.lower()
        except:
            return None

    def open_this_pc(self):
        """Open This PC and list drives"""
        try:
            # Open This PC directly
            os.system('explorer shell:MyComputerFolder')
            time.sleep(1)
            
            # Get and list available drives
            drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:")]
            self.current_items = drives
            
            self.speak("Here are the available drives:")
            for idx, drive in enumerate(drives, 1):
                print(f"{idx}. {drive}")
            
            return drives
        except Exception as e:
            print(f"Error opening This PC: {str(e)}")
            return []

    def navigate_to_drive(self, drive_number):
        """Navigate to specific drive"""
        try:
            drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:")]
            idx = int(drive_number) - 1
            
            if 0 <= idx < len(drives):
                selected_drive = drives[idx]
                # Open the drive and focus on it
                os.system(f'explorer {selected_drive}')
                self.current_path = selected_drive
                self.speak(f"Opening drive {selected_drive}")
                
                # List contents of the drive
                self.list_current_directory()
            else:
                self.speak("Invalid drive number")
        except Exception as e:
            print(f"Error navigating to drive: {str(e)}")

    def list_current_directory(self):
        """List contents of current directory"""
        try:
            items = os.listdir(self.current_path)
            self.current_items = items
            
            self.speak(f"Contents of {self.current_path}:")
            for idx, item in enumerate(items, 1):
                print(f"{idx}. {item}")
            
            return items
        except Exception as e:
            print(f"Error listing directory: {str(e)}")
            return []

    def navigate_to_folder(self, folder_number):
        """Navigate to specific folder in current directory"""
        try:
            items = self.current_items
            idx = int(folder_number) - 1
            
            if 0 <= idx < len(items):
                selected_item = items[idx]
                new_path = os.path.join(self.current_path, selected_item)
                
                if os.path.isdir(new_path):
                    self.current_path = new_path
                    os.system(f'explorer "{new_path}"')
                    self.speak(f"Opening folder {selected_item}")
                    self.list_current_directory()
                else:
                    os.startfile(new_path)
                    self.speak(f"Opening file {selected_item}")
            else:
                self.speak("Invalid item number")
        except Exception as e:
            print(f"Error navigating to folder: {str(e)}")

    def go_back(self):
        """Go back to parent directory"""
        try:
            parent_path = os.path.dirname(self.current_path)
            if parent_path and parent_path != self.current_path:
                self.current_path = parent_path
                os.system(f'explorer "{parent_path}"')
                self.speak("Going back")
                self.list_current_directory()
            else:
                self.speak("Already at root directory")
        except Exception as e:
            print(f"Error going back: {str(e)}")

    def execute_command(self, command):
        try:
            # This PC navigation
            if 'this pc' in command:
                self.open_this_pc()
                return

            # Drive navigation
            if 'drive' in command and any(char.isdigit() for char in command):
                drive_num = ''.join(filter(str.isdigit, command))
                self.navigate_to_drive(drive_num)
                return

            # Folder navigation
            if 'open folder' in command or 'folder' in command:
                folder_num = ''.join(filter(str.isdigit, command))
                if folder_num:
                    self.navigate_to_folder(folder_num)
                return

            # Go back
            if 'go back' in command or 'back' in command:
                self.go_back()
                return

            # List contents
            if 'list' in command or 'show contents' in command:
                self.list_current_directory()
                return

            # Google search
            if 'search' in command:
                search_query = command.replace('search', '').strip()
                search_url = f'https://www.google.com/search?q={quote(search_query)}'
                os.system(f'start chrome {search_url}')
                self.speak(f"Searching for {search_query}")
                return

            self.speak("Please specify what you'd like me to do")

        except Exception as e:
            print(f"Error: {str(e)}")
            self.speak("I couldn't process that command")

    def run(self):
        self.speak("Ready for your commands")
        
        while self.is_active:
            command = self.listen()
            if command:
                if 'exit' in command or 'quit' in command:
                    self.speak("Goodbye!")
                    break
                self.execute_command(command)
            time.sleep(0.1)

def main():
    print("=" * 50)
    print("JARVIS - Voice Assistant")
    print("=" * 50)
    print("\nYou can say:")
    print("- 'this pc' (shows drives)")
    print("- 'open drive 1' (or 2, 3, etc.)")
    print("- 'open folder 1' (or any number)")
    print("- 'go back'")
    print("- 'list' or 'show contents'")
    print("- 'search [anything]'")
    print("- 'quit' to exit")
    
    jarvis = Jarvis()
    jarvis.run()

if __name__ == "__main__":
    main()
