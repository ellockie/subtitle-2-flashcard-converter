import re


def count_qa_sets(qa_set):
    qa_count = len(re.findall(r'(?m)^Q: ', qa_set))
    print(f"\nThe number of QA set(s) generated:  {qa_count}")
