# HTbfRs2
"Hacked together but funcitonal read splitter" - A script to split highly concatenated reads from oxford nanopore sequencing.

DETAILS DETAIL DETAILS
.
.
.
DETAILS DETAIL DETAILS

## Dependencies
- [SeqKit](https://bioinf.shenwei.me/seqkit/)
- [BLAST+ execitables](https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html)
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
### Commandline arguments
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
