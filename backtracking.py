def subset_sum_backtracking(array, sum):
    if sum < 0:
        return
    if len(array) == 0:
        if sum == 0:
            yield []
        return
    for solution in subset_sum_backtracking(array[1:], sum):
        yield solution
    for solution in subset_sum_backtracking(array[1:], sum - array[0]):
        yield [array[0]] + solution


if __name__ == "__main__":
    solution = subset_sum_backtracking([-7, -3, -2, 5, 8], 0)
    for entry in solution:
        print entry    