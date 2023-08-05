import argparse
import smallBixTools as st


def haplo_aligned_file(infile, outfile):
    '''
    Haplotypes an aligned fasta file. Each sequence which is the same is only included once. The last sequence id in
    the file associated with this sequence is used as the seqid in the outfile.
    :param infile: The .fasta formatted file to be haplotyped
    :param outfile: The place to write the haplotyped .fasta file to on disc.
    :return: No return.
    '''
    print("Haplotyping the aligned input file: {}".format(infile))
    dct = st.fasta_to_dct(infile)
    print("Input file has {} sequences".format(len(dct)))
    rev_haplo_dct = {}
    haplo_dct = {}
    for k, v in dct.items():
        rev_haplo_dct[v] = k
    for k, v in rev_haplo_dct.items():
        haplo_dct[v] = k
    st.dct_to_fasta(haplo_dct, outfile)
    print("Output file has {} sequences".format(len(haplo_dct)))
    print("Completed. Written to file: {}".format(outfile))


def main(infile, outfile):
    haplo_aligned_file(infile, outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Haplotypes the aligned input file.')
    parser.add_argument('-in', '--infile', type=str,
                        help='An aligned fasta file', required=True)
    parser.add_argument('-out', '--outfile', type=str,
                        help='A place to write the aligned haplotyped version of the input file.', required=True)

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile

    main(infile, outfile)
