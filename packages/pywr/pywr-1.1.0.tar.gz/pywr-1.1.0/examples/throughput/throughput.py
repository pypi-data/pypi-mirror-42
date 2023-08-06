import pyximport; pyximport.install()
from _throughput import time_my_c_func
from pywr.core import Model, Input, Output, Scenario
from pywr.solvers import Solver, solver_registry
from pywr_pyomo_solver import PyomoSolver
import time


class NullSolver(Solver):
    name = 'null'
    def setup(self, model):
        pass

    def solve(self, model):
        for scenario_index in model.scenarios.combinations:
            self.solve_scenario(model, scenario_index)

    def solve_scenario(self, model, si):

        for node in model.nodes:
            node.commit(si.global_id, 0.0)

    def reset(self):
        pass

solver_registry.append(NullSolver)

def my_func(a, b):
    return a * b


def time_my_func(n):
    a = 1
    b = 2

    t0 = time.time()
    for i in range(n):
        my_func(a, b)
    t1 = time.time()

    return (t1 - t0) / n


def time_pywr_model(solver):

    m = Model(solver=solver)
    for r in range(10):
        i = Input(m, name=f'in{r}', max_flow=r)
        o = Output(m, name=f'out{r}', cost=-r)
        i.connect(o)
    Scenario(m, 'test', size=100)

    m.setup()
    m.reset()

    t0 = time.time()
    m.run()
    t1 = time.time()

    return (t1 - t0) / (len(m.timestepper) * len(m.scenarios.combinations))


def bench(timing_func, name, func_kwargs):
    print(f'Benchmarking {name} function call ...', end='')
    t = timing_func(**func_kwargs)
    print(' done.')
    return t


if __name__ == '__main__':

    print('Starting throughput benchmarking.')

    results = {}
    for func, label, kwargs in ((time_my_func, 'Python', {'n': 10000}),
                        (time_my_c_func, 'Cython', {'n': 10000}),
                        (time_pywr_model, 'Pywr-GLPK', {'solver': 'glpk'}),
                        (time_pywr_model, 'Pywr-Pyomo', {'solver': 'pyomo'}),
                        (time_pywr_model, 'Pywr-Null', {'solver': 'null'}),
                        ):
        t = bench(func, label, kwargs)
        results[label] = t

    for label, t in results.items():
        print(f'{label}: {t:.4}s per call')

