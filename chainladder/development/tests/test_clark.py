import numpy as np
from chainladder.utils.cupy import cp
import chainladder as cl
from rpy2.robjects.packages import importr
from rpy2.robjects import r

CL = importr('ChainLadder')
genins = cl.load_sample('genins')

def test_clarkldf():
    model = cl.ClarkLDF().fit(genins)
    df = r('ClarkLDF(GenIns)').rx('THETAG')
    r_omega = df[0][0]
    r_theta = df[0][1]
    assert abs(model.omega_.iloc[0,0] - r_omega) < 1e-2
    assert abs(model.theta_.iloc[0,0]/12 - r_theta) < 1e-2


def test_clarkldf_weibull():
    model = cl.ClarkLDF(growth='weibull').fit(genins)
    df = r('ClarkLDF(GenIns, G="weibull")').rx('THETAG')
    r_omega = df[0][0]
    r_theta = df[0][1]
    assert abs(model.omega_.iloc[0,0] - r_omega) < 1e-2
    assert abs(model.theta_.iloc[0,0]/12 - r_theta) < 1e-2

def test_clarkcapecod():
    df = r('ClarkCapeCod(GenIns, Premium=10000000+400000*0:9)')
    r_omega = df.rx('THETAG')[0][0]
    r_theta = df.rx('THETAG')[0][1]
    r_elr = df.rx('ELR')[0][0]
    premium = genins.latest_diagonal*0+1
    premium.values = (np.arange(10)*400000+10000000)[None, None, :, None]
    model = cl.ClarkLDF().fit(genins, sample_weight=premium)
    assert abs(model.omega_.iloc[0,0] - r_omega) < 1e-2
    assert abs(model.theta_.iloc[0,0]/12 - r_theta) < 1e-2
    assert abs(model.elr_.iloc[0,0] - r_elr) < 1e-2

def test_clarkcapcod_weibull():
    df = r('ClarkCapeCod(GenIns, Premium=10000000+400000*0:9, G="weibull")')
    r_omega = df.rx('THETAG')[0][0]
    r_theta = df.rx('THETAG')[0][1]
    r_elr = df.rx('ELR')[0][0]
    premium = genins.latest_diagonal*0+1
    premium.values = (np.arange(10)*400000+10000000)[None, None, :, None]
    model = cl.ClarkLDF(growth="weibull").fit(genins, sample_weight=premium)
    assert abs(model.omega_.iloc[0,0] - r_omega) < 1e-2
    assert abs(model.theta_.iloc[0,0]/12 - r_theta) < 1e-2
    assert abs(model.elr_.iloc[0,0] - r_elr) < 1e-2
