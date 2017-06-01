from tkinter import *
import random
import time
import os
import pickle
from pathlib import Path


class Ball:

    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.color = color
        self.id = canvas.create_oval(10, 10, 25, 25, fill=self.color)
        self.canvas.tag_raise('all')
        self.canvas.move(self.id, 250, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.hit_bottom = False
        self.score = 0
        self.mylevel = 0
        self.life = 3

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = self.mylevel
        if pos[3] >= self.canvas_height:
            self.x = random.randint(-1, 1)
            self.y = -3
            self.life -= 1
            canvas.delete(self.id) #Deletes the rectangle
            self.id = canvas.create_oval(10, 10, 25, 25, fill=self.color)
            self.canvas.move(self.id, 250, 100)
            starts = [-3, -2, -1, 1, 2, 3]
            random.shuffle(starts)
            self.x = starts[0]
            self.y = -3
        if self.hit_paddle(pos):
            self.x = random.randint(-self.mylevel-1, self.mylevel+1)
            self.y = -self.mylevel
            print(self.x)
            print("level:", self.mylevel)
            self.score += 1
        if pos[0] <= 0:
            if self.mylevel < 4:
                self.x = self.mylevel+1
            else:
                self.x = 3
        if pos[2] >= self.canvas_width:
            if self.mylevel < 4:
                self.x = -(self.mylevel+1)
            else:
                self.x = -3
        lives["text"] = "lives:", self.life

    def game_score(self):
        score["text"] = "score:", self.score

    def game_level(self):
        if self.score % 10 == 0:
            self.mylevel = int((self.score / 10)+1)
            level["text"] = "level:", self.mylevel


def restart_game():
    global start_time
    global total_pause_time
    global playing
    global restart
    global results_label
    global restart_btn
    global game_on
    game_on = True
    ball.mylevel = 1
    ball.life = 3
    ball.score = 0
    total_pause_time = 0
    playing = True
    start_time = time.time()
    results_label.destroy()
    restart_btn.destroy()


class Paddle:

    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 480)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0

    def turn_right(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[2] >= self.canvas_width:
            self.x = 0
        else:
            self.x = ball.mylevel + 18

    def turn_left(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        else:
            self.x = -(ball.mylevel + 18)


def timer():
    global start_time
    global pause_start_time
    global pause_end_time
    global total_pause_time

    if len(str(pause_start_time)) > 1 and len(str(pause_end_time)) > 1:
        pause_time = pause_end_time - pause_start_time
        total_pause_time += pause_time

    now_time = time.time()
    sec = round(now_time - (start_time + total_pause_time))

    if sec >= 3600:
        hours = int(sec/3600)
        sec -= hours * 3600
    else:
        hours = 0

    if sec >= 60:
        minutes = int(sec/60)
        sec -= (minutes * 60)
    else:
        minutes = 0

    if len(str(minutes)) == 1:
        minutes = '%02x' % minutes
    if len(str(sec)) == 1:
        sec = '%02x' % sec
    if hours == 0:
        total_time = "time: {}:{}".format(minutes, sec)
    else:
        total_time = "time: {}:{}:{}".format(hours, minutes, sec)

    pause_start_time = 0
    pause_end_time = 0
    clock["text"] = total_time


def pause(event):
    global playing
    global pause_start_time
    global pause_end_time
    if game_on:
        if playing:
            playing = False
            pause_start_time = time.time()
            pause_msg["text"] = "Pause"
        elif not playing:
            playing = True
            pause_end_time = time.time()
            pause_msg["text"] = ""


def start_game():
    global start
    global playing
    global paddle
    global ball
    global start_time
    global game_on
    start = True
    playing = True
    game_on = True
    start_btn.destroy()
    start_time = time.time()
    paddle = Paddle(canvas, "blue")
    ball = Ball(canvas, paddle, "red")


def callback():
    global player_name
    global restart
    player_name = str(entry_field.get())
    if len(player_name) > 0:
        data_entry()
        entry_label.destroy()
        entry_field.destroy()
        entry_btn.destroy()
        total_score_label.destroy()
        game_over_label.destroy()
        results_label["text"] = "Top players: \n {}".format(sort_list())
        results_label.pack()
        results_label.place(x=170, y=100)
        restart_btn.place(x=190, y=280)


def data_entry():
    global player_name
    global game_data
    folder_path = os.getcwd()
    file_path = "{}/pingresults12345.dat".format(folder_path)
    ball.score = int(ball.score)
    my_file = Path(file_path)
    if my_file.is_file():
        game_results = open(file_path, 'rb')
        game_data = pickle.load(game_results)
        game_results.close()
        if player_name in game_data:
            game_data[player_name].append(ball.score)
        else:
            game_data[player_name] = [ball.score]
    else:
        game_data = {}
        game_data[player_name] = [ball.score]
    game_results = open(file_path, 'wb')
    pickle.dump(game_data, game_results)
    game_results.close()


def sort_list():
    game_score_list = []
    folder_path = os.getcwd()
    file_path = "{}/pingresults12345.dat".format(folder_path)
    game_results = open(file_path, 'rb')
    game_data = pickle.load(game_results)
    game_results.close()
    if len(game_data) > 1:
        for i in game_data:
            if len(i) > 1:
                for n in game_data[i]:
                    game_score_list.append(n)
            else:
                game_score_list.append(game_data[i])
        game_score_list = sorted(game_score_list, reverse=True)
        if len(game_score_list) >= 6:
            game_score_list = game_score_list[:5]
        total_score_list = ""
        n = 1

        while len(game_score_list) > 0:
            max_score = max(game_score_list)
            for player in game_data:
                if max_score in game_data[player] and n < 6:
                    player_score = "{}. {}: {}".format(n, player, max_score)
                    n += 1
                    if len(total_score_list) == 0:
                        total_score_list = "{}".format(player_score)
                    else:
                        total_score_list = "{} \n {}".format(total_score_list, player_score)
                    game_score_list.remove(max_score)
        return total_score_list


pause_start_time = 0
pause_end_time = 0
total_pause_time = 0

tk = Tk()

tk.title("Arkanoid")
tk.resizable(0, 0)
#tk.wm_attributes("-topmost", 1)   da bi bilo top
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)

clock = Label(tk, font=('times', 18, 'bold'))
clock.place(x=10, y=5)

score = Label(tk, font=('times', 18, 'bold'))
score.place(x=160, y=5)

level = Label(tk, font=('times', 18, 'bold'))
level.place(x=290, y=5)

lives = Label(tk, font=('times', 18, 'bold'))
lives.place(x=420, y=5)

canvas.bind_all('<KeyPress-space>', pause)

pause_msg = Label(tk, font=('times', 60, 'bold'))
pause_msg.place(x=160, y=220)

canvas.pack()
tk.update()

# play game
start = False
playing = False
restart = False
game_on = False
game_score_list = []

start_btn = Button(tk, text="Start", font=('Helvetica', 18), command=start_game)
start_btn.pack()
start_btn.place(x=210, y=220)


while 1:
    if start:
        if playing and game_on:
            if ball.life != 0:
                if ball.life == 1:
                    lives['fg'] = "red"
                else:
                    lives['fg'] = "black"
                ball.draw()
                paddle.draw()
                paddle.x = 0
                paddle.y = 0
                timer()
                ball.game_score()
                ball.game_level()
            else:
                game_on = False
                score_msg = "Your scored: {}".format(ball.score)

                total_score_label = Label(tk, font=('Helvetica', 40, 'bold'))
                total_score_label["text"] = score_msg
                total_score_label.pack()
                total_score_label.place(x=100, y=140)

                game_over_label = Label(tk, font=('Helvetica', 40, 'bold'))
                game_over_label["text"] = "Game Over!"
                game_over_label.pack()
                game_over_label.place(x=115, y=180)

                playing = False

                entry_label = Label(tk, font=('Helvetica', 18, 'bold'))
                entry_label["text"] = "Type your name:"
                entry_label.pack()
                entry_label.place(x=160, y=260)

                entry_field = Entry(tk)
                entry_field.pack()
                entry_field.place(x=150, y=295)

                entry_btn = Button(tk, text = "OK", width=10, command=callback)
                entry_btn.pack()
                entry_btn.place(x=180, y=330)

                results_label = Label(tk, font=('Helvetica', 18, 'bold'))
                restart_btn = Button(tk, text="Restart", font=('Helvetica', 18), command=restart_game)

    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
