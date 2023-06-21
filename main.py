import os
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
            self.file_name = "app_data.csv"
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
        self.create_db_file_if_missing()

        # for i in self.special_options:
        #     print(i)

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

    def create_db_file_if_missing(self) -> None:
        if not os.path.exists(self.file_name):
            open(self.file_name, 'w').close()

    def get_db_to_list(self) -> list[list[str]]:
        """
        Reads the DB and adds every element in a row to list.

        :return:
        [['Coca Cola', '02.03.2020', '03.04.2022', 'The Coca-Cola Company', 'unit', '200',
        'b1 / 1 / 3', '1000', 'original taste'], [..], [..]]
        """
        db_file = []
        with open(self.file_name, 'r') as db:
            rows = db.readlines()
            for row in rows:
                inner_list = [el.rstrip() for el in row.split(self.SEPARATOR)[:-1]]
                db_file.append(inner_list)

        return db_file

    def get_db_to_list_with_description(self) -> list[list[str]]:
        """
        Read the DB and adds description to each field

        :return:
        [['Name: Coca Cola', 'Expiry date: 02.03.2020', 'Entry date: 03.04.2022',
        'Manufacturer: The Coca-Cola Company', 'Unit: unit', 'Stock: 200', 'Position: b1 / 1 / 3',
        'Available items at shelf: 1000', 'Comment: original taste'], [..], [..]]
        """
        db_file = self.get_db_to_list()
        db_with_desc = []
        for inner_list in db_file:
            inner_with_desc = []
            for i, item in enumerate(inner_list):
                if i == 0:
                    description = "Name"
                else:
                    description = self.DESCRIPTION_NO_NAME[i - 1]
                inner_with_desc.append(f"{description}: {item}")
            db_with_desc.append(inner_with_desc)

        return db_with_desc

    def write_list_to_db(self, list_to_write: list) -> bool:
        string_build = self.SEPARATOR.join(list_to_write)
        try:
            with open(self.file_name, 'a') as db:
                db.write(string_build)
            return True
        except Exception as e:
            c.print_error(f"There was a problem writing \"{list_to_write}\" to the file: {e}")
            return False

    # todo
    def write_all_data_to_db(self):
        print("Product was added successfully!")

    def is_at_least_one_item_in_location(self, location: str) -> bool:
        db = self.get_db_to_list()
        for row in db:
            if row[6] == location:
                return True
        return False

    def get_all_unique_locations_for_item(self, item_name: str, expiry_date: str):
        db = self.get_db_to_list()
        set_of_positions = {, }
        for row in db:
            if item_name == row[0] and expiry_date == row[1]:
                set_of_positions.add(row[6])



if __name__ == "__main__":
    wh = Warehouse()
    # wh = Warehouse('t.csv')
    # wh.run_app()
    # result = wh.get_db_to_list()
    # print(result)
    print(wh.is_at_least_one_item_in_location('b3 / 1 / 3'))
    print(wh.is_at_least_one_item_in_location('g3 / 1 / 3'))
