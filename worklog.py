import csv
import datetime
import time
import re
import sys

from tools import (clear_screen)


class Worklog:

    active_log = []
    display_list = []
    time_format = "%d-%m-%Y"
    date_str ="DD-MM-YYYY"

    def __init__(self):
        self.load_log()

# **
# *** Menu methods ***
# **

    def menu(self):
        """
        Main Menu allows user to navigate worklog program
        :return: None
        """
        while True:
            clear_screen()
            print(""" Main Menu
(1) Create a new entry.
(2) Search for an existing entry
(3) Change date format
(exit) type end to program at any time
(menu) to return to this menu
""")
            option = input("please select an option: ")
            self.keywords(option)
            if option == "1" or option == "(1)":
                clear_screen()
                self.new_entry()
            elif option == "2" or option == "(2)":
                clear_screen()
                self.search()
            elif option == "3" or option == "(3)":
                clear_screen()
                self.date_format()
            else:
                clear_screen()
                print("you need to select an option from the main menu list")
                self.menu()

    def date_format(self):
        """
        Menu that allows the format of the date to be changed to either MM-DD-YYYY or DD-MM-YYYY
        :return: None
        """
        clear_screen()

        while True:
            print(""" Time format
(1) DD-MM-YYYY
(2) MM-DD-YYYY
(exit) type end to program
(menu) to return to main menu
""")
            option = input("please select an option: ")
            self.keywords(option)
            if option == "1" or option == "(1)":
                self.time_format = "%d-%m-%Y"
                self.date_str = "DD-MM-YYYY"
                clear_screen()
                break

            elif option == "2" or option == "(2)":
                self.time_format = "%m-%d-%Y"
                self.date_str = "MM-DD-YYYY"
                clear_screen()
                break

            else:
                clear_screen()
                print("you need to select an option from the main menu list")
                self.menu()

    def search(self):
        """
        Menu that displays options for searching the worklog and calls their respective functions
        :return: None
        """
        print(""" Search Menu
(1) Search by date.
(2) Search by task
(3) Search by duration
(4) Search by comment
(exit) type end to program at any time
(menu) to return to main menu
""")
        option = input("please select an option 1, 2 or exit: ")
        self.keywords(option)
        if option == "1" or option == "(1)":
            clear_screen()
            self.search_date()

        elif option == "2" or option == "(2)":
            clear_screen()
            self.search_string('task')
        elif option == "3" or option == "(3)":
            clear_screen()
            self.search_duration()
        elif option == "4" or option == "(4)":
            clear_screen()
            self.search_string('comments')
        else:
            clear_screen()
            "please enter one of the options in brakets"
            self.keywords(option)

    def display(self):
        """
        prints the contents of an individual entry, provides options for the deletion or editing of presented entry
        and allows forward and reverse scrolling through a sorted list of entries (newest first)
        :return: None
        """

        index = 0
        self.display_list = sorted(self.display_list, key=lambda date_key: date_key['date'], reverse=True)

        if len(self.display_list) == 0:  # checks to see if the search list is empty (no matches)
            clear_screen()
            input("Nothing to display press enter to return to main menu: ")
            return None

        while True:
            clear_screen()
            stamp = self.display_list[index]['date']
            entry_date = datetime.datetime.fromtimestamp(stamp)
            entry_date = entry_date.strftime(self.time_format)
            print("""entry {} of {}:
Date: {}
Task: {}
Duration: {} minutes
Comments: {}""".format((index + 1),
                       len(self.display_list),
                       entry_date,
                       self.display_list[index]['task'],
                       self.display_list[index]['duration'],
                       self.display_list[index]['comments']))

            options = input(
                "options:(exit) exit program, (menu) main menu,(E) Edit, (D) Delete, (P) Previous, [Enter] Next: ")
            self.keywords(options)
            if options.lower() == 'd' or options.lower() == 'delete':
                self.active_log.remove(self.display_list[index])
                self.save()
                self.display_list.remove(self.display_list[index])
                if len(self.display_list) == 0:  # checks to see if the search list is empty (no matches)
                    clear_screen()
                    input("Nothing to display press enter to return to main menu: ")
                    return None

            elif options.lower() == 'e' or options.lower() == 'edit':
                self.active_log.remove(self.display_list[index])
                self.save()
                self.edit(self.display_list[index])
                self.display_list = sorted(self.display_list, key=lambda date_key: date_key['date'], reverse=True)

            elif options.lower() == "" or options.lower() == "next":
                if index >= (len(self.display_list) - 1):
                    index = 0
                else:
                    index += 1
            elif options.lower() == 'p' or options.lower() == 'previous':
                if index <= 0:
                    index = len(self.display_list) - 1
                else:
                    index -= 1
            elif options.lower() == 'menu':
                break
            else:
                self.keywords(options)

# **
# *** Entry modification methods
# **

    def new_entry(self):
        """
        creates new entry dict from user input that is added to self.active_log and saved to CSV file
        :return: None
        """

        id_now = datetime.datetime.now().timetuple()
        id_now = time.mktime(id_now)  # generate a unique ID from the time stamp of now


        while True:
            date_text = input(
                "please enter a date for the task {} leave blank for today: ".format(self.date_str))
            self.keywords(date_text)
            if date_text == "":
                date = datetime.date.today().timetuple()
                date = time.mktime(date)
                break
            else:
                try:
                    date_new = datetime.datetime.strptime(date_text, self.time_format)
                except ValueError:
                    print("please follow {} format for date".format(self.date_str))
                else:
                    date = time.mktime(date_new.timetuple())  # convert date into timestamp to allow sorting
                    break

        while True:
            duration = input("please enter the duration of the task in minutes: ")
            self.keywords(duration)

            if duration.isdigit():
                duration = int(duration)
                break
            else:
                print("duration must be a number")

        while True:
            task = input("What task have you been performing? ")
            self.keywords(task)
            if task == "":
                print("task required")
            else:
                break

        comments = ""
        print("please enter a comment leave a blank line to end comment: ")
        while True:

            new_comment = input("")
            self.keywords(new_comment)
            if new_comment == "":
                if comments == "":
                    clear_screen()
                    print("comments required")
                    print("please enter a comment leave a blank line to end comment: ")
                else:
                    break
            else:
                if comments == "":
                    comments = comments + new_comment
                else:
                    comments = comments + '\n' + new_comment

        entry = {"date": date, "duration": duration, "task": task, "comments": comments, "ID": id_now}
        self.active_log.append(entry)
        self.save()
        clear_screen()

        stamp = entry['date']
        entry_date = datetime.datetime.fromtimestamp(stamp)
        entry_date = entry_date.strftime(self.time_format)

        input("""Entry added successfully
Date: {}
Duration: {duration}
Task: {task}
Comments: {comments}

Press enter to continue""".format(entry_date, **entry))
        clear_screen()

    def edit(self, previous_entry):
        """
        allows for the editing of existing entries with user input, updates the active_log and saves changes to CSV.
        :param previous_entry: an existing entry dict
        :return: None
        """
        clear_screen()
        while True:
            date_text = input(
                "please enter a date for the task {} leave blank to keep previous: ".format(self.date_str))

            if self.keywords(date_text, True):
                pass
            elif date_text == "":
                date = previous_entry['date']
                break
            else:
                try:
                    date_new = datetime.datetime.strptime(date_text, self.time_format)
                except ValueError:
                    print("please follow {} format for date".format(self.date_str))
                else:
                    date = time.mktime(date_new.timetuple())  # convert date into timestamp to allow sorting
                    break

        while True:
            duration = input("please enter the duration of the task in minutes leave blank to keep previous: ")

            if self.keywords(duration, True):
                pass
            elif duration == "":
                duration = previous_entry['duration']
                break
            elif duration.isdigit():
                duration = int(duration)
                break
            else:
                print("duration must be a number")

        while True:
            task = input("What task have you been performing? leave blank to keep previous: ")
            if self.keywords(task, True):
                pass
            elif task == "":
                task = previous_entry['task']
                break
            else:
                break

        comments = ""
        print("please enter a comment leave a blank line to end comment: empty comment will keep previous: ")
        while True:
            new_comment = input("")
            self.keywords(new_comment)
            if new_comment == "":
                if comments == "":
                    comments = previous_entry['comments']
                    break
                else:
                    break
            else:
                if comments == "":
                    comments = comments + new_comment
                else:
                    comments = comments + '\n' + new_comment

        entry = {"date": date, "duration": duration, "task": task, "comments": comments, "ID": previous_entry["ID"]}
        self.active_log.append(entry)
        self.display_list.remove(previous_entry)
        self.display_list.append(entry)
        self.save()

        stamp = entry['date']
        entry_date = datetime.datetime.fromtimestamp(stamp)
        entry_date = entry_date.strftime(self.time_format)

        clear_screen()
        input("""Entry added successfully
Date: {}
Duration: {duration}
Task: {task}
Comments: {comments}

Press enter to continue""".format(entry_date, **entry))
        clear_screen()

