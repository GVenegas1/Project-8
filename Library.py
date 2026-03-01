
#Author:Gabriel Venegas
#Github:GVenegas1
#Date:  Feb 27, 2026
#Description: A system that tracks library items like books and movies,
# track patrons, and handle checkouts, returns, and late fines.

class LibraryItem:
    def __init__ (self, item_id, title):
        """Sets up the basic info for library"""
        self._library_item_id =  item_id
        self._title = title
        self._location ="ON_SHELF"
        self._checked_out_by = None
        self._requested_by  = None
        self._date_checked_out = 0

    def get_library_item_id (self):
        """returns a unique id of the item"""
        return self._library_item_id

    def  get_title(self):
        """returns the title of the item"""
        return self._title

    def get_location (self):
        """returns where the item is located"""
        return self._location

    def set_location (self,  new_location):
        """updates the location of the item"""
        self._location = new_location

    def get_checked_out_by(self):
        """returns the patron who has the item"""
        return self._checked_out_by

    def set_checked_out_by(self, patron):
        """sets which patron has checked out the item"""
        self._checked_out_by = patron

    def get_requested_by(self):
        """Returns the patron who put a hold on the item"""
        return self._requested_by

    def set_requested_by(self, patron):
        """sets which patron is requesting the item"""
        self._requested_by = patron

    def get_date_checked_out(self):
        """returns the day the item was taken out"""
        return self._date_checked_out

    def set_date_checked_out(self, day):
        """Sets the day the item was taken out"""
        self._date_checked_out = day


class Book(LibraryItem):
    """specific type of library item for books"""

    def __init__(self, item_id, title, author):
        """looks for a book with an author and checks in LibraryItem"""
        super().__init__(item_id, title)
        self._author = author

    def get_author (self):
        """returns the author of the book"""
        return self._author

    def get_check_out_length (self):
        """books are checked out for 21 days"""
        return 21


class Album(LibraryItem):
    """A specific type of library item for music albums"""

    def __init__(self, item_id, title, artist):
        """looks for a album with an artist and checks in LibraryItem"""

        super().__init__(item_id, title)
        self._artist = artist

    def get_artist (self):
        """returns the artist of the album"""
        return self._artist

    def get_check_out_length (self):
        """albums can be checked out for 14 days"""
        return 14


class Movie(LibraryItem):
    """specific type of library item for movies"""

    def __init__ (self, item_id, title, director):
        """shows a movie with a director and inherits from LibraryItem"""
        super().__init__(item_id, title)
        self._director = director

    def get_director (self):
        """returns the director of the movie"""
        return self._director

    def get_check_out_length(self):
        """movies can be checked out for 7 days"""
        return 7


class Patron:
    """representing a person who is a member of the library"""

    def __init__(self, patron_id, name):
        """sets up the patron with an id and name"""
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = []
        self._fine_amount = 0.0

    def get_patron_id(self):
        """returns the patrons id"""
        return self._patron_id

    def get_name(self):
        """returns the patrons name"""
        return self._name

    def get_fine_amount(self):
        """returns how much the patron owes in fines"""
        return self._fine_amount

    def get_checked_out_items(self):
        """returns the list of items the patron has"""
        return self._checked_out_items

    def add_library_item(self, library_item):
        """Adds an item to the patrons checkout list"""
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        """removes an item from the patrons checkout list"""
        if library_item in self._checked_out_items:
            self._checked_out_items.remove(library_item)

    def amend_fine (self, amount):
        """changes the fee amount"""
        self._fine_amount = self._fine_amount + amount


class Library:
    """main class that runs the library"""

    def __init__ (self):
        """starts the library with empty lists and starts at 0"""
        self._holdings = []
        self._members = []
        self._current_date = 0

    def add_library_item(self, library_item):
        """adds a new item to the library collection"""
        self._holdings.append(library_item)

    def add_patron(self, patron):
        """Adds a new item to the library"""
        self._members.append(patron)

    def lookup_library_item_from_id(self, item_id):
        """finds an item in the holdings using its ids"""
        for current_item in self._holdings:
            if current_item.get_library_item_id() == item_id:
                return current_item
        return None

    def lookup_patron_from_id(self, patron_id):
        """Finds a member in the library using their id"""
        for current_patron in self._members:
            if current_patron.get_patron_id() == patron_id:
                return current_patron
        return None

    def check_out_library_item (self, patron_id, item_id):
        """handles the logic for a patron checking out an item"""
        found_patron = self.lookup_patron_from_id(patron_id)
        if found_patron == None:
            return "patron not found"

        found_item = self.lookup_library_item_from_id(item_id)
        if found_item == None:
            return "item not found"

        if found_item.get_location() == "CHECKED_OUT":
            return "item already checked out"

        if found_item.get_location() == "ON_HOLD_SHELF":
            if found_item.get_requested_by() != found_patron:
                return "item on hold by other patron"

        #Success:update everything
        found_item.set_checked_out_by(found_patron)
        found_item.set_date_checked_out(self._current_date)
        found_item.set_location("CHECKED_OUT")

        if found_item.get_requested_by() == found_patron:
            found_item.set_requested_by (None)

        found_patron.add_library_item (found_item)
        return "check out successful"

    def return_library_item(self, item_id):
        """returning an item to the library"""
        found_item = self.lookup_library_item_from_id(item_id)
        if found_item == None:
            return "item not found"

        if found_item.get_location() != "CHECKED_OUT":
            return "item already in library"

        patron_who_had_it = found_item.get_checked_out_by()
        patron_who_had_it.remove_library_item(found_item)

        if found_item.get_requested_by() != None:
            found_item.set_location("ON_HOLD_SHELF")
        else:
            found_item.set_location("ON_SHELF")

        found_item.set_checked_out_by(None)
        return "return successful"

    def request_library_item(self, patron_id, item_id):
        """Allows a patron to put a hold on a specific item"""
        found_patron = self.lookup_patron_from_id(patron_id)
        if found_patron == None:
            return "patron not found"

        found_item = self.lookup_library_item_from_id(item_id)
        if found_item == None:
            return "item not found"

        if found_item.get_requested_by() != None:
            return "item already on hold"

        found_item.set_requested_by(found_patron)

        if found_item.get_location() == "ON_SHELF":
            found_item.set_location ("ON_HOLD_SHELF")

        return "request successful"

    def pay_fine (self, patron_id, amount):
        """allows a patron to pay off their fines"""
        found_patron = self.lookup_patron_from_id(patron_id)
        if found_patron == None:
            return "patron not found"

        found_patron.amend_fine(-amount)
        return "payment successful"

    def increment_current_date(self):
        """advances the date and adds fines for overdue items"""
        self._current_date = self._current_date + 1

        for current_patron in self._members:
            for current_item in current_patron.get_checked_out_items():
                days_out = self._current_date - current_item.get_date_checked_out()

                if days_out > current_item.get_check_out_length():
                    current_patron.amend_fine(0.10)