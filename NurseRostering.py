from pysat.solvers import Glucose4
from AMK_LADDER import LadderEncoder
# from LADDER_AMO import Chia_block, MaHoa_block, Noi_block       
import math
class NurseRostering:
    def __init__(self, solver, day, n_nurse):
        self.next_id = 1
        self.giai = solver
        self.d = day
        self.n = n_nurse
        self.var_map = {}
        self.shift = ['D', 'E', 'N', 'O']

        for nurse in range(self.n):
            for day in range(self.d):
                for s in self.shift:
                    self.var_map[(nurse, day, s)] = self.next_id
                    self.next_id += 1

    def var(self, nurse, day, shift):
            return self.var_map[(nurse, day, shift)]
        
    def encoding(self):
            self.constraints_1()
            self.constraints_2()
            self.constraints_3()
            self.constraints_4()
            self.constraints_5()
            self.constraints_6()
            self.constraints_7()
            self.constraints_8()
            self.constraints_9()
            self.constraints_10()
            self.constraints_11()

    def constraints_1(self):
            for nurse in range(self.n):
                for day in range(self.d):
                    clause = [self.var(nurse,day,s) for s in self.shift]
                    self.giai.add_clause(clause)

                    for i in range(len(clause)):
                        for j in range(i+1, len(clause)):
                            self.giai.add_clause([-clause[i],-clause[j]])
        
    def constraints_2(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                curr_var = [self.var(nurse,day,'O') for day in range(self.d)]
                self.next_id = encoder.ALK_FOR_LADDER(self.giai, curr_var, 1,7)

    def constraints_3(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                curr_var = [self.var(nurse,day,'O') for day in range(self.d)]
                self.next_id = encoder.ALK_FOR_LADDER(self.giai, curr_var, 4, 14)

    def constraints_4(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                curr_var = [self.var(nurse,day, 'E') for day in range(self.d)]
                self.next_id = encoder.ALK_FOR_LADDER(self.giai, curr_var, 4, 14)
        
    def constraints_5(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                curr_var = [self.var(nurse,day, 'E') for day in range(self.d)]
                self.next_id = encoder.AMK_FOR_LADDER(self.giai, curr_var, 8, 14)

    def constraints_6(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                curr_var = [self.var(nurse,day, 'O') for day in range(self.d)]
                self.next_id = encoder.AMK_FOR_LADDER(self.giai, curr_var, 8, 28)

    def constraints_7(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                curr_var = [self.var(nurse,day, 'N') for day in range(self.d)]
                self.next_id = encoder.AMK_FOR_LADDER(self.giai, curr_var, 4, 14)
        
    def constraints_8(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                curr_var = [self.var(nurse,day, 'N') for day in range(self.d)]
                self.next_id = encoder.ALK_FOR_LADDER(self.giai, curr_var, 1, 14)

    def constraints_9(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                lich_lam_viec = []
                for day in range(self.d):
                    v_E = self.var(nurse, day, 'E')
                    v_N = self.var(nurse, day, 'N')
                    lich_lam_viec.append(v_E)
                    lich_lam_viec.append(v_N)
                self.next_id = encoder.ALK_FOR_LADDER(self.giai, lich_lam_viec, 2, 14)

    def constraints_10(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                lich_lam_viec = []
                for day in range(self.d):
                    v_E = self.var(nurse, day, 'E')
                    v_N = self.var(nurse, day, 'N')
                    lich_lam_viec.append(v_E)
                    lich_lam_viec.append(v_N)
                self.next_id = encoder.AMK_FOR_LADDER(self.giai, lich_lam_viec, 4, 14)


    def constraints_11(self):
            for nurse in range(self.n):
                encoder = LadderEncoder(self.next_id)
                curr_var = [self.var(nurse, day, 'N') for day in range(self.d)]
                self.next_id = encoder.AMK_FOR_LADDER(self.giai, curr_var, 1, 2)
    ##########################################################################
    # DISPLAY
    ##########################################################################
    
    def display_schedule(self, model: list):
    
        if not model:
            print("Không tìm thấy lịch hợp lệ!")
            return
    
        true_vars = set(model)
    
        nurse_width = 10
        cell_width = 4
    
        total_width = nurse_width + (self.d * (cell_width + 1)) + 1
    
        print("\n" + "=" * total_width)
        print("LỊCH TRỰC ĐIỀU DƯỠNG".center(total_width))
        print("=" * total_width)
    
        header = f"{'Y tá':<{nurse_width}}|"
    
        for j in range(self.d):
            header += f"{j:^{cell_width}}|"
    
        print(header)
        print("-" * total_width)
    
        for i in range(self.n):
            row = f"{f'{i:02d}':<{nurse_width}}|"
    
            for j in range(self.d):
                assigned_shift = "--"

                for shift in self.shift:
                    var_id = self.var(i, j, shift)
    
                    if var_id in true_vars:
                        assigned_shift = shift
                        break
    
                row += f"{assigned_shift:^{cell_width}}|"
    
            print(row)
    
        print("=" * total_width)
    
    ##########################################################################
    # VERIFY SCHEDULE
    ##########################################################################

    def verify_schedule(self, model: list):
        """
        Kiểm tra lịch trực có thỏa tất cả ràng buộc hay không.
        """

        if not model:
            print("Model rỗng!")
            return False

        true_vars = set(v for v in model if v > 0)

        errors = []

        # ==========================================================
        # Helper
        # ==========================================================
        def has_shift(i, j, shift):
            return self.var(i, j, shift) in true_vars

        def count_shift(window, shifts):
            cnt = 0
            for day in window:
                for s in shifts:
                    if has_shift(i, day, s):
                        cnt += 1
            return cnt

        # ==========================================================
        # Constraint 1
        # Mỗi ngày đúng 1 ca
        # ==========================================================
        for i in range(self.n):
            for j in range(self.d):

                assigned = 0

                for s in self.shift:
                    if has_shift(i, j, s):
                        assigned += 1

                if assigned != 1:
                    errors.append(
                        f"C1: Nurse {i}, day {j} có {assigned} ca"
                    )

        # ==========================================================
        # Constraint 2
        # Trong 7 ngày liên tiếp: tối đa 6 ngày làm
        # <=> ít nhất 1 ngày OFF
        # ==========================================================
        for i in range(self.n):
            for start in range(self.d - 7 + 1):

                off_count = 0

                for j in range(start, start + 7):
                    if has_shift(i, j, 'O'):
                        off_count += 1

                if off_count < 1:
                    errors.append(
                        f"C2: Nurse {i}, window {start}-{start+6} không có ngày nghỉ"
                    )

        # ==========================================================
        # Constraint 3
        # 14 ngày liên tiếp phải có ít nhất 4 OFF
        # ==========================================================
        for i in range(self.n):
            for start in range(self.d - 14 + 1):

                off_count = 0

                for j in range(start, start + 14):
                    if has_shift(i, j, 'O'):
                        off_count += 1

                if off_count < 4:
                    errors.append(
                        f"C3: Nurse {i}, window {start}-{start+13} có {off_count} OFF"
                    )

        # ==========================================================
        # Constraint 4 + 5
        # 14 ngày:
        # 4 <= E <= 8
        # ==========================================================
        for i in range(self.n):
            for start in range(self.d - 14 + 1):

                e_count = 0

                for j in range(start, start + 14):
                    if has_shift(i, j, 'E'):
                        e_count += 1

                if e_count < 4:
                    errors.append(
                        f"C4: Nurse {i}, window {start}-{start+13} chỉ có {e_count} ca E"
                    )

                if e_count > 8:
                    errors.append(
                        f"C5: Nurse {i}, window {start}-{start+13} có {e_count} ca E"
                    )

        # ==========================================================
        # Constraint 6
        # 28 ngày liên tiếp phải có ít nhất 20 ngày làm
        # <=> tối đa 8 OFF
        # ==========================================================
        for i in range(self.n):
            for start in range(self.d - 28 + 1):

                off_count = 0

                for j in range(start, start + 28):
                    if has_shift(i, j, 'O'):
                        off_count += 1

                if off_count > 8:
                    errors.append(
                        f"C6: Nurse {i}, window {start}-{start+27} có {off_count} OFF"
                    )

        # ==========================================================
        # Constraint 7 + 8
        # 14 ngày:
        # 1 <= N <= 4
        # ==========================================================
        for i in range(self.n):
            for start in range(self.d - 14 + 1):

                n_count = 0

                for j in range(start, start + 14):
                    if has_shift(i, j, 'N'):
                        n_count += 1

                if n_count > 4:
                    errors.append(
                        f"C7: Nurse {i}, window {start}-{start+13} có {n_count} ca N"
                    )

                if n_count < 1:
                    errors.append(
                        f"C8: Nurse {i}, window {start}-{start+13} không có ca N"
                    )

        # ==========================================================
        # Constraint 9 + 10
        # Trong 7 ngày:
        # 2 <= E+N <= 4
        # ==========================================================
        for i in range(self.n):
            for start in range(self.d - 7 + 1):

                count_en = 0

                for j in range(start, start + 7):

                    if has_shift(i, j, 'E'):
                        count_en += 1

                    if has_shift(i, j, 'N'):
                        count_en += 1

                if count_en < 2:
                    errors.append(
                        f"C9: Nurse {i}, window {start}-{start+6} chỉ có {count_en} ca E/N"
                    )

                if count_en > 4:
                    errors.append(
                        f"C10: Nurse {i}, window {start}-{start+6} có {count_en} ca E/N"
                    )

        # ==========================================================
        # Constraint 11
        # Không có 2 ca đêm liên tiếp
        # ==========================================================
        for i in range(self.n):
            for j in range(self.d - 1):

                if has_shift(i, j, 'N') and has_shift(i, j + 1, 'N'):
                    errors.append(
                        f"C11: Nurse {i} làm N liên tiếp ngày {j}-{j+1}"
                    )

        # ==========================================================
        # RESULT
        # ==========================================================
        if len(errors) == 0:
            print("Lịch hợp lệ ✓")
            return True

        print("\nLịch KHÔNG hợp lệ!")
        print("=" * 60)

        for err in errors:
            print(err)

        print("=" * 60)
        print(f"Tổng số lỗi: {len(errors)}")

        return False
if __name__ == "__main__":
    solver = Glucose4()

    num_days = 28
    num_nurses = 10

    print(f"Đang khởi tạo bài toán: {num_nurses} y tá, {num_days} ngày...")

    rostering = NurseRostering(
        solver,
        day=num_days,
        n_nurse=num_nurses
    )

    rostering.encoding()

    print(f"Tổng số biến đã sinh ra: {rostering.next_id - 1}")
    print("Đang tiến hành giải bài toán...")

    is_solved = solver.solve()

    if is_solved:

        print("Giải thành công! Đang lấy kết quả...\n")

        sat_model = solver.get_model()

        # Hiển thị lịch
        rostering.display_schedule(sat_model)

        # Kiểm tra lại lời giải
        print("\nĐANG KIỂM TRA RÀNG BUỘC...")
        valid = rostering.verify_schedule(sat_model)

        if valid:
            print("\nKẾT QUẢ: MODEL HỢP LỆ ✓")
        else:
            print("\nKẾT QUẢ: MODEL KHÔNG HỢP LỆ ✗")

    else:
        print("Không tìm được phương án xếp lịch thỏa mãn tất cả ràng buộc (UNSAT)!")
            
        

