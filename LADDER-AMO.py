'''
from pysat.solvers import Glucose4
import math

def AMO(Giai, dayso, start_i_dayso):
    n = len(dayso)
    if n == 0:
        return start_i_dayso
    
    S = list(range(start_i_dayso, start_i_dayso + n - 1))

    Giai.add_clause([-dayso[0], S[0]])   

    for i in range(1, n - 1):
        Giai.add_clause([-dayso[i], S[i]])
        Giai.add_clause([-S[i-1], S[i]])
        Giai.add_clause([-S[i-1], -dayso[i]])
    Giai.add_clause([-S[n-2], -dayso[n-1]])
    return start_i_dayso + n - 1

def Chia_block(dayso, block_size, overlap_size=0):
    danh_sach_blocks = []
    n = len(dayso)
    start_index = 0
    while start_index < n:
        end_index = min(start_index + block_size, n)
        block = dayso[start_index:end_index]
        danh_sach_blocks.append(block)
        start_index += block_size
    return danh_sach_blocks

def Lay_Start_Var_Block(n_vars, number_of_block, weight):
    return n_vars + number_of_block * weight + 1

def Lay_Number_Block(idx_area, isReverse, weight):
    number_of_block = 2 * idx_area
    if isReverse:
        number_of_block -= 1
    return number_of_block

def MaHoa_block(Giai, danh_sach_blocks, n_vars, weight):
    n_Areas = len(danh_sach_blocks)
    
    for idx, area in enumerate(danh_sach_blocks):
        # Khối đầu tiên (B1) chỉ cần mã hóa xuôi
        if idx == 0:
            num_block_xuoi = Lay_Number_Block(idx, isReverse=False, weight=weight)
            start_id = Lay_Start_Var_Block(n_vars, num_block_xuoi, weight)
            AMO(Giai, area, start_id)
            
        # Khối cuối cùng chỉ cần mã hóa ngược
        elif idx == n_Areas - 1:
            num_block_nguoc = Lay_Number_Block(idx, isReverse=True, weight=weight)
            start_id = Lay_Start_Var_Block(n_vars, num_block_nguoc, weight)
            AMO(Giai, area[::-1], start_id)
            
        # Các khối ở giữa cần cả 2 chuỗi xuôi và ngược để nối hai bên
        else:
            # 1. Chuỗi ngược (phục vụ nối với khối bên trái)
            num_block_nguoc = Lay_Number_Block(idx, isReverse=True, weight=weight)
            start_id_nguoc = Lay_Start_Var_Block(n_vars, num_block_nguoc, weight)
            AMO(Giai, area[::-1], start_id_nguoc)
            
            # 2. Chuỗi xuôi (phục vụ nối với khối bên phải)
            num_block_xuoi = Lay_Number_Block(idx, isReverse=False, weight=weight)
            start_id_xuoi = Lay_Start_Var_Block(n_vars, num_block_xuoi, weight)
            AMO(Giai, area, start_id_xuoi)

def Noi_block(Giai, n_vars, danh_sach_blocks, weight):
    n_Areas = len(danh_sach_blocks)
    overlap = weight - 1

    # Duyệt qua từng cặp khối kề nhau (idx và idx + 1)
    for idx in range(n_Areas - 1):
        # Lấy ID biến bắt đầu của chuỗi xuôi khối bên trái
        num_block1 = Lay_Number_Block(idx, isReverse=False, weight=weight)
        start_var_block1 = Lay_Start_Var_Block(n_vars, num_block1, weight)
        
        # Lấy ID biến bắt đầu của chuỗi ngược khối bên phải
        num_block2 = Lay_Number_Block(idx + 1, isReverse=True, weight=weight)
        start_var_block2 = Lay_Start_Var_Block(n_vars, num_block2, weight)
        
        # Tiến hành nối đối xứng từng cặp biến phụ
        for i in range(overlap):
            left_var = start_var_block1 + i
            right_var = start_var_block2 + (overlap - 1 - i)
            
            Giai.add_clause([-left_var, -right_var])

if __name__ == "__main__":
    g = Glucose4()
    
    X = list(range(1, 11)) # 10 biến gốc từ 1 đến 10
    n_vars = len(X)
    weight = 4
    
    print("--- PHẦN 1: CHIA BLOCK ---")
    danh_sach_blocks = Chia_block(X, block_size=weight)
    for idx, b in enumerate(danh_sach_blocks):
        print(f"Vùng Area {idx}: {[f'X{i}' for i in b]}")
        
    print("\n--- PHẦN 2: MÃ HÓA TỪNG BLOCK ---")
    MaHoa_block(g, danh_sach_blocks, n_vars, weight)
    print("Mã hóa các vùng xuôi/ngược hoàn tất.")

    print("\n--- PHẦN 3: NỐI CÁC BLOCK LẠI ---")
    Noi_block(g, n_vars, danh_sach_blocks, weight)
    print("Đã nạp toàn bộ các mệnh đề nối đối xứng vào SAT Solver.")
    
    g = Glucose4()
    MaHoa_block(g, danh_sach_blocks, n_vars, weight)
    Noi_block(g, n_vars, danh_sach_blocks, weight)
    
    g.add_clause([X[5]]) 
    is_sat_valid = g.solve()
    print(f"Kết quả SAT khi chỉ có X3=True: {is_sat_valid} (Mong đợi: True)")
    if is_sat_valid:
        print("Biến nhận giá trị 1 (Chỉ lấy các biến gốc > 0):")
        print([item for item in g.get_model() if 0 < item ])
'''
from pysat.solvers import Glucose4
import math
def AMO(Giai, dayso, start_i_dayso):
    n = len(dayso)
    if n == 0:
        return start_i_dayso
    
    S = list(range(start_i_dayso, start_i_dayso + n - 1))

    Giai.add_clause([-dayso[0], S[0]])   

    for i in range(1, n - 1):
        Giai.add_clause([-dayso[i], S[i]])
        Giai.add_clause([-S[i-1], S[i]])
        Giai.add_clause([-S[i-1], -dayso[i]])
    Giai.add_clause([-S[n-2], -dayso[n-1]])
    return start_i_dayso + n - 1

