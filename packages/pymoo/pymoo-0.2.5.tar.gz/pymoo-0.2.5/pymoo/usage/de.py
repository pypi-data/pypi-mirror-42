from pymoo.optimize import minimize
from pymop.factory import get_problem

problem = get_problem("rastrigin", n_var=10)

res = minimize(problem,
               method='de',
               method_args={
                   'variant': "DE/best/1/bin",
                   'CR': 2,
                   'F': 0.75,
                   'n_replace': 5,
                   'pop_size': 200
               },
               termination=('n_gen', 1000),
               disp=True)

print("Best solution found: %s" % res.X)
print("Function value: %s" % res.F)
