import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk

wifi_connected = False   # 🔥 GLOBAL STATE


# ---------- App Functions ----------

def open_wifi(wire_fixed):   # 🔥 PASS STATE HERE
    win = tk.Toplevel(root)
    center_window(win, 300, 200)
    win.title("WiFi")
    win.configure(bg="#111827")

    tk.Label(win, text="Enter WiFi Password", fg="white", bg="#111827",
             font=("Arial", 12)).pack(pady=10)

    entry = tk.Entry(win, show="*", font=("Arial", 12))
    entry.pack(pady=5)

    def check():
        global wifi_connected
        password = entry.get()

        # 🔥 CASE 1: wire not fixed
        if not wire_fixed:
            messagebox.showerror("Error", "Couldn't find WiFi (wire disconnected)")
            return

        # 🔥 CASE 2: correct password
        if password == "modern":
            wifi_connected = True
            messagebox.showinfo("Status", "WiFi Connected!")
            root.destroy()

        # 🔥 CASE 3: wrong password
        else:
            messagebox.showerror("Error", "Wrong Password")

    tk.Button(win, text="Connect", command=check).pack(pady=10)


def open_settings():
    win = tk.Toplevel(root)
    center_window(win, 300, 200)
    win.title("Settings")
    win.configure(bg="#111827")

    tk.Label(win, text="RAM: 8GB", fg="white", bg="#111827").pack(pady=5)
    tk.Label(win, text="CPU: Intel i5", fg="white", bg="#111827").pack(pady=5)
    tk.Label(win, text="OS: Custom OS v1.0", fg="white", bg="#111827").pack(pady=5)


def open_cmd(wire_fixed):   # 🔥 PASS STATE HERE
    win = tk.Toplevel(root)
    center_window(win, 350, 250)
    win.title("Command Prompt")
    win.configure(bg="black")

    entry = tk.Entry(win, font=("Consolas", 12), bg="black", fg="lime")
    entry.pack(pady=10)

    output = tk.Text(win, height=4, width=35,
                     font=("Consolas", 12),
                     bg="black", fg="white", bd=0)
    output.pack(pady=10)

    # Color tags
    output.tag_config("blue", foreground="blue")
    output.tag_config("red", foreground="red")
    output.tag_config("yellow", foreground="yellow")
    output.tag_config("green", foreground="green")

    def run():
        cmd = entry.get().lower()
        output.delete("1.0", tk.END)

        if cmd == "ipconfig":
            output.insert(tk.END, "IP Address: ")

            output.insert(tk.END, "1")
            output.insert(tk.END, "9", "blue")
            output.insert(tk.END, "2")

            output.insert(tk.END, ".")

            output.insert(tk.END, "1")
            output.insert(tk.END, "6", "red")
            output.insert(tk.END, "8")

            output.insert(tk.END, ".")

            output.insert(tk.END, "1", "yellow")

            output.insert(tk.END, ".")

            output.insert(tk.END, "1")
            output.insert(tk.END, "0", "green")

        # 🔥 NEW COMMAND
        elif cmd == "wlan_interfaces":
            if wire_fixed:
                output.insert(tk.END, "WiFi Name: modern_vip\n")
                output.insert(tk.END, "Password: modern")
            else:
                output.insert(tk.END, "No WiFi adapters found")

        else:
            output.insert(tk.END, "Irrelevant command")

    tk.Button(win, text="Run", command=run).pack()


def open_camera():
    win = tk.Toplevel(root)
    center_window(win, 300, 200)
    win.title("Camera")
    win.configure(bg="#111827")

    tk.Label(win, text="[Camera Feed Placeholder]",
             fg="white", bg="#111827").pack(expand=True)


# ---------- Helper ----------

def center_window(win, w, h):
    x = (root.winfo_x() + root.winfo_width() // 2) - w // 2
    y = (root.winfo_y() + root.winfo_height() // 2) - h // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


# ---------- MAIN FUNCTION ----------

def run_interface(wire_fixed):   # 🔥 IMPORTANT CHANGE
    global root, wifi_connected

    wifi_connected = False

    root = tk.Tk()
    root.title("Computer Interface")
    root.geometry("1000x600")
    root.configure(bg="#0a0a0a")

    screen_width = 900
    screen_height = 520

    screen = tk.Frame(root, bd=5, relief="sunken")
    screen.place(relx=0.5, rely=0.5, anchor="center",
                 width=screen_width, height=screen_height)

    # ---------- Wallpaper ----------
    image = Image.open("game/wallpaper.png")
    image = image.resize((screen_width, screen_height))

    bg_image = ImageTk.PhotoImage(image)

    bg_label = tk.Label(screen, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ---------- ICONS ----------
    icon_frame = tk.Frame(bg_label, bg="")
    icon_frame.place(relx=0.5, rely=0.5, anchor="center")

    btn_style = {
        "width": 12,
        "height": 5,
        "font": ("Arial", 12, "bold"),
        "bg": "#1e293b",
        "fg": "white",
        "activebackground": "#334155",
        "bd": 2
    }

    tk.Button(icon_frame, text="WiFi",
              command=lambda: open_wifi(wire_fixed), **btn_style)\
        .grid(row=0, column=0, padx=25, pady=25)

    tk.Button(icon_frame, text="Settings",
              command=open_settings, **btn_style)\
        .grid(row=0, column=1, padx=25, pady=25)

    tk.Button(icon_frame, text="Command",
              command=lambda: open_cmd(wire_fixed), **btn_style)\
        .grid(row=1, column=0, padx=25, pady=25)

    tk.Button(icon_frame, text="Camera",
              command=open_camera, **btn_style)\
        .grid(row=1, column=1, padx=25, pady=25)

    # ---------- TASKBAR ----------
    taskbar = tk.Frame(bg_label, bg="#020617", height=40)
    taskbar.pack(side="bottom", fill="x")

    tk.Label(taskbar, text="Start", fg="white", bg="#020617",
             font=("Arial", 10, "bold")).pack(side="left", padx=10)

    time_label = tk.Label(taskbar, fg="white", bg="#020617")
    time_label.pack(side="right", padx=10)

    def update_time():
        now = datetime.now()
        formatted = now.strftime("%H:%M  %d-%m-%Y  %A")
        time_label.config(text=formatted)
        root.after(1000, update_time)

    update_time()

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

    return wifi_connected