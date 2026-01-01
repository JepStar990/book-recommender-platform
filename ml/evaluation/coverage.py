def coverage(recommended_ids, total_ids):
    return len(set(recommended_ids)) / len(total_ids)
