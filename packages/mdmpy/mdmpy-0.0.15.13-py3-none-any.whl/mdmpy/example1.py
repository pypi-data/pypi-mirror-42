
import os
os.environ["PATH"] = "D:/Downloads/Software (General Use)/SUTD/Solvers/IPOPT/Ipopt64-3.12.11/bin/" + os.pathsep + os.environ["PATH"]
import csv
import math
import requests
import pandas as pd
import numpy as np
import scipy.stats as stats
import pyomo.environ as aml
import util

url = "http://pages.stern.nyu.edu/~wgreene/Text/Edition7/TableF18-2.csv"

df = pd.DataFrame(index=np.arange(0, 840), columns=np.arange(0,7))
with requests.Session() as s:
    download = s.get(url)


    cr = csv.reader(download.content.decode().splitlines())
    next(cr)
    for ix, row in enumerate(cr):
        df.loc[ix] = [int(x) for x in row]

# mdm0 = mdmpy.MDM(df,   # input dataframe
#                  0,    # the choice is index 0
#                  4,    # there are 4 possible choices
#                  [2,3] # we will use columns index 2 and 3 (3rd and 4th column, Python indices start from 0)
#                  )
# mdm0.model_init()
# mdm0.model_solve("ipopt")
# beta0 = [mdm0.m.beta[idx].value for idx in mdm0.m.beta]
# print(beta0)
# ll0 = mdm0.ll(beta0)
# print(ll0)


class MDM:
    """
    The main class of the package. This models the Marginal Distribution
    Models (MDM)
    """
    def __init__(self,
                 input_dataframe,
                 ch_id: int,
                 num_choices: int,
                 list_of_coefs,
                 input_cdf=util.exp_cdf,
                 input_pdf=util.exp_pdf):
        """"
        The class is initialised with a 2D NumPy array, which acts as a
        table in the 'wide' format in Discrete Choice Modelling.
        One set of inputs are relevant column indices, such as the choice
        index, and the coefficients that will be considered in the model
        Another input is the number of choices or alternatives each
        individual has. The data is then made into other NumPy arrays used
        in the class methods.

        Default CDF/PDF of the model is the Multinomial Logit (MNL) model,
        which is globally convex in its support. Other CDFs and PDFs will
        be supported

        This will require some other changes to allow for individual-specific
        coefficients, which will be added at a later date.
        """

        num_indiv = int(input_dataframe.shape[0]/num_choices)
        # check if numerically equivalent
        if not num_indiv == input_dataframe.shape[0]/num_choices:
            raise ValueError("""Unexpectedly, the number of columns does not divide
                                by the number of choices, as inputed.""")
        num_attr = len(list_of_coefs)
        Z = np.array(input_dataframe.iloc[:, ch_id]).reshape((num_indiv, num_choices))
        X = np.reshape(np.array(input_dataframe.iloc[:, list_of_coefs]),
                       (num_indiv, num_choices, num_attr))
        self._X = X # is indexed in the order (indiv, choice, attr)
        self._Z = Z # choice of each individual
        self._num_indiv = num_indiv  # number of individuals
        self._num_attr = num_attr # number of attributes/coefficients
        self._num_choices = num_choices # number of alternatives/choices
        self._cdf = input_cdf # sets the cdf for the model
        self._pdf = input_pdf # sets corresponding pdf (has to be inputted, not automatic)

    def ll(self, input_beta, corr_lambs=None) -> float:
        """This function gets the log-likelihood using the current beta. If
        the corresponding lambdas for each individual are given, then it will
        use those, rather than re-computing them, which saves computations"""
        loglik = 0
        for i in range(self._num_indiv):
            x_i = self._X[i]
            if corr_lambs is None:
                cor_lamb = util.find_corresponding_lambda(self._cdf, input_beta, x_i)
            else:
                cor_lamb = corr_lambs[i]
            for k, choice in enumerate(self._Z[i]):
                if choice:
                    x_ik = x_i[k]
                    f_arg_ik = cor_lamb - sum(x*y for x, y in zip(input_beta, x_ik))
                    loglik += math.log(1-self._cdf(f_arg_ik))
                else:
                    pass
        return loglik

    def __loglikexpr(self, heteroscedastic=False, lag_f=None):
        ### TODO - refactor the double summation over I and K, which is repeated
        if lag_f is None:
            lag_f=lambda arg: aml.log(1-self._cdf(arg))
        if heteroscedastic:
            return sum(sum(
                        self._Z[i][k]*self.m.alpha[k]*lag_f(
                            self.m.lambda_[i]-sum(
                                self.m.beta[l]*self._X[i][k][l] for l in self.m.L)
                                    ) for k in self.m.K) for i in self.m.I)
        else:
            return sum(sum(
                        self._Z[i][k]*lag_f(
                            self.m.lambda_[i]-sum(
                                self.m.beta[l]*self._X[i][k][l] for l in self.m.L)
                                    ) for k in self.m.K) for i in self.m.I)

    def model_init(self, heteroscedastic=False, model_seed=None):
        """"This method initializes the pyomo model as an instance
        attribute m. Values can later be taken directly from m."""
        self.m = aml.ConcreteModel()
        # Model Sets
        self.m.K = aml.Set(initialize=range(self._num_choices))
        self.m.L = aml.Set(initialize=range(self._num_attr))
        self.m.I = aml.Set(initialize=range(self._num_indiv))


        ### Model Variables ###
        # Initialize at some certain seed
        # For checking if convexity gives numerical stability
        if model_seed:
            np.random.seed(model_seed)
            numpy_stan_exp = np.random.standard_exponential
            self.m.beta = aml.Var(self.m.L, initialize=lambda _: numpy_stan_exp()) # 1 arg required for initialize
            self.m.lambda_ = aml.Var(self.m.I, initialize=lambda _: numpy_stan_exp())
            ### TODO - Delete OR add verbosity flag to determine if these should be printed
            print([self.m.beta[h].value for h in self.m.L])
            print([self.m.lambda_[g].value for g in self.m.I])
        else:
            self.m.beta = aml.Var(self.m.L)
            self.m.lambda_ = aml.Var(self.m.I)

        # Handling heteroscedascity
        if heteroscedastic:
            # known heteroscedasticity
            if isinstance(heteroscedastic, list):
                self.m.alpha = {idx:v for idx, v in enumerate(heteroscedastic)}
            # else, unknown heteroscedasticity
            else:
                self.m.alpha = aml.Var(self.m.K, domain=aml.PositiveReals)
