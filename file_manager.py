from typing import NewType, Self

from analyzer import Datasets, ModelTypes, Dataset, Model


# file imports
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

class Entry:
    def __new__(cls, *args, **kwargs) -> Self:
        return super().__new__(cls)
    
    def __init__(
            self, 
            dataset: Dataset,
            temperature: float,
            model: Model,
            query: str,
            response: str) -> None:
        self.dataset = dataset
        self.temperature = temperature
        self.model = model
        self.query = query
        self.response = response


    def parse_to_csv(self) -> str:
        return ','.join(map(str, [
            self.dataset.value,
            self.temperature,
            self.model.value,
            '"' + self.query + '"',
            '"' + self.response + '"']))

print(Entry(Datasets.ALL, 1.0, ModelTypes.MAP_REDUCE, "test query?", "test response.").parse_to_csv())


def write_output(content: str) -> str:
    output_file = open("test.txt",'a')
    output_file.write(content + "\n")
    output_file.close()
    return content


def get_dataset_text(dataset: Dataset) -> str:
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

