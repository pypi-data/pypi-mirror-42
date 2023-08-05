#!/usr/local/bin/python3.7
import curses
from rover_position_rjg.clients.monitor.app import App
from rover_position_rjg.clients.monitor.messenger import Messenger
from rover_position_rjg.clients.monitor.presenter import Presenter
from rover_position_rjg.clients.monitor.view import View


class Shell:
    def __init__(self, stdscr: any):
        stdscr.timeout(6)
        self.view = View(stdscr)
        self.view.display_template()
        self.messenger = Messenger()
        self.presenter = Presenter(self.view)
        self.app = App(self.presenter, self.messenger)
        self.running = True

    def run(self, stdscr: any):
        self.hide_cursor()
        curses.cbreak()
        while self.running:
            try:
                self.messenger.check_messages()
                char = stdscr.getch(0, 0)
                self.handle_character(char)
            except (KeyboardInterrupt, SystemExit):
                self.quit()

    def hide_cursor(self):
        try:
            curses.curs_set(0)
        except:
            # Terminal doesn't support invisible cursor
            pass

    def handle_character(self, char: int):
        if char == -1:
            return
        if char == ord('0'):
            self.messenger.toggle_record_all()
        if char == ord('1'):
            self.messenger.toggle_record_imu_data()
        if char == ord('2'):
            self.messenger.toggle_record_attitude_data()
        if char == ord('3'):
            self.messenger.toggle_record_beacon_data()
        if char == ord('4'):
            self.messenger.toggle_record_position_switch()
        if char == ord('a'):
            self.messenger.toggle_position_publish_attitude_data()
        if char == ord('b'):
            self.messenger.toggle_position_publish_beacon_data()
        if char == ord('c'):
            self.messenger.position_calibrate()
        if char == ord('i'):
            self.messenger.toggle_position_publish_imu_data()
        if char == ord('o'):
            self.messenger.toggle_position_publish_position_data()
        if char == ord('p'):
            self.messenger.toggle_position_pause_imu()
        if char == ord('q'):
            self.quit()
        if char == ord('t'):
            self.messenger.toggle_position_track_position()
        if char == ord('x'):
            self.messenger.position_exit()

    def quit(self):
        self.running = False
        self.app.quit()

