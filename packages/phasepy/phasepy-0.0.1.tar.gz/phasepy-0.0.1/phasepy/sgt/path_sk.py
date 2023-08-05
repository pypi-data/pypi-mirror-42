import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import cumtrapz

def fobj_sk(inc, spath, T, mu0, ci, sqrtci, model):   
    ro = inc[:-1]
    alpha = inc[-1]
    mu = model.muad(ro, T)
    obj = np.zeros_like(inc)
    obj[:-1] = mu - (mu0 + alpha*sqrtci)
    obj[-1] = spath - sqrtci.dot(ro)
    return obj

def ten_beta0_sk(ro1, ro2, Tsat, Psat, model, n = 200, full_output = False ):
    
    if (ro1 - ro2).sum() > 0:
        ro_aux = ro1.copy()
        ro1 = ro2.copy()
        ro2 = ro_aux
    nc = model.nc
    
    #adimensionalizar variables 
    Tfactor, Pfactor, rofactor, tenfactor, zfactor = model.sgt_adim(Tsat)
    Pad = Psat*Pfactor
    ro1a = ro1*rofactor
    ro2a = ro2*rofactor
    
    cij = model.ci(Tsat)
    cij /= cij[0,0]
    ci = np.diag(cij)
    sqrtci = np.sqrt(ci)
    
    mu0 = model.muad(ro1a, Tsat)
    
    #extremos funcion de recorrido
    s0 = sqrtci.dot(ro1a)
    s1 = sqrtci.dot(ro2a)
    spath = np.linspace(s0, s1, n)
    ro = np.zeros([nc,n])
    alphas = np.zeros(n)
    ro[:,0] = ro1a
    ro[:,-1] = ro2a
    
    deltaro = ro2a - ro1a
    i = 1
    r0 = ro1a + deltaro * (spath[i]-s0)
    r0 = np.hstack([r0, 0])
    ro0 = fsolve(fobj_sk,r0,args=(spath[i], Tsat, mu0, ci, sqrtci, model))
    ro[:,i] = ro0[:-1]
    
    for i in range(1,n):
        ro0 = fsolve(fobj_sk, ro0, args=(spath[i], Tsat, mu0, ci, sqrtci, model))
        alphas[i] = ro0[-1]
        ro[:,i] = ro0[:-1]
        
    #derivadas respecto a funcion de recorrido
    drods = np.gradient(ro, spath, edge_order = 2, axis = 1)
    
    suma = np.zeros(n)
    dom = np.zeros(n)
    for k in range(n):
        for i in range(nc):
            for j in range(nc):
                suma[k] += cij[i,j]*drods[i,k]*drods[j,k]
        dom[k] = model.dOm(ro[:,k], Tsat, mu0, Pad)
    dom[0] = 0
    dom[-1] = 0
    
    integral = np.nan_to_num(np.sqrt(2*dom*suma))
    tension = np.trapz(integral, spath)
    tension *= tenfactor
    
    if full_output:
        with np.errstate(divide='ignore'):
            intz = (np.sqrt(suma/(2*dom)))
        intz[np.isinf(intz)] = 0
        z = cumtrapz(intz,spath, initial = 0)
        z /= zfactor
        ro /= rofactor
        return tension, ro, z
    
    return tension