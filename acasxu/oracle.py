import os
import numpy as np
import nnet


np.random.seed(123456)

pi = 3.141592

COC          = 0
WEAK_LEFT    = 1
WEAK_RIGHT   = 2
STRONG_LEFT  = 3
STRONG_RIGHT = 4


def test_property_01(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec    

    if (rho >= 55947.691 and
        v_own >= 1145 and
        v_int <= 60):
        return yvec[COC] <= 1500

    else:
        return True


def test_property_02(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec
        
    if Nx < 2:
        return None
    
    elif (rho >= 55947.691 and
          v_own >= 1145 and
          v_int <= 60):
        return np.argmax(yvec) != COC
    
    else:
        return True


def test_property_03(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec
        
    if Nx == 1 and Ny in [7, 8, 9]:
        return None

    elif (1500 <= rho <= 1800 and
          -0.06 <= theta <= 0.06 and
          psi >= 3.10 and
          v_own >= 980 and
          v_int >= 960):
        return np.argmin(yvec) != COC

    else:
        return True


def test_property_04(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec
        
    if Nx == 1 and Ny in [7, 8, 9]:
        return None
    
    elif (1500 <= rho <= 1800 and
          -0.06 <= theta <= 0.06 and
          psi == 0 and
          v_own >= 1000 and
          700 <= v_int <= 800):
        return np.argmin(yvec) != COC
    
    else:
        return True

        
def test_property_05(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec
        
    if Nx == 1 or Ny != 1:
        return None
    
    elif (250 <= rho <= 400 and
          0.2 <= theta <= 0.4 and
          -pi <= psi <= -pi + 0.005 and
          100 <= v_own <= 400 and
          0 <= v_int <= 400):
        return np.argmin(yvec) == STRONG_RIGHT
    
    else:
        return True


def test_property_06(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec
        
    if Nx != 1 or Ny != 1:
        return None
    
    elif (12000 <= rho <= 62000 and
          (0.7 <= theta <= pi or -pi <= theta <= -0.7) and
          -pi <= psi <= -pi + 0.005 and
          100 <= v_own <= 1200 and
          0 <= v_int <= 1200):
        return np.argmin(yvec) == COC
    else:
        return True


def test_property_07(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec
        
    if Nx != 1 or Ny != 9:
        return None

    elif (0 <= rho <= 60760 and
          -pi <= theta <= pi and
          -pi <= psi <= pi and
          100 <= v_own <= 1200 and
          0 <= v_int <= 1200):
        return np.argmin(yvec) not in [STRONG_RIGHT, STRONG_LEFT]
    
    else:
        return True


def test_property_08(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec
        
    if Nx != 2 or Ny != 9:
        return None
        
    elif(0 <= rho <= 60760 and
         -pi <= theta <= -0.75 * pi and
         -0.1 <= psi <= 0.1 and
         600 <= v_own <= 1200 and
         600 <= v_int <= 1200):
        return np.argmin(yvec) in [WEAK_LEFT, COC]
    
    else:
        return True


def test_property_09(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec
        
    if Nx != 3 or Ny != 3:
        return None

    elif (2000 <= rho <= 7000 and
          -0.4 <= theta <= -0.14 and
          -pi <= psi <= -pi + 0.01 and
          100 <= v_own <= 150 and
          0 <= v_int <= 150):
        return np.argmin(yvec) == STRONG_LEFT
    else:
        return True


def test_property_10(Nx, Ny, xvec, yvec):
    rho, theta, psi, v_own, v_int = xvec
        
    if Nx != 4 or Ny != 5:
        return None
    
    elif (36000 <= rho <= 60760 and
          0.7 <= theta <= pi and
          -pi <= psi <= -pi + 0.01 and
          900 <= v_own <= 1200 and
          600 <= v_int <= 1200):
        return np.argmin(yvec) == COC
    else:
        return True


def test_properties(Nx, Ny, xvec, yvec):
    return (test_property_01(Nx, Ny, xvec, yvec) and
            test_property_02(Nx, Ny, xvec, yvec) and
            test_property_03(Nx, Ny, xvec, yvec) and
            test_property_04(Nx, Ny, xvec, yvec) and
            test_property_05(Nx, Ny, xvec, yvec) and
            test_property_06(Nx, Ny, xvec, yvec) and
            test_property_07(Nx, Ny, xvec, yvec) and
            test_property_08(Nx, Ny, xvec, yvec) and
            test_property_09(Nx, Ny, xvec, yvec) and
            test_property_10(Nx, Ny, xvec, yvec))


def mk_samples(Nx, Ny, nb_samples, rect=False):
    X = np.ndarray(shape=(nb_samples, 5))
    Y = np.ndarray(shape=(nb_samples, 5))
    ind = 0

    filename = '%s/nnet/ACASXU_run2a_%d_%d_batch_2000.nnet' % (
        os.path.dirname(__file__) or '.', Nx, Ny
    )
    nn = nnet.NeuralNetwork(filename, True, True)

    X = np.random.uniform(nn.input_min, nn.input_max,
                          [nb_samples, nn.output_dims])

    Y = np.zeros(nb_samples)

    ind = 0
    while ind < nb_samples:
        outputs = nn.evaluate(X[ind])
        if test_properties(Nx, Ny, X[ind], outputs) is False:
            continue

        Y[ind] = np.argmin(outputs)
        if rect:
            rho, theta, psi, v_own, v_int = X[ind]
            X[ind][0] = rho * np.cos(theta)
            X[ind][1] = rho * np.sin(theta)

        ind += 1

    # ensure all labels are present in data
    s = set(Y)
    for lbl in range(5):
        if lbl not in s:
            Y[lbl] = lbl
            
    return X, Y

