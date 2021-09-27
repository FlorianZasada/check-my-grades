from win10toast import ToastNotifier

class notifier():
    def __init__(self, title, body, time):
        self.title = title
        self.body = body
        self.time = time

        self.notify()
    
    def notify(self):
        toaster = ToastNotifier(self.title, self.body, self.time)
        toaster.show_toast()


if __name__ == "__main__":
    notifier()