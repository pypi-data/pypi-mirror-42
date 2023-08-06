from .Generalmodel import CoastalModel
from .Dynamic import estimate_explicite_matrix, estimate_implicite_matrix
import numpy as np


class Model(CoastalModel):
    """Model to solve primitives equations in the ocean in one dimension
    """

    def __init__(self, grid_size, t_end):
        """Model for solving primitive equation of the ocean in one dimension.

        Attributes:
            grid_size (int) size of the grid
            t_end (float) time to end the simulation in day
        """

        self.grid_size = grid_size
        # Creation of CoastalModel object
        CoastalModel.__init__(self, imax=3, jmax=3, kmax=100)
        # Time parametrisation
        self.t_str = 0  # Start time
        self.t_end = t_end * 24 * 3600  # End time in seconds since t_str
        self.t_out = 0.  # First date of output (in seconds since t_str)
        self.dt_out = 1. * 3600  # Output period in seconds (each hour)
        self.dt_3D = 50.  # Time step of the 3D mode (baroclinic / internal)
        self.ndtfast = 0  # Number of sub-barotropic time step per 3D time step
        # Physical Parametrisation
        self.GRAV = 9.81  # Gravitational constant in m.s-2
        self.FCOR = 1e-4  # Coriolis parameter (2 cos(latitude) Omega) in rd/s
        self.KAPPA = 0.4  # Von Karman constant (without units)
        self.Z0B = .0035  # Rugosity in m
        self.RHO_REF = 1026  # kg.m-3  seawater density
        self.RHO_AIR = 1.25  # kg.m-3  air density
        self.CD_AIR = 0.0016  # Drag coefficient
        # Numerical parameters
        self.ALP = 0.5  # Implicitation rate for diffusion equation solving
        self.MU_v = 1e-2  # Vertical turbulent viscosity m2.s-1
        self.MU_h = 1.0  # Horizontal turbulent viscosity m2.s-1
        # Boundary conditions : closed everywhere by default
        self.l_obc = {
            'north': False,
            'south': False,
            'west': False,
            'east': False
        }

    def set_variable(self):
        """Function to define variabeles in the Model

        Args:
            None

        return:
            None
        """

        # Set horizontal cell size and define vertical grid
        (ni, nj, nk) = self.estimate_size_grid()
        self.ni = ni
        self.nj = nj
        self.nk = nk
        self.define_Hgrid(self.grid_size)
        self.define_Vgrid(nk)

        # Initialise bathymetry for U, V and T points
        self.init_bathy(ni, nj)

        # Initialise land/sea mask for U, V, T and S points from bathymetry
        self.init_mask(ni, nj, self.l_obc)

        # Define 2D variables
        self.define_var2D(ni, nj)

        # Define 3D variables
        self.define_var3D(ni, nj, nk)
        self.kz_u[:] = self.MU_v
        self.kz_v[:] = self.MU_v

        # Define temporary variables
        self.v3d_u = np.zeros((nk, ni, nj))
        self.u3d_v = np.zeros((nk, ni, nj))
        self.t = self.t_str

        # Define atmospheric forcing variables
        self.Pres = np.ones((ni, nj)) * 1013.15
        self.Xstr = np.zeros((ni, nj)) + self.RHO_AIR * self.CD_AIR * 100.
        self.Ystr = np.zeros((ni, nj))

    def solve_equations(self, i, j, l_cori=True, l_epgr=True,
                        l_frot=True, l_atms=True):
        """Function to solve primitive primitive equation of the ocean
        in one dimension

        Args:
            i (int) x index in the grid
            j (int) y index in the grid
            l_cori (bool)  Coriolis force
            l_epgr (bool) External pressure gradient (tide)
            l_frot (bool) Bottom fricton
            l_atms (bool) Atmospheric forcings (Wind)

        return :
            None
        """
        # Set model variables
        self.set_variable()

        # Initialeze current speed by 0 m/s
        self.u3d[:, i, j] = 0
        self.v3d[:, i, j] = 0

        # Beginning of the temporal loop
        while self.t < self.t_end:

            self.t += self.dt_3D
            self.ht_u[i, j] = self.h_u[i, j]
            self.ht_v[i, j] = self.h_v[i, j]

            # Begin of the computation of the 3D model
            np.set_printoptions(suppress=True, linewidth=np.nan,
                                threshold=np.nan)
            print('-' * 30, '\nStart 3D model', self.t)

            # Update total water heights (zeta + bathymetry) at t, u, v points
            self.ht_t = self.h_t + 0.0  # The surface dont move
            self.ht_u[i, j] = self.h_u[i, j] + 0.0
            self.ht_v[i, j] = self.h_v[i, j] + 0.0

            # Compute bottom drag coefficient
            Cfrot_u = (self.KAPPA / np.log(1 + (self.sig_u[1] + 1)
                                           * self.ht_u[i, j] / self.Z0B))**2
            Cfrot_v = (self.KAPPA / np.log(1 + (self.sig_u[1] + 1)
                                           * self.ht_v[i, j] / self.Z0B))**2

            # Start to add different forcings to right hand side
            self.rhs_u3d[:] = 0.
            self.rhs_v3d[:] = 0.

            # Add Coriolis term    #### a voir après
            if l_cori:
                self.rhs_u3d[:, i, j] += + self.FCOR * self.v3d[:, i, j]
                self.rhs_v3d[:, i, j] += -self.FCOR * self.u3d[:, i, j]

            # Add external pressure gradient
            omega_maree = 2 * np.pi / (12 * 3600 + 24 * 60)
            if l_epgr:
                self.rhs_u3d[:, i, j] += - 0.00001 * \
                    np.sin(omega_maree * self.t)
                self.rhs_v3d[:, i, j] += - 0.00001 * \
                    np.sin(omega_maree * self.t)

            # Add bottom friction     ### tension de fond
            if l_frot:
                V_bot = (self.u3d[1, i, j]**2 + self.v3d[1, i, j]**2)**.5
                self.rhs_u3d[1, i, j] += - Cfrot_u * V_bot * self.u3d[1, i, j]\
                    / (self.ht_u[i, j] * self.dsig_u[1])
                self.rhs_v3d[1, i, j] += - Cfrot_v * V_bot * self.v3d[1, i, j]\
                    / (self.ht_v[i, j] * self.dsig_u[1])

            # Add wind effect
            if l_atms:
                self.rhs_u3d[self.kmax, i, j] += self.Xstr[i, j] / \
                    self.RHO_REF / (self.ht_u[i, j] * self.dsig_u[self.kmax])
                self.rhs_v3d[self.kmax, i, j] += self.Ystr[i, j] \
                    / self.RHO_REF / (self.ht_v[i, j] * self.dsig_u[self.kmax])

            # Prepare solving
            self.rhs_u3d *= self.dt_3D
            self.rhs_v3d *= self.dt_3D

            # Update u3D
            # Diffusion explicit part : matrix B_exp * uz^{n}
            B_exp = estimate_explicite_matrix(self.nk, self.dt_3D, self.ALP,
                                              self.MU_v, self.ht_u[i, j], self)

            # Diffusion implict part : matrix A_imp * uz^{n+1}
            A_imp = estimate_implicite_matrix(self.nk, self.dt_3D, self.ALP,
                                              self.MU_v, self.ht_u[i, j], self)

            # Add diffusion terms
            self.rhs_u3d[:, i, j] += B_exp.dot(self.u3d[:, i, j])

            # Tridiagonal solving
            self.u3d[1:, i, j] = np.linalg.solve(A_imp[1:, 1:],
                                                 self.rhs_u3d[1:, i, j])

            # Update v3D
            # Diffusion explicit part : matrix B_exp * uz^{n}
            B_exp = estimate_explicite_matrix(self.nk, self.dt_3D, self.ALP,
                                              self.MU_v, self.ht_v[i, j], self)

            # Diffusion implict part : matrix A_imp * uz^{n+1}
            A_imp = estimate_implicite_matrix(self.nk, self.dt_3D, self.ALP,
                                              self.MU_v, self.ht_v[i, j], self)

            # Add diffusion terms
            # initial condition
            self.rhs_v3d[:, i, j] += B_exp.dot(self.v3d[:, i, j])

            # Tridiagonal solving
            self.v3d[1:, i, j] = np.linalg.solve(
                A_imp[1:, 1:], self.rhs_v3d[1:, i, j])

            # Print the min and max of each variable
            np.set_printoptions(
                suppress=True, linewidth=np.nan, threshold=np.nan)
            print('Min and MAx of Extrem Zeta %f %f' %
                  (self.zeta.min(), self.zeta.max()))
            print('Min and Max of 2D U  et V  %f %f' %
                  (np.abs(self.u2d).max(), np.abs(self.v2d).max()))
            print('Abs Min and Max of 3D Uz et Vz %f %f' %
                  (np.abs(self.u3d).max(), np.abs(self.v3d).max()))

            # Write variable
            self.create_outputfile()
            self.create_variables()
            ind_t = 0
            self.write_variables(ind_t, self.t)
            ind_t += 1
            self.nc.close()

    def __repr__(self):
        """Function to output the characteristics of the simulation

        Args:
            None

        Returns:
            string: characteristics of the simulation

        """

        return "grid size {}, Simulation time {}"\
            .format(self.grid_size, self.t_end)
