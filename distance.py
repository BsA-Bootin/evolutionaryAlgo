def merge_count(arr):
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2
    left, inv_count_left = merge_count(arr[:mid])
    right, inv_count_right = merge_count(arr[mid:])
    merged, inv_count_merge = merge_split(left, right)
    
    return merged, inv_count_left + inv_count_right + inv_count_merge

def merge_split(left, right):
    result = []
    inv_count = 0
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            inv_count += len(left) - i

    result.extend(left[i:])
    result.extend(right[j:])
    return result, inv_count

def kendall_tau_distance(perm1, perm2):
    if len(perm1) != len(perm2):
        raise ValueError("Permutations must have the same length")

    # Create lists to store ranks
    rank_perm1 = [0] * len(perm1)
    rank_perm2 = [0] * len(perm2)

    for i, val in enumerate(perm1):
        rank_perm1[val] = i
    for i, val in enumerate(perm2):
        rank_perm2[val] = i

    # Compute the difference in ranks using merge-based counting
    distance = merge_count([rank_perm1[i] - rank_perm2[i] for i in range(len(perm1))])[1]

    return distance