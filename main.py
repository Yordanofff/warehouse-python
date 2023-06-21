import sys
import re

from color_output import ColorOutput

c = ColorOutput()


def get_string_length_without_ansi(some_text: str):
    return len(re.sub("\u001B\\[[;\\d]*m", "", some_text))


class Warehouse:
    def __init__(self, file_name: str = None):
        self.SEPARATOR = ";"
        self.SEPARATOR_WHEN_PRINTING = " | "
        self.file_name = file_name
        if not file_name:
            file_name = "app_data.csv"
        self.LETTER_SECTION = "ab"
        self.NUM_SECTION = 2
        self.NUM_SHELVES = 3
        self.NUM_NUMBERS = 4
        self.UNIT_OPTIONS = {
            "kg": 100,
            "liter": 100,
            "meter": 10,
            "unit": 1000
        }
        self.USER_QUESTIONS = ["product name", "expiry date", "entry date", "manufacturer", "unit",
                               "available stock", "comment (optional)"]
        self.DESCRIPTION_NO_NAME = ["Expiry date", "Entry date", "Manufacturer", "Unit", "Stock", "Position",
                                    "Available items at shelf", "Comment"]
        self.TEMP_USED_LOCATIONS_NOT_IN_DB = []
        self.ANSWERS = []

        self.SPECIAL_CMDS = ["reset!", "stop!"]

        self.special_options = [f"Use \"{c.get_bold_yellow('reset!')}\" to reset the data input.",
                                f"Use \"{c.get_bold_yellow('stop!')}\" to go back to the menu.",
                                f"Dates need to be formatted as {c.get_bold_yellow('dd.mm.yyyy')} or {c.get_bold_yellow('d.m.yyyy')} and can be separated by {c.get_bold_yellow('.')} or {c.get_bold_yellow('/')}",
                                f"Expiry date can be {c.get_bold_yellow('n/a')}",
                                f"Entry date can be {c.get_bold_yellow('today')}",
                                f"Units can be: {c.get_bold_yellow(', '.join(list(self.UNIT_OPTIONS.keys())))}",
                                f"Forbidden character: {c.get_bold_yellow(self.SEPARATOR)}"
                                ]

    def run_app(self):
        print(c.get_yellow("y"))
        print(c.get_bold_yellow("yb"))
        for i in self.special_options:
            print(i)

    def print_csv_formatted(self, db_list: list):
        pass

    def print_menu_options_in_frame(self, title: str, rows: list, color: str) -> None:
        """
        Adds frame to data, so it looks better. The frame will be as big as the longest row + spaces on both sides + 2
        Every row will start at a fixed position (spaces_on_each_side) - not centered

        :param title: "this is title"
        :param rows: ['test', 'bla', 'some str']
        :param color: c.ANSI_GREEN ("\u001B[32m") or else
        :return:
        =========================
        |     this is title     |
        =========================
        |     test              |
        |     bla               |
        |     some str          |
        =========================
        """

        new_list = rows.copy()
        new_list.append(title)

        longest_word: int = get_string_length_without_ansi(str(max(new_list, key=len)))
        spaces_on_each_side: int = 5

        frame_len = spaces_on_each_side * 2 + longest_word + 2

        print(c.get_ansi_formatted("=" * frame_len, color))
        print(f"{c.get_ansi_formatted(self.SEPARATOR_WHEN_PRINTING.strip(), color)}"
              f"{' ' * spaces_on_each_side}"
              f"{title}"
              f"{' ' * (frame_len - (get_string_length_without_ansi(title) + spaces_on_each_side + 2))}"
              f"{c.get_ansi_formatted(self.SEPARATOR_WHEN_PRINTING.strip(), color)}")
        print(c.get_ansi_formatted("=" * frame_len, color))

        for row in rows:
            print(
                f"{c.get_ansi_formatted(self.SEPARATOR_WHEN_PRINTING.strip(), color)}"
                f"{' ' * spaces_on_each_side}"
                f"{row}"
                f"{' ' * (frame_len - (get_string_length_without_ansi(row) + spaces_on_each_side + 2))}"
                f"{c.get_ansi_formatted(self.SEPARATOR_WHEN_PRINTING.strip(), color)}")
        print(c.get_ansi_formatted("=" * frame_len, color))

    def get_all_valid_user_input(self) -> list:
        title = "Enter the data for the items that you want to add:"
        print()
        self.print_menu_options_in_frame(title, self.special_options, c.ANSI_GREEN)


if __name__ == "__main__":
    wh = Warehouse()
    # wh.run_app()
    wh.get_all_valid_user_input()