#                 self.m.AlphaSumCons = aml.Constraint(expr=sum(self.m.alpha[k] for k in self.m.K)==num_choices)
                self.m.FixOneAlphaC = aml.Constraint(expr=self.m.alpha[0] == 1)

                def _tol_cons(model, k, ALPHA_TOL=0.3):
                    return model.alpha[k] >= ALPHA_TOL

                self.m.AlphaTol = aml.Constraint(self.m.K, rule=_tol_cons)

        # Objective Function
        ### TODO Hardcode in the other common distributions, especially
        ### Those with a region which is simultaneously reliability function
        ### convex and logconcave, which guarantees concave objective
        ### This hardcoding should simplify the algebraic expression
        ### for the solver, and hence allow to see more
        ###### Dists under consideration:
        ###### Hyperbolic secant - region: non-negative numbers AKA above median
        ###### ... distributions with suitable unbounded regions
        ###### ... satisfying tail convex+tail logconcave
        if heteroscedastic:
            if self._cdf == util.exp_cdf:
                O_expr = self.__loglikexpr(heteroscedastic=True, lag_f=lambda arg: -arg)
            else:
                O_expr = self.__loglikexpr(heteroscedastic=True)

        else:
            # Model CDF simplifications
            if self._cdf == util.exp_cdf:
                O_expr = self.__loglikexpr(lag_f=lambda arg: -arg)
            ### seems bugged ###
            if self._cdf == util.gumbel_cdf:
                O_expr = self.__loglikexpr(lag_f=lambda arg: aml.log(1-aml.exp(-aml.exp(-arg))))
            ### seems bugged ###
            else:
                O_expr = self.__loglikexpr()

        # Model Objective
        self.m.O = aml.Objective(expr=O_expr, sense=aml.maximize)

        # Lagrangian Constraints (for each individual)
        # MEM
        if heteroscedastic and self._cdf == util.exp_cdf:
            def _lag_cons(model, i):
                return sum(aml.exp(model.alpha[k]*(sum(
                    model.beta[l]*self._X[i][k][l] for l in model.L)-model.lambda_[i])) for k in model.K) <= 1
        elif self._cdf == util.exp_cdf:
            def _lag_cons(model, i):
                return sum(aml.exp(sum(
                    model.beta[l]*self._X[i][k][l] for l in model.L)-model.lambda_[i]) for k in model.K) <= 1
        ### seems bugged ###
        elif self._cdf == util.gumbel_cdf:
            def _lag_cons(model, i):
                return sum(1-aml.exp(-aml.exp(
                            (model.lambda_[i]-sum(
                                model.beta[l]*self._X[i][k][l] for l in model.L))
                                    )) for k in model.K) <= 1
        ### seems bugged ###
        else:
            def _lag_cons(model, i):
                return sum(1-self._cdf(model.lambda_[i]-sum(
                    model.beta[l]*self._X[i][k][l] for l in model.L)) for k in model.K) <= 1
        self.m.C = aml.Constraint(self.m.I, rule=_lag_cons)

        # Scale restriction - not required
        # but might help solver not get lost and diverge
        def _beta_size_cons(model, l):
            return (-20, model.beta[l], 20)
        self.m.BetaSizeCon = aml.Constraint(self.m.L, rule=_beta_size_cons)

        def _lamb_size_cons(model, i):
            return (-100, model.lambda_[i], 100)
        self.m.LambSizeCon = aml.Constraint(self.m.I, rule=_lamb_size_cons)

    def add_conv(self, conv_min: float = 0):
        """This function restricts the argument of the CDF and PDF such
        that they are above a set limit, commonly zero. This restricts
        the domain to a region whereby the 1-CDF is convex."""
        def _con_cons(model, i, k):
            return model.lambda_[i]-sum(model.beta[l]*self._X[i][k][l] for l in model.L) >= conv_min
        self.m.convcon = aml.Constraint(self.m.I, self.m.K, rule=_con_cons)

    def model_solve(self, solver, solver_exec_location=None, tee: bool = False, **kwargs):
        """Start a solver to solve the model"""
        self.solver = aml.SolverFactory(solver, executable=solver_exec_location)
        self.solver.options.update(kwargs)
        return self.solver.solve(self.m, tee=tee)

    def _calc_grad_lambda_beta(self, beta_iterate, corr_lambs):
        f_arg_input = corr_lambs - np.dot(self._X, beta_iterate).T
        f_lambda = self._pdf(f_arg_input)
        numerator = np.sum((self._X.T*f_lambda), 1) # sum 1 means sum over all choices
        denominator = np.sum(f_lambda, 0)
        return (numerator/denominator).T

    def _calc_grad_ll_beta(self, beta_iterate):
        """This function is the part where the gradient is actually calculated."""
        corr_lambs = np.empty(self._num_indiv)
        for i in range(self._num_indiv):
            corr_lambs[i] = util.find_corresponding_lambda(self._cdf, beta_iterate, self._X[i])
        grad_mat = ((((self._X - self._calc_grad_lambda_beta(beta_iterate, corr_lambs)[:, np.newaxis, :]) *
                        ((self._pdf(corr_lambs - np.dot(self._X, beta_iterate).T)).T)[:, :, np.newaxis]) /
                            (1 - (self._cdf(corr_lambs - np.dot(self._X, beta_iterate).T)).T)[:, :, np.newaxis]) *
                                self._Z[:, :, np.newaxis])
        return grad_mat.sum((0, 1)), corr_lambs

    def grad_desc(self,
                  initial_beta,
                  max_steps: int = 50,
                  grad_mult=1,
                  eps: float = 10**-7,
                  verbosity=0):
        """Starts a gradient-descent based method using the CDF and PDF.
        Requires a starting beta iterate.

        TODO : to add f_arg_min which will be pass onto the gradient
        calculators and use grad_lambda_beta to move towards
        a convex region, which is above f_arg_min
        """
        last_log_lik = self.ll(initial_beta)
        beta_iterate = initial_beta #initialize
        for num_step in range(max_steps):
            grad, corr_lambs = self._calc_grad_ll_beta(beta_iterate)
            print(grad)
            beta_iterate = beta_iterate + grad_mult*(grad/(num_step+1))
            # once no more big gains are made, stop
            cur_ll = self.ll(beta_iterate, corr_lambs=corr_lambs)
            if verbosity == 1:
                print(cur_ll)
            if math.isnan(cur_ll):
                print("An Error occurred in calculating Loglikelihood")
                break # no point continuing when LL has is nan
            if abs(last_log_lik-cur_ll) < eps:
                break
            last_log_lik = cur_ll
        return beta_iterate


mdm2 = MDM(df,   # input dataframe
                 0,    # the choice is index 0
                 4,    # there are 4 possible choices
                 [1, 2, 3, 4], # we will use columns index 2 and 3 (3rd and 4th column, Python indices start from 0)
                 input_cdf=util.gumbel_cdf)
mdm2.model_init()
mdm2.add_conv()
mdm2.model_solve("ipopt")
beta2 = [mdm2.m.beta[idx].value for idx in mdm2.m.beta]
print(beta2)
ll2 = mdm2.ll(beta2)
print(ll2)

mdm1 = MDM(df,   # input dataframe
                 0,    # the choice is index 0
                 4,    # there are 4 possible choices
                 [1, 2, 3, 4] # now instead we use all 4 choice-specific-data columns
                 )
mdm1._cdf = stats.expon.cdf
mdm1._pdf = stats.expon.pdf
mdm1.grad_desc([0.01, 0.01, 0.01, 0.01],
               grad_mult=0.01,
               verbosity=1)
# mdm1.model_init()
# mdm1.model_solve("ipopt")
# beta1 = [mdm1.m.beta[idx].value for idx in mdm1.m.beta]
# print(beta1)
# ll1 = mdm1.ll(beta1)
# print(ll1)