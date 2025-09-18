import webview
import subprocess
import json
import os
import re

class Api:
    def __init__(self):
        self.process = None

    def run_test(self):
        subprocess.run("test.cmd")
        
    def save_settings(self, dictionary):
        filepath = window.create_file_dialog(webview.FileDialog.SAVE, directory='./saved_settings', save_filename='.json', allow_multiple=False)
        if filepath:
            with open(filepath[0], "w", encoding="utf-8") as f:
                json.dump(dictionary, f, ensure_ascii=False, indent=4)

    def load_settings(self):
        filepath = window.create_file_dialog(webview.FileDialog.OPEN)
        if filepath:
            with open(filepath[0], "r", encoding="utf-8") as f:
                return f.read()
        return ""
    
    def selectFolder(self):
        return window.create_file_dialog(webview.FileDialog.FOLDER, allow_multiple=False)
    
    def selectTrainDataDir(self):
        dir = window.create_file_dialog(webview.FileDialog.FOLDER, allow_multiple=False)
        if dir is None:
            # キャンセルされた
            return ""
        
        dirs = os.listdir(dir[0])
        for d in dirs:
            if re.fullmatch(r"[1-9][0-9]*_.+", d):
                return dir
        return 'フォルダ内に "数値_文字" （例 1_train）のフォルダが必要です。教師画像とキャプションをそのフォルダに配置します'

    def selectFile(self):
        return window.create_file_dialog(webview.FileDialog.OPEN, allow_multiple=False)

    def isLearning(self):
        return self.process and self.process.poll() is None
        
    def exec(self, command, kohya_ss_folder):
        if self.isLearning():
            return "learning"
        
        print(kohya_ss_folder)
        print(command)
        if os.name == "nt":
            # Windows
            commands = f'cd {kohya_ss_folder} && call venv\\Scripts\\activate && {command}'
        else:
            # Linux
            commands = f'cd {kohya_ss_folder} && source venv/bin/activate && {command}'
            
        self.process = subprocess.Popen(commands, shell=True, text=True)

window = webview.create_window("kohya-ss GUI", url="./index.html", js_api=Api())
webview.start(http_server=True, debug=False)