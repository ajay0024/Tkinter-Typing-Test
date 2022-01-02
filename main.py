import time
from tkinter import *
from tkinter import ttk, filedialog, font
import re, time

# filename = ""
sampletext = 'What if some lines of text in the widget are very long, longer than the width of the widget? By ' \
             'default, the text wraps around to the next line. This behavior can be changed with the wrap ' \
             'configuration option. It defaults to char, meaning wrap lines at any character. Other options are word ' \
             'to wrap lines only at word breaks (e.g., spaces), and none meaning to not wrap lines at all. In the ' \
             'latter case, some text of longer lines won\'t be visible unless we attach a horizontal scrollbar to the ' \
             'widget '
sampletext = sampletext.lower()
# remove non alpha characters
regex = re.compile('[^a-zA-Z ]')
sampletext = regex.sub("", sampletext)

spaces = [-1]
for x in range(len(sampletext)):

    if sampletext[x] == " ":
        spaces.append(x)

print(spaces)

root = Tk()
root.title("Typing Test")
# root.geometry("600x700")

# filename = StringVar()
wm_text = StringVar()
s = ttk.Style()
s.configure('Danger.TFrame', background='cyan')

wrong_words = {}
current_word_index = 0
line = 1
total_right_characters = 0
total_characters = 0
total_right_words = 0
start_time = 0
current_time_text = StringVar()
error_labels = []


def update_clock():
    time_passed = int(time.time() - start_time)
    current_time_text.set(f"Time Spent : {time_passed}")
    if time_passed < 60:
        root.after(1000, update_clock)
    else:
        time_over()


def time_over():
    global error_labels
    print(wrong_words)
    target_text.focus()
    entry.grid_forget()
    time_label.grid_forget()
    wpm_label.grid(row=0, column=0, columnspan=1, sticky="w")
    wpm_label["text"] = f"Words per Minute: {total_right_words}"
    cpm_label.grid(row=0, column=1, columnspan=2, sticky="e")
    cpm_label["text"] = f"Characters per Minute: {total_right_characters}"
    if len(wrong_words) > 0:
        error_text = f"You actually wrote {total_characters} characters per minute. \nHowever, you made following mistakes:"
        actual_cpm_label["text"] = error_text
        actual_cpm_label.grid(row=2, column=0, columnspan=3, sticky="nwes")
        row = 3
        for word in wrong_words:
            new_label1 = ttk.Label(mainframe, text=f"{word} : ", font=resultFont,
                                   background="cyan")
            new_label1.grid(row=row, column=0, columnspan=1, sticky="e")
            new_label2 = ttk.Label(mainframe, text=f"{wrong_words[word]}", font=resultFont,
                                   background="cyan")
            new_label2.grid(row=row, column=1, columnspan=1, sticky="w")
            row += 1
            error_labels.append(new_label1)
            error_labels.append(new_label2)
    else:
        error_text = f"📝 You entered no Wrong Word 📝"
        actual_cpm_label["text"] = error_text
        actual_cpm_label.grid(row=2, column=0, columnspan=3, sticky="nwes")
    reset_btn.grid(columnspan=3, sticky="w")


def reset():
    global wrong_words, current_word_index, line, total_right_characters, total_characters, total_right_words, start_time, current_time_text, error_labels, line
    wpm_label.grid_forget()
    cpm_label.grid_forget()
    actual_cpm_label.grid_forget()
    for e in error_labels:
        e.grid_remove()
    time_label.grid(row=0, column=0, columnspan=2, sticky="w")
    entry.grid(row=2, stick="ew", columnspan=3)
    entry.delete(0, 'end')
    wrong_words = {}
    current_word_index = 0
    total_right_characters = 0
    total_characters = 0
    total_right_words = 0
    start_time = 0
    error_labels = []
    current_time_text.set("Start Typing")
    target_text.tag_remove('highlightword', f'{line}.0 ', 'end')
    target_text.tag_remove('highlightRightChar', f'{line}.0 ', 'end')
    target_text.tag_remove('highlightWrongChar', f'{line}.0 ', 'end')
    target_text.tag_add('highlightword', '1.0 ', '1.0 wordend')  # Highlight First Word

    reset_btn.grid_forget()


