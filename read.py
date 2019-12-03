import csv

class Read:

    def __init__(self,file):

        self.file = file
        self.list = []

    def read_csv(self):

        with open(self.file) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                self.list.append(row[0])
            return self.list
