import pygame
import random
import time
import turtle
import json
from tkinter import *

THEME_COLOR = "#375362"

# Class thể hiện đối tượng Câu hỏi
# Một đối tượng Question gồm có 3 fields: 
# - question: đề bài
# - correct_answer: đáp án đúng
# - answers: các đáp án
class Question:
    def __init__(self, question: str, correct_answer: str, answers: list):
        self.question_text = question
        self.correct_answer = correct_answer
        self.answers = answers

        
# Class thể hiện trạng thái hiện tại của trò chơi
class GameState:
    # Điểm số hiện tại
    score = 0

    # Khởi động lại đồng hồ bấm giờ: cho giá trị bằng thời gian hiện tại
    def reset_timer(self):
        self.start_time = time.time()
    
    # Trả về thời gian trả lời câu hỏi (tính bằng giây), bằng cách lấy
    # thời gian đồng hồ trừ đi thời gian start_time đã lưu.
    def get_timer(self):
        return time.time() - self.start_time


# Class thể hiện giao diện màn hình câu hỏi
class QuizInterface:
    def __init__(self) -> None:
        # Khởi tạo đối tượng cụ thể lưu trạng thái của trò chơi
        self.state = GameState()
        
        # Vẽ hình nhân vật.
        self.avatar = turtle.Turtle()
        
        # Khởi tạo cây bút chuyên dùng để vẽ thời gian.
        self.pen_timer = turtle.Turtle()
        
        # Khởi tạo cây bút chuyên dùng để vẽ Điểm số.
        self.pen_score = turtle.Turtle()
        
        # Gọi hàm thiết lập màn hình    
        self.setup_turtle()
        
        # Chơi nhạc
        self.play_music("music.wav")

        # Vẽ thời gian
        self.state.reset_timer()
        self.draw_timer()
        # Kết hợp các câu đố vui đọc từ File với các câu tính nhẩm Siêu Trí Tuệ.
        data = self.read_data()

        # Xáo trộn các câu hỏi một cách ngẫu nhiên
        random.shuffle(data)
        for index, question in enumerate(data):
            question_no = index + 1
            self.display_question(question_no, question)

    # Thiết lập màn hình giao diện turtle
    def setup_turtle(self):
        # Màn hình turtle
        self.screen = turtle.Screen()
        # Thiết lập kích thước màn hình 
        self.screen.setup(1200, 600)
        # Thiết lập ảnh nền cho màn hình
        self.screen.bgpic('background_hospital.gif')
        # Thiết lập tiêu đề cho cửa sổ chương trình
        turtle.title("Siêu Trí Tuệ")

    # Dùng thư viện pygame để chơi âm thanh. 
    def play_music(self, file):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        
    def play_sound(self, file):
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file)
        sound.play()
            
    def draw_avatar(self, image):
        # Phải gọi lệnh turtle.addshape trước khi vẽ ảnh.
        turtle.addshape(image)
        self.avatar.speed(0)
        self.avatar.clear()
        self.avatar.penup()
        self.avatar.setposition(350, -100)
        # Lưu ý: turtle chỉ vẽ được ảnh có định dạng .gif
        self.avatar.shape(image)

    def draw_timer(self):
        # Ẩn con rùa.
        self.pen_timer.hideturtle()
        # Nhấc bút lên.
        self.pen_timer.penup()
        # Xoá, để khi vẽ điểm không bị đè lên nhau.
        self.pen_timer.clear()
        # Đổi màu.
        self.pen_timer.color('green')
        # Đặt vị trí.
        self.pen_timer.setposition(10, 160)
        # Viết timer ra màn hình.
        self.pen_timer.write(f"Time: {self.format_time(round(self.state.get_timer()))}", font=self.get_font(20))
        # Vẽ lại timer sau 1000ms (1 giây) nữa
        turtle.Screen().ontimer(self.draw_timer, 1000)

    def draw_score(self):
        # Ẩn con rùa.
        self.pen_score.hideturtle()
        # Nhấc bút lên.
        self.pen_score.penup()
        # Xoá, để khi vẽ điểm không bị đè lên nhau.
        self.pen_score.clear()
        # Đổi màu.
        self.pen_score.color('white')
        # Đặt vị trí.
        self.pen_score.setposition(340, 150)
        # Viết điểm số ra màn hình.
        self.pen_score.write(f"Score: {self.state.score}", font=self.get_font(25))

    # In câu hỏi ra màn hình
    def display_question(self, question_no, question):
        # In ra dấu * ngăn cách giữa hai câu hỏi
        print("***************************")
        print(question["question"])
        # Xoá màn hình trước khi vẽ để chữ khỏi bị viết đè lên nhau
        turtle.clear()
        # Ẩn con rùa (hình tam giác) 
        turtle.hideturtle()
        # Nhấc bút lên (để khỏi để lại dấu vết)
        turtle.penup()
        
        # Đặt vị trí bút (để viết câu hỏi)
        turtle.setposition(-500, 80)
        # In câu hỏi ra màn hình Turtle và cho biết cỡ font chữ.
        turtle.write(f"Câu {question_no}: {question['question']}", font=self.get_font(15))
        
        # Đặt vị trí bút (để viết category)
        turtle.setposition(-500, 50)
        # In câu hỏi ra màn hình Turtle và cho biết cỡ font chữ.
        turtle.write(f"Chủ đề: {question['category']}. Độ khó: {question['difficulty']}", font=self.get_font(12))
        
        # In câu trả lời ra màn hình Turtle.
        for index, answer in enumerate(question["answers"]):
            turtle.setposition(-500, 50 - 30 * (index + 1))
            turtle.write(answer, font=self.get_font(15))
        
        # Gọi hàm viết điểm số ra màn hình.
        self.draw_score()
        # Vẽ hình nhân vật trạng thái bình thường 
        self.draw_avatar('KimNguu-normal.gif')
        # Trước khi hỏi câu hỏi mới, cần khởi động lại đồng hồ bấm giờ
        self.state.reset_timer()

        # Hỏi người dùng nhập câu trả lời qua giao diện Turtle
        result = turtle.textinput("Siêu Lập Trình", "Câu trả lời của bạn là gì?\n")    # So sánh kết quả của người chơi nhập vào với đáp án
        self.check_result(result, question["correct_answer"])

    # So sánh câu trả lời với đáp án
    def check_result(self, result, answer):
        # Thời gian người chơi trả lời câu hỏi (tính bằng giây).
        time_taken = self.state.get_timer()
        # Tính điểm thưởng nếu trả lời nhanh.
        if time_taken < 5:
            bonus = 5
        else:
            bonus = 0
        if result == answer:
            # Cộng điểm nếu người chơi trả lời đúng
            # Cộng điểm trả lời đúng và cả điểm thưởng nữa.
            self.state.score += 10 + bonus    
            # Chơi âm thanh cho biết trả lời đúng.
            self.play_sound("correct_answer.wav")

            # Vẽ hình nhân vật khi trả lời đúng.
            self.draw_avatar('KimNguu-correct.gif')
            print("Đúng rồi")
        else:
            # Chơi âm thanh cho biết trả lời sai.
            self.play_sound("wrong_answer.wav")

            # Vẽ hình nhân vật khi trả lời sai.
            self.draw_avatar('KimNguu-wrong.gif')
            print("Sai rồi")

        # Chờ một chút để thấy rõ nhân vật cử động.
        time.sleep(0.5)
        print("Thời gian trả lời câu hỏi là:", round(time_taken), "giây")
        if bonus > 0:
            print("Bạn nhận được điểm thưởng là", bonus, "vì trả lời nhanh")            
        print("Điểm hiện tại của bạn là: ", self.state.score)

    # Khai báo dữ liệu câu hỏi và đáp án
    def read_data(self):
        # Ban đầu, mảng dữ liệu là trống
        data = []
            
        f = open("data.json", 'r', encoding='utf-8')
        result = json.load(f)
        data = result["questions"]
        f.close() 
        # Trả về mảng dữ liệu data     
        return data

    # Trả về font chữ với kích thước được cho.
    def get_font(self, font_size):
        return ("Arial", font_size, "normal")
    
    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        return min_sec_format       

