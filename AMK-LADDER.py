from pysat.solvers import Glucose4
import math
def AMK(Giai, dayso, start_i_dayso, k):
     n = len(dayso)
     def S(i,j):
        return start_i_dayso + i*k + (j - 1)
     Giai.add_clause([-dayso[0], S(0,1)])
     for j in range(2,k+1):
         Giai.add_clause([-S(0,j)])

     for i in range(1, n-1):
        for j in range(1, k+1):
            Giai.add_clause([-S(i-1,j), S(i,j)])

        for i in range(1, n-1):
            Giai.add_clause([-dayso[i], S(i,1)])  

        for j in range(2, k+1):
            Giai.add_clause([-dayso[i],-S(i-1,j-1),S(i,j)])

     for i in range(k, n):
        Giai.add_clause([-dayso[i],-S(i-1,k)])

     return start_i_dayso + (n-1)*k + 1

def Area(vars, weight, number):
    start_index = weight * number
    end_index = min(start_index + weight, len(vars))
    return vars[start_index:end_index]

def EncodingAreas(Giai, area, number, n_Areas, start_id_var):
    next_var = start_id_var
    if number != 0:
        next_var = AMK(Giai, area, start_id_var, 1)
    if number != n_Areas - 1:
        next_var = AMK(Giai, area[::-1], next_var, 1)
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
    g.add_clause([3])
    result = g.solve()
    print("SAT:", result)
    if result:
        model = g.get_model()
        true_vars = [x for x in model if x > 0]
        print("Biến nhận giá trị 1:")
        print(true_vars)
if __name__ == "__main__":
    main()