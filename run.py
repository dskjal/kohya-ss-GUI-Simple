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
        
    def save_settings(self, dictionary:str):
        filepath = window.create_file_dialog(webview.FileDialog.SAVE, directory='./', save_filename='.json', allow_multiple=False)
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
    
    def get_caption_files(self, folder:str):
        if os.path.isdir(folder):
            return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".txt") and os.path.isfile(os.path.join(folder, f))]
        return []
    
    def addTag(self, folder:str, tag:str, isHead:bool=True):
        '''
            Args:
                folder(str) : キャプションファイルのあるフォルダ。
                isHead(bool) : True=トリガーワードを先頭に挿入。False=トリガーワードを末尾に挿入
        '''
        text_files = self.get_caption_files(folder)
        if not text_files:
            return "フォルダが存在しないか、フォルダ内に .txt ファイルがありません"
        
        processed_file_count = 0
        for file in text_files:
            with open(file, mode="r+", encoding="utf-8") as f:
                content = f.read()
                f.seek(0)

                # すでにタグが存在するならスキップ
                tags = [t.strip() for t in content.split(',')]
                if tag in tags:
                    continue
                
                processed_file_count += 1

                if isHead:
                    f.write(f'{tag}, {content}')
                else:
                    f.write(f'{content}, {tag}')

        return f'{processed_file_count} 個のファイルが変更されました'

    def moveTag(self, folder:str, tag:str, isHead:bool=True):
        '''
            Args:
                folder(str) : キャプションファイルのあるフォルダ。
                isHead(bool) : True=トリガーワードを先頭に移動。False=トリガーワードを末尾に移動
        '''
        text_files = self.get_caption_files(folder)
        if not text_files:
            return "フォルダが存在しないか、フォルダ内に .txt ファイルがありません"
        
        processed_file_count = 0
        for file in text_files:
            with open(file, mode="r+", encoding="utf-8") as f:
                content = f.read()
                f.seek(0)

                # タグの移動
                tags = [t.strip() for t in content.split(',')]
                if tag in tags:
                    processed_file_count += 1

                    tags.remove(tag)
                    content = ', '.join(tags)

                    # 書き込み
                    if isHead:
                        f.write(f'{tag}, {content}')
                    else:
                        f.write(f'{content}, {tag}')

        return f"{processed_file_count} 個のファイルが変更されました"
        
    def replaceUnderscoreToSpace(self, folder:str):
        text_files = self.get_caption_files(folder)
        if not text_files:
            return "フォルダが存在しないか、フォルダ内に .txt ファイルがありません"
        
        for file in text_files:
            with open(file, mode="r+", encoding="utf-8") as f:
                content = f.read().replace('_', ' ')
                f.seek(0)
                f.write(content)

        return f'{len(text_files)} 個のファイルが変更されました'


    def isLearning(self):
        return self.process and self.process.poll() is None
        
    def exec(self, command:str, kohya_ss_folder:str):
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