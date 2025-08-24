import turtle
import colorsys
import tkinter as tk

languages = {
    "English": {"title": "ArtistTurtle", "color": "Color Count", "angle": "Angle", "step": "Step Size", "speed": "Speed", "start": "Start", "stop": "Stop", "reset": "Reset"},
    "Türkçe": {"title": "ArtistTurtle", "color": "Renk Sayısı", "angle": "Açı", "step": "Adım Uzunluğu", "speed": "Hız", "start": "Başlat", "stop": "Durdur", "reset": "Sıfırla"},
    "Deutsch": {"title": "ArtistTurtle", "color": "Farbanzahl", "angle": "Winkel", "step": "Schrittlänge", "speed": "Geschwindigkeit", "start": "Start", "stop": "Stopp", "reset": "Zurücksetzen"},
    "中文": {"title": "艺术海龟", "color": "颜色数量", "angle": "角度", "step": "步长", "speed": "速度", "start": "开始", "stop": "停止", "reset": "重置"}
}

class ArtistTurtle:
    def __init__(self, master):
        self.master = master
        self.lang = "English"
        self.texts = languages[self.lang]
        master.title(self.texts["title"])
        master.geometry("900x700")  # Pencereyi büyüttük
        master.resizable(False, False)

        # Sliderlar üstte
        slider_frame = tk.Frame(master)
        slider_frame.pack(pady=5)
        self.color_scale = tk.Scale(slider_frame, from_=1, to=100, orient=tk.HORIZONTAL, length=150, label=self.texts["color"])
        self.color_scale.set(50)
        self.color_scale.pack(side=tk.LEFT, padx=2)
        self.angle_scale = tk.Scale(slider_frame, from_=1, to=359, orient=tk.HORIZONTAL, length=150, label=self.texts["angle"])
        self.angle_scale.set(141)
        self.angle_scale.pack(side=tk.LEFT, padx=2)
        self.step_scale = tk.Scale(slider_frame, from_=1, to=10, orient=tk.HORIZONTAL, length=150, label=self.texts["step"])
        self.step_scale.set(2)
        self.step_scale.pack(side=tk.LEFT, padx=2)
        self.speed_scale = tk.Scale(slider_frame, from_=1, to=50, orient=tk.HORIZONTAL, length=150, label=self.texts["speed"])
        self.speed_scale.set(10)
        self.speed_scale.pack(side=tk.LEFT, padx=2)

        # Butonlar sliderların altında
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)

        tk.Label(btn_frame, text="Language:").pack(side=tk.LEFT, padx=2)
        self.lang_var = tk.StringVar(value=self.lang)
        tk.OptionMenu(btn_frame, self.lang_var, *languages.keys(), command=self.update_language).pack(side=tk.LEFT, padx=2)
        self.about_btn = tk.Button(btn_frame, text="About", command=self.show_about)
        self.about_btn.pack(side=tk.LEFT, padx=2)
        self.start_btn = tk.Button(btn_frame, text=self.texts["start"], command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=2)
        self.stop_btn = tk.Button(btn_frame, text=self.texts["stop"], command=self.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        self.reset_btn = tk.Button(btn_frame, text=self.texts["reset"], command=self.reset)
        self.reset_btn.pack(side=tk.LEFT, padx=2)

        # Turtle ekranı, pencerenin geri kalanını kaplayacak şekilde
        canvas = tk.Canvas(master, width=880, height=550)  # Büyük canvas
        canvas.pack()
        self.screen = turtle.TurtleScreen(canvas)
        self.screen.bgcolor("black")
        self.t = turtle.RawTurtle(self.screen)
        self.t.hideturtle()
        self.t.speed(0)
        self.screen.tracer(0)

        self.running = False
        self.i = 0
        self.colors = []

    def show_about(self):
        about_text = """# ArtistTurtle

ArtistTurtle is an interactive art tool using Python's Turtle module to create colorful, rotating star and spiral patterns.
With a Tkinter GUI, you can adjust angle, step size, color count, and animation speed.

LICENSE: MIT License

Copyright (c) 2025 Ege Önder
"""
        about_window = tk.Toplevel(self.master)
        about_window.title("About ArtistTurtle")
        about_window.geometry("350x300")
        about_window.resizable(False, False)
        text_widget = tk.Text(about_window, wrap=tk.WORD)
        text_widget.pack(expand=True, fill=tk.BOTH)
        text_widget.insert(tk.END, about_text)
        text_widget.config(state=tk.DISABLED)

    def update_language(self, value):
        self.lang = value
        self.texts = languages[self.lang]
        self.master.title(self.texts["title"])
        self.color_scale.config(label=self.texts["color"])
        self.angle_scale.config(label=self.texts["angle"])
        self.step_scale.config(label=self.texts["step"])
        self.speed_scale.config(label=self.texts["speed"])
        self.start_btn.config(text=self.texts["start"])
        self.stop_btn.config(text=self.texts["stop"])
        self.reset_btn.config(text=self.texts["reset"])

    def draw(self):
        if not self.running:
            return
        n = self.color_scale.get()
        if len(self.colors) != n:
            self.colors = [colorsys.hsv_to_rgb(i/n,1,1) for i in range(n)]
        self.t.pencolor(self.colors[self.i % n])
        self.t.forward(self.i * self.step_scale.get())
        self.t.right(self.angle_scale.get())
        self.screen.update()
        self.i += 1
        self.master.after(self.speed_scale.get(), self.draw)

    def start(self):
        if not self.running:
            self.running = True
            self.draw()

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.i = 0
        self.t.reset()
        self.t.hideturtle()
        self.screen.bgcolor("black")
        self.screen.tracer(0)
        self.colors = []

root = tk.Tk()
app = ArtistTurtle(root)
root.mainloop()
