import opencc
from datasets import load_dataset
from tqdm.contrib import tzip
import time
import random
import difflib

analyze_type = 'time' # time, gen_diff_samples
train_ds = load_dataset('bigscience/xP3mt', 'zh', split='train')

inputs = train_ds['inputs']
targets = train_ds['targets']

if analyze_type == 'time':    

    def time_analyzer(cvtr=None):
        
        total_len = len(inputs)
        estimated_len = 10000

        time0 = time.time()
        for inp, tgt in tzip(inputs[:estimated_len], targets[:estimated_len]):
            if cvtr != None:
                translated_inp = cvtr.convert(inp)
                translated_tgt = cvtr.convert(tgt)

        elapsed_time = time.time() - time0

        return elapsed_time * (total_len / estimated_len)

    
    print("Time to iterate all samples: ", time_analyzer())

    one2one_cvtr = opencc.OpenCC('s2t.json')
    
    print("Time to translate using one-to-one mapping", time_analyzer(one2one_cvtr))

    idiom_cvtr = opencc.OpenCC('s2twp.json')

    print("Time to tranlate with Taiwanese idiom", time_analyzer(idiom_cvtr))



else:
    one2one_cvtr = opencc.OpenCC('s2t.json')
    idiom_cvtr = opencc.OpenCC('s2twp.json')

    random.seed(10)
    random.shuffle(inputs)

    sample_size = 10
    counter = 0

    for inp in inputs:
        one2one_inp = one2one_cvtr.convert(inp)
        idiom_inp = idiom_cvtr.convert(inp)

        if one2one_inp != idiom_inp:
            # print("==== original text ====")
            # print(inp)

            # print("==== one-to-one translation ====")
            # print(one2one_inp)

            # print("==== idiom translation ====")
            # print(idiom_inp)

            print("==== differences ====")
            differences = difflib.ndiff(one2one_inp, idiom_inp)
            for diff in differences:
                if diff[0] != ' ':
                    print(diff)

            counter += 1

            if counter == sample_size:
                exit(0)






    

