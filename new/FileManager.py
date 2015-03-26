import os

try:
    import cPickle as pickle
except ImportError:
    print "cPickle is not available, using standard pickle module."
    import pickle


def pickle_dump(data, filename):  # saves data into filename
    with open(filename, "w") as out_file:
        pickle.dump(data, out_file)


def pickle_load(filename):        # reads data out of filename
    with open(filename) as in_file:
        return pickle.load(in_file)

# File Data format
# {'folder_name': [{'file_name':'data'}, {'folder_name':'contents'}]}


class FileManagerException(Exception):
    pass


class Manager(object):
    file_data = {"/": [{}, {}]}

    def __init__(self, pickled_fs="HTMLEditor.pick"):
        self.pickled_fs_name = pickled_fs
        if os.path.exists(pickled_fs):
            self.load_data()
        else:
            self.save_data()

    def load_data(self):
        self.file_data = pickle_load(self.pickled_fs_name)

    def save_data(self):
        pickle_dump(self.file_data, self.pickled_fs_name)

    def add_file(self, name, contents):
        self._add_file(name, contents, self.file_data["/"])
        self.save_data()

    def get_file(self, name):
        return self._get_file(name, self.file_data["/"])

    def new_folder(self, path):
        self._new_folder(path, self.file_data["/"])
        self.save_data()

    def get_folder(self, path):
        return self._get_folder(path, self.file_data["/"])

    def _add_file(self, name, contents, last):
        name = name.split("/")
        head = name[0]
        name.remove(head)
        tail = name
        if not tail:
            last[0][head] = contents
        else:
            if head not in last[1]:
                last[1][head] = [{}, {}]
            self._add_file("/".join(tail), contents, last[1][head])

    def _get_file(self, name, last):
        name = name.split("/")
        head = name[0]
        name.remove(head)
        tail = name
        if not tail:
            return head, last[0][head]
        else:
            if head not in last[1]:
                raise FileManagerException("File/Folder does not exist")
            return self._get_file("/".join(tail), last[1][head])

    def _new_folder(self, path, last):
        path = path.split("/")
        head = path[0]
        path.remove(head)
        tail = path
        if not tail:
            last[1][head] = [{}, {}]
        else:
            if head not in last[1]:
                last[1][head] = [{}, {}]
            self._new_folder("/".join(tail), last[1][head])

    def _get_folder(self, path, last):
        path = path.split("/")
        head = path[0]
        path.remove(head)
        tail = path
        if not tail:
            return head, last[1][head]
        else:
            if head not in last[1]:
                raise FileManagerException("File/Folder does not exist")
            return self._get_folder("/".join(tail), last[1][head])


# Simple testing
if __name__ == "__main__":
    m = Manager()
    m.add_file("dir1/dir1/test.txt", "Bassus victrix saepe imperiums galatae est.")
    print m.get_file("dir1/dir1/test.txt")
    m.new_folder("dir/folder/path")
    print m.get_folder("dir/folder/path")
    print m.get_folder("dir1/dir1")
    print m.file_data