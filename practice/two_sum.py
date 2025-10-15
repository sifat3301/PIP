def two_sum(nums, target):
    start, end = 0, len(nums) - 1
    arr = sorted(nums)
    while start <= end:
        if arr[start] + arr[end] == target:
            return [arr[start], arr[end]]
        elif arr[start] + arr[end] < target:
            start += 1
        else:
            end -= 1
    return []

print(two_sum([2, 7, 11, 15], 9))