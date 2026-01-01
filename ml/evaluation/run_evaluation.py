from ml.evaluation.precision_at_k import precision_at_k

if __name__ == "__main__":
    print("Precision@5:", precision_at_k(5))
    print("Precision@10:", precision_at_k(10))