def character_entered(e):
    global current_word_index, line, start_time, current_time_text
    if start_time == 0:
        start_time = time.time()
        update_clock()
    char_index = spaces[current_word_index] + 1
    target_word = target_text.get(f'{line}.{char_index} ', f'{line}.{char_index} wordend')
    entered_word = entry.get().strip()
    right_characters = 0
    wrong_characters = 0
    for i in range(len(target_word)):
        if i > (len(entered_word) - 1):
            target_text.tag_remove('highlightRightChar', f'{line}.{char_index + i}', f'{line}.{char_index + i + 1}')
            target_text.tag_remove('highlightWrongChar', f'{line}.{char_index + i}', f'{line}.{char_index + i + 1}')
        elif target_word[i] == entered_word[i]:
            target_text.tag_add('highlightRightChar', f'{line}.{char_index + i}', f'{line}.{char_index + i + 1}')
            right_characters += 1
        else:
            target_text.tag_add('highlightWrongChar', f'{line}.{char_index + i}', f'{line}.{char_index + i + 1}')
            wrong_characters += 1
    if e.char == " ":
        less_characters = max(0, len(target_word) - len(entered_word))
        extra_characters = max(0, len(entered_word) - len(target_word))
        word_completed(right_characters, wrong_characters, less_characters, extra_characters)


def word_completed(right_characters, wrong_characters, less_characters, extra_characters):
    global current_word_index, line, total_right_words, total_characters, total_right_characters
    global wrong_words
    print(f"right: {right_characters}, wrong: {wrong_characters}")
    print(f"less: {less_characters}, extra: {extra_characters}")

    # Previous Word
    char_index = spaces[current_word_index] + 1
    target_text.tag_remove('highlightword', f'{line}.{char_index} ', f'{line}.{char_index} wordend')
    target_word = target_text.get(f'{line}.{char_index} ', f'{line}.{char_index} wordend')
    entered_word = entry.get().strip()

    # Remove tags
    target_text.tag_remove('highlightRightChar', f'{line}.{char_index} ', f'{line}.{char_index} wordend')
    target_text.tag_remove('highlightWrongChar', f'{line}.{char_index} ', f'{line}.{char_index} wordend')

    # update data
    total_right_characters += right_characters
    total_characters += right_characters + wrong_characters + extra_characters
    if entered_word == target_word:
        total_right_words += 1
    else:
        wrong_words[target_word] = entered_word
        # Add false tag if wrong word
        target_text.tag_add('highlightWrongChar', f'{line}.{char_index} ', f'{line}.{char_index} wordend')

    print(f"right words: {total_right_words}")
    print(f"right characters: {total_right_characters}")
    print(f"total characters: {total_characters}")

    # Delete current word from entry
    entry.delete(0, 'end')

    # Move on to next word
    current_word_index += 1
    char_index = spaces[current_word_index] + 1
    print(line, char_index)
    target_text.tag_add('highlightword', f'{line}.{char_index} ', f'{line}.{char_index} wordend')
    target_text.see(f"{line}.{char_index} + 1 display lines")


mainframe = ttk.Frame(root, padding="50", style='Danger.TFrame')

mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

baseFont = font.Font(family='Lucida Console', name='appHighlightFont', size=20, weight='normal')
resultFont = font.Font(family='Lucida Console', name='resultFont', size=14, weight='normal')

# Time Label
time_label = ttk.Label(mainframe, text="tim", font=baseFont, background="cyan")
time_label.grid(column=0, columnspan=2, sticky="w")
current_time_text.set("Start Typing")
time_label["textvariable"] = current_time_text

# WPM and CPM Label
wpm_label = ttk.Label(mainframe, text="", font=resultFont, background="cyan")
cpm_label = ttk.Label(mainframe, text="", font=resultFont, background="cyan")

# Make Targte Text
target_text = Text(mainframe, width=40, height=3, font=baseFont, wrap="word", padx=10, pady=10)
target_text.insert('1.0', sampletext)

# Make Tags and set initial tag
target_text.tag_configure('highlightword', background='DarkOliveGreen2', relief='raised')
target_text.tag_configure('highlightRightChar', foreground="white")
target_text.tag_configure('highlightWrongChar', foreground="red")
target_text.tag_add('highlightword', '1.0 ', '1.0 wordend')  # Highlight First Word

target_text['state'] = 'disabled'
ys = ttk.Scrollbar(mainframe, orient='vertical', command=target_text.yview, )
target_text['yscrollcommand'] = ys.set

target_text.grid(column=0, row=1, columnspan=2, sticky='nwes', pady=10)
ys.grid(column=2, row=1, sticky='ns', columnspan=1, pady=10)

# Make Input entry
entry = ttk.Entry(mainframe, font=baseFont, justify="center")
entry.grid(stick="ew", columnspan=3)
entry.bind("<KeyRelease>", character_entered)

# Actual CPM
actual_cpm_label = ttk.Label(mainframe, text="", font=resultFont, background="cyan")
actual_cpm_label.configure(anchor="center")

# Reset button ttk button does not support font
reset_btn = Button(mainframe, text="Reset", default="active", font=resultFont,command=reset)
root.mainloop()
