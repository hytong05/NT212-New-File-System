class Metadata:
    def __init__(self):
        self.file_attributes = {}

    def add_file(self, file_name, attributes):
        self.file_attributes[file_name] = attributes

    def get_file_attributes(self, file_name):
        return self.file_attributes.get(file_name, None)

    def list_files(self):
        return list(self.file_attributes.keys())

    def remove_file(self, file_name):
        if file_name in self.file_attributes:
            del self.file_attributes[file_name]