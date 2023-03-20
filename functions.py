def keplerian_orbit(t,rv0,period,K,ecc,omega,t_peri):
#   Description:
#      Computation of the keplerian radial velocity
#   Input parameters:
#      t: array of time
#      rv0: systemic radial velocity
#      period: orbital period
#      K: radial velocity semi-amplitude
#      ecc: eccentricity of the orbit
#      omega: angle of periastron
#      t_peri: time of periastron_passage
#   Output parameters:
#      rv: radial velocity array
    rv0,period,rv,ecc,omega,t_peri=params
    omega=omega*np.pi/180.0
    sinf,cosf=true_anomaly(t,period,ecc,t_peri)
    cosftrueomega=cosf*np.cos(omega)-sinf*np.sin(omega)
    rv=rv0+K*(ecc*np.cos(omega)+cosftrueomega)
    return rv

def true_anomaly(t,period,ecc,t_peri):
#   Description:
#      Computation of the true anomaly solving the Kepler
#      equations numerically. A precision of 1.EE-06 is
#      hard coded.
#   Input parameters:
#      t: array of time
#      period: orbital period
#      ecc: eccentricity of the orbit
#      t_peri: time of periastron_passage
#   Output parameters:
#      sinf: sinus of the true anomaly
#      cosf: cosinus of the true anomaly
    sinf=[]
    cosf=[]
    for i in range(len(t)):
        fmean=2.0*np.pi*(t[i]-t_peri)/period
        #Solve by Newton's method x(n+1)=x(n)-f(x(n))/f'(x(n))
        fecc=fmean
        diff=1.0
        while(diff>1.0E-6):
            fecc_0=fecc
            fecc=fecc_0-(fecc_0-ecc*np.sin(fecc_0)-fmean)/(1.0-ecc*np.cos(fecc_0))
            diff=np.abs(fecc-fecc_0)
        sinf.append(np.sqrt(1.0-ecc*ecc)*np.sin(fecc)/(1.0-ecc*np.cos(fecc)))
        cosf.append((np.cos(fecc)-ecc)/(1.0-ecc*np.cos(fecc)))
    return np.array(sinf),np.array(cosf)
