import json
import time
import openai
import pandas as pd
from environ import Env
from pathlib import Path

env = Env()
env.read_env()

openai.api_key = env('OPENAI_API_KEY')

data_path = Path(__file__).parent.joinpath('data')
original_dataset_path = data_path.joinpath('hotel-q&a.json')
dataset_path = data_path.joinpath('hotel-q&a-data.jsonl')
train_path = data_path.joinpath('hotel-q&a-train.jsonl')
test_path = data_path.joinpath('hotel-q&a-test.jsonl')

def prepare_data(path: Path, train_path: Path | None = None, test_path: Path | None = None):
    """

    Args:
        path (string): path to data.json {"question": q, "answer": a}
    """
    data = pd.read_json(path)
    print(f"Before cleaning: {len(data)=}")
    
    data = data[data['question'].str.endswith('?')]
    print(f"After cleaning: {len(data)=}")

    # Modify the dataset to look like:
    # {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
    data.columns = ['prompt', 'completion']

    if not (train_path or test_path):
        print(f"Data size: {len(data)=}")
        data.to_json(dataset_path, orient='records', lines=True)
        return 

    # Create a training set by selecting a subset of the data
    train_data = data.sample(frac=0.8, random_state=333)
    print(f"Train data size: {len(train_data)=}")
    train_data.to_json(train_path, orient='records', lines=True)

    # Create a test set using the remaining data
    test_data = data.drop(train_data.index)
    print(f"Test data size: {len(test_data)=}")
    test_data.to_json(test_path, orient='records', lines=True)


def fine_tune():

    fine_tuning_job = openai.FineTune.create(
        api_key=env('OPENAI_API_KEY'),
        model='curie',
        batch_size=3, 
        n_epochs=2,
        # learning_rate=1e-5,
        # max_tokens = 256,
        training_file=openai.File.create(file=open(dataset_path), purpose='fine-tune')['id']
    )
    
    
    job_id = fine_tuning_job["id"]
    print(f"Fine-tuning job created with ID: {job_id}")

    job_id = "ft-9VqGRN3FyA8KDs6yK3vveyhW"

    while True:
        fine_tuning_status = openai.FineTune.retrieve(job_id)
        status = fine_tuning_status["status"]
        print(f"Fine-tuning job status: {status}")

        with open('./status.json', 'r') as f:
            data = json.load(f)
            data.append(json.dumps([fine_tuning_status]))

        with open('./status.json', 'a') as f:
            f.write(json.dumps(data))

        if status in ["completed", "failed", 'succeeded']:
            break

        time.sleep(60)


# prepare_data(original_dataset_path)
fine_tune()





