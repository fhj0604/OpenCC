# script for translating simplified Chinese to traditional Chinese
import argparse
import os
import json
from tqdm import tqdm
import opencc



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_dir", type=str, default="natural-instructions-2.8")
    args = parser.parse_args()
    return args

def load_data(args):
    print("Load data...")
    tasks_dir = os.path.join(args.src_dir, "tasks")
    task_files = os.listdir(tasks_dir)
    all_data = []
    for i, task in enumerate(tqdm(task_files)):
        if not task.endswith('json'):
            continue
        with open(os.path.join(tasks_dir, task), "r") as f:
            data = json.load(f)
        '''
        dict_keys(['Contributors', 'Source', 'URL', 'Categories', 'Reasoning', 'Definition', 'Input_language', 'Output_language', 'Instruction_language', 'Domains', 'Positive Examples', 'Negative Examples', 'Instances', 'Instance License'])
        '''
        all_data.append({
            "file": task,
            "data": data
        })
    return all_data
    

def translate(all_data, cvtr):
    print("Start translation...")
    for i, data in enumerate(tqdm(all_data)):
        if "Chinese" in data['data']['Input_language'] or "Chinese" in data['data']['Output_language'] or "Chinese" in data['data']['Instruction_language']:
            for key in ['Positive Examples', 'Negative Examples', 'Instances']:
                for j, example in enumerate(data['data'][key]):
                    for _key in ['input', 'output']:
                        if isinstance(example[_key], str):
                            all_data[i]['data'][key][j][_key] = cvtr.convert(example[_key])
                        else:
                            for k, ex in enumerate(example[_key]):
                                all_data[i]['data'][key][j][_key][k] = cvtr.convert(ex)
    return all_data

def write_result(args, translated_data):
    print("Write to file...")
    s2t_task_dir = os.path.join(args.src_dir, "s2t_tasks")

    if not os.path.exists(s2t_task_dir):
        os.makedirs(s2t_task_dir)
    
    for d in tqdm(translated_data):
        with open(os.path.join(s2t_task_dir, d['file']), "w") as f:
            json.dump(d['data'], f, indent=4, ensure_ascii=False)
        
    print(f"All file are saved under {s2t_task_dir}")

def main():
    args = parse_args()
    
    all_data = load_data(args)

    print(f"Total files: {len(all_data)}")

    cvtr = opencc.OpenCC('s2twp.json')


    translated_data = translate(all_data, cvtr)
                    
    write_result(args, translated_data)
    



if __name__ == "__main__":
    main()




