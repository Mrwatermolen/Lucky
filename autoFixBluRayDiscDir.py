# content: auto fix Bluray directory structure
# author: Lam mingPang(mplin)
# datetime:2021/10/21
import os
import sys
import tkinter
from tkinter import filedialog

dir_mode = ['os.F_OK', 'os.R_OK', 'os.W_OK']
dir_status = [False, False, False]  # exist, read, write
bluRayStruct = {
    'BDMV': {
        'self': ['', 'AUXDATA', 'BACKUP', 'BDJO',
                 'CLIPINF', 'JAR', 'META', 'PLAYLIST', 'STREAM'],
        'BACKUP': ['', 'BDJO', 'CLIPINF', 'JAR', 'PLAYLIST']
    },
    'CERTIFICATE': {'self': ['', 'BACKUP']}
}
bluRaySource = ''
missing = []

if 'win' in sys.platform:
    root = tkinter.Tk()
    root.withdraw()
    bluRaySource = filedialog.askdirectory()
else:
    bluRaySource = input("请输入需要检查的蓝光光盘目录")


for index, authority in enumerate(dir_mode):
    if not os.access(bluRaySource, eval(authority)):
        print(f"dir: {bluRaySource} status: {authority} is {False}")
        break
    dir_status[index] = True
if dir_status[0] and dir_status[1] and dir_status[2]:
    for folder in bluRayStruct:
        first_path = os.path.join(bluRaySource, folder)
        for item in bluRayStruct[folder]:
            second_path = (first_path) if (item == 'self') else (
                os.path.join(first_path, item))
            for final_item in bluRayStruct[folder][item]:
                valid_path = os.path.join(second_path, final_item)
                if not os.path.exists(valid_path):
                    missing_dir = os.path.join(os.path.join(
                        folder, item.replace('self', '')), final_item)
                    if missing_dir == os.path.join(folder, ''):
                        print(f"{bluRaySource}该目录非蓝光光盘目录")
                        for i in range(len(missing)):
                            print(f"已创建的文件夹{missing[i]}")
                        exit(0)
                    os.mkdir(valid_path)
                    missing.append(missing_dir)

if missing == []:
    print(f"{bluRaySource}的蓝光光盘目录结构完整")
else:
    print(f"{bluRaySource}的蓝光光盘目录结构缺失")
    for i in range(len(missing)):
        print(f"修复缺失文件夹{missing[i]}")