# **
# *** search methods ***
# **

    def search_string(self, field):
        """
        searches for a string of characters or regex in a specified "field" of all worklog entries (default)
        alternatively searches for an exact match not case sensitive
        :param field: dict key for an entry eg "task"
        :return: None
        """
        self.display_list = []

        search_match = input("do you want to search {} for an exact match Y/[N]: ".format(field))
        if search_match.lower() == 'y':
            match = True
        else:
            match = False

        find = input("enter your search terms: ")

        for entry in self.active_log:
            if match:
                if re.match(find, entry[field], flags=re.IGNORECASE):
                    self.display_list.append(entry)
            else:
                if re.search(find, entry[field], flags=re.IGNORECASE):
                    self.display_list.append(entry)

        self.display()

    def search_duration(self):
        """
        searches the duration field of all worklog entries to see if they are within a range
        or match a specific duration. Determined by if one or two durations are given (min and max)
        :return: None
        """

        clear_screen()
        is_range = True
        self.display_list = []

        while True:
            min_time = input("please enter a minimum time for the task: ")
            if min_time.isdigit():
                min_time = int(min_time)
                break
            else:
                clear_screen()
                print("time must be numbers only:")

        clear_screen()
        while True:
            max_time = input("please enter a maximum time for the task " +
                             "or leave blank to search for a specific time: ")

            if max_time == "":
                is_range = False
                break
            elif max_time.isdigit():
                max_time = int(max_time)
                break
            else:
                clear_screen()
                print("time must be numbers only:")

        for entry in self.active_log:

            if is_range:
                if min_time <= entry['duration'] <= max_time:
                    self.display_list.append(entry)
            else:
                if min_time == entry['duration']:
                    self.display_list.append(entry)

        self.display()

    def search_date(self):
        """
        Search all worklog entries by date. date is requested from the user with a given format.
        a single entry will look for a specific date two dates will look for a range of dates including given dates
        :return:
        """
        date_range = input("enter two dates a range of dates {} {} or a single date:".format(self.date_str,
                                                                                             self.date_str))
        self.keywords(date_range)
        dates = re.findall(r'\d{2}-\d{2}-\d{4}', date_range)

        if len(dates) < 1:
            clear_screen()
            print("no date entered or incorrect format")
            self.search_date()
        elif len(dates) == 1:

            datetime_new = datetime.datetime.strptime(dates[0], self.time_format)
            date = time.mktime(datetime_new.timetuple())  # convert to time stamp

            self.active_log = sorted(self.active_log,
                                     key=lambda date_key: date_key['date'],
                                     reverse=True)
            self.display_list = []

            for entry in self.active_log:
                if entry['date'] == date:
                    self.display_list.append(entry)

            self.display()

        elif len(dates) == 2:

            datetime1 = datetime.datetime.strptime(dates[0], self.time_format)
            datetime2 = datetime.datetime.strptime(dates[1], self.time_format)
            date1 = time.mktime(datetime1.timetuple())  # convert to time stamp
            date2 = time.mktime(datetime2.timetuple())  # convert to time stamp

            self.active_log = sorted(self.active_log,
                                     key=lambda date_key: date_key['date'],
                                     reverse=False)
            self.display_list = []

            for entry in self.active_log:
                if date1 <= entry['date'] <= date2:
                    self.display_list.append(entry)

            self.display()
        else:
            clear_screen()
            print("too many dates given two dates are required for a range, one date for individual dates.")
            self.search_date()

# **
# *** Tools ***
# **

    def keywords(self, string, cannot=False):
        """checks if a string contains keyword to exit the program or return to main menu"""
        if cannot and (string == 'menu' or string == 'exit'):
            print("you cannot exit mid edit")
            return True

        if string.lower() == "exit" or string.lower() == "(exit)":
            sys.exit()
        elif string.lower() == "menu" or string.lower() == "(menu)":
            self.menu()

    def load_log(self):
        """ Reads a csv file and writes its entire contents to self.active_log (a list of dictionaries) """
        with open('log.csv', newline='') as csvfile:
            csv_log = csv.DictReader(csvfile)
            self.active_log = list(csv_log)

        for entry in self.active_log:
            entry['date'] = float(entry['date'])
            entry['ID'] = float(entry['ID'])
            entry['duration'] = int(entry['duration'])

    def save(self):
        """saves self.active_log information to a csv file"""

        with open('log.csv', 'w', newline="\n") as csvfile:
            fieldnames = ["date", "duration", "task", "comments", "ID"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            self.active_log = sorted(self.active_log, key=lambda date_key: date_key['date'], reverse=True)

            for entry in self.active_log:
                writer.writerow(entry)
