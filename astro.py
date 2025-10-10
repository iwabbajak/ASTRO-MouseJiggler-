# ADD SYSTEM TRAY HIDE AND SHOW

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QSystemTrayIcon,
    QMenu, QAction, QWidget, QMessageBox
)
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
import sys
import threading
import time
import pyautogui
import keyboard
import random


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

stylesheet_2 = """
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
        uic.loadUi('astro.ui', self)
        self.AstroActivate_Flag = False

        # Window setup
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint)
        self.setWindowTitle("ASTRO")
        self.setWindowIcon(QtGui.QIcon('startup.png'))
        self.setFixedSize(220, 160)

        # Button connections
        self.cmdActivate.clicked.connect(self.Activate_astro)
        self.cmdClose.clicked.connect(self.terminate_application)

        # Start background mouse jiggle
        self.start_jiggle_mouse()

        # Setup system tray
        self.create_tray_icon()

        # Setup keyboard shortcut (Ctrl+Shift+A)
        keyboard.add_hotkey('ctrl+shift+a', self.toggle_window_visibility)

    # ---- Activation toggle ----
    def Activate_astro(self):
        if not self.AstroActivate_Flag:
            self.AstroActivate_Flag = True
            self.cmdActivate.setText("ON")
            self.cmdActivate.setStyleSheet(stylesheet_2)
        else:
            self.AstroActivate_Flag = False
            self.cmdActivate.setText("OFF")
            self.cmdActivate.setStyleSheet(stylesheet_1)

    # ---- Terminate program ----
    def terminate_application(self):
        self.tray_icon.hide()
        QApplication.quit()

    # ---- Perform Alt+Tab program ----
    def perform_alt_tab(self):
        try:
            tab_count = random.randint(3, 11)  # Random number of Alt+Tab presses
            pyautogui.keyDown('alt')
            for _ in range(tab_count):
                pyautogui.press('tab')
                time.sleep(0.3)  # small delay between each tab switch
            pyautogui.keyUp('alt')
            print(f"Performed Alt+Tab {tab_count} time(s).")
        except Exception as e:
            print(f"Error performing Alt+Tab: {e}")


    # ---- Mouse Jiggler ----
    def jiggle_mouse(self):
        screen_width, screen_height = pyautogui.size()
        pyautogui.FAILSAFE = False

        last_alt_tab_time = time.time()  # Track when Alt+Tab last happened

        while True:
            if self.AstroActivate_Flag:
                x, y = pyautogui.position()
                new_x = x + random.randint(-100, 100)
                new_y = y + random.randint(-100, 100)
                new_x = max(100, min(screen_width - 100, new_x))
                new_y = max(100, min(screen_height - 100, new_y))
                
                # Move and click
                pyautogui.moveTo(new_x, new_y, duration=0.5)
                # pyautogui.press('left')
                
                # Check if 8 minutes (480s) have passed for Alt+Tab
                if time.time() - last_alt_tab_time >= 20:
                    self.perform_alt_tab()
                    last_alt_tab_time = time.time()
                
                time.sleep(5)
            else:
                time.sleep(0.1)


    def start_jiggle_mouse(self):
        thread = threading.Thread(target=self.jiggle_mouse)
        thread.daemon = True
        thread.start()

    # ---- System Tray setup ----
    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(QtGui.QIcon('startup.png'), self)
        self.tray_icon.setToolTip("ASTRO - Mouse Jiggler")

        # Tray menu
        tray_menu = QMenu()
        show_action = QAction("Show / Hide Window", self)
        quit_action = QAction("Exit", self)

        show_action.triggered.connect(self.toggle_window_visibility)
        quit_action.triggered.connect(self.terminate_application)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Double-click on tray icon toggles window visibility
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_window_visibility()

    # ---- Show / Hide logic ----
    def toggle_window_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FrmAstro()
    window.show()
    sys.exit(app.exec_())
