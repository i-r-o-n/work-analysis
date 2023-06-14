from utils.text_analyzer import Dataset


dataset_options = [
    "all years",
    "freshman",
    "sophomore",
    "junior",
    "senior"
]

def parse_dataset(dataset_selection: str) -> Dataset:
    # [!] dataset_options order must match enum order for this to work
    return Dataset(dataset_options.index(dataset_selection))