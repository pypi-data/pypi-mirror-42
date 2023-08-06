import numpy as np


def estimate_explicite_matrix(nk, dt_3D, alp, mu, ht, M):
    """ Definition of explicit matrix for diffusion process
    Args:
      nk    : Number of sigma vertical layers
      dt_3D : Timestep
      alp   : Numerical coefficient for diffusion scheme
      mu    : Vertical turbulence coefficient
      ht    : Water column heigth
      M     : Model class (contains sigma definition)
    return:
        explicit matrix for diffusion process
    """
    dz_u = M.dsig_u
    dz_w = M.dsig_w
    az = np.zeros((nk-1))
    bz = np.ones((nk))
    cz = np.zeros((nk-1))

    az[1:] = (1-alp)*dt_3D*mu/(dz_u[2:]*dz_w[1:-1]*ht**2)
    cz[1:] = (1-alp)*dt_3D*mu/(dz_u[1:-1]*dz_w[1:-1]*ht**2)
    bz[2:-1] = 1-(az[1:-1] + cz[1:-1])
    bz[1] = 1-dt_3D*(1-alp)*mu/(dz_u[1]*dz_w[1]*ht**2)
    bz[M.kmax] = 1-dt_3D*(1-alp)*mu/(dz_u[M.kmax]*dz_w[M.kmax-1]*ht**2)

    B_exp = np.diag(az, -1) + np.diag(bz, 0) + np.diag(cz, 1)

    return B_exp


def estimate_implicite_matrix(nk, dt_3D, alp, mu, ht, M):
    """ Definition of implicit matrix for diffusion process
    Args:
      nk    : Number of sigma vertical layers
      dt_3D : Timestep
      alp   : Numerical coefficient for diffusion scheme
      mu    : Vertical turbulence coefficient
      ht    : Water column heigth
      M     : Model class (contains sigma definition)
    return:
        implicit matrix for diffusion process
    """
    dz_u = M.dsig_u
    dz_w = M.dsig_w

    ####
    az = np.zeros((nk-1))
    bz = np.ones((nk))
    cz = np.zeros((nk-1))
    ####
    az[1:] = (-alp)*dt_3D*mu/(dz_u[2:]*dz_w[1:-1]*ht**2)
    cz[1:] = (-alp)*dt_3D*mu/(dz_u[1:-1]*dz_w[1:-1]*ht**2)
    bz[2:-1] = 1-(az[1:-1] + cz[1:-1])
    bz[1] = 1-dt_3D*(-alp)*mu/(dz_u[1]*dz_w[1]*ht**2)
    bz[M.kmax] = 1-dt_3D*(-alp)*mu/(dz_u[M.kmax]*dz_w[M.kmax-1]*ht**2)

    A_imp = np.diag(az, -1) + np.diag(bz, 0) + np.diag(cz, 1)

    return A_imp
