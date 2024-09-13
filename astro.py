from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5 import  uic,QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import sys
import datetime
import threading
import time
import pyautogui
import keyboard
import random
from PyQt5.QtCore import Qt,QTimer, QTime

stylesheet_1 = """
        QPushButton {
            border-radius: 1px;
            background-color: darkred;
            color: white;
            border: 2px solid white;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: maroon;
        }
        """

stylesheet_2= """
        QPushButton {
            border-radius: 1px;
            background-color: green;
            color: white;
            border: 2px solid white;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: green;
        }
        """


class FrmAstro(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Load the user interface from the ui file
        uic.loadUi('astro.ui', self)
        self.AstroActivate_Flag = False
         # Set window flags to show only the close button
        self.setWindowFlags(Qt.Window  | Qt.WindowTitleHint)
        # Set the title of the window
        self.setWindowTitle("ASTRO")
        self.setWindowIcon(QtGui.QIcon('startup.png'))
        # Set the size of the window
        self.setFixedSize(210, 150)
        
        # Set Command Activate Astro
        self.cmdActivate.clicked.connect(self.Activate_astro)

         # Set Command Terminate program
        self.cmdClose.clicked.connect(self.terminate_application)

        self.start_jiggle_mouse()

    def Activate_astro(self):
        if self.AstroActivate_Flag == False:
            self.AstroActivate_Flag = True
            self.cmdActivate.setText("ON")
            # Apply the stylesheet to the button
            self.cmdActivate.setStyleSheet(stylesheet_2)

        else:
            self.AstroActivate_Flag = False
            self.cmdActivate.setText("OFF")
            # Apply the stylesheet to the button
            self.cmdActivate.setStyleSheet(stylesheet_1)

    def terminate_application(self):
        # Terminate the application
        QApplication.quit()

    # Mouse Jakkler
    def jiggle_mouse(self):
        screen_width, screen_height = pyautogui.size()  # Get screen 
        pyautogui.FAILSAFE = False
        while True:
            if self.AstroActivate_Flag:
                # Get the current mouse position
                x, y = pyautogui.position()
                
                # Randomly move the mouse a little bit
                new_x = x + random.randint(-10, 10)
                new_y = y + random.randint(-10, 10)
                
                # Check if new position is within screen bounds
                if new_x < 100 or new_x >= screen_width-100:
                    new_x = random.randint(100, screen_width - 100)  # Reset to a random valid position
                if new_y < 100 or new_y >= screen_height-100:
                    new_y = random.randint(100, screen_height - 100)  # Reset to a random valid position
                # Move the mouse to the new position
                pyautogui.moveTo(new_x, new_y, duration=0.1)
                
                # Wait for a short period before the next jiggle
                time.sleep(1)
            else:
                time.sleep(0.1)  # Sleep briefly if jiggler is inactive
    
    def start_jiggle_mouse(self):
        # Create a new thread for the jiggle_mouse method
        thread = threading.Thread(target=self.jiggle_mouse)
        thread.daemon = True
        thread.start()

    # Start the mouse jiggler in a separate thread
    # jiggler_thread = threading.Thread(target=jiggle_mouse)
    # jiggler_thread.daemon = True
    # jiggler_thread.start()

if __name__ == '__main__':
    app = QApplication([])
    
    window = FrmAstro()
    window.show()
    
    app.exec_()
