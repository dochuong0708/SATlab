from pysat.solvers import Glucose3

def solve_sudoku(grid):
    solver = Glucose3()

    # Hàm hỗ trợ lấy ID của biến SAT từ tọa độ (row, col, val)
    def get_id(r, c, v):
        return r * 81 + c * 9 + v + 1

    # 1. Điền các ô đã có số sẵn (Unit Clauses)
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                val = grid[r][c] - 1 # Chuyển về 0-8
                solver.add_clause([get_id(r, c, val)])

    # Hàm tạo ràng buộc Exactly One (ALO + AMO Binomial)
    def add_exactly_one(vars_list):
        # ALO: At Least One (Ít nhất một số đúng)
        solver.add_clause(vars_list)
        
        # AMO: At Most One sử dụng BINOMIAL encoding (Tối đa một số đúng)
        # Duyệt qua từng cặp để ép chúng không đồng thời là True
        for i in range(len(vars_list)):
            for j in range(i + 1, len(vars_list)):
                solver.add_clause([-vars_list[i], -vars_list[j]])

    # 2. Ràng buộc: Mỗi ô (r, c) phải có đúng 1 giá trị v
    for r in range(9):
        for c in range(9):
            add_exactly_one([get_id(r, c, v) for v in range(9)])

    # 3. Ràng buộc: Mỗi hàng r phải có đúng 1 giá trị v
    for r in range(9):
        for v in range(9):
            add_exactly_one([get_id(r, c, v) for c in range(9)])

    # 4. Ràng buộc: Mỗi cột c phải có đúng 1 giá trị v
    for c in range(9):
        for v in range(9):
            add_exactly_one([get_id(r, c, v) for r in range(9)])

    # 5. Ràng buộc: Mỗi khối 3x3 phải có đúng 1 giá trị v
    for br in range(3): # Block row
        for bc in range(3): # Block col
            for v in range(9):
                block_vars = []
                for r in range(br * 3, (br + 1) * 3):
                    for c in range(bc * 3, (bc + 1) * 3):
                        block_vars.append(get_id(r, c, v))
                add_exactly_one(block_vars)

    # Giải toán
    if solver.solve():
        model = solver.get_model()
        # Chuyển kết quả từ SAT model về lại grid Sudoku
        result = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                for v in range(9):
                    if get_id(r, c, v) in model:
                        result[r][c] = v + 1
        return result
    else:
        return None

# Ví dụ một đề bài Sudoku (0 là ô trống)
sudoku_input = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solution = solve_sudoku(sudoku_input)
if solution:
    for row in solution:
        print(row)
else:
    print("Không có lời giải!")