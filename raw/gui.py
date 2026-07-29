from tkinter import *
from tkinter import messagebox
import backend as stuff
import threading
import ai

name = "TheAppHouse"
root = Tk()
root.title(name)
root.state("zoomed")
COLORS = {
    "bg": "#243c3c",
    "text": "#FFFFFF"
}

threading.Thread(target=stuff.start, daemon=True).start()

root.update()

w, h = root.winfo_width(), root.winfo_height()

main = Frame(root)
main.pack(fill="both", expand=True)
main.configure(bg=COLORS["bg"])

def clearMain():
    for widget in main.winfo_children():
        widget.destroy()

titlefont = ("Arial", 15)

def formatUsage():
    result = ""
    for app, ms in stuff.usage.items():
        minutes = ms/60000
        result += f"{app}: {minutes:.1f} minutes\n"
    return result

def formatMs(ms):
    seconds = ms / 1000
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f}m"
    hours = minutes / 60
    return f"{hours:.1f}h"

class SubApp:
    def __init__(self):
        self.frame = None
    def start(self):
        clearMain()
        self.frame = Frame(main)
        self.frame.pack(fill="both", expand=True)
        self.frame.config(bg=COLORS["bg"])
        Button(self.frame, text="Back", command=self.back).place(x=w-50, y=100)
    def formatText(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, Label):
                widget.config(fg=COLORS["text"])
                widget.config(bg=COLORS["bg"])
    def about(self):
        root.title("About The App House")
        Label(self.frame, text="About The App House", font=titlefont).place(relx=0.5, y=50, anchor="center")
        Label(self.frame, text="""
            The App House version 1.0
            Made in Python 3.14

            Ideas for the future:
                - File explorer system
                - App creation software
            
            Copyright (c) VirRB
        """, font=("Arial", 10), justify="center").place(relx=0.5, y=150, anchor="center")
    def Oracle(self):
        root.title("Oracle")
        Label(self.frame, text="Oracle", font=titlefont).place(relx=0.5, y=50, anchor="center")
        promptBox = Entry(self.frame)
        promptBox.place(x=50, y=50)
        youBox = Label(self.frame, text="Ask anything...")
        youBox.place(x=50, y=100)
        outBox = Label(self.frame, text="")
        outBox.place(x=50, y=150)
        def send():
            prompt = promptBox.get()
            prompt = prompt.strip()
            if not prompt:
                return
            
            promptBox.delete(0, END)
            sendButton.config(state="disabled")
            youBox.config(text=f"You: {prompt}")
            outBox.config(text="")
            config = f"""
                You are the Oracle, an AI assistant designed to help users with their computer usage
                be concise.
                The amount apps are used:
                {formatUsage()}
                Favorite app:
                {stuff.getHighest()["app"]}
                User asked:
                {prompt}
            """
            response = ai.askAI(config)
            outBox.config(text=f"Oracle: {response}")
            sendButton.config(state="normal")
        sendButton = Button(self.frame, text="Send", command=lambda: threading.Thread(target=send, daemon=True).start())
        sendButton.place(x=200, y=50)
    def UsageTime(self):
        root.title("Observatory")
        Label(self.frame, text="The Observatory", font=titlefont).place(relx=0.5, y=50, anchor="center")
        statsFrame = []
        def refresh():
            for widget in statsFrame:
                widget.destroy()
            usage = stuff.usage
            highest = stuff.getHighest()
            if usage == {}:
                warn = Label(self.frame, text="You do not have any saved memory...")
                warn.place(x=50, y=100)
                statsFrame.append(warn)
                return
            thing = Label(self.frame, text=f"Your most used app is {highest['app']}\nwhich you have used for {formatMs(highest['ms'])}")
            quote = stuff.makeQuote()
            thing2 = Label(self.frame, text=quote)
            statsFrame.append(thing2)
            statsFrame.append(thing)
            thing.place(x=50, y=100)
            thing2.place(x=50, y=150)
            y = 200
            for app, ms in usage.items():
                n = Label(self.frame, text=f"{app}: {formatMs(ms)}")
                n.place(x=50, y=y)
                statsFrame.append(n)
                y += 50
            self.formatText()
        def deleteMem():
            confirm = messagebox.askyesno("Confirm", message="Are you sure you want to delete ALL saved memory?\nThis cannot be undone")
            if not confirm:
                return
            stuff.usage.clear()
            stuff.save()
            refresh()
        refresh()
        Button(self.frame, text="Refresh", command=refresh).place(x=w-150, y=100)
        Button(self.frame, text="Save", command=stuff.save).place(x=w-200, y=100)
        Button(self.frame, text="Clear Memory", command=deleteMem).place(x=w-300, y=100)

    def back(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        root.title(name)
        spawnMain()

def spawnMain():
    sub = SubApp()
    clearMain()
    Label(main, text="The App House", font=titlefont).place(relx=0.5, y=50, anchor="center")
    Button(main, text="🔭Observatory", command=lambda: (sub.start(), sub.UsageTime(), sub.formatText())).place(x=100, y=50)
    Button(main, text="✨Oracle", command=lambda: (sub.start(), sub.Oracle(), sub.formatText())).place(x=225, y=50)
    Button(main, text="❓About", command=lambda: (sub.start(), sub.about(), sub.formatText())).place(x=100, y=125)
    for widget in main.winfo_children():
        if isinstance(widget, Label):
            widget.config(bg=COLORS["bg"])
            widget.config(fg=COLORS["text"])

spawnMain()


if __name__ == "__main__":
    root.mainloop()