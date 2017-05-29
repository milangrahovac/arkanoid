from tkinter import *
import random
import time

total_pause_time = 0


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
            self.x = random.randint(-(self.mylevel)-1, self.mylevel+1)
            self.y = -(self.mylevel)
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

    def restart_game(self):
        global start_time
        global total_pause_time
        global playing
        self.mylevel = 1
        self.life = 3
        self.score = 0
        total_pause_time = 0
        playing = True
        canvas.delete(msg1, msg2)
        restart_btn.destroy()
        start_time = time.time()


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
#    pause_time = 0
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
    start = True
    playing = True
    start_btn.destroy()
    start_time = time.time()
    paddle = Paddle(canvas, "blue")
    ball = Ball(canvas, paddle, "red")

pause_start_time = 0
pause_end_time = 0

tk = Tk()

tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
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

start_btn = Button(tk, text="Start", font=('Helvetica', 18), fg='red', bg='blue', command=start_game)
start_btn.pack()
start_btn.place(x=210, y=220)

while 1:
    if not start:
        pass
    else:
        if not playing:
            pass
        else:

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
                score_msg = "Your scored: {}".format(ball.score)
                msg1 = canvas.create_text(230, 160, text=score_msg, font=('Helvetica', 40))
                msg2 = canvas.create_text(230, 200, text="Game Over !!!", font=('Helvetica', 40))
                playing = False
                restart_btn = Button(tk, text="Restart", font=('Helvetica', 18), fg='red', bg='blue', command=ball.restart_game)
                restart_btn.pack()
                restart_btn.place(x=180, y=240)

    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
