import sys

args = sys.argv

file_path_1 = args[1]
file_path_2 = args[2]

vocab1 = set(line.strip() for line in open(file_path_1))
vocab2 = set(line.strip() for line in open(file_path_2))

new_words = vocab1.difference(vocab2)
#print(new_words)
print("\n".join(new_words))

