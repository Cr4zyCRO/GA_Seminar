import time

# https://archive.topcoder.com/ProblemStatement/pm/4489
class PolyominoCut:
    def __init__(self):
        self.memo = {}

    # Generate all distinct k-polyominoes using DFS and memoization.    
    def generate_polyominoes(self, k):
        
        if k == 1:
            return [[[0, 0]]]

        smaller_polyominoes = self.generate_polyominoes(k - 1)
        polyominoes = set()

        for poly in smaller_polyominoes:
            for x, y in poly:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_cell = (x + dx, y + dy)
                    if new_cell not in poly:
                        new_poly = poly + [new_cell]
                        normalized_poly = self.normalize(new_poly)
                        polyominoes.add(tuple(normalized_poly))

        return [list(poly) for poly in polyominoes]

    # Normalize a polyomino by translating it to the origin and sorting cells.
    def normalize(self, poly):
    
        min_x = min(x for x, y in poly)
        min_y = min(y for x, y in poly)
        normalized = sorted((x - min_x, y - min_y) for x, y in poly)
        return normalized

    # Check if the remaining part of the board is connected using BFS.
    def is_connected(self, board, width, height):
        visited = set()
        start = None

        for x in range(width):
            for y in range(height):
                if board[x][y] == 1:
                    start = (x, y)
                    break

        if start is None:
            return True

        queue = [start]
        visited.add(start)

        while queue:
            cx, cy = queue.pop()
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited and board[nx][ny] == 1:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

        # Count remaining 1s on the board
        remaining_squares = sum(row.count(1) for row in board)
        return len(visited) == remaining_squares


    # Count the number of ways to cut a k-polyomino while keeping the board connected.
    def count(self, k, width, height):

        polyominoes = self.generate_polyominoes(k)
        count = 0

        for poly in polyominoes:
            for x_offset in range(width):
                for y_offset in range(height):
                    # Place polyomino on the board
                    board = [[1] * height for _ in range(width)]
                    valid = True

                    for x, y in poly:
                        nx, ny = x + x_offset, y + y_offset
                        if 0 <= nx < width and 0 <= ny < height:
                            board[nx][ny] = 0
                        else:
                            valid = False
                            break

                    if not valid:
                        continue

                    # Check if the remaining board is connected
                    if self.is_connected(board, width, height):
                        count += 1

        return count

    # Run tests from a file and write results to another file.
    def run_tests_from_file(self, input_file, output_file):
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0

        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            lines = infile.readlines()

            for i in range(0, len(lines), 4):
                total_tests += 1
                try:
                    k = int(lines[i].strip())
                    width = int(lines[i + 1].strip())
                    height = int(lines[i + 2].strip())
                    expected_result = int(lines[i + 3].strip().split(': ')[1])

                    start_time = time.time()
                    result = self.count(k, width, height)
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    if result == expected_result:
                        passed_tests += 1
                        outfile.write(
                            f"#Test {total_tests} passed successfully.\n\tTime to process: {elapsed_time:.6f} seconds.\n"
                        )
                    else:
                        failed_tests += 1
                        outfile.write(
                            f"#Test {total_tests} failed.\n\tExpected: {expected_result}, Got: {result}. Time to process: {elapsed_time:.6f} seconds.\n"
                        )
                except (ValueError, IndexError) as e:
                    failed_tests += 1
                    outfile.write(
                        f"#Test {total_tests} failed due to input error: {str(e)}.\n"
                    )

            # Write summary to the output file
            outfile.write("\nTest Summary:\n")
            outfile.write(f"Total Tests: {total_tests}\n")
            outfile.write(f"Passed Tests: {passed_tests}\n")
            outfile.write(f"Failed Tests: {failed_tests}\n")

        # Print summary to console
        print(f"Total Tests: {total_tests}")
        print(f"Passed Tests: {passed_tests}")
        print(f"Failed Tests: {failed_tests}")


polyomino_cut = PolyominoCut()
input_file='polyomino_tasks_and_solutions.txt'
otuput_file='polyomino_test_results.txt'
polyomino_cut.run_tests_from_file(input_file,otuput_file)
