"""Plotting functions."""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.ticker import LogLocator
from matplotlib.ticker import MaxNLocator

from scipy.optimize import OptimizeResult
from ProcessOptimizer import expected_minimum

def plot_convergence(*args, **kwargs):
    """Plot one or several convergence traces.

    Parameters
    ----------
    * `args[i]` [`OptimizeResult`, list of `OptimizeResult`, or tuple]:
        The result(s) for which to plot the convergence trace.

        - if `OptimizeResult`, then draw the corresponding single trace;
        - if list of `OptimizeResult`, then draw the corresponding convergence
          traces in transparency, along with the average convergence trace;
        - if tuple, then `args[i][0]` should be a string label and `args[i][1]`
          an `OptimizeResult` or a list of `OptimizeResult`.

    * `ax` [`Axes`, optional]:
        The matplotlib axes on which to draw the plot, or `None` to create
        a new one.

    * `true_minimum` [float, optional]:
        The true minimum value of the function, if known.

    * `yscale` [None or string, optional]:
        The scale for the y-axis.

    Returns
    -------
    * `ax`: [`Axes`]:
        The matplotlib axes.
    """
    # <3 legacy python
    ax = kwargs.get("ax", None)
    true_minimum = kwargs.get("true_minimum", None)
    yscale = kwargs.get("yscale", None)

    if ax is None:
        ax = plt.gca()

    ax.set_title("Convergence plot")
    ax.set_xlabel("Number of calls $n$")
    ax.set_ylabel(r"$\min f(x)$ after $n$ calls")
    ax.grid()

    if yscale is not None:
        ax.set_yscale(yscale)

    colors = cm.viridis(np.linspace(0.25, 1.0, len(args)))

    for results, color in zip(args, colors):
        if isinstance(results, tuple):
            name, results = results
        else:
            name = None

        if isinstance(results, OptimizeResult):
            n_calls = len(results.x_iters)
            mins = [np.min(results.func_vals[:i])
                    for i in range(1, n_calls + 1)]
            ax.plot(range(1, n_calls + 1), mins, c=color,
                    marker=".", markersize=12, lw=2, label=name)

        elif isinstance(results, list):
            n_calls = len(results[0].x_iters)
            iterations = range(1, n_calls + 1)
            mins = [[np.min(r.func_vals[:i]) for i in iterations]
                    for r in results]

            for m in mins:
                ax.plot(iterations, m, c=color, alpha=0.2)

            ax.plot(iterations, np.mean(mins, axis=0), c=color,
                    marker=".", markersize=12, lw=2, label=name)

    if true_minimum:
        ax.axhline(true_minimum, linestyle="--",
                   color="r", lw=1,
                   label="True minimum")

    if true_minimum or name:
        ax.legend(loc="best")

    return ax


def plot_regret(*args, **kwargs):
    """Plot one or several cumulative regret traces.

    Parameters
    ----------
    * `args[i]` [`OptimizeResult`, list of `OptimizeResult`, or tuple]:
        The result(s) for which to plot the cumulative regret trace.

        - if `OptimizeResult`, then draw the corresponding single trace;
        - if list of `OptimizeResult`, then draw the corresponding cumulative
        regret traces in transparency, along with the average cumulative regret
        trace;
        - if tuple, then `args[i][0]` should be a string label and `args[i][1]`
          an `OptimizeResult` or a list of `OptimizeResult`.

    * `ax` [`Axes`, optional]:
        The matplotlib axes on which to draw the plot, or `None` to create
        a new one.

    * `true_minimum` [float, optional]:
        The true minimum value of the function, if known.

    * `yscale` [None or string, optional]:
        The scale for the y-axis.

    Returns
    -------
    * `ax`: [`Axes`]:
        The matplotlib axes.
    """
    # <3 legacy python
    ax = kwargs.get("ax", None)
    true_minimum = kwargs.get("true_minimum", None)
    yscale = kwargs.get("yscale", None)

    if ax is None:
        ax = plt.gca()

    ax.set_title("Cumulative regret plot")
    ax.set_xlabel("Number of calls $n$")
    ax.set_ylabel(r"$\sum_{i=0}^n(f(x_i) - optimum)$ after $n$ calls")
    ax.grid()

    if yscale is not None:
        ax.set_yscale(yscale)

    colors = cm.viridis(np.linspace(0.25, 1.0, len(args)))

    if true_minimum is None:
        results = []
        for res in args:
            if isinstance(res, tuple):
                res = res[1]

            if isinstance(res, OptimizeResult):
                results.append(res)
            elif isinstance(res, list):
                results.extend(res)
        true_minimum = np.min([np.min(r.func_vals) for r in results])

    for results, color in zip(args, colors):
        if isinstance(results, tuple):
            name, results = results
        else:
            name = None

        if isinstance(results, OptimizeResult):
            n_calls = len(results.x_iters)
            regrets = [np.sum(results.func_vals[:i] - true_minimum)
                       for i in range(1, n_calls + 1)]
            ax.plot(range(1, n_calls + 1), regrets, c=color,
                    marker=".", markersize=12, lw=2, label=name)

        elif isinstance(results, list):
            n_calls = len(results[0].x_iters)
            iterations = range(1, n_calls + 1)
            regrets = [[np.sum(r.func_vals[:i] - true_minimum) for i in
                        iterations] for r in results]

            for cr in regrets:
                ax.plot(iterations, cr, c=color, alpha=0.2)

            ax.plot(iterations, np.mean(regrets, axis=0), c=color,
                    marker=".", markersize=12, lw=2, label=name)

    if name:
        ax.legend(loc="best")

    return ax


def _format_scatter_plot_axes(ax, space, ylabel, dim_labels=None):
    # Work out min, max of y axis for the diagonal so we can adjust
    # them all to the same value
    diagonal_ylim = (np.min([ax[i, i].get_ylim()[0]
                             for i in range(space.n_dims)]),
                     np.max([ax[i, i].get_ylim()[1]
                             for i in range(space.n_dims)]))

    if dim_labels is None:
        dim_labels = ["$X_{%i}$" % i if d.name is None else d.name
                      for i, d in enumerate(space.dimensions)]

    # Deal with formatting of the axes
    for i in range(space.n_dims):  # rows
        for j in range(space.n_dims):  # columns
            ax_ = ax[i, j]

            if j > i:
                ax_.axis("off")

            # off-diagonal axis
            if i != j:
                # plots on the diagonal are special, like Texas. They have
                # their own range so do not mess with them.
                ax_.set_ylim(*space.dimensions[i].bounds)
                ax_.set_xlim(*space.dimensions[j].bounds)
                if j > 0:
                    ax_.set_yticklabels([])
                else:
                    ax_.set_ylabel(dim_labels[i])

                # for all rows except ...
                if i < space.n_dims - 1:
                    ax_.set_xticklabels([])
                # ... the bottom row
                else:
                    [l.set_rotation(45) for l in ax_.get_xticklabels()]
                    ax_.set_xlabel(dim_labels[j])

                # configure plot for linear vs log-scale
                priors = (space.dimensions[j].prior, space.dimensions[i].prior)
                scale_setters = (ax_.set_xscale, ax_.set_yscale)
                loc_setters = (ax_.xaxis.set_major_locator,
                               ax_.yaxis.set_major_locator)
                for set_major_locator, set_scale, prior in zip(
                        loc_setters, scale_setters, priors):
                    if prior == 'log-uniform':
                        set_scale('log')
                    else:
                        set_major_locator(MaxNLocator(6, prune='both'))

            else:
                ax_.set_ylim(*diagonal_ylim)
                ax_.yaxis.tick_right()
                ax_.yaxis.set_label_position('right')
                ax_.yaxis.set_ticks_position('both')
                ax_.set_ylabel(ylabel)

                ax_.xaxis.tick_top()
                ax_.xaxis.set_label_position('top')
                ax_.set_xlabel(dim_labels[j])

                if space.dimensions[i].prior == 'log-uniform':
                    ax_.set_xscale('log')
                else:
                    ax_.xaxis.set_major_locator(MaxNLocator(6, prune='both'))

    return ax


def partial_dependence(space, model, i, j=None, sample_points=None,
                       n_samples=250, n_points=40):
    """Calculate the partial dependence for dimensions `i` and `j` with
    respect to the objective value, as approximated by `model`.

    The partial dependence plot shows how the value of the dimensions
    `i` and `j` influence the `model` predictions after "averaging out"
    the influence of all other dimensions.

    Parameters
    ----------
    * `space` [`Space`]
        The parameter space over which the minimization was performed.

    * `model`
        Surrogate model for the objective function.

    * `i` [int]
        The first dimension for which to calculate the partial dependence.

    * `j` [int, default=None]
        The second dimension for which to calculate the partial dependence.
        To calculate the 1D partial dependence on `i` alone set `j=None`.

    * `sample_points` [np.array, shape=(n_points, n_dims), default=None]
        Randomly sampled and transformed points to use when averaging
        the model function at each of the `n_points`.

    * `n_samples` [int, default=100]
        Number of random samples to use for averaging the model function
        at each of the `n_points`. Only used when `sample_points=None`.

    * `n_points` [int, default=40]
        Number of points at which to evaluate the partial dependence
        along each dimension `i` and `j`.

    Returns
    -------
    For 1D partial dependence:

    * `xi`: [np.array]:
        The points at which the partial dependence was evaluated.

    * `yi`: [np.array]:
        The value of the model at each point `xi`.

    For 2D partial dependence:

    * `xi`: [np.array, shape=n_points]:
        The points at which the partial dependence was evaluated.
    * `yi`: [np.array, shape=n_points]:
        The points at which the partial dependence was evaluated.
    * `zi`: [np.array, shape=(n_points, n_points)]:
        The value of the model at each point `(xi, yi)`.
    """
    if sample_points is None:
        sample_points = space.transform(space.rvs(n_samples=n_samples))

    if j is None:
        bounds = space.dimensions[i].bounds
        # XXX use linspace(*bounds, n_points) after python2 support ends
        xi = np.linspace(bounds[0], bounds[1], n_points)
        xi_transformed = space.dimensions[i].transform(xi)

        yi = []
        for x_ in xi_transformed:
            rvs_ = np.array(sample_points)
            rvs_[:, i] = x_
            yi.append(np.mean(model.predict(rvs_)))

        return xi, yi

    else:
        # XXX use linspace(*bounds, n_points) after python2 support ends
        bounds = space.dimensions[j].bounds
        xi = np.linspace(bounds[0], bounds[1], n_points)
        xi_transformed = space.dimensions[j].transform(xi)

        bounds = space.dimensions[i].bounds
        yi = np.linspace(bounds[0], bounds[1], n_points)
        yi_transformed = space.dimensions[i].transform(yi)

        zi = []
        for x_ in xi_transformed:
            row = []
            for y_ in yi_transformed:
                rvs_ = np.array(sample_points)
                rvs_[:, (j, i)] = (x_, y_)
                row.append(np.mean(model.predict(rvs_)))
            zi.append(row)

        return xi, yi, np.array(zi).T

def x_dependence(space, model, x, i, j=None, n_points=40):
    """Calculate the dependence for dimensions `i` and `j` with
    respect to the objective value, as approximated by `model`.

    The dependence plot shows how the value of the dimensions
    `i` and `j` influence the `model` predictions when all other
    parameter values are set as constants defined by the argument 'x'.

    Parameters
    ----------
    * `space` [`Space`]
        The parameter space over which the minimization was performed.

    * `model`
        Surrogate model for the objective function.

    * `x` [`list`]
        The values to be used for all parameters other than i, and j if j is defined.

    * `i` [int]
        The first dimension for which to calculate the partial dependence.

    * `j` [int, default=None]
        The second dimension for which to calculate the partial dependence.
        To calculate the 1D partial dependence on `i` alone set `j=None`.

    * `n_points` [int, default=40]
        Number of points at which to evaluate the partial dependence
        along each dimension `i` and `j`.

    Returns
    -------
    For 1D dependence:

    * `xi`: [np.array]:
        The points at which the dependence was evaluated.

    * `yi`: [np.array]:
        The value of the model at each point `xi`.

    For 2D dependence:

    * `xi`: [np.array, shape=n_points]:
        The points at which the dependence was evaluated.
    * `yi`: [np.array, shape=n_points]:
        The points at which the dependence was evaluated.
    * `zi`: [np.array, shape=(n_points, n_points)]:
        The value of the model at each point `(xi, yi)`.
    """

    assert model.n_features_ == len(x), 'Number of defined parameters must be equal to number of features'
    if j is None: # 1d plot
        bounds = space.dimensions[i].bounds
        # XXX use linspace(*bounds, n_points) after python2 support ends
        xi = np.linspace(bounds[0], bounds[1], n_points)
        xi_transformed = space.dimensions[i].transform(xi) # The values for parameter i for which 
            #predictions should be made

        yi = np.zeros(n_points) # preallocating array
        for ii in range(n_points): # Loop through all values for parameter 'i'
            rvs_ = np.array(x).reshape(1,-1) # Create a 1d array with the values of all parameters
            rvs_[0,i] = xi_transformed[ii] # Replace parameter 'i'
            yi[ii] = model.predict(rvs_) # Predict using surogate function
        return xi, yi

    else: # 2d plot
        # Works same way as above (1d plot) except both parameter 'i' and 'j' are the ones being varied
        # XXX use linspace(*bounds, n_points) after python2 support ends
        bounds = space.dimensions[j].bounds
        xi = np.linspace(bounds[0], bounds[1], n_points)
        xi_transformed = space.dimensions[j].transform(xi)

        bounds = space.dimensions[i].bounds
        yi = np.linspace(bounds[0], bounds[1], n_points)
        yi_transformed = space.dimensions[i].transform(yi)

        zi=np.zeros([n_points,n_points])
        for ii in range(n_points):
            for jj in range(n_points):
                rvs_ = np.array(x).reshape(1,-1)
                rvs_[0, (j, i)] = (xi_transformed[ii], yi_transformed[jj])
                zi[jj,ii] = model.predict(rvs_)

        return xi, yi, zi

def plot_objective(result, levels=10, n_points=40, n_samples=250, size=2,
                   zscale='linear', dimensions=None, usepartialdependence=True, pars='result', expected_minimum_samples = None):
    """Pairwise dependence plot of the objective function.

    The diagonal shows the dependence for dimension `i` with
    respect to the objective function. The off-diagonal shows the
    dependence for dimensions `i` and `j` with
    respect to the objective function. The objective function is
    approximated by `result.model.`

    Pairwise scatter plots of the points at which the objective
    function was directly evaluated are shown on the off-diagonal.
    A red point can indicate a type of minimum defined by "pars".
    If "pars" is a list, a red point just indicates the values in this list.

    Note: search spaces that contain `Categorical` dimensions are
          currently not supported by this function.

    Parameters
    ----------
    * `result` [`OptimizeResult`]
        The result for which to create the scatter plot matrix.

    * `levels` [int, default=10]
        Number of levels to draw on the contour plot, passed directly
        to `plt.contour()`.

    * `n_points` [int, default=40]
        Number of points at which to evaluate the partial dependence
        along each dimension.

    * `n_samples` [int, default=250]
        Number of random samples to use for averaging the model function
        at each of the `n_points`.

    * `size` [float, default=2]
        Height (in inches) of each facet.

    * `zscale` [str, default='linear']
        Scale to use for the z axis of the contour plots. Either 'linear'
        or 'log'.

    * `dimensions` [list of str, default=None] Labels of the dimension
        variables. `None` defaults to `space.dimensions[i].name`, or
        if also `None` to `['X_0', 'X_1', ..]`.

    * `usepartialdependence` [bool, default=false] Wether to use partial
        dependence or not when calculating dependence. If false plot_objective
        will use the x_dependence function instead of partial_dependence function

    * `pars` [str, default = 'result' or list of floats] Defines the values for the red
        points in the plots, and if partialdependence is false, this argument also 
        defines what the values of the other parameters should be when calculating dependence plots.
        Valid strings:  'result' - Use best observed parameters
                        'expected_minimum' - Parameters that gives the best minimum
                            Calculated using scipy's minimize method
                        'expected_minimum_random' - Parameters that gives the best minimum
                            when using naive random sampling
    * `expected_minimum_samples` [float, default = None] Determines how many points should be evaluated
        to find the minimum when using 'expected_minimum' or 'expected_minimum_random'
        
    Returns
    -------
    * `ax`: [`Axes`]:
        The matplotlib axes.
    """
    space = result.space
    samples = np.asarray(result.x_iters)
    rvs_transformed = space.transform(space.rvs(n_samples=n_samples))

    if zscale == 'log':
        locator = LogLocator()
    elif zscale == 'linear':
        locator = None
    else:
        raise ValueError("Valid values for zscale are 'linear' and 'log',"
                         " not '%s'." % zscale)

    fig, ax = plt.subplots(space.n_dims, space.n_dims,
                           figsize=(size * space.n_dims, size * space.n_dims))

    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95,
                        hspace=0.1, wspace=0.1)
    # Here we define the parameters for which to plot the red dot (2d plot) and the red dotted line (1d plot).
    # These same parameters will be used for evaluating the plots when not using partial dependence.
    if isinstance(pars,str):
        if pars == 'result':
            # Using the best observed result
            x_eval = result.x
        elif pars == 'expected_minimum':
            # Do a gradient based minimum search using scipys own minimizer
            if expected_minimum_samples: # If a value for expected_minimum_samples has been parsed
                x_eval,_ = expected_minimum(result, n_random_starts=expected_minimum_samples, random_state=None)
            else: # Use standard of 20 random starting points
                x_eval,_ = expected_minimum(result, n_random_starts=20, random_state=None)
        elif pars == 'expected_minimum_random':
            # Do a minimum search by evaluating the function with n_samples sample values
            if expected_minimum_samples: # If a value for expected_minimum_samples has been parsed
                x_eval = expected_min_random_sampling(result.models[-1], space, n_samples=expected_minimum_samples)
            else: # Use standard of 10^n_parameters. Note this becomes very slow for many parameters
                x_eval = expected_min_random_sampling(result.models[-1], space, n_samples=10**len(result.x))
        else:
            raise ValueError('Argument ´pars´ must be a valid string (´result´)')
    elif isinstance(pars,list):
        assert len(pars) == len(result.x) , 'Argument ´pars´ of type list must have same length as number of features'
        # Using defined x_values
        x_eval = pars
    else:
        raise ValueError('Argument ´pars´ must be a string or a list')
    for i in range(space.n_dims):
        for j in range(space.n_dims):
            if i == j:
                if usepartialdependence:
                    xi, yi = partial_dependence(space, result.models[-1], i,
                                            j=None,
                                            sample_points=rvs_transformed,
                                            n_points=n_points)
                else:
                    xi, yi = x_dependence(space, result.models[-1], x_eval, i, j=None, n_points=n_points)
                ax[i, i].plot(xi, yi)
                ax[i, i].axvline(x_eval[i], linestyle="--", color="r", lw=1)

            # lower triangle
            elif i > j:
                if usepartialdependence:
                    xi, yi, zi = partial_dependence(space, result.models[-1],
                                                i, j,
                                                rvs_transformed, n_points)
                else:
                    xi, yi, zi = x_dependence(space, result.models[-1], x_eval, i, j, n_points = n_points)
                ax[i, j].contourf(xi, yi, zi, levels,
                                locator=locator, cmap='viridis_r')
                ax[i, j].scatter(samples[:, j], samples[:, i],
                                c='k', s=10, lw=0.)
                ax[i, j].scatter(x_eval[j], x_eval[i],
                                c=['r'], s=20, lw=0.)

    if usepartialdependence:
        ylabel="Partial dependence"
    else:
        ylabel="Dependence"
    return _format_scatter_plot_axes(ax, space, ylabel=ylabel,
                                        dim_labels=dimensions)


def plot_evaluations(result, bins=20, dimensions=None):
    """Visualize the order in which points where sampled.

    The scatter plot matrix shows at which points in the search
    space and in which order samples were evaluated. Pairwise
    scatter plots are shown on the off-diagonal for each
    dimension of the search space. The order in which samples
    were evaluated is encoded in each point's color.
    The diagonal shows a histogram of sampled values for each
    dimension. A red point indicates the found minimum.

    Note: search spaces that contain `Categorical` dimensions are
          currently not supported by this function.

    Parameters
    ----------
    * `result` [`OptimizeResult`]
        The result for which to create the scatter plot matrix.

    * `bins` [int, bins=20]:
        Number of bins to use for histograms on the diagonal.

    * `dimensions` [list of str, default=None] Labels of the dimension
        variables. `None` defaults to `space.dimensions[i].name`, or
        if also `None` to `['X_0', 'X_1', ..]`.

    Returns
    -------
    * `ax`: [`Axes`]:
        The matplotlib axes.
    """
    space = result.space
    samples = np.asarray(result.x_iters)
    order = range(samples.shape[0])
    fig, ax = plt.subplots(space.n_dims, space.n_dims,
                           figsize=(2 * space.n_dims, 2 * space.n_dims))

    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95,
                        hspace=0.1, wspace=0.1)

    for i in range(space.n_dims):
        for j in range(space.n_dims):
            if i == j:
                if space.dimensions[j].prior == 'log-uniform':
                    low, high = space.bounds[j]
                    bins_ = np.logspace(np.log10(low), np.log10(high), bins)
                else:
                    bins_ = bins
                ax[i, i].hist(samples[:, j], bins=bins_,
                              range=space.dimensions[j].bounds)

            # lower triangle
            elif i > j:
                ax[i, j].scatter(samples[:, j], samples[:, i], c=order,
                                 s=40, lw=0., cmap='viridis')
                ax[i, j].scatter(result.x[j], result.x[i],
                                 c=['r'], s=20, lw=0.)

    return _format_scatter_plot_axes(ax, space, ylabel="Number of samples",
                                     dim_labels=dimensions)

def expected_min_random_sampling(model, space, n_samples = 100000):
    # Make model predictions using n_samples random samples
    # and return the sample_valus that results in the minimum function value

    # sample points from search space
    random_samples = space.rvs(n_samples=n_samples)
    
    # make estimations with surrogate
    y_random = model.predict(space.transform(random_samples))
    index_best_objective = np.argmin(y_random)
    min_x = random_samples[index_best_objective]
    
    return min_x