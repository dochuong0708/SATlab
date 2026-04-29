from pysat.solvers import Glucose4
def Giai_SODUKU(Bang):
    Giai = Glucose4()
    def laydiachi(hang,cot,giatri):
     return hang*81 + cot*9 + giatri + 1
    for hang in range(9):
       for cot in range(9):
           if Bang[hang][cot] !=0:
               giatri=Bang[hang][cot]-1
               Giai.add_clause([laydiachi(hang,cot,giatri)])
    def dung1(daysodung):
      Giai.add_clause(daysodung)
      for i in range(len(daysodung)):
           for j in range(i+1,len(daysodung)):
            Giai.add_clause([-daysodung[i],-daysodung[j]])
    for hang in range(9):
       for cot in range(9):
        dung1([laydiachi(hang,cot,giatri) for giatri in range(9)])
    for hang in range(9):
       for giatri in range(9):
        dung1([laydiachi(hang,cot,giatri) for cot in range(9)])
    for cot in range(9):
       for giatri in range(9):
        dung1([laydiachi(hang,cot,giatri) for hang in range(9)])
    for hang_cua_khoi in range(3):
     for cot_cua_khoi in range(3):
        for giatri in range(9):
            giatri_cua_khoi = []
            for hang in range(hang_cua_khoi*3,(hang_cua_khoi+1)*3):
                for cot in range(cot_cua_khoi*3,(cot_cua_khoi+1)*3):
                    giatri_cua_khoi.append(laydiachi(hang,cot,giatri))
            dung1(giatri_cua_khoi)

    if Giai.solve():
      danhsachketqua = Giai.get_model()
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
Giaiphap = Giai_SODUKU(Nhap_SUDOKU)
if Giaiphap: 
    for hang in Giaiphap: 
        print(hang) 
else: 
        print("Không có lời giải!") 