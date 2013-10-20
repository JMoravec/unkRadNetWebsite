import os
import sys

# ensure pyeq2 can be imported
if os.path.join(sys.path[0][:sys.path[0].rfind(os.sep)], '../..') not in sys.\
        path:
    sys.path.append(os.path.join(sys.path[0][:sys.path[0].rfind(os.sep)],
                                 '../..'))
if os.path.join(sys.path[0][:sys.path[0].rfind(os.sep)],
                'radnet/Data/') not in sys.path:
    sys.path.append(os.path.join(sys.path[0][:sys.path[0].rfind(os.sep)],
                                 'radnet/Data'))
import pyeq2
from Data.models import *


def fitToCurve(filterID):
    print filterID
    equation = pyeq2.Models_2D.Exponential.DoubleExponential()

    filterID = int(filterID)

    #get activity numbers from database
    mainFilter = Filter.objects.get(id=filterID)
    print mainFilter
    activity = Activity.objects.filter(Filter=filterID)

    # What this section does is reads the data from the file
    # given from the initial argument and formats it so the zunzun.com
    # code can read it.
    # We need two separate Strings so we can have two equations found.
    alpha = 'X\tY\n'
    beta = 'X\tY\n'

    # set the stings with the data points from the database
    for dataPoint in activity:
        alpha = alpha + str(dataPoint.deltaT) + "\t" + \
            str(dataPoint.alphaAct) + "\n"
        beta = beta + str(dataPoint.deltaT) + "\t" + \
            str(dataPoint.betaAct) + "\n"

    #fit plot to alpha data
    #get coefficients from zunzun
    data = alpha
    pyeq2.dataConvertorService().ConvertAndSortColumnarASCII(data,
                                                             equation, False)
    equation.Solve()

    #change the coefficients to float type
    alphaInitial1 = float(equation.solvedCoefficients[0])
    alphaLam1 = float(equation.solvedCoefficients[1])
    alphaInitial2 = float(equation.solvedCoefficients[2])
    alphaLam2 = float(equation.solvedCoefficients[3])

    # put data into database
    newCurveA = AlphaCurve()
    newCurveA.Filter = mainFilter
    newCurveA.alpha1 = alphaInitial1
    newCurveA.alpha2 = alphaInitial2
    newCurveA.alpha1Lambda = alphaLam1
    newCurveA.alpha2Lambda = alphaLam2

    #try to save
    newCurveA.save()

    #fit plot to beta data
    data = beta
    pyeq2.dataConvertorService().ConvertAndSortColumnarASCII(data,
                                                             equation, False)
    equation.Solve()

    betaInitial1 = float(equation.solvedCoefficients[0])
    betaLam1 = float(equation.solvedCoefficients[1])
    betaInitial2 = float(equation.solvedCoefficients[2])
    betaLam2 = float(equation.solvedCoefficients[3])

    newCurveB = BetaCurve()
    newCurveB.Filter = mainFilter
    newCurveB.beta1 = betaInitial1
    newCurveB.beta2 = betaInitial2
    newCurveB.beta1Lambda = betaLam1
    newCurveB.beta2Lambda = betaLam2
    newCurveB.save()
