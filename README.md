# HTbfRs2
"Hacked together but funcitonal read splitter" - A script to split highly concatenated reads from oxford nanopore sequencing.

DETAILS DETAIL DETAILS
.
.
.
DETAILS DETAIL DETAILS

## Dependencies
- [SeqKit](https://bioinf.shenwei.me/seqkit/)
- [BLAST+ executables](https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html)
  - blastn
  - makeblastdb[^1]
- Python >= 3.11
  - Pandas
  - Numpy
  - Biopython
  - Matplotlib[^2]
  - Seaborn[^2]

[^1]: only needed if using different barcodes from those in [EXP-PBC001](https://store.nanoporetech.com/pcr-barcoding-expansion-1-12.html)
[^2]: if plotting barcode hit distributions

## Setup

DETAILS DETAIL DETAILS
.
.
.
DETAILS DETAIL DETAILS

## Usage
### Data prerequisites
As with the previous version of this tool, the number of reads processed at any one time is the biggest bottleneck. This tool tries to circumvent this by automatically splitting data files prior to analysis.
The optimal number of reads to split into will depend on the length of reads and computer being used, however during testing 25,000 reads (100,000 lines for fastq) was found to work well and is set as the default.

### Command line arguments

- `-s, --sample` : the fastq sample to processes

- `-o, --output` : the directory to save results to. Defaults to ./output/

- `-B, --blastn_path` : the directory to the blastn executable, if not in $PATH

- `-N, --split_number` : how many reads to split the data file into. Defaults to 25,000

- `-t, --threads` : how many threads to use. Used for blastn and the final splitting step. Default is 4.

### Output

## Examples

DETAILS DETAIL DETAILS
.
.
.
DETAILS DETAIL DETAILS

### Relative distributions of barcode hits
**Before:**

<img src="example_images/Barplot_unsplit.png" width="75%">

**After:**

<img src="example_images/Barplot_split.png" width="75%">
