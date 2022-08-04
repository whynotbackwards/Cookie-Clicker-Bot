import pyglet
import random
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import time

# https://colorhunt.co/palette/1c0a00361500603601cc9544
BG_COLOR_1 = '#CC9544'
BG_COLOR_2 = '#603601'
TEXT_FG = '#361500'
BUTTON_BG = TEXT_FG
BUTTON_CLICKED_BG = '#CC9544'

YN = ['Yes', 'No']

pyglet.font.add_file('fonts/Arcadepix.ttf')
pyglet.font.add_file('fonts/Dragon Ball.ttf')

commence_texts = ["Let's go!", "It's clickin' time!", "Pick that cookie up! ... NOW!", "Time for dessert!",
                  "'C' is for cookie,\nthat's good enough for me!", "Hasta la vista, cookie!",
                  "Say hello to my little clicker!", "Nobody puts Cookie Bot\nin a corner!"]


class Inputter(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title_font = Font(family='Dragon Ball', size=20)
        self.button_font = Font(family='Arcadepix', size=16)
        self.text_font = Font(family='Trebuchet MS', size=12)
        self.randomize_font = Font(family='Trebuchet MS', size=10)
        self.config(padx=20, pady=20)
        self.title("Super Awesome Cookie Clicker Bot: Settings")
        self.config(bg=BG_COLOR_1)

        title_str = "Super Awesome\nCookie Clicker Bot\nSettings"
        self.title_label = tk.Label(self, text=title_str, font=self.title_font, bg=BG_COLOR_1, fg=TEXT_FG)

        name_str = "Enter the name of your Cookie Bot:"
        self.name_label = tk.Label(self, text=name_str, bg=BG_COLOR_1, font=self.text_font, fg=TEXT_FG)
        self.name = tk.StringVar()
        self.name_entry = tk.Entry(self, textvariable=self.name, justify='center', width=30)

        self.random_name = tk.BooleanVar()
        self.random_name_checkbox = tk.Checkbutton(self, text="Randomize!", variable=self.random_name, onvalue=True,
                                                   offvalue=False, command=self.change_name_entry_state, bg=BG_COLOR_1,
                                                   fg=TEXT_FG, font=self.randomize_font)

        total_mins_str = "Enter number of total bot minutes:"
        self.total_mins_label = tk.Label(self, text=total_mins_str, bg=BG_COLOR_1, fg=TEXT_FG, font=self.text_font)
        self.total_mins = tk.IntVar()
        self.total_mins_entry = tk.Entry(self, textvariable=self.total_mins, width=8, justify='center')
        self.total_mins_entry.delete(0, tk.END)
        self.total_mins_entry.insert(0, '20')

        click_secs_str = "Enter number of seconds per clicking loop:"
        self.click_secs_label = tk.Label(self, text=click_secs_str, bg=BG_COLOR_1, fg=TEXT_FG, font=self.text_font)
        self.click_secs = tk.IntVar()
        self.click_secs_entry = tk.Entry(self, textvariable=self.click_secs, width=8, justify='center')
        self.click_secs_entry.delete(0, tk.END)
        self.click_secs_entry.insert(0, '5')

        item_limit_str = "Enter the item limit for each item:"
        self.item_limit_label = tk.Label(self, text=item_limit_str, bg=BG_COLOR_1, fg=TEXT_FG, font=self.text_font)
        self.item_limit = tk.IntVar()
        self.item_limit_entry = tk.Entry(self, textvariable=self.item_limit, width=8, justify='center')
        self.item_limit_entry.delete(0, tk.END)
        self.item_limit_entry.insert(0, '50')

        style = ttk.Style()
        style.configure('TMenubutton', width=4)

        mute_str = "Would you like to mute the clicking?"
        self.mute_label = tk.Label(self, text=mute_str, bg=BG_COLOR_1, fg=TEXT_FG, font=self.text_font)
        self.mute = tk.StringVar()
        self.mute_option = ttk.OptionMenu(self, self.mute, YN[1], *YN, style='TMenubutton')

        achievements_str = "Would you like to see the achievements?"
        self.achievements_label = tk.Label(self, text=achievements_str, bg=BG_COLOR_1, fg=TEXT_FG, font=self.text_font)
        self.achievements = tk.StringVar()
        self.achievements_option = ttk.OptionMenu(self, self.achievements, YN[0], *YN, style='TMenubutton')

        self.commence_button = tk.Button(self, text="Commence the Clicking!", command=self.commence_clicking)
        self.commence_button.config(padx=20, pady=20, bg=BUTTON_BG, fg='white', height=3, width=20,
                                    font=self.button_font)

        self.arrange_widgets()

        self.mainloop()

    def arrange_widgets(self):
        """Assigns widgets to tkinter window grid."""
        self.title_label.grid(column=0, row=0, columnspan=2, pady=(20, 40), sticky='EW')

        self.name_label.grid(column=0, row=1, padx=5, pady=0, sticky='E')
        self.name_entry.grid(column=1, row=1, padx=5, pady=0, sticky='W')
        self.random_name_checkbox.grid(column=1, row=2, padx=5, pady=2, sticky='W')

        self.total_mins_label.grid(column=0, row=3, padx=5, pady=15, sticky='E')
        self.total_mins_entry.grid(column=1, row=3, padx=5, pady=15, sticky='W')

        self.click_secs_label.grid(column=0, row=4, padx=5, pady=15, sticky='E')
        self.click_secs_entry.grid(column=1, row=4, padx=5, pady=15, sticky='W')

        self.item_limit_label.grid(column=0, row=5, padx=5, pady=15, sticky='E')
        self.item_limit_entry.grid(column=1, row=5, padx=5, pady=15, sticky='W')

        self.mute_label.grid(column=0, row=6, padx=5, pady=15, sticky='E')
        self.mute_option.grid(column=1, row=6, padx=5, pady=15, sticky='W')

        self.achievements_label.grid(column=0, row=7, padx=5, pady=15, sticky='E')
        self.achievements_option.grid(column=1, row=7, padx=5, pady=15, sticky='W')

        self.commence_button.grid(column=0, row=8, columnspan=2, padx=20, pady=20, sticky='EW')

    def commence_clicking(self):
        """Closes the settings window and commences the clicking."""
        disable_elements = [self.commence_button, self.name_entry, self.random_name_checkbox, self.total_mins_entry,
                            self.click_secs_entry, self.item_limit_entry, self.mute_option, self.achievements_option]
        for element in disable_elements:
            element.config(state=tk.DISABLED)
        self.commence_button.config(bg=BUTTON_CLICKED_BG)

        self.flash_bg_color()

        time.sleep(0.5)
        self.commence_button.config(text=random.choice(commence_texts))
        self.update()
        time.sleep(0.75)

        self.assign_variables()

        self.destroy()

    def flash_bg_color(self):
        """Flashes the background color while performing a countdown in the button text to warn the user that we are
        going to begin."""
        bg_elements = [self, self.name_label, self.random_name_checkbox, self.title_label, self.total_mins_label,
                       self.click_secs_label, self.item_limit_label, self.mute_label, self.achievements_label]

        for i in range(3, -1, -1):

            time.sleep(0.5)

            for element in bg_elements:
                element.config(bg=BG_COLOR_2)
            self.commence_button.config(bg=BUTTON_CLICKED_BG)
            self.commence_button.config(text=str(i))

            self.update()

            time.sleep(0.5)

            for element in bg_elements:
                element.config(bg=BG_COLOR_1)
            self.commence_button.config(bg=BUTTON_BG)
            self.update()

    def assign_variables(self):
        """Assigns variables created from settings window to use for Cookie Bot."""
        self.name = self.name.get().strip()
        self.random_name = self.random_name.get()
        self.total_mins = self.total_mins.get()
        self.click_secs = self.click_secs.get()
        self.item_limit = self.item_limit.get()
        self.mute = True if self.mute.get() == 'Yes' else False
        self.achievements = True if self.achievements.get() == 'Yes' else False

    def change_name_entry_state(self):
        """Disables/enables the name entry field depending on current name randomize checkbox state."""
        if self.name_entry['state'] == tk.NORMAL:
            self.name_entry.delete(0, tk.END)
            self.name_entry.config(state=tk.DISABLED)
        else:
            self.name_entry.config(state=tk.NORMAL)
