'''
from pysat.solvers import Glucose4
import math

def AMK(g, block, number_block, k):
    w = len(block)
    for j in range(0,w-1):
        Xij = block[j]
        Rij1 = SCVar(number_block, j, 0)
        g.add_clause([-Xij, Rij1])
        print(f"AMK: -{Xij} OR {Rij1}")

    for j in range(1,w - 1):
        for s in range(0, min(j,k)):
            Xij = block[j]
            Rijm1s = SCVar(number_block, j-1, s)
            Rijs = SCVar(number_block, j ,s)
            g.add_clause([-Rijm1s, Rijs])
            print(f"AMK: -{Rijm1s} OR {Rijs}")
    
    for j in range(1, w -1):
        for s in range(1,min(j+1,k)):
            Xij = block[j]
            Rijm1sm1 = SCVar(number_block, j-1, s-1)
            Rijs = SCVar(number_block, j ,s)
            g.add_clause([-Xij, -Rijm1sm1, Rijs])
            print(f"AMK: -{Xij} OR -{Rijm1sm1} OR {Rijs}")

    for j in range(k):
        Xij = block[j]
        Rijj = SCVar(number_block, j, j)
        g.add_clause([-Xij, Rijj])
        print(f"AMK: -{Xij} OR {Rijj}")

    for j in range(1, w-1):
        for s in range(1, min(j + 1, k)):
            Rijm1sm1 = SCVar(number_block, j-1,s-1)
            Rijs = SCVar(number_block, j ,s)
            g.add_clause([Rijm1sm1, -Rijs])
            print(f"AMK: {Rijm1sm1} OR -{Rijs}")
    for j in range(1, w-1):
        for s in range(1, min(j-1,k)):
            Xij = block[j]
            Rijm1s = SCVar(number_block, j-1, s)
            Rijs = SCVar(number_block, j, s)
            g.add_clause([Xij, Rijm1s, -Rijs])
            print(f"AMK: {Xij} OR {Rijm1s} OR -{Rijs}")
    for j in range(k, w):
        Xij = block[j]
        Rijm1k = SCVar(number_block, j-1, k-1)
        g.add_clause([-Xij, - Rijm1k])
        print(f"AMK: -{Xij} OR -{Rijm1k}")
# tim hieu cach in ra CNF
def Area(vars, weight, number):
    start_index = weight * number
    end_index = min(start_index + weight, len(vars))
    return vars[start_index:end_index]

def EncodingAreas(g, area, number_area, k, n_Areas, weight):
    number_block1 = NumberBlock(number_area, True, weight)
    number_block2 = NumberBlock(number_area, False, weight)
    block1 = area
    block2 = area[::-1]
    if number_area != 0:
        AMK(g, block1, number_block1,k)
    if number_area != n_Areas -1:
        AMK(g,block2, number_block2, k)

def NumberBlock(number_of_area, isFirst, weight):
    number_of_block = 2 * number_of_area
    if isFirst:
        number_of_block -= 1
    return number_of_block

def ConnectAreas(g, number_area1, number_area2, k, weight):
    w = weight
    number_block1 = NumberBlock(number_area1, False, weight)
    number_block2 = NumberBlock(number_area2, True, weight)
    for j in range(2, w+1):
        for p in range(1,k+1):
            j1 = (w - j + 1) - 1
            s1 = (k - p + 1) - 1
            R_var1 = SCVar(number_block1, j1, s1)

            j2 = (j - 1) - 1
            s2 = (p - 1 + 1) - 1

            if s1 >= 0 and s2 >= 0:
                R_var2 = SCVar(number_block2, j2, s2)
                g.add_clause([-R_var1, -R_var2])
def SC_AMK(g, vars, k, weight):
    n_var = len(vars)
    n_Areas = math.ceil(len(vars)/weight)

    for number in range(n_Areas):
        area = Area(vars, weight, number)
        EncodingAreas(g, area, number, k, n_Areas, weight)
    for number in range(n_Areas - 1):
        ConnectAreas(g, number, number + 1, k, weight)
dictionary_id = {}
next_id = [1]

def KeySCVar(i,j,s):
    return f"{i}_{j}_{s}"

def SCVar(i,j,s):
    key = KeySCVar(i,j,s)

    if key in dictionary_id:
        return dictionary_id[key]

    dictionary_id[key] = next_id[0]
    next_id[0] += 1

    return dictionary_id[key]

def main():
    g = Glucose4()
    global dictionary_id, next_id
    dictionary_id = {}
    vars = list(range(1,11))
    weight = 4
    k = 2
    next_id = [max(vars) + 1]
    
    SC_AMK(g, vars, k, weight)
    
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
'''
from math import ceil
from pysat.solvers import Glucose4

