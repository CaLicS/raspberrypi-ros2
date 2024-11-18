import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
from tkinter import PhotoImage
import subprocess

class ROS2PublisherNode(Node):
    def __init__(self):
        super().__init__('gui_publisher_node')
        self.publisher_ = self.create_publisher(String, 'help', 10)
    
    def send_message(self, message):
        msg = String()
        msg.data = message
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent message: {msg.data}')

class GUIApp:
    def __init__(self, ros_node):
        self.window = tk.Tk()
        self.window.title("ROS2 Voice Control")
        
        # 창 크기 설정
        self.window.geometry("800x480")
        self.window.overrideredirect(True)
        self.window.configure(background = "White")
                           
        self.button_text = tk.StringVar()
        self.button_text.set("Start")

        #self.start_image = PhotoImage(file="/home/sjm/ros2_ws/src/my_publisher_package/my_publisher_package/helpbutton.png")
        #self.stop_image = PhotoImage(file="/home/sjm/ros2_ws/src/my_publisher_package/my_publisher_package/mic.png")

        pil_image = Image.open("/home/sjm/ros2_ws/src/my_publisher_package/my_publisher_package/helpbutton.png")
        resized_pil_image = pil_image.resize((350,350), Image.ANTIALIAS)
        self.start_image = ImageTk.PhotoImage(resized_pil_image)

        pil_image = Image.open("/home/sjm/ros2_ws/src/my_publisher_package/my_publisher_package/mic.png")
        resized_pil_image = pil_image.resize((350,350), Image.ANTIALIAS)
        self.stop_image = ImageTk.PhotoImage(resized_pil_image)

        # if self.button_text == "Start":
        #     self.button = tk.Button(self.window, image = tk_image, command = self.on_button_click)
        #     self.button.image = tk_image
        #     self.button.place(x = 50, y = 50)
        # else:
        #     self.button = tk.Button(self.window, image = mic_image, command = self.on_button_click)
        #     self.button.image = mic_image
        #     self.button.place(x = 50, y = 50)

        #self.button = tk.Button(self.window, textvariable=self.button_text, command=self.on_button_click, width=20, height=2)
        self.button = tk.Button(self.window, image = self.start_image, command = self.on_button_click)
        self.button.place(x = 50, y = 50)

        self.quit_button = tk.Button(self.window, text="Quit", command=self.quit, width = 8, height=2)
        self.quit_button.place(x = 700, y = 400)

        self.ros_node = ros_node
        self.is_recognizing = False

    def on_button_click(self):
        if self.is_recognizing:
            subprocess.run(['espeak', "멈추겠습니다."])
            self.ros_node.send_message("stop")
            self.button.config(image = self.start_image)
            self.is_recognizing = False
        else:
            self.ros_node.send_message("start")
            self.button.config(image = self.stop_image)
            self.is_recognizing = True

    def run(self):
        self.window.mainloop()

    def quit(self):
        self.ros_node.get_logger().info("Exit")
        self.window.quit()

def ros2_spin(ros_node):
    rclpy.spin(ros_node)

def main():
    rclpy.init()

    # ROS2 노드 생성
    ros_node = ROS2PublisherNode()

    # ROS2 스레드 생성 및 실행
    ros_thread = Thread(target=ros2_spin, args=(ros_node,), daemon=True)
    ros_thread.start()

    # GUI 생성 및 실행
    app = GUIApp(ros_node)
    app.run()
    # root = tk.Tk()
    # root.geometry("800x480+0+0")
    # root.overrideredirect(True)
    # root.configure(background = "white")

    # 프로그램 종료 시 rclpy 종료
    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