# Class thể hiện giao diện màn hình bắt đầu.
class HomeInterface:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Siêu Trí Tuệ")
        self.window.geometry("600x600")
        self.window.configure(bg='#FFC75F')

        # Hiển thị tiêu đề
        self.display_title()
        
        # Hiển thị footer
        self.display_footer()

        # Hiển thị các nút
        self.buttons()

        # Lặp màn hình
        self.window.mainloop()

    def display_title(self):
        """Hiển thị tiêu đề"""

        # Tạo tiêu đề
        title = Label(self.window, text="Siêu Trí Tuệ",
                      width=30, bg="#FFC75F", fg="#4B4453", font=("ariel", 30, "bold"))

        # Vị trí tiêu đề
        title.place(relx=0.5, rely=0.2, anchor=CENTER)
    
    def display_footer(self):
        """Hiển thị tiêu đề"""

        # Tạo tiêu đề
        text = Label(self.window, text="Nguyen Anh Tuan - Final Project CS101 - STEAM FOR VIET NAM",
                      width=65, bg="#FFC75F", fg="#4B4453", font=("ariel", 12, "bold"))

        # Vị trí tiêu đề
        text.place(relx=0.5, rely=0.9, anchor=CENTER)

    def start_game(self):
        # Khởi tạo giao diện màn hình câu hỏi.   
        self.window.destroy()
        quiz = QuizInterface()
    
    def buttons(self):
        """Hiển thị nút Start và nút Quit trên màn hình"""
        start_button = Button(self.window, text="Start", command=self.start_game,
                             width=15, height=2, bg="green", fg="white",
                             highlightbackground='#845EC2', font=("ariel", 16, "bold"))

        # palcing the button  on the screen
        start_button.place(relx=0.5, rely=0.4, anchor=CENTER)

        # This is the second button which is used to Quit the self.window
        quit_button = Button(self.window, text="Quit", command=self.window.destroy,
                             width=15, height=2, bg="red", fg="white",
                             highlightbackground='red', font=("ariel", 16, " bold"))

        # placing the Quit button on the screen
        quit_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    
def main():
    home = HomeInterface()
    

if __name__ == "__main__":
    main()
    pygame.quit()
