import pygame
import random
import time
import turtle
import json
from tkinter import *

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
    QUESTION_TIME = 20
    
    def __init__(self):
        self.score = 0
        self.name = None
        self.running = False
    
    # Khởi động lại đồng hồ bấm giờ: cho giá trị bằng thời gian hiện tại + thời gian trả lời câu hỏi
    def reset_timer(self):
        self.start_time = time.time() + self.QUESTION_TIME
    
    # Trả về thời gian trả lời câu hỏi (tính bằng giây), bằng cách lấy
    # thời gian start_time đã lưu trừ đi thời gian đồng hồ.
    def get_timer(self):
        countdown = round(self.start_time - time.time())
        
        return countdown if countdown > 0 else 0


# Class thể hiện giao diện màn hình câu hỏi
class QuizInterface:
    def __init__(self) -> None:
        # Gọi hàm thiết lập màn hình    
        self.setup_turtle()
        
        # Khởi tạo đối tượng cụ thể lưu trạng thái của trò chơi
        self.state = GameState()
        self.state.running = True
        
        # Vẽ hình nhân vật.
        self.avatar = turtle.Turtle()
        
        # Khởi tạo cây bút chuyên dùng để vẽ thời gian.
        self.pen_timer = turtle.Turtle()
        
        # Khởi tạo cây bút chuyên dùng để vẽ Điểm số.
        self.pen_score = turtle.Turtle()
        
        # Khởi tạo cây bút chuyên dùng để vẽ Điểm số.
        self.pen_name = turtle.Turtle()
        
        # Chơi nhạc
        self.play_music("music.wav")
        
        # Vẽ hình nhân vật trạng thái bình thường 
        self.draw_avatar('KimNguu-normal.gif')
        
        # Hỏi người dùng nhập tên
        while True:
            result = turtle.textinput("Siêu Lập Trình", "Hãy nhập tên của bạn.\n")
            if result is not None and len(result) > 0:
                self.state.name = result
                break

        # Vẽ tên người chơi
        self.draw_name()
        
        # Gọi hàm viết điểm số ra màn hình.
        self.draw_score()
        
        # Vẽ thời gian
        self.state.reset_timer()
        self.draw_timer()
        
        # Đọc dữ liệu câu hỏi
        questions = self.read_data()
        self.number_questions = len(questions)

        # Xáo trộn các câu hỏi một cách ngẫu nhiên
        random.shuffle(questions)
        for index, question in enumerate(questions):
            question_no = index + 1
            self.display_question(question_no, question)
            if question_no == self.number_questions:
                # Đặt vị trí bút (để viết câu hỏi)
                turtle.setposition(-300, -150)
                # In câu hỏi ra màn hình Turtle và cho biết cỡ font chữ.
                turtle.write("Chúc mừng bạn đã hoàn thành!", font=self.get_font(18))
                self.write_result()
                time.sleep(2)
                self.reset()
                home = HomeInterface()
                
    def reset(self):
        self.state.running = False
        self.screen.setup(0, 0)
        turtle.clear()
        self.avatar.clear()
        self.pen_score.clear()
        self.pen_name.clear()
        self.pen_timer.clear()
        pygame.mixer.music.stop()       

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
        
        if self.state.running is True:
            # Vẽ lại timer sau 1000ms (1 giây) nữa
            self.screen.ontimer(self.draw_timer, 1000)
        
    def draw_name(self):
        self.pen_name = turtle.Turtle()
        # Ẩn con rùa.
        self.pen_name.hideturtle()
        # Nhấc bút lên.
        self.pen_name.penup()
        # Xoá, để khi vẽ name không bị đè lên nhau.
        self.pen_name.clear()
        # Đổi màu.
        self.pen_name.color('white')
        # Đặt vị trí.
        self.pen_name.setposition(280, 180)
        # Viết điểm số ra màn hình.
        self.pen_name.write(f"Người chơi: {self.state.name}", font=self.get_font(16))

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
        self.pen_score.setposition(280, 150)
        # Viết điểm số ra màn hình.
        self.pen_score.write(f"Điểm: {self.state.score}", font=self.get_font(16))

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
        
        
        score = 0
        difficulty_label = None
        if question['difficulty'] == "easy":
            score = 5
            difficulty_label = "Dễ"
        elif question['difficulty'] == "medium":
            score = 10
            difficulty_label = "Trung bình"
        elif question['difficulty'] == "hard":
            score = 15
            difficulty_label = "Khó"
        
        # In category, độ khó và điểm của câu hỏi ra màn hình Turtle và cho biết cỡ font chữ.
        turtle.write(f"Chủ đề: {question['category']} | Độ khó: {difficulty_label} | Điểm: {score}", font=self.get_font(13))
        
        # In các câu trả lời ra màn hình Turtle.
        for index, answer in enumerate(question["answers"]):
            turtle.setposition(-500, 50 - 30 * (index + 1))
            turtle.write(answer, font=self.get_font(15))
            
        # Thiết lập lại avatar
        self.draw_avatar('KimNguu-normal.gif')
        
        # Trước khi hỏi câu hỏi mới, cần khởi động lại đồng hồ bấm giờ
        self.state.reset_timer()
        
        while True:
            # Hỏi người dùng nhập câu trả lời qua giao diện Turtle
            result = turtle.textinput("Siêu Lập Trình", "Câu trả lời của bạn là gì?\n")    # So sánh kết quả của người chơi nhập vào với đáp án
            if result is not None and len(result) > 0:
                self.check_result(result, question["correct_answer"], question["difficulty"])
                break

    # So sánh câu trả lời với đáp án
    def check_result(self, result, answer, difficulty):
        # Thời gian người chơi trả lời câu hỏi (tính bằng giây).
        time_taken = self.state.get_timer()
        
        # Tính điểm thưởng nếu trả lời nhanh.
        if time_taken > 15:
            bonus = 5
        else:
            bonus = 0
            
        if result == answer:
            score = 0
            if difficulty == "easy":
                score = 5
            elif difficulty == "medium":
                score = 10
            elif difficulty == "hard":
                score = 15
            
            # Nếu hết thời gian trả lời đúng chỉ nhận được 2 điểm.
            if time_taken == 0:
                score = 2
            
            # Cộng điểm nếu người chơi trả lời đúng
            # Cộng điểm trả lời đúng và cả điểm thưởng nữa.
            self.state.score += score + bonus    
            
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
        
        # Gọi hàm viết điểm số ra màn hình.
        self.draw_score()

    # Đọc dữ liệu câu hỏi
    def read_data(self):
        # Ban đầu, mảng dữ liệu là trống
        data = []
        
        # Đọc dữ liệu câu hỏi từ tệp data.json
        f = open("data.json", 'r', encoding='utf-8')
        result = json.load(f)
        data = result["questions"]
        f.close()
        
        # Trả về mảng dữ liệu data     
        return data
    
    # Lưu kết quả vào tệp ranking.json
    def write_result(self):
        filename = 'ranking.json'
        data = None
        
        # Đọc dữ liệu từ tệp json
        with open(filename, "r") as file:
            data = json.load(file)
        
        # Thêm dữ liệu vào mảng ranking
        data['ranking'].append({
            "name": self.state.name,
            "score": self.state.score
        })
        
        # Ghi dữ liệu vào tệp json
        with open(filename, "w") as file:
            json.dump(data, file)

    # Trả về font chữ với kích thước được cho.
    def get_font(self, font_size):
        return ("Arial", font_size, "normal")
    
    # Hiển thị thời gian dưới dạng 00:00
    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        return min_sec_format       


# Class thể hiện giao diện màn hình Ranking.
class RankingInterface:
    def __init__(self) -> None:
        # Khởi tạo Window
        self.window = Tk()
        self.window.title("Siêu Trí Tuệ")
        self.window.geometry("600x600")
        self.window.configure(bg='#FFC75F')
        
        self.display_title()
        
        container = Frame(self.window)
        container.pack(fill="both", expand=True, padx=80, pady=80)
        canvas = Canvas(container)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        rankings = self.read_data()
        
        rankings = sorted(rankings, key=lambda k: k['score'], reverse=True)
        
        print(rankings)
        
        for (index, item) in enumerate(rankings):
            Label(scrollable_frame, text=f"{index + 1} | {item['name']} | {item['score']}\n", width=30, bg="white", fg="#4B4453", font=("ariel", 15, "bold")).pack()

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Hiển thị các nút
        self.buttons()

        # Lặp màn hình
        self.window.mainloop()

    def display_title(self):
        # Tạo tiêu đề
        title = Label(self.window, text="Bảng Xếp Hạng",
                      width=30, bg="#FFC75F", fg="#4B4453", font=("ariel", 20, "bold"))

        # Vị trí tiêu đề
        title.place(relx=0.5, rely=0.05, anchor=CENTER)

    def read_data(self):
        # Ban đầu, mảng dữ liệu là trống
        data = []
        
        # Đọc dữ liệu câu hỏi từ tệp ranking.json
        f = open("ranking.json", 'r', encoding='utf-8')
        result = json.load(f)
        data = result["ranking"]
        f.close()
        
        # Trả về mảng dữ liệu data     
        return data
    
    def close(self):
        self.window.destroy()
        # Tạo lại màn hình home
        home = HomeInterface()
    
    def buttons(self):
        # Khởi tạo nút "Thoát"
        quit_button = Button(self.window, text="Đóng", command=self.close,
                             width=15, height=2, bg="red", fg="white",
                             highlightbackground='red', font=("ariel", 16, " bold"))

        # Đặt vị trí nút "Thoát" trên màn hình
        quit_button.place(relx=0.5, rely=0.92, anchor=CENTER)

