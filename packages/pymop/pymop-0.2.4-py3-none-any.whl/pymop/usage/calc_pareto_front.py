from pymop.factory import get_problem, get_uniform_weights

# for some problems the pareto front does not need any parameters
pf = get_problem("tnk").pareto_front()
pf = get_problem("osy").pareto_front()

# for other problems the number of non-dominated points can be defined
pf = get_problem("zdt1").pareto_front(n_pareto_points=100)

# for DTLZ for example the reference direction should be provided, because the pareto front for the
# specific problem will depend on the factory for the reference lines
ref_dirs = get_uniform_weights(100, 3)
pf = get_problem("dtlz1", n_var=7, n_obj=3).pareto_front(ref_dirs)
