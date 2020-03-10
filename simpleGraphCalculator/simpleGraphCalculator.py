from tkinter import *
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import urllib.request

class Calculator:

    def input_value(self, val):
        self.entry_value.insert("end", val)

    def clear_all(self):
        self.entry_value.delete(0, "end")
    
    def get_result(self):
        try:
            #return_value = eval(self.entry_value.get())

            #https://api.mathjs.org/
            #replace '+' to '%2B'
            api_url = "http://api.mathjs.org/v4/?expr="
            expr = self.entry_value.get().replace("+", "%2B")
            url = api_url + expr
            print(url)
            url_data = urllib.request.urlopen(url)
            print(url_data)
            return_value = url_data.read().decode('utf-8')
            #write entry value to file
            f = open("calc_log.txt", "w")
            f.write(self.entry_value.get())
            f.close()
        except SyntaxError or NameError :
            # clear entry
            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, 'Input Error, Press AC Button')
        else :
            # clear entry
            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, return_value)

    def get_last_log(self):
        #read entry value from file
        f = open("calc_log.txt", "r")
        read_value = f.read()
        self.entry_value.delete(0, "end")
        self.entry_value.insert(0, read_value)
        f.close()

    def __init__(self, main):      
        #main
        main.title("Simple Calculator") #생성할 창 제목
        main.geometry() #기하학을 쓸거

        #입력창 생성(위치, 가로길이, 정렬)
        self.entry_value = Entry(main, width=40, justify=RIGHT) 

        #그리드 쓸것(행위치, 열위치, 열몇개합칠건지)
        self.entry_value.grid(row = 0, column = 0, columnspan = 3)

        #커서생기게 
        self.entry_value.focus_set() 

        #Generating Buttons
        #람다 : 무기명 함수. 그냥 함수 쓰면 매개변수를 못 넣는데 람다로 지정한 후에는 매개변수를 넣을 수 있음 
        Button(main, text = "=", width = 30, command = lambda:self.get_result()).grid(row = 5, column = 2, columnspan=2)
        Button(main, text = "AC", width = 10, command = lambda:self.clear_all()).grid(row = 4, column = 0)
        Button(main, text = "<", width = 10, command = lambda:self.get_last_log()).grid(row = 0, column = 3)
        Button(main, text = "+", width = 10, command = lambda:self.input_value('+')).grid(row = 1, column = 3)
        Button(main, text = "-", width = 10, command = lambda:self.input_value('-')).grid(row = 2, column = 3)
        Button(main, text = "x", width = 10, command = lambda:self.input_value('x')).grid(row = 3, column = 3)
        Button(main, text = "/", width = 10, command = lambda:self.input_value('/')).grid(row = 4, column = 3)
        Button(main, text = ".", width = 10, command = lambda:self.input_value('.')).grid(row = 4, column = 2)
        Button(main, text = "(", width = 10, command = lambda:self.input_value('(')).grid(row = 5, column = 0)
        Button(main, text = ")", width = 10, command = lambda:self.input_value(')')).grid(row = 5, column = 1)
        Button(main, text = "7", width = 10, command = lambda:self.input_value(7)).grid(row = 1, column = 0)
        Button(main, text = "8", width = 10, command = lambda:self.input_value(8)).grid(row = 1, column = 1)
        Button(main, text = "9", width = 10, command = lambda:self.input_value(9)).grid(row = 1, column = 2)
        Button(main, text = "4", width = 10, command = lambda:self.input_value(4)).grid(row = 2, column = 0)
        Button(main, text = "5", width = 10, command = lambda:self.input_value(5)).grid(row = 2, column = 1)
        Button(main, text = "6", width = 10, command = lambda:self.input_value(6)).grid(row = 2, column = 2)
        Button(main, text = "1", width = 10, command = lambda:self.input_value(1)).grid(row = 3, column = 0)
        Button(main, text = "2", width = 10, command = lambda:self.input_value(2)).grid(row = 3, column = 1)
        Button(main, text = "3", width = 10, command = lambda:self.input_value(3)).grid(row = 3, column = 2)
        Button(main, text = "0", width = 10, command = lambda:self.input_value(0)).grid(row = 4, column = 1)

        #파일 만들기
        f = open("calc_log.txt", "w")
        f.close()



class ScienceCalculator(Calculator): #Calculator class를 상속받음
    def get_sqrt(self): #루트
        try:
            return_value = eval(self.entry_value.get())
        except SyntaxError or NameError:
            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, 'Input Error, Press AC button')
        else :
            calc_value = math.sqrt(return_value)
            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, calc_value)

    def get_pow(self): #제곱근
        try:
            return_value = eval(self.entry_value.get())
        except SyntaxError or NameError:
            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, 'Input Error, Press AC button')
        else:
            calc_value = math.pow(return_value, 2)
            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, calc_value)

    def __init__(self, main):
        super().__init__(main) #super 클래스를 가져옴.
        main.title("Science Calculator")
        Button(main, text = "sqrt", width = 10, command = lambda:self.get_sqrt()).grid(row = 5, column = 0)
        Button(main, text = "pow", width = 10, command = lambda:self.get_pow()).grid(row = 5, column = 1)




class GraphCalculator(ScienceCalculator): #ScienceCalculator를 상속받음
    x = []
    y = []
    fig = Figure(figsize=(3,3), dpi = 100)
    ax = fig.add_subplot(111) #colume, subcolumn, row
    canvas = None

    def get_sqrt(self): #루트
        super().get_sqrt()
        for t in np.linspace(0, 100, 100): #시작점, 끝점, 그 사이의 점개수
            self.x.append(t) #x축에는 t의 값을 ㄴ
            self.y.append(math.sqrt(t)) #y축에는 t의 루트값을
        self.ax.plot(self.x, self.y) #plot에다가 x,y값을 넣어주고
        self.canvas = FigureCanvasTkAgg(self.fig, main) #canvas에 fig를 넣어줌 
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=4) #canvas창 위치조정

    def get_pow(self): #제곱근
        super().get_pow()
        for t in np.linspace(0, 100, 100): #시작점, 끝점, 그 사이의 점개수
            self.x.append(t) #x축에는 t의 값을 
            self.y.append(math.pow(t, 2)) #y축에는 t의 제곱의 값을
        self.ax.plot(self.x, self.y) #plot에다가 x,y값을 넣어주고
        self.canvas = FigureCanvasTkAgg(self.fig, main) #canvas에 fig를 넣어줌 
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=4) #canvas창 위치조정    

    
#main
main = Tk()
calc = GraphCalculator(main) #생성자. Tk 창을 만든것이 main이니까. main을 넣어주고. 그 객체를 Calc라고 할거
main.mainloop()
