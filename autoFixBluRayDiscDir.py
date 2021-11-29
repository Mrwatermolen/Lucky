# content: auto fix Bluray directory structure
# author: MH
# datetime:2021/10/29
import os
import sys


def simplifyPath(path: str) -> str:
    leng = len(path)
    if leng == 1:
        return "/"

    idx = 0
    pathlist0 = path.split('/')
    pathlist1 = []
    for i in pathlist0:
        if i and i != '.':
            pathlist1.append(i)

    pathlist0 = []
    for i in pathlist1:
        if i != '..':
            idx += 1
            pathlist0.append(i)
        else:
            if idx > 0:
                pathlist0.pop()
                idx -= 1

    if idx <= 0:
        return "/"
    else:
        res = "/"
        for i in range(idx):
            if i < idx-1:
                res += pathlist0[i] + '/'
            else:
                res += pathlist0[i]
    return res


if __name__ == '__main__':
    # BDMV/AUXDATA
    # BDMV/BACKUP
    # BDMV/BDJO
    # BDMV/CLIPINF
    # BDMV/JAR
    # BDMV/META
    # BDMV/PLAYLIST
    # BDMV/STREAM
    # BDMV/BACKUP/BDJO
    # BDMV/BACKUP/CLIPINF
    # BDMV/BACKUP/JAR
    # BDMV/BACKUP/PLAYLIST
    # CERTIFICATE/BACKUP
    dir_mode = ['os.F_OK', 'os.R_OK', 'os.W_OK']
    dir_status = [False, False, False]  # exist, read, write
    bluRayStruct = {
        'BDMV': {
            '.': ['', 'AUXDATA', 'BACKUP', 'BDJO',
                  'CLIPINF', 'JAR', 'META', 'PLAYLIST', 'STREAM'],
            'BACKUP': ['BDJO', 'CLIPINF', 'JAR', 'PLAYLIST']
        },
        'CERTIFICATE': {'.': ['', 'BACKUP']}
    }
    bluRay_source = ''
    missing = []
    is_bluRay = True

    try:
        import tkinter
        from tkinter import filedialog
        root = tkinter.Tk()
        root.withdraw()
        bluRay_source = filedialog.askdirectory()
    except:
        bluRay_source = input("请输入需要检查的蓝光光盘目录")

    for index, authority in enumerate(dir_mode):
        if not os.access(bluRay_source, eval(authority)):
            print(f"dir: {bluRay_source} status: {authority} is {False}")
            break
        dir_status[index] = True

    if dir_status[0] and dir_status[1] and dir_status[2]:
        for folder in bluRayStruct:
            first_path = os.path.join(bluRay_source, folder)

            if not os.path.exists(first_path):
                print(f"检查目录'{bluRay_source}' 缺少{folder}文件夹，该目录非蓝光光盘目录")
                for i in range(len(missing)):
                    print(f"已创建的文件夹{missing[i]}")
                is_bluRay = False
                break

            for second_folder in bluRayStruct[folder]:
                second_path = os.path.join(first_path, second_folder)

                for final_item in bluRayStruct[folder][second_folder]:
                    valid_path = os.path.join(second_path, final_item)

                    if not os.path.exists(valid_path):
                        missing_dir = os.path.join(os.path.join(
                            folder, second_folder), final_item)
                        os.mkdir(valid_path)
                        missing.append(missing_dir)
        if missing == [] and is_bluRay:
            print(f"{bluRay_source}的蓝光光盘目录结构完整")
        elif is_bluRay:
            print(f"{bluRay_source}的蓝光光盘目录结构缺失")
            for i in range(len(missing)):
                m = simplifyPath(
                    '/' + missing[i].replace('\\', '/'))  # for win
                print(f"修复缺失文件夹{m[1:]}")
