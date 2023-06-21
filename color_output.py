class ColorOutput:
    def __init__(self):
        self.ANSI_RESET = "\u001B[0m"
        self.ANSI_YELLOW = "\u001B[33m"
        self.ANSI_RED = "\u001B[31m"
        self.ANSI_GREEN = "\u001B[32m"
        self.ANSI_BOLD = "\u001B[1m"

    def get_bold_yellow(self, msg):
        return self.get_bold(self.get_yellow(msg))

    def get_yellow(self, msg):
        return self.get_ansi_formatted(msg, self.ANSI_YELLOW)

    def get_bold(self, msg):
        return self.get_ansi_formatted(msg, self.ANSI_BOLD)

    def print_error(self, msg):
        return f"Error: {self.get_ansi_formatted(msg, self.ANSI_RED)}"

    def print_warning(self, msg):
        return f"Warning: {self.get_ansi_formatted(msg, self.ANSI_YELLOW)}"

    def get_ansi_formatted(self, msg, ansi_style):
        return f"{ansi_style}{msg}{self.ANSI_RESET}"
