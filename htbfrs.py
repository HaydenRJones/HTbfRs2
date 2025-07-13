#     ============================================
#    |  _    _ _______ _      __ _____      ___   |
#    | | |  | |__   __| |    / _|  __ \    |__ \  |
#    | | |__| |  | |  | |__ | |_| |__) |___   ) | |
#    | |  __  |  | |  | '_ \|  _|  _  // __| / /  |
#    | | |  | |  | |  | |_) | | | | \ \\__ \/ /_  |
#    | |_|  |_|  |_|  |_.__/|_| |_|  \_\___/____| |
#    |                                            |
#     ============================================
#
# Hacked together, (but/barely) functional read spliter
# HJ - 24/05/25
#

import os
import time
import argparse
import multiprocessing
import htrs_funcs as htrs

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        prog = 'htbfrs2.py',
        description = 'Hacked together (but/barely functional) read spliter \nsplit highly concatenated reads from ONT sequencing',
        epilog = 'version 2.0 - HJ 24/05/25')
    
    parser.add_argument('-s', '--sample', 
                    help = 'Directory to the fastq file to processes',
                    required = True)
    
    parser.add_argument('-o', '--output', 
                    help = 'Directory to the save data to.',
                    default = f'{os.getcwd()}/output')
    
    parser.add_argument('-B', '--blastn_path', 
                    help = 'Directory to the blastn executable if not in $PATH',
                    default = 'blastn')
    
    parser.add_argument('-N', '--split_number', 
                    help = 'How many reads for breaking up the data.\nDefault value is 25,000',
                    type = int,
                    default = 25000)
    
    parser.add_argument('-t', '--threads', 
                    help = 'Number of threads to use for BLAST searches.\nDefault value is 4',
                    type = int,
                    default = 4)
    
    parser.add_argument('-W', '--word_size', 
                    help = 'The word size to use for BLAST searches\nDefault value is 10',
                    type = int,
                    default = 10)
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    # make output folder
    if not os.path.exists(args.output):
        print('making output folder')
        os.makedirs(args.output)
    
    folder_time = time.time()
    
    # break up the file, and convert it into fasta. Return a list of fasta files to blast
    print('splitting file')
    file_list = htrs.preprocess_data(args.sample, args.split_number, args.output)
    
    file_time = time.time()
    
    print('running blast')
    for file in file_list:
        
        htrs.blast(args.blastn_path, 'ref/barcodes', file, args.word_size, args.threads)
        #htrs.blast('blastn', 'ref/barcodes', file, 10, 4)
    
    blast_time = time.time()
    
    print('splitting reads')
    with multiprocessing.Pool(args.threads) as p:
        
        p.map(htrs.split_reads, file_list)
        
    end_time = time.time()
    
    print(f'''
          making folders   :  {round(folder_time - start_time, 3)}
          splitting files  :  {round(file_time - folder_time, 3)}
          blasting reads   :  {round(blast_time - file_time, 3)}
          splitting reads  :  {round(end_time - blast_time, 3)}
          --------------------{'-' * len(str(round(end_time - start_time, 3)))}
          total runtime    :  {round(end_time - start_time, 3)}
          ''')
    
    
    
    
    
    
    
