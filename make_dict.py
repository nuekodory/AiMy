import sys
from pathlib import Path


if __name__ == '__main__':
    args = sys.argv

    if len(args) < 2:
        print("few args")
        exit(0)

    input_path = Path(args[1])
    pos_out = input_path.with_suffix(".pos.txt")
    neg_out = input_path.with_suffix(".neg.txt")

    positives = []
    negatives = []

    with input_path.open(mode='r') as f:
        for line in f:
            words = line.split()
            if len(words) == 2:
                if words[0][0:2] == "ポジ":
                    positives.append(words[1])
                elif words[0][0:2] == "ネガ":
                    negatives.append(words[1])

    with pos_out.open(mode='w') as pf:
        for word in positives:
            pf.write(word + "\n")

    with neg_out.open(mode='w') as nf:
        for word in negatives:
            nf.write(word + "\n")





