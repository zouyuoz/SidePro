import pyautogui
import keyboard
import threading
import time
import tkinter as tk
from tkinter import messagebox

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        root.title("自動點擊器")

        # 座標輸入框
        tk.Label(root, text="點擊位置（多個以分號分隔，格式 x,y）：").pack()
        self.positions_entry = tk.Entry(root, width=50)
        self.positions_entry.pack()
        self.positions_entry.insert(0, "500,500;700,400;600,600")

        # 間隔輸入框
        tk.Label(root, text="點擊間隔（秒）：").pack()
        self.interval_entry = tk.Entry(root, width=10)
        self.interval_entry.pack()
        self.interval_entry.insert(0, "1.5")

        # 狀態標籤
        self.status_label = tk.Label(root, text="狀態：暫停")
        self.status_label.pack(pady=10)

        # 提示標籤（顯示是否在添加位置模式）
        self.add_mode_label = tk.Label(root, text="添加位置模式：關閉", fg="red")
        self.add_mode_label.pack()

        # 開始/暫停按鈕
        self.toggle_btn = tk.Button(root, text="開始", command=self.toggle)
        self.toggle_btn.pack()

        # 記錄點擊座標
        tk.Label(root, text="每分鐘點擊的座標 (格式 x,y)：").pack()
        self.record_position_entry = tk.Entry(root, width=50)
        self.record_position_entry.pack()
        self.record_position_entry.insert(0, "100,100")

        # 設定記錄並啟用功能按鈕
        self.record_toggle_btn = tk.Button(root, text="啟用每分鐘點擊", command=self.toggle_recording)
        self.record_toggle_btn.pack()

        self.running = False
        self.add_position_mode = False  # 是否處於添加位置模式
        self.recording = False  # 是否啟用每分鐘點擊
        self.thread = threading.Thread(target=self.click_loop, daemon=True)
        self.thread.start()

        # F6 快捷鍵 開始/暫停
        keyboard.add_hotkey("F6", self.toggle)

        # A鍵：切換添加位置模式
        keyboard.add_hotkey("a", self.toggle_add_mode)

        # C鍵：若在添加位置模式，記錄游標位置
        keyboard.add_hotkey("c", self.capture_position)

        # 每分鐘點擊的循環
        self.record_thread = threading.Thread(target=self.record_click_loop, daemon=True)
        self.record_thread.start()

    def parse_positions(self):
        raw = self.positions_entry.get().strip()
        pos_list = []
        try:
            parts = raw.split(";")
            for p in parts:
                if p.strip() == "":
                    continue
                x_str, y_str = p.split(",")
                x, y = int(x_str), int(y_str)
                pos_list.append((x, y))
            return pos_list
        except Exception:
            messagebox.showerror("錯誤", "位置格式錯誤，請確認輸入格式為 x,y; x,y; ...")
            return None

    def toggle(self):
        self.running = not self.running
        self.status_label.config(text=f"狀態：{'運行中' if self.running else '暫停'}")
        self.toggle_btn.config(text="暫停" if self.running else "開始")

    def toggle_add_mode(self):
        self.add_position_mode = not self.add_position_mode
        if self.add_position_mode:
            self.add_mode_label.config(text="添加位置模式：開啟，按 C 記錄游標位置", fg="green")
        else:
            self.add_mode_label.config(text="添加位置模式：關閉", fg="red")

    def capture_position(self):
        if self.add_position_mode:
            x, y = pyautogui.position()
            # 取得現有文字，加入分號再加新位置
            current_text = self.positions_entry.get().strip()
            if current_text and not current_text.endswith(";"):
                current_text += ";"
            new_text = f"{current_text}{x},{y}"
            self.positions_entry.delete(0, tk.END)
            self.positions_entry.insert(0, new_text)
            # 反饋訊息
            self.add_mode_label.config(text=f"已加入位置：({x}, {y})，繼續按 C 或按 A 離開", fg="green")

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            self.record_toggle_btn.config(text="停止每分鐘點擊")
            self.record_position = self.record_position_entry.get().strip()
            self.record_x, self.record_y = map(int, self.record_position.split(","))
        else:
            self.record_toggle_btn.config(text="啟用每分鐘點擊")

    def record_click_loop(self):
        while True:
            if self.recording:
                # 記錄當前游標位置
                current_x, current_y = pyautogui.position()

                # 移動到指定位置
                pyautogui.moveTo(self.record_x, self.record_y)
                pyautogui.click()

                # 點擊後將游標歸位
                pyautogui.moveTo(current_x, current_y)

                # 每分鐘一次
                time.sleep(60)
            else:
                time.sleep(0.1)

    def click_loop(self):
        idx = 0
        while True:
            if self.running:
                positions = self.parse_positions()
                if not positions:
                    self.running = False
                    self.status_label.config(text="狀態：暫停 (錯誤)")
                    self.toggle_btn.config(text="開始")
                    time.sleep(1)
                    continue
                try:
                    interval = float(self.interval_entry.get())
                except ValueError:
                    interval = 1.5

                x, y = positions[idx]
                pyautogui.moveTo(x, y)
                pyautogui.click()
                idx = (idx + 1) % len(positions)
                time.sleep(interval)
            else:
                time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
