import os
from dotenv import load_dotenv
import tkinter as tk
import json
import threading
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FILE = "history.json"

messages = [
    {"role": "system", "content": "Odgovarjaj jasno, naravno in v jeziku uporabnika."}
]

# ---------- LOAD ----------
def load():
    global messages
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            messages = json.load(f)
    except:
        pass

# ---------- SAVE ----------
def save():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# ---------- AI CALL ----------
def ask_ai():
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return r.choices[0].message.content

# ---------- UI MESSAGE ----------
def add_message(text, role):
    frame = tk.Frame(chat_frame, bg="#0f172a")
    frame.pack(fill="both", pady=6, anchor="e" if role == "user" else "w")

    color = "#2563eb" if role == "user" else "#374151"

    bubble = tk.Label(
        frame,
        text=text,
        bg=color,
        fg="white",
        wraplength=420,
        justify="left",
        padx=12,
        pady=8
    )

    bubble.pack(anchor="e" if role == "user" else "w")

    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1)

# ---------- TYPING EFFECT ----------
def type_message(text, label, i=0):
    if i <= len(text):
        label.config(text=text[:i])
        chat_canvas.update_idletasks()
        chat_canvas.yview_moveto(1)
        root.after(10, lambda: type_message(text, label, i+1))

# ---------- SEND ----------
def send(event=None):
    text = entry.get().strip()
    if not text:
        return

    entry.delete(0, tk.END)

    messages.append({"role": "user", "content": text})
    add_message(text, "user")

    add_message("AI piše...", "ai")

    def run_ai():
        try:
            reply = ask_ai()
            messages.append({"role": "assistant", "content": reply})

            # remove last "AI piše..."
            chat_frame.winfo_children()[-1].destroy()

            frame = tk.Frame(chat_frame, bg="#0f172a")
            frame.pack(fill="both", pady=6, anchor="w")

            label = tk.Label(
                frame,
                text="",
                bg="#374151",
                fg="white",
                wraplength=420,
                justify="left",
                padx=12,
                pady=8
            )
            label.pack(anchor="w")

            type_message(reply, label)
            save()

        except Exception as e:
            add_message(str(e), "ai")

    threading.Thread(target=run_ai).start()

# ---------- UI ----------
root = tk.Tk()
root.title("AI MAX Chat")
root.configure(bg="#0f172a")

chat_canvas = tk.Canvas(root, bg="#0f172a", highlightthickness=0)
scrollbar = tk.Scrollbar(root, command=chat_canvas.yview)
chat_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
chat_canvas.pack(side="left", fill="both", expand=True)

chat_frame = tk.Frame(chat_canvas, bg="#0f172a")
chat_canvas.create_window((0,0), window=chat_frame, anchor="nw")

chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))

entry = tk.Entry(root, bg="#1e293b", fg="white", insertbackground="white", width=55)
entry.pack(pady=8)

tk.Button(root, text="Pošlji", command=send).pack()

entry.bind("<Return>", send)

load()

root.mainloop()