class LadderEncoder:

    def __init__(self, start_id: int):
        self.next_id = start_id
        self.var_map = {}

    def AMK_FOR_LADDER(self, giai: Glucose4, vars: list[int], k: int, weight: int) -> int:
        n_vars = len(vars)
        n_areas = ceil(n_vars / weight)

        # Ma hoa cho tung khu vuc
        for area_id in range(n_areas):
            area = self.lay_khu_vuc(vars, weight, area_id)

            self.mahoa_khu_vuc(giai = giai, area = area, area_id = area_id, k = k, n_areas = n_areas, weight = weight)

        # noi cac khu vuc
        for area_id in range(n_areas - 1):
            self.noi_khu_vuc(giai = giai, area1_id = area_id, area2_id = area_id + 1, k = k, weight = weight)

        self.var_map.clear()
        return self.next_id
    
    def ALK_FOR_LADDER(self, giai: Glucose4, vars: list[int], k: int, weight: int) -> int:
        negative_vars = [-var for var in vars]
        self.AMK_FOR_LADDER(giai = giai, vars = negative_vars, k = weight - k, weight = weight)
        self.var_map.clear()
        return self.next_id
    
    def ladder_exk(self,giai: Glucose4,vars: list[int],k: int,weight: int) -> int:
    
        self.AMK_FOR_LADDER(
            giai=giai,
            vars=vars,
            k=k,
            weight=weight
        )

        self.ALK_FOR_LADDER(
            giai=giai,
            vars=vars,
            k=k,
            weight=weight
        )
        return self.next_id

    
    def lay_khu_vuc(self, vars: list[int], weight: int, area_id: int) -> list[int]:
        start = weight * area_id
        end = min(start + weight, len(vars))
        return vars[start:end]
    
    def mahoa_khu_vuc(self, giai: Glucose4, area: list[int], area_id: int, k: int, n_areas: int, weight: int) -> int:
        block_truoc = self.sothutu_block(area_id, is_first = True)
        block_sau = self.sothutu_block(area_id, is_first = False)

        khu_vuc_truoc = area
        khu_vuc_sau = area[::-1]

        if n_areas == 1:
            self.AMK(giai, khu_vuc_truoc, block_truoc,k)
            return
        if area_id != 0:
            self.AMK(giai, khu_vuc_truoc, block_truoc, k)

        if area_id != n_areas - 1:
            self.AMK(giai, khu_vuc_sau, block_sau, k)

    def noi_khu_vuc(self, giai: Glucose4, area1_id: int, area2_id: int, k: int, weight: int) -> None:
        block1 = self.sothutu_block(area1_id, is_first = False)
        block2 = self.sothutu_block(area2_id, is_first = True)
        for j in range(2, weight + 1):
            for p in range(1, k + 1):
                j1 = weight - j
                s1 = k - p

                j2 = j - 2
                s2 = p - 1

                if j1 < 0 or j2 < 0 or s1 < 0 or s2 < 0:
                    continue

                r1 = self.SC_VAR(block1, j1, s1)
                r2 = self.SC_VAR(block2, j2, s2)

                giai.add_clause([-r1, -r2])


    def AMK(self, giai: Glucose4, block: list[int], block_id: int, k: int) -> int:
        w = len(block)

        if w == 0:
            return
        
        if k >= w:
            k = w
        
        if k < 0:
            giai.add_clause([])
            return
        if k == 0:
            for x in block:
                giai.add_clause([-x])
            return
        
        for j in range(w):
            x_ij = block[j]
            r_ij1 = self.SC_VAR(block_id, j, 0)

            clause = [-x_ij, r_ij1]
            giai.add_clause(clause)

        for j in range(1, w):
            for s in range(min(j, k)):

                r_prev = self.SC_VAR(block_id, j - 1, s)
                r_curr = self.SC_VAR(block_id, j, s)

                clause = [-r_prev, r_curr]
                giai.add_clause(clause)


        for j in range(1, w):
            for s in range(1, min(j + 1, k)):

                x_ij = block[j]
                r_prev = self.SC_VAR(block_id, j - 1, s - 1)
                r_curr = self.SC_VAR(block_id, j, s)

                clause = [-x_ij, -r_prev, r_curr]
                giai.add_clause(clause)

        for j in range(k):
            x_ij = block[j]
            r_jj = self.SC_VAR(block_id, j, j)

            clause = [x_ij, -r_jj]
            giai.add_clause(clause)

        for j in range(1, w):
            for s in range(1, min(j + 1, k)):

                r_prev = self.SC_VAR(block_id, j - 1, s - 1)
                r_curr = self.SC_VAR(block_id, j, s)

                clause = [r_prev, -r_curr]
                giai.add_clause(clause)

        for j in range(1, w):
            for s in range(min(j, k)):

                x_ij = block[j]
                r_prev = self.SC_VAR(block_id, j - 1, s)
                r_curr = self.SC_VAR(block_id, j, s)

                clause = [x_ij, r_prev, -r_curr]
                giai.add_clause(clause)
               

        for j in range(k, w):
            x_ij = block[j]
            r_prev_k = self.SC_VAR(block_id, j - 1, k - 1)

            clause = [-x_ij, -r_prev_k]
            giai.add_clause(clause)
    def SC_VAR(self, block_id:int, j: int, s: int) -> int:
        key = (block_id, j, s)

        if key not in self.var_map:
            self.var_map[key] = self.next_id
            self.next_id += 1

        return self.var_map[key]
    
    def sothutu_block(self, area_id: int, is_first: bool) -> int:
        block_number = 2*area_id
        if is_first:
            block_number -= 1


        return block_number
    
def main():
    giai = Glucose4()
    vars = list(range(1, 16))
    weight = 14

    k = 4
    encoder = LadderEncoder(start_id = len(vars) + 1) 
    encoder.ladder_exk(giai, vars, k, weight)
    
    
    result = giai.solve()
    print("SAT:", result)

    if result:

        model = giai.get_model()
        true_vars = [x for x in model if x > 0]
        print("Biến nhận giá trị 1:")
        print(true_vars)


if __name__ == "__main__":
    main()
        
