from analyzer import Dataset

with open("data/1.txt") as file1:
    year1 = file1.read()
with open("data/2.txt") as file2:
    year2 = file2.read()
with open("data/3.txt") as file3:
    year3 = file3.read()
with open("data/4.txt") as file4:
    year4 = file4.read()
with open("data/all.txt") as file0:
    year_all = file0.read()


def get_dataset(dataset: Dataset) -> str:
    match dataset:
        case 1:
            return year1
        case 2:
            return year2
        case 3:
            return year3
        case 4:
            return year4
        case _:
            return year_all

