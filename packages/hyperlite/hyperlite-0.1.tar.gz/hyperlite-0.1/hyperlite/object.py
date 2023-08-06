
class Object(object):
    def __init__(self, data: dict, collection):
        self.collection = collection
        for key, value in data.items():
            self.__dict__[key] = value

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__

    def save(self):
        # Logic to save the self.__dict__ to database
        pass
