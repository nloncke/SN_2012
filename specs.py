import matplotlib.pyplot as plt
import numpy as np

def process_data(filename):
    """Converts raw data from a file into three arrays...
    """

    file_arr = np.genfromtxt(filename)

## Note to self: these are not separate arrays yet!!!  They are only
## pointers and have the same base as file_arr.  Potential source of
## confusion...
    dayarr = np.unique(file_arr[:, 0]) ## This array holds all the day
                                ## numbers in increasing order
                                ## (starting negative through zero, to
                                ## the positive
    lams = np.unique(file_arr[:, 1]) ## All the wavelengths
                                ## values, non-repeating
    specs = file_arr[:, 2].reshape((len(dayarr),len(lams))) ## All the
                                ## spectra values per day in order of
                                ## increasing wavelength
    return dayarr, lams, specs

def day_idx(day,dayarr):
    """Prints the index number of the input day in dayarr.  E.g. '-15'
    yields '5' or something like that.
    """

    idx = np.where(dayarr==day)[0][0]
    return idx


# Also, two other ways to do it:

## (y==day).tolist().index(True)

## minday = dayarr[0]
## idx_list= []
    ## for entry in dayarr:
    ## index = entry - minday
    ## index = np.array()
# return index


def plotspec(day, dayarr, lams, specs, display=True, save=False, ext='pdf'):
    """Plots flux values vs. wavelength for a specified day
    """

    # day_idx(dayarr,day)
    # idx = np.where(dayarr==day)[0][0]
    # title = 'Day ' + str(day)

    xvals = lams
    yvals = specs[day_idx(day, dayarr),:]
    title = 'Day {0:+04d}'.format(day)

    plt.plot(xvals,yvals)
    plt.xlabel(r'$\lambda$')    
    plt.ylabel(r'$f(\lambda)$')
    plt.title(title)

    if display:
        plt.show()

    if save:
        outfile = 'day{0:+04}.{1}'.format(day, ext)
        plt.savefig(outfile)
    else:
        outfile = None

    return outfile


def specplotter(dayarr, lams, specs, ext='pdf'):
    """Function factory that produces plotter_func, a function that
    takes in just the day and plots everything
    """
    def plotter_func(day):
        return plotspec(day, dayarr, lams, specs, ext)
    return plotter_func

def filespecplotter(filename, ext='pdf'):
    """Plotting function for spectra in {0}.""".format(filename)

    dayarr, lams, specs = process_data(filename)
    return specplotter(dayarr, lams, specs, ext)

