from pysat.solvers import Glucose4
import math

def laydiachi_giatri_bandau(hang,cot,giatri):
    return hang*81 + cot*9 + giatri + 1

def laydiachi_giatri_bit(hang,cot,giatri):
    return 729 + hang*36 + cot*4 + giatri + 1

def BinaryEncoding_cho_1_o(Giai, hang, cot):
    k = 4
    for giatri in range(9):
        x = laydiachi_giatri_bandau(hang,cot,giatri)
        binary = format(giatri,'04b')

        for gt_bit in range(k):
            if binary[gt_bit] == '1':
                Giai.add_clause([-x,laydiachi_giatri_bit(hang,cot,gt_bit)])
            else:
                Giai.add_clause([-x,-laydiachi_giatri_bit(hang,cot,gt_bit)])
        
        menhde = [x]
        for gt_bit in range(k):
            if binary[gt_bit] == '1':
                menhde.append(-laydiachi_giatri_bit(hang,cot,gt_bit))
            else:
                menhde.append(laydiachi_giatri_bit(hang,cot,gt_bit))
        Giai.add_clause(menhde)
    Giai.add_clause([laydiachi_giatri_bandau(hang,cot,giatri) for giatri in range(9)])
def Quy_tac_sudoku(Giai):
    for hang in range(9):
        for cot in range(9):
            for gt1 in range(9):
                for gt2 in range(gt1+1,9):
                    Giai.add_clause([-laydiachi_giatri_bandau(hang,cot,gt1),-laydiachi_giatri_bandau(hang,cot,gt2)])
    
    for hang in range(9):
        for gt in range(9):
            for c1 in range(9):
                for c2 in range(c1+1,9):
                    Giai.add_clause([-laydiachi_giatri_bandau(hang,c1,gt),-laydiachi_giatri_bandau(hang,c2,gt)])

    for cot in range(9):
        for gt in range(9):
            for h1 in range(9):
                for h2 in range(h1+1,9):
                    Giai.add_clause([-laydiachi_giatri_bandau(h1,cot,gt),-laydiachi_giatri_bandau(h2,cot,gt)])
    
    for hang_cua_khoi in range(3):
        for cot_cua_khoi in range(3):
            for gt in range(9):
                khoi = []
                for hang in range(hang_cua_khoi*3,hang_cua_khoi*3+3):
                    for cot in range(cot_cua_khoi*3,cot_cua_khoi*3+3):
                        khoi.append((hang,cot))

                for i in range(len(khoi)):
                    for j in range(i+1,len(khoi)):
                        h1,c1 = khoi[i]
                        h2,c2 = khoi[j]
                        Giai.add_clause([-laydiachi_giatri_bandau(h1,c1,gt),-laydiachi_giatri_bandau(h2,c2,gt)])

def Giai_SUDOKU(Bang):
    Giai = Glucose4()

    for hang in range(9):
        for cot in range(9):
            BinaryEncoding_cho_1_o(Giai,hang,cot)

    Quy_tac_sudoku(Giai)

    for hang in range(9):
        for cot in range(9):
            if Bang[hang][cot] != 0:
                gt = Bang[hang][cot] - 1
                Giai.add_clause([laydiachi_giatri_bandau(hang,cot,gt)])

    if Giai.solve():
        model = Giai.get_model()
        kq=[[0]*9 for _ in range(9)]

        for hang in range(9):
            for cot in range(9):
                for gt in range(9):
                    if laydiachi_giatri_bandau(hang,cot,gt) in model:
                        kq[hang][cot] = gt+1
        return kq
    else:
        return None

Bang = [
[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9]
]

Giai = Giai_SUDOKU(Bang)

if Giai:
    for hang in Giai:
        print(hang)
else:
    print("Không có lời giải!")