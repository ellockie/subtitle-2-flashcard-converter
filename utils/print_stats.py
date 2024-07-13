import re


def count_qa_sets(qa_set):
    qa_count = len(re.findall(r'(?m)^Q: ', qa_set))
    print(f"\nThe string contains {qa_count} QA set(s).")
