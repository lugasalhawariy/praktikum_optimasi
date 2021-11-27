##max = 300x1+500x2
##s.t 2x1+x2<=400
## 2x1+5x2<=800
## x1,x2<=0 Integer
from pulp import *
#definisikan variable
#x1 maupun x2 tidak boleh bernilai negatif
x1 = LpVariable("x1",lowBound=0,cat='Integer')
x2 = LpVariable("x2",lowBound=0,cat='Integer')
#definisikan mode maksimal
prob = LpProblem("myProblem", LpMaximize)
#definisikan constrain
prob +=2*x1+x2<=400
prob +=2*x1+5*x2<=800
#definisikan solusi
prob +=300*x1+500*x2
#run
status = prob.solve()
rsltX1 = int(value(x1))
rsltX2 = int(value(x2))
rsltZ = int(300*rsltX1+500*rsltX2)
print('hasil Maksimal dari LP adalah ','300*',rsltX1,'+ 500*',rsltX2,' = ',rsltZ)
print('-> Kue Dadar yang diproduksi sebaiknya berjumlah ',rsltX1)
print('-> Kue Apem yang diproduksi sebaiknya berjumlah ',rsltX2)
print('-> Keuntungan maksimal yang didapat berjumlah Rp.',rsltZ)