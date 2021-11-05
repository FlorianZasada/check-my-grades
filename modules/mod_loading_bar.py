import sys
import time

class loading_bar():
    def __init__(self, width, steps):
        self.width = width
        self.steps = steps

        sys.stdout.write("[%s]" % ("." * self.width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.width+1)) # return to start of line, after '['

        for i in range(self.width):
            time.sleep(self.steps)
            # update the bar
            sys.stdout.write("#")
            sys.stdout.flush()

        sys.stdout.write("]\n") # this ends the progress bar

if __name__ == "__main__":
    loading_bar(1, 1)