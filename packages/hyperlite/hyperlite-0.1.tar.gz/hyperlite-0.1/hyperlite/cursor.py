class Cursor(object):
    def __init__(self, total_page, data):
        self.total_page = total_page
        self.curr_page = 0
        self.data = data

    def has_next(self):
        return self.total_page != self.curr_page

    def move_next(self):
        self.curr_page += 1
        # Login to fetching data from server and assign to self.data

    def get(self):
        return self.data

    def __str__(self):
        return str(self.data)
