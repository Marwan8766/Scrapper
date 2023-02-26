class Place:
    def __init__(self):
        self.name = ""
        self.link = ""
        self.rating = ""
        self.type = ""
        self.description = ""
        self.image = ""
        self.open_close_times = {}

    def to_dict(self):
        return {
            'name': self.name,
            'link': self.link,
            'rating': self.rating,
            'type': self.type,
            'description': self.description,
            'image': self.image,
            'open_close_times': self.open_close_times
        }    