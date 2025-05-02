class Memories:
    def __init__(self, stamp_id, stamp_title, date, notes, image_path=""):
        self.stamp_id = stamp_id
        self.stamp_title = stamp_title
        self.date = date
        self.notes = notes
        self.image_path = image_path

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Memories(
            stamp_id=data["stamp_id"],
            stamp_title=data["stamp_title"],
            date=data["date"],
            notes=data["notes"],
            image_path=data.get("image_path", "")
        )