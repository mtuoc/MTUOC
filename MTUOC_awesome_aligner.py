#    MTUOC_awesome_aligner
#    Copyright (C) 2022  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os


def align_awesome_aligner(FILE1, FILE2, OUTPUT_FILE, model="bert-base-multilingual-cased", device="cpu", cuda_visible_devices="0"):
    command="paste "+FILE1+" "+FILE2+" | sed 's/\t/ ||| /g' > corpus.tmp"
    os.system(command)
    if device=="cpu":
        command="awesome-align --output_file="+OUTPUT_FILE+" --model_name_or_path "+model+" --data_file=corpus.tmp --extraction 'softmax' --batch_size 32"
        os.system(command)
        
        
        
    elif device=="cuda":
        command="CUDA_VISIBLE_DEVICES="+cuda_visible_devices+" awesome-align --output_file="+OUTPUT_FILE+" --model_name_or_path "+model+" --data_file=corpus.tmp --extraction 'softmax' --batch_size 32"
        os.system(command)
    
    command="rm corpus.tmp"
    os.system(command)

def finetune_awesome(FILET1, FILET2, FILEV1, FILEV2, initial_model="bert-base-multilingual-cased", output_dir="finetuned_model",device="cpu", cuda_visible_devices="0"):
    command="paste "+FILET1+" "+FILET2+" | sed 's/\t/ ||| /g' > traincorpus.tmp"
    os.system(command)
    command="paste "+FILEV1+" "+FILEV2+" | sed 's/\t/ ||| /g' > evalcorpus.tmp"
    os.system(command)
    if device=="cpu":
        command="awesome-train --output_dir="+output_dir+" --model_name_or_path="+initial_model+" --extraction 'softmax' --do_train --train_tlm --train_so --train_data_file=traincorpus.tmp --per_gpu_train_batch_size 2 --gradient_accumulation_steps 4 --num_train_epochs 1 --learning_rate 2e-5 --save_steps 4000 --max_steps 20000 --do_eval --eval_data_file=evalcorpus.tmp"
        os.system(command)
    
    elif device=="cuda":
        command="CUDA_VISIBLE_DEVICES="+cuda_visible_devices+" awesome-train --output_dir="+output_dir+" --model_name_or_path="+initial_model+" --extraction 'softmax' --do_train --train_tlm --train_so --train_data_file=traincorpus.tmp --per_gpu_train_batch_size 2 --gradient_accumulation_steps 4 --num_train_epochs 1 --learning_rate 2e-5 --save_steps 4000 --max_steps 20000 --do_eval --eval_data_file=evalcorpus.tmp"
        os.system(command)
    command="rm traincorpus.tmp"
    os.system(command)
    command="rm valcorpus.tmp"
    os.system(command)





if __name__ == "__main__":
    FILET1="train.sp.es"
    FILET2="train.sp.ca"

    FILEV1="val.sp.es"
    FILEV2="val.sp.ca"
    
    finetune_awesome(FILET1, FILET2, FILEV1, FILEV2, initial_model="bert-base-multilingual-cased", output_dir="finetuned_model",device="cuda", cuda_visible_devices="0")
    
    FILE1="train.sp.es"
    FILE2="train.sp.ca"
    OUTPUT_FILE="train.sp.es.ca.align"
    align_awesome_aligner(FILE1, FILE2, OUTPUT_FILE, model="./finetuned_model/checkpoint-12000/", device="cuda", cuda_visible_devices="0")


