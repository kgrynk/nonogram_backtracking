import numpy as np

# For given line of a picture, check if it matches the goal for this line
def line_correct(line, goal):
    # Check if sum equals, optimization
    if sum(line) != sum(goal):
        return False
    i = 0
    # Check every 'block'
    for block in goal:
        while i < len(line):
            if line[i] == 1:
                break
            if line[i] == -1:
                return False
            i += 1
        else:
            return False

        bits = 0

        while i < len(line):
            if line[i] == 0:
                break
            if line[i] == -1:
                return False
            bits += 1
            i += 1

        if not bits == block:
            return False

    while i < len(line):
        if line[i] == 1 or line[i] == -1:
            return False
        i += 1

    return True


# Very similar function, but works also for the part of the line and allow -1 (unknown) bits
def part_incorrect(line, goal, end):
    line_bits = sum(line[0:end+1])
    goal_bits = sum(goal)
    space_left = len(line) - end
    if goal_bits - line_bits >= space_left:
        return True

    i = 0
    for block in goal:
        while i <= end:
            if line[i] == 1:
                break
            i += 1
        else:
            return False

        bits = 0

        while i <= end:
            if line[i] == 0:
                break
            bits += 1
            i += 1
        else:
            return bits > block

        if not bits == block:
            return True

    while i <= end:
        if line[i] == 1 or line[i] == -1:
            return True
        i += 1

    return False


def main():

    # 4 tests - the last one is the hardest (size 20) - it takes about 80 sec
    # usually too slow for pictures of size 25
    for t in range(1,5):
        input_name = "test" + str(t) + ".txt"
        output_name = "result" + str(t) + ".txt"
        print("Test " + str(t) + "...")

        with open(input_name, "r+") as input_file:
            with open(output_name, "w+") as output_file:
                # process input
                top = input_file.readline().split()
                n = int(top[0])
                m = int(top[1])
                j = 0

                rows_goal = []
                cols_goal = []

                for line in input_file:
                    if j < n:
                        rows_goal.append(list(map(int, line.split())))
                    else:
                        cols_goal.append(list(map(int, line.split())))
                    j += 1

                # picture is unknown yet
                picture = np.full((n, m), -1, dtype=int)
                index = 0

                while True:
                    i = index // m
                    j = index % m

                    # we will try 0 (white), 1 (black), then set -1 (unknown bit) and go back
                    picture[i][j] += 1
                    if picture[i][j] == 2:
                        picture[i][j] = -1
                        index -= 1
                        continue

                    # line or column is incorrect, so we try again
                    if part_incorrect(picture[i], rows_goal[i], j) or part_incorrect(picture[:, j], cols_goal[j], i):
                        continue

                    if i == n - 1 and j == m - 1:
                        end = True

                        # end of image, we need to do final check
                        for row_i in range(n):
                            if not line_correct(picture[row_i], rows_goal[row_i]):
                                end = False
                                break
                        if end:
                            for col_j in range(m):
                                if not line_correct(picture[:, col_j], cols_goal[col_j]):
                                    end = False
                                    break
                        if end:
                            break
                        else:
                            continue
                    index += 1

                # picture is correct, write solution
                for i in range(n):
                    for j in range(m):
                        if picture[i][j] == 1:
                            output_file.write('#')
                        elif picture[i][j] == 0:
                            output_file.write('.')
                        else:
                            output_file.write('?')
                    output_file.write('\n')


if __name__ == '__main__':
    main()