import argparse
import threading
import tkinter as tk
from tkinter import messagebox

from core.detect import detect_target
from core.messenger import StopRun, start_bot


def launch_gui(once=False):
    try:
        target = detect_target()
    except RuntimeError as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("TikTok Auto Messenger", str(exc))
        root.destroy()
        return

    root = tk.Tk()
    root.title("TikTok Auto Messenger")
    root.geometry("460x240")

    if target is None:
        tk.Label(
            root,
            text="No Brave, Chrome, or Edge profile was found on this PC.",
            font=("Arial", 11),
            wraplength=420,
        ).pack(pady=24, padx=16)
        root.mainloop()
        return

    tk.Label(root, text="Detected browser", font=("Arial", 11)).pack(pady=(16, 4))
    tk.Label(root, text=target.message, font=("Arial", 13)).pack()
    if not target.tiktok_login_found:
        tk.Label(
            root,
            text="TikTok login was not found in that profile.",
            font=("Arial", 10),
        ).pack(pady=4)

    status = tk.Label(root, text="", font=("Arial", 10), wraplength=420)
    status.pack(pady=8)

    button_text = "Send one message" if once else "Start messaging"
    outcome = {"error": None, "summary": None}

    def post_status(text):
        root.after(0, lambda value=text: status.config(text=value))

    def finish():
        button.config(state=tk.NORMAL, text=button_text)
        if outcome["error"] is not None:
            status.config(text=str(outcome["error"]))
            messagebox.showerror("Stopped", str(outcome["error"]))
            return
        summary = outcome["summary"] or "Finished."
        status.config(text=summary)
        messagebox.showinfo("Done", summary)

    def worker():
        try:
            outcome["summary"] = start_bot(once=once, on_status=post_status)
        except StopRun as exc:
            outcome["error"] = exc
        except Exception as exc:
            outcome["error"] = exc
        finally:
            root.after(0, finish)

    def begin():
        button.config(state=tk.DISABLED, text="Running...")
        status.config(text="Starting.")
        threading.Thread(target=worker, daemon=True).start()

    button = tk.Button(root, text=button_text, font=("Arial", 12), command=begin)
    button.pack(pady=12)
    root.mainloop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    launch_gui(once=args.once)


if __name__ == "__main__":
    main()
