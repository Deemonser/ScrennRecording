import cv2
import pathlib, os, time
import shutil, subprocess


def find_all_file(dir, end_name):
    path = pathlib.Path(dir)
    return path.rglob(end_name)


def move_rename(fileList, dir):
    for file in fileList:
        path = pathlib.Path(file)
        print(path)
        rename = str(file).replace('/', '$$').replace(':$$', '$$$')
        print(rename)
        join = os.path.join(dir, rename)
        print(join)
        path.rename(join)


def reserve_name(file):
    path = pathlib.Path(file)

    print(path)
    rename = str(path.parent) + '/' + path.name.replace('$$', '/')
    print(rename)
    if not os.path.exists(os.path.dirname(rename)):
        os.makedirs(os.path.dirname(rename))
    path.rename(rename)


def moveFile(dir, end_name, to_dir):
    file_list = find_all_file(dir, end_name)
    print(file_list)
    move_rename(file_list, to_dir)


def restore(dir, end_name):
    path = pathlib.Path(dir)
    file_list = path.glob(end_name)
    for file in file_list:
        reserve_name(file)


def compression(file):
    path = pathlib.Path(file)
    tmp_name = str(path.absolute()).replace(path.name, str(time.time()) + path.suffix)
    out_file = tmp_name.replace(path.suffix, "-out" + path.suffix)
    shutil.copy(file, tmp_name)
    video = cv2.VideoCapture(tmp_name)
    fps = video.get(cv2.CAP_PROP_FPS)
    subprocess.call(
        'ffmpeg -y -threads 4 -r ' + str(fps) + ' -i ' + tmp_name + ' ' + out_file,
        shell=True)

    os.remove(file)
    os.rename(out_file, file)
    os.remove(tmp_name)


def aa(dir):
    path = pathlib.Path(dir)
    file_list = path.glob('*.mp4')

    for file in file_list:
        path = pathlib.Path(file)
        print(path.absolute())
        rename = str(path.absolute()).replace(
            '华为ServiceComb课程', '阶段1：微服务课程-19.华为ServiceComb课程')

        print(rename)
        if not os.path.exists(os.path.dirname(rename)):
            os.makedirs(os.path.dirname(rename))
        path.rename(rename)


if __name__ == '__main__':
    path = pathlib.Path(r'/Volumes/DEEMONS/Videos/tmp')
    file_list = path.glob('*.mp4')

    for file in file_list:
        compression(file)

    # aa(r'/Volumes/DEEMONS/Videos')
    # moveFile(r'/Volumes/DEEMONS/Videos', '*.mp4', r'/Volumes/DEEMONS/Videos/tmp')
    # restore(r'/Volumes/DEEMONS/Videos', '*.mp4')
