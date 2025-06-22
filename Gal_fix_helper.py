import subprocess
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
import re

# 取得 AppID 清單（支援 pacman 和 flatpak 版 protontricks）
def get_appid_list():
    try:
        result = subprocess.run(["protontricks", "--list"], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        try:
            result = subprocess.run(["flatpak", "run", "com.github.Matoking.protontricks", "--list"],
                                    capture_output=True, text=True, check=True)
        except FileNotFoundError:
            messagebox.showerror("錯誤", "找不到 protontricks，請安裝：\n\nsudo pacman -S protontricks\n或\nflatpak install flathub com.github.Matoking.protontricks")
            return []

    apps = []
    for line in result.stdout.split('\n'):
        match = re.match(r"(.*) \((\d+)\)$", line.strip())
        if match:
            app_name, app_id = match.groups()
            apps.append((app_id,app_name))
    return apps

# 執行複製動作：只使用 AppID 作為資料夾路徑
def copy_to_steam_app(appid):
    steam_path = Path.home() / ".steam/steam/steamapps/compatdata" / appid / "pfx/drive_c"
    steam_path.mkdir(parents=True, exist_ok=True)

    script_dir = Path(__file__).resolve().parent
    src_path = script_dir / "vn_winestuff-main"

    if not src_path.exists():
        messagebox.showerror("錯誤", f"找不到 vn_winestuff-main 資料夾：\n{src_path}")
        return

    for item in src_path.iterdir():
        dest = steam_path / item.name
        try:
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
        except Exception as e:
            messagebox.showerror("複製錯誤", f"複製 {item.name} 時出錯：{e}")
            return

    messagebox.showinfo("完成", f"已複製到：\n{steam_path}")


def detect_protontricks_cmd(appid):
    if shutil.which("protontricks"):
        return ["protontricks", appid, "shell"]
    if shutil.which("flatpak"):
        try:
            flatpak_list = subprocess.check_output(["flatpak", "list"], text=True)
            if "com.github.Matoking.protontricks" in flatpak_list:
                return ["flatpak", "run", "com.github.Matoking.protontricks", appid, "shell"]
        except Exception:
            pass
    return None

def launch_shell_in_terminal(command):
    terminal_cmd = None
    if shutil.which("x-terminal-emulator"):
        terminal_cmd = ["x-terminal-emulator", "-e"] + command
    elif shutil.which("gnome-terminal"):
        terminal_cmd = ["gnome-terminal", "--"] + command
    elif shutil.which("konsole"):
        terminal_cmd = ["konsole", "-e"] + command
    elif shutil.which("xfce4-terminal"):
        terminal_cmd = ["xfce4-terminal", "-e", " ".join(command)]
    else:
        messagebox.showerror("找不到終端機", "找不到可用的終端機，請手動執行：\n" + " ".join(command))
        return

    subprocess.Popen(terminal_cmd)
    messagebox.showinfo("手動關閉 Shell", "已開啟 Proton Shell，請除錯後關閉終端機(Konsole)，再按『確定』繼續。")


# GUI 主介面
class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Galgame fix工具")
        self.root.geometry("640x900")
        self.apps = get_appid_list()  # apps 為 [(appid, name), ...]
        self.create_widgets()

    def create_widgets(self):
        # 建立一個水平容器 frame，放 Label + 輸入欄 + 按鈕
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(fill=tk.X, pady=10, padx=10)

        # 左側標題文字
        ttk.Label(self.top_frame, text="選擇Steam App（雙擊）/ 手動輸入 AppID", font=("Arial", 14)).pack(side=tk.LEFT)

        # 右側輸入框
        self.manual_entry = ttk.Entry(self.top_frame, font=("Arial", 12), width=10)
        self.manual_entry.pack(side=tk.LEFT, padx=(15, 5))

        # 右側按鈕
        self.manual_button = ttk.Button(self.top_frame, text="複製修正檔案", command=self.manual_copy)
        self.manual_button.pack(side=tk.LEFT, padx=5)


        # 顯示 AppID + 遊戲名稱
        # 包裝在一個 Frame 裡，讓 Listbox 和 Scrollbar 共用
        listbox_frame = ttk.Frame(self.root)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # 建立 Scrollbar
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 建立 Listbox，連接 scrollbar
        self.app_listbox = tk.Listbox(listbox_frame, height=18, font=("Arial", 12), yscrollcommand=scrollbar.set)
        self.app_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.app_listbox.yview)

        # 填入 AppID 資料
        for appid, app_name in self.apps:
            self.app_listbox.insert(tk.END, f"{app_name} - {appid}")

        self.app_listbox.bind("<Double-Button-1>", self.on_double_click)

        # 勾選框 + 複製按鈕容器
        options_frame = ttk.Frame(self.root)
        options_frame.pack(fill=tk.X, padx=20, pady=10)

        # 勾選框子區塊
        checkbox_frame = ttk.LabelFrame(options_frame, text="安裝指令複製,請點擊你需要安裝的選項", padding=(10, 10))
        checkbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.options = [ "wmp11" , "quartz_dx" , "quartz2", "mf", "xaudio29", "dgvoodoo2", "mciqtz32"]
        self.checkbox_vars = {}

        for i, option in enumerate(self.options):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(checkbox_frame, text=option, variable=var)
            cb.grid(row=i % 3, column=i // 3, sticky=tk.W, padx=5, pady=2)
            self.checkbox_vars[option] = var

        # 複製按鈕區塊（放在右側）
        button_frame = ttk.Frame(options_frame)
        button_frame.pack(side=tk.RIGHT, padx=(10, 0))

        self.copy_button = ttk.Button(button_frame, text="複製指令", command=self.copy_command_to_clipboard)
        self.copy_button.pack(pady=10)
        self.shell_button = ttk.Button(button_frame, text="開啟 Proton Shell", command=self.open_shell)
        self.shell_button.pack(pady=5)


    def on_double_click(self, event):
        selection = self.app_listbox.curselection()
        if not selection:
            return
        appid = self.apps[selection[0]][0]  # 取 tuple 中的 appid 數字
        self.manual_entry.delete(0, tk.END)
        self.manual_entry.insert(0, appid)
        copy_to_steam_app(appid)

    def manual_copy(self):
        appid = self.manual_entry.get().strip()
        if not appid.isdigit():
            messagebox.showwarning("格式錯誤", "請輸入App ID")
            return
        copy_to_steam_app(appid)

    def copy_command_to_clipboard(self):
        selected_options = [opt for opt, var in self.checkbox_vars.items() if var.get()]
        cmd_text = "sh codec.sh " + " ".join(selected_options)
        self.root.clipboard_clear()
        self.root.clipboard_append(cmd_text)
        self.root.update()  # 立即更新剪貼簿
        messagebox.showinfo("已複製", f"已複製到剪貼簿：\n{cmd_text}")

    def open_shell(self):
        appid = self.manual_entry.get().strip()
        if not appid.isdigit():
            messagebox.showwarning("格式錯誤", "請輸入有效的 AppID")
            return

        cmd = detect_protontricks_cmd(appid)
        if not cmd:
            messagebox.showerror("找不到指令", "無法偵測 protontricks 或 flatpak 安裝版本")
            return

        launch_shell_in_terminal(cmd)




# 執行主程式
if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
