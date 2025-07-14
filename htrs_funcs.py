# Hacked together, (but/barely) functional read spliter
# HJ - 24/05/25
#
from glob import glob
import subprocess
import pandas as pd
from Bio import SeqIO
from collections import defaultdict
import os

# def setup_dir(target_dir):

#     print()

def preprocess_data(target, file_size, output_folder):
    
    # split the file 
    command = f"split -l {file_size * 4} {target} {output_folder}/{target.split('/')[-1]}."
    subprocess.run(command, shell = True)
    
    for file in glob(f'{output_folder}/*'):
        
        command = f"seqkit fq2fa {file} -o {file}.fa"
        subprocess.run(command, shell = True)
    
    return(glob(f'{output_folder}/*.fa'))
    
def blast(blastn_path, database, target, word_size, num_threads):
    
    # Command to run blast, and a header to append to the output tsv file. 
    # We probably don't need to do this but it makes it a bit easier to parse later
    command = f'{blastn_path} -db {os.path.dirname(os.path.realpath(__file__))}/{database} -query {target} -word_size {word_size} -num_threads {num_threads} -out {target}.out -outfmt "6 qseqid sseqid qlen pident length mismatch gapopen qstart qend sstart send evalue bitscore"'
    #header = 'qseqid	sseqid	qlen	pident	length	mismatch	gapopen	qstart	qend	sstart	send	evalue	bitscore'
    
    subprocess.run(command, shell = True)
    subprocess.run(f'cat {os.path.dirname(os.path.realpath(__file__))}/header {target}.out > {target}.tsv', shell = True)
    
def split_reads(target):
    cutoff = 18
    
    # Read in the blast tsv, and filter based on the hit length (alternatives might be eval or bitscore!)
    df = pd.read_csv(f'{target}.tsv', sep = '\t')
    df = df.loc[df['length'] >= cutoff]
    
    # Save the hit table as a dict for faster access. Delete the df afterwards to save memory
    hitDict = defaultdict(list)
    for _, row in df.iterrows():
        hitDict[row['qseqid']].append((row['qstart'], row['qend'], row['sstart'], row['send']))
    del(df)
    
    # Make an empty string to save our split sequences to
    splitSeqs = ''
    
    # Loop over each read in the file
    for record in SeqIO.parse(f"{'.'.join(target.split('.')[:-1])}", 'fastq'):
        
        # Get a bunch of info relating to the current read
        name = str(record.id)
        seq  = str(record.seq)
        qual = ''.join([chr(score + 33) for score in record.letter_annotations['phred_quality']]) 
    
        # Check to see if the read exists in our hit dicionary
        # If it does processes the readm if not write the read and go to the next
        hits = hitDict.get(name)
        if hits:
            
            # Make an empty list to store the split coordinates
            # Loop over each one, storing them and then sorting so they are in order
            # Finally save to a list of regions (including the start and stop) that need to be split
            splits = []
            
            for i in range(len(hits)):
                
                splits.append(hits[i][hits[i][2:].index(min(hits[i][2:]))])
            
            splits.sort()
            
            # Go pair by pair through splits, and use those values to break up the read.
            # Saving it to our string as we go
            regions = [0] + splits + [len(seq)]
            for i in range(len(regions) - 1): 
                
                span = [regions[i], regions[i + 1]]
                
                newName = f'{name}_{i}'
                newSeq  = f'{seq[span[0]:span[1]]}'
                newQual = f'{qual[span[0]:span[1]]}'
                
                splitSeqs += f'@{newName}\n{newSeq}\n+\n{newQual}\n'
             
        else:
            splitSeqs += f'@{name}\n{seq}\n+\n{qual}\n'

    # Save the file to the disk after all reads are split
    with open(f"{'.'.join(target.split('.')[:-1])}_split.fastq", 'w') as f: #.fastq
        f.writelines(splitSeqs)
