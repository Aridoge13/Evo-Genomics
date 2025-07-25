import argparse
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt


def parse_gtf(gtf_path):
    transcripts = defaultdict(list)
    genes = set()

    with open(gtf_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9 or parts[2] != 'exon':
                continue
            start, end, attributes = int(parts[3]), int(parts[4]), parts[8]
            attr_dict = {}
            for item in attributes.strip().split(';'):
                if item.strip():
                    key, val = item.strip().split()
                    attr_dict[key] = val.strip('"')
            gene_id = attr_dict.get('gene_id')
            transcript_id = attr_dict.get('transcript_id')
            if gene_id and transcript_id:
                transcripts[transcript_id].append((start, end))
                genes.add(gene_id)
    return transcripts, genes


def compute_stats(transcripts):
    summary = []
    for tid, exons in transcripts.items():
        exon_count = len(exons)
        length = sum(e - s + 1 for s, e in exons)
        summary.append(
            {'transcript_id': tid, 'exon_count': exon_count, 'length': length})
    return pd.DataFrame(summary)


def filter_transcripts(df, min_len=200, min_exons=2):
    return df[(df['length'] >= min_len) & (df['exon_count'] >= min_exons)]


def extract_filtered_gtf(input_gtf, keep_transcript_ids, output_gtf):
    with open(input_gtf, 'r') as infile, open(output_gtf, 'w') as out:
        for line in infile:
            if line.startswith('#'):
                out.write(line)
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue
            attrs = parts[8]
            if 'transcript_id' in attrs:
                for tid in keep_transcript_ids:
                    if f'transcript_id "{tid}"' in attrs:
                        out.write(line)
                        break


def plot_histograms(df, out_prefix):
    plt.hist(df['length'], bins=50, color='skyblue', edgecolor='black')
    plt.title("Transcript Length Distribution")
    plt.xlabel("Length (bp)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_lengths.png")
    plt.close()

    plt.hist(df['exon_count'], bins=30, color='orange', edgecolor='black')
    plt.title("Exon Count per Transcript")
    plt.xlabel("Exons")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_exon_counts.png")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="QC and filter EviAnn GTF annotation")
    parser.add_argument("gtf", help="Input GTF file")
    parser.add_argument("--min_length", type=int, default=200)
    parser.add_argument("--min_exons", type=int, default=2)
    parser.add_argument("--output_filtered", default="filtered.gtf")
    parser.add_argument("--summary_csv", default="transcript_summary.csv")
    parser.add_argument("--plot_prefix", default="transcript_qc")
    args = parser.parse_args()

    transcripts, genes = parse_gtf(args.gtf)
    print(f"Total transcripts: {len(transcripts)}")
    print(f"Total genes: {len(genes)}")

    df = compute_stats(transcripts)
    df.to_csv(args.summary_csv, index=False)

    plot_histograms(df, args.plot_prefix)

    filtered_df = filter_transcripts(df, args.min_length, args.min_exons)
    print(f"Transcripts after filtering: {len(filtered_df)}")

    extract_filtered_gtf(args.gtf, set(
        filtered_df['transcript_id']), args.output_filtered)
    print(f"Filtered GTF written to: {args.output_filtered}")


if __name__ == "__main__":
    main()