def Area(vars, weight, number):
    start_index = weight * number
    end_index = min(start_index + weight, len(vars))
    return vars[start_index:end_index]

def EncodingAreas(Giai, area, number, n_Areas, start_id_var):
    next_var = start_id_var
    if number != 0:
        next_var = AMO(Giai, area, start_id_var)
    if number != n_Areas - 1:
        next_var = AMO(Giai, area[::-1], next_var)
    return next_var

def ConnectAreas(Giai,  n_vars, number1, number2, weight):    
    number_of_block1 = NumberBlock(number1, False, weight)
    number_of_block2 = NumberBlock(number2, True, weight)
    start_var_block1 = StartVarBlock(n_vars, number_of_block1, weight)
    start_var_block2 = StartVarBlock(n_vars, number_of_block2, weight)
    overlap = weight - 1
    for i in range(overlap):
        left_var  = start_var_block1 + i
        right_var = start_var_block2 + (overlap - 1 - i)
        Giai.add_clause([-left_var, -right_var])

def SC(Giai, vars, weight):
    n_var = len(vars)
    next_var = n_var + 1
    n_Areas = math.ceil(len(vars) / weight)
    for number in range(n_Areas):
        area = Area(vars, weight, number)
        next_var = EncodingAreas(Giai, area, number, n_Areas, next_var)
    for number in range(n_Areas - 1):
        ConnectAreas(Giai, n_var, number, number + 1, weight)

def NumberBlock(number_of_area, isFirst, weight):
    number_of_block = 2 * number_of_area
    if isFirst:
        number_of_block -= 1
    return number_of_block

def StartVarBlock(n_vars, number_of_block, weight):
    return n_vars + number_of_block * weight + 1

def main():
    g = Glucose4()
    vars = list(range(1, 11))
    weight = 4
    SC(g, vars, weight)
    g.add_clause([4])
    result = g.solve()
    print("SAT:", result)
    if result:
        model = g.get_model()
        true_vars = [x for x in model if x > 0]
        print("Biến nhận giá trị 1:")
        print(true_vars)
if __name__ == "__main__":
    main()