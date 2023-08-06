import autograd.numpy as anp

from pymop.problem import Problem


class Rosenbrock(Problem):
    def __init__(self, n_var=2):
        super().__init__(n_var=n_var, n_obj=1, n_constr=0, xl=-2.048, xu=2.048, type_var=anp.double)

    def _evaluate(self, x, out, *args, **kwargs):
        l = []
        for i in range(x.shape[1] - 1):
            l.append(100 * anp.square((x[:, i + 1] - anp.square(x[:, i]))) + anp.square((1 - x[:, i])))
        out["F"] = anp.sum(anp.column_stack(l), axis=1)