# Class thể hiện giao diện màn hình bắt đầu.
class HomeInterface:
    def __init__(self) -> None:
        # Khởi tạo Window
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
        # Tạo tiêu đề
        title = Label(self.window, text="Siêu Trí Tuệ",
                      width=30, bg="#FFC75F", fg="#4B4453", font=("ariel", 30, "bold"))

        # Vị trí tiêu đề
        title.place(relx=0.5, rely=0.2, anchor=CENTER)
    
    def display_footer(self):
        text = Label(self.window, text="Nguyễn Anh Tuấn - Dự án cuối khoá học CS101",
                      width=65, bg="#FFC75F", fg="#4B4453", font=("ariel", 12, "bold"))

        text.place(relx=0.5, rely=0.9, anchor=CENTER)
        
        text = Label(self.window, text="STEAM FOR VIET NAM",
                      width=65, bg="#FFC75F", fg="#4B4453", font=("ariel", 12, "bold"))

        text.place(relx=0.5, rely=0.95, anchor=CENTER)

    def start_game(self):
        # Đóng cửa sổ hiện tại
        self.window.destroy()
        # Khởi tạo giao diện màn hình câu hỏi.   
        quiz = QuizInterface()
    
    def display_rank(self):
        # Đóng cửa sổ hiện tại
        self.window.destroy()
        
        # Khởi tạo giao diện bảng xếp hạng.
        ranking = RankingInterface()
    
    def buttons(self):
        # Khởi tạo nút "Bắt đầu"
        start_button = Button(self.window, text="Bắt đầu", command=self.start_game,
                             width=15, height=2, bg="green", fg="white",
                             highlightbackground='#845EC2', font=("ariel", 16, "bold"))

        # Đặt vị trí nút "Bắt Đầu" trên màn hình
        start_button.place(relx=0.5, rely=0.4, anchor=CENTER)

        # Khởi tạo nút "Thoát"
        quit_button = Button(self.window, text="Bảng xếp hạng", command=self.display_rank,
                             width=15, height=2, bg="green", fg="white",
                             highlightbackground='green', font=("ariel", 16, " bold"))

        # Đặt vị trí nút "Thoát" trên màn hình
        quit_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    
def main():
    # Khởi tạo màn hình
    home = HomeInterface()
    
if __name__ == "__main__":
    main()
    pygame.quit()
