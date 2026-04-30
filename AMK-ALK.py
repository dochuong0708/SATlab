from pysat.solvers import Glucose4
def Giai_SUDOKU(Bang):
    Giai = Glucose4()
    def laydiachi(hang,cot,giatri):
        return hang*81 + cot*9 + giatri + 1
    for hang in range(9):
        for cot in range(9):
            if Bang[hang][cot] != 0:
                giatri = Bang[hang][cot] - 1
                Giai.add_clause([laydiachi(hang,cot,giatri)])
    counter = [730]
    '''
    def AMK(daysodung, k):
     n = len(daysodung)
     S = {}

     for i in range(n-1):
        for j in range(1, k+1):
            S[(i, j)] = counter[0]
            counter[0] += 1

     for i in range(n-1):
        Giai.add_clause([-daysodung[i], S[(i,1)]])

     for i in range(1, n-1):
        for j in range(1, k+1):
            Giai.add_clause([-S[(i-1,j)], S[(i,j)]])

     for i in range(1, n-1):
        Giai.add_clause([-daysodung[i], S[(i,1)]])  # j = 1

        for j in range(2, k+1):
            Giai.add_clause([-daysodung[i],-S[(i-1,j-1)],S[(i,j)]])

     for i in range(k, n):
        Giai.add_clause([-daysodung[i],-S[(i-1,k)]])
    '''
    def ALK(daysodung, k):
     n = len(daysodung)
     R = {}
     for i in range(n-1):
        for j in range(1, k+1):
            R[(i, j)] = counter[0]
            counter[0] += 1

     for i in range(n-1):
        Giai.add_clause([-daysodung[i], R[(i, 1)]])
  
     for i in range(1, n-1):
        for j in range(1, k+1):
            Giai.add_clause([-R[(i-1, j)], R[(i, j)]])

     for i in range(1, n-1):
        Giai.add_clause([-daysodung[i], R[(i, 1)]])
        for j in range(2, k+1):
            Giai.add_clause([-daysodung[i],-R[(i-1, j-1)],R[(i, j)]])

     for i in range(1, n-1):
        for j in range(1, k+1):
            Giai.add_clause([daysodung[i],R[(i-1, j)],-R[(i, j)]])

     for i in range(1, min(k, n-1)+1):
        Giai.add_clause([daysodung[i],-R[(i, i)]])

     for i in range(1, n-1):
        for j in range(2, k+1):
            Giai.add_clause([R[(i-1, j-1)],-R[(i, j)]])

     last = n - 2
     if k == 1:
        Giai.add_clause([R[(last, 1)], daysodung[n-1]])
     else:
        Giai.add_clause([R[(last, k)], daysodung[n-1]])
        Giai.add_clause([R[(last, k)], R[(last, k-1)]])


    def EXACTLY_ONE(daysodung):
       # AMK(daysodung,1) #(Dung them ALO)
        ALK(daysodung,1) 
        n = len(daysodung)
        for i in range(n):
            for j in range(i+1,n):
             Giai.add_clause([-daysodung[i],-daysodung[j]])


    for hang in range(9):
        for cot in range(9):
            EXACTLY_ONE([laydiachi(hang,cot,giatri) for giatri in range(9)])
    for hang in range(9):
        for giatri in range(9):
            EXACTLY_ONE([laydiachi(hang,cot,giatri) for cot in range(9)])
    for giatri in range(9):
        for cot in range(9):
            EXACTLY_ONE([laydiachi(hang,cot,giatri) for hang in range(9)])
    for hang_cua_khoi in range(3):
            for cot_cua_khoi in range(3):
                for giatri in range(9):
                    giatri_cua_khoi = []
                    for hang in range(hang_cua_khoi*3,(hang_cua_khoi+1)*3):
                        for cot in range(cot_cua_khoi*3,(cot_cua_khoi+1)*3):
                            giatri_cua_khoi.append(laydiachi(hang,cot,giatri))
                    EXACTLY_ONE(giatri_cua_khoi)
    if Giai.solve():
        model = Giai.get_model()
        danhsachketqua = set(x for x in model if x > 0)
        ketqua = [[0 for _ in range(9)] for _ in range(9)]
        for hang in range(9):
            for cot in range(9):
                for giatri in range(9):
                    if laydiachi(hang,cot,giatri) in danhsachketqua:
                        ketqua[hang][cot] = giatri + 1

        return ketqua
    else:
        return None
Nhap_SUDOKU = [ [5, 3, 0, 0, 7, 0, 0, 0, 0], 
                 [6, 0, 0, 1, 9, 5, 0, 0, 0],
                 [0, 9, 8, 0, 0, 0, 0, 6, 0], 
                 [8, 0, 0, 0, 6, 0, 0, 0, 3], 
                 [4, 0, 0, 8, 0, 3, 0, 0, 1], 
                 [7, 0, 0, 0, 2, 0, 0, 0, 6], 
                 [0, 6, 0, 0, 0, 0, 2, 8, 0], 
                 [0, 0, 0, 4, 1, 9, 0, 0, 5], 
                 [0, 0, 0, 0, 8, 0, 0, 7, 9] ] 
Giaiphap = Giai_SUDOKU(Nhap_SUDOKU)
if Giaiphap: 
    for hang in Giaiphap: 
        print(hang) 
else: 
        print("Không có lời giải!")