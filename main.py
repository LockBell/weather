import os.path

import matplotlib.pyplot as plt
import platform
import csv

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# os check
if platform.system() == "Darwin":
    plt.rcParams.update({"font.family": "AppleGothic"})
elif platform.system() == "Windows":
    plt.rcParams.update({"font.family": "Malgun Gothic"})
else:
    print("미지원 OS")
    exit(1)


def change_graph(new_frame: Frame):
    new_frame.tkraise()


# file 을 읽는 함수
def read_csv(file_path: str):
    with open(file_path, 'r', encoding="UTF-8") as file:
        x, y = [], []
        for item in list(csv.reader(file))[1:]:
            if item[0] != '0.0':
                x.append(item[0].split('-')[2])
                y.append(float(item[1]))
        figure.clear()
        pl = figure.add_subplot(1, 1, 1)
        pl.set_xlabel('날짜(일)')
        pl.set_ylabel('강우량')
        pl.set_title(file_path.replace('_', ' ').split(".")[0])
        pl.plot(x, y, '-')
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0)
    change_graph(graph_frame)


# file donwload function
def download_file(path: str):
    items = dict()
    cp_path = f"./{os.path.basename(path)}"
    with open(cp_path, 'w') as cp_file:
        writer = csv.writer(cp_file)
        writer.writerow(["하루 총 우량", "날짜"])
        with open(path, 'r', encoding="cp949") as file:
            for item in list(csv.reader(file))[1:]:
                date = item[-1].split(' ')[0]
                items[date] = items.get(date, 0.0) + float(item[-2])
        writer.writerows(sorted([[k, v] for k, v in items.items()], key=lambda c: c[0]))
    read_csv(cp_path)


def get_data():
    y = year.get().strip()
    m = month.get().strip().zfill(2)
    file_path = f"./서울시_강우량_정보_{y}년{m}월.csv"
    if os.path.exists(file_path):
        read_csv(file_path)
        return True
    elif os.path.exists(f"./서울시_강우량_정보_{y}년"):
        if os.path.exists(f"./서울시_강우량_정보_{y}년/서울시_강우량_정보_{y}년{m}월.csv"):
            message.configure(text="다운로드 중")
            change_graph(message_frame)
            download_file(f"./서울시_강우량_정보_{y}년/서울시_강우량_정보_{y}년{m}월.csv")
            return True
    message.configure(text="존재하지 않는 날짜 입니다.")
    change_graph(message_frame)


# gui 생성
tk = Tk()
tk.title("서울시 강우량 조회")
graph_frame = Frame(tk, width=10, height=7)
main_frame = Frame(tk)
message_frame = Frame(tk)

month = StringVar(tk)
year = StringVar(tk)

# 날짜 입력 텍스트
Label(main_frame, text="연도:", height=1).pack(side=LEFT)
Entry(main_frame, width=10, textvariable=year).pack(side=LEFT)
Label(main_frame, text="월:", height=1).pack(side=LEFT)
Entry(main_frame, width=10, textvariable=month).pack(side=LEFT)
# month.pack(side=LEFT)
Button(main_frame, text="검색", command=get_data).pack(side=LEFT)

# 그래프 프레임
Button(graph_frame, text="뒤로가기", command=lambda: change_graph(main_frame)).grid(row=0, column=0, sticky=W)
Label(graph_frame, text="강우량 검색").grid(row=0, column=0)
figure = Figure(figsize=(10, 7), dpi=100)
canvas = FigureCanvasTkAgg(figure, master=graph_frame)
canvas.get_tk_widget().grid(row=1, column=0)

# 메세지 프레임
Button(message_frame, text="뒤로가기", command=lambda: change_graph(main_frame)).pack()
message = Label(message_frame)
message.pack()

main_frame.grid(row=0, column=0, sticky=NSEW)
graph_frame.grid(row=0, column=0, sticky=NSEW)
message_frame.grid(row=0, column=0, sticky=NSEW)
change_graph(main_frame)

# 종료 방지
tk.mainloop()
