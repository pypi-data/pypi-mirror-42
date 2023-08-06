import numpy as np
import netCDF4


class CoastalModel:
    """
    Main class describing the model
    """

    def __init__(self, imax, jmax, kmax):
        """
        Define and initialise the first and last point indexes in the three
        directions (x,y,z) or (east-west, south-north, vertical).
        Inputs :
          imax : last index in the x direction given by the user
          jmax : last index in the y direction given by the user
          kmax : last index in the z direction given by the user
        Outputs :
          self.imin : first index in the x direction
          self.jmin : first index in the y direction
          self.kmin : first index in the z direction
          self.imax : last index in the x direction
          self.jmax : last index in the y direction
          self.kmax : last index in the z direction
        """
        if imax < 3 or jmax < 3:
            raise Exception('2D grid mesh must be composed of 3 by 3 cells')

        self.imin = 0
        self.imax = imax
        self.jmin = 0
        self.jmax = jmax
        self.kmin = 0
        self.kmax = kmax

    def estimate_size_grid(self):
        """
        Get number of mesh in each directions
        Outputs :
          ni : number of mesh in the x direction
          nj : number of mesh in the y direction
          nk : number of mesh in the z direction
        """
        ni = self.imax - self.imin + 1
        nj = self.jmax - self.jmin + 1
        nk = self.kmax - self.kmin + 1
        return ni, nj, nk

    def init_bathy(self, ni, nj):
        """
        Define and initialise the bathymetric arrays
        Inputs :
          ni : number of points within the grid in the x direction
          nj : number of points within the grid in the y direction
        Outputs :
          self.h_t : the bathymetry at the t point
          self.h_u : the bathymetry at the u point
          self.h_v : the bathymetry at the v point
        """
        self.h_t = np.ones((ni, nj), order='F') * 100.
        self.h_u = np.ones((ni, nj), order='F') * 100.
        self.h_v = np.ones((ni, nj), order='F') * 100.

    def init_mask(self, ni, nj, l_obc):
        """
        Initialises the mask arrays
        Inputs :
          l_obc : a dictionnary that describes the nature (open/closed) of the
                  four domain boundaries
        Outputs :
          self.mask_t : the mask at the t point (1 : for water ; 0 for land)
          self.mask_u : the mask at the u point (1 : for water ; 0 for land)
          self.mask_v : the mask at the v point (1 : for water ; 0 for land)
          self.mask_s : the mask at the s point (1 : water everywhere
          ; 0 if any land)
        """

        # Default value is 1 : water everywhere
        self.mask_t = np.ones((ni, nj), order='F')
        self.mask_u = np.ones((ni, nj), order='F')
        self.mask_v = np.ones((ni, nj), order='F')
        self.mask_s = np.ones((ni, nj), order='F')

    def define_var2D(self, ni, nj):
        """
        Define the arrays required for the 2D model
        Inputs :
          ni : number of points within the grid in the x direction
          nj : number of points within the grid in the y direction
        Outputs :
          self.zeta : zeta the elevation (above a reference level) of
                      the free elevation in meter
          self.u2d : the horizontal west-east component of the mean vertical
                     current in m/s
          self.v2d : the horizontal south-north component of the mean vertical
                     current in m/s

          self.ht_t : total water depth at the t-point within the Arakawa
          C-grid
          self.ht_u : total water depth at the u-point within the Arakawa
          C-grid
          self.ht_v : total water depth at the v-point within the Arakawa
          C-grid

          self.rhs_u_2d : right hand side of the u-momentum equation ;
                          it will cumulate all the acceleration at the right
                          hand side : pressure gradient, advection, coriolis,
                          bottom friction, wind friction, atmospherical
                          pressure gradient
          self.rhs_v_2d : idem as previous for v-momentum
        """
        self.zeta = np.zeros((ni, nj), order='F')
        self.u2d = np.zeros((ni, nj), order='F')
        self.v2d = np.zeros((ni, nj), order='F')
        self.ht_t = np.zeros((ni, nj), order='F')
        self.ht_u = np.zeros((ni, nj), order='F')
        self.ht_v = np.zeros((ni, nj), order='F')
        self.rhs_u2d = np.zeros((ni, nj), order='F')
        self.rhs_v2d = np.zeros((ni, nj), order='F')

    def define_var3D(self, ni, nj, nk):
        """
        function that defines the arrays required for the 3D model
        inputs :
        ni : number of points within the grid in the x direction
        nj : number of points within the grid in the y direction
        nk : number of points within the grid in the z direction
        outputs :
        self.uz : the horizontal west-east component of the current in m.s-1
        self.vz : the horizontal south-north component of the current in m.s-1
        self.wz : the vertical component of the current within the
                  sigma framework in s-1
        self.rhs_u_3d_4_2dcoupling : terms from the 3D required for the
                                     coupling in the 2D for the u-momentum
        self.rhs_v_3d_4_2dcoupling : terms from the 3D required for the
                                     coupling in the 2D for the v-momentum
        """

        self.u3d = np.zeros((nk, ni, nj), order='F')
        self.v3d = np.zeros((nk, ni, nj), order='F')
        self.w3d = np.zeros((nk, ni, nj), order='F')
        self.rhs_u3d = np.empty((nk, ni, nj), order='F')
        self.rhs_v3d = np.empty((nk, ni, nj), order='F')
        self.kz_u = np.zeros((nk, ni, nj), order='F')
        self.kz_v = np.zeros((nk, ni, nj), order='F')

    def define_Hgrid(self, grid_size):
        """
        Define the size of the grid element
        Inputs :
          grid_size : the size of one edge of the grid in meter
        Outputs :
          self.dx : the size of the grid cell in the x direction at the
                    t point in meter
          self.dx_u : the size of the grid cell in the x direction at the
                      u point in meter
          self.dx_v : the size of the grid cell in the x direction at the
                      v point in meter
          self.dx_s : the size of the grid cell in the x direction at the
                      s point in meter
          self.dy : the size of the grid cell in the y direction at the
                    t point in meter
          self.dy_u : the size of the grid cell in the y direction at the
                      u point in meter
          self.dy_v : the size of the grid cell in the y direction at the
                      v point in meter
          self.dy_s : the size of the grid cell in the x direction at the
                      s point in meter
        """

        self.dx = grid_size
        self.dx_u = grid_size
        self.dx_v = grid_size
        self.dx_s = grid_size
        self.dy = grid_size
        self.dy_u = grid_size
        self.dy_v = grid_size
        self.dy_s = grid_size

    def define_Vgrid(self, nk):
        """
        Define the variables and arrays of the vertical grid
        Inputs :
          nk : number of vertical sigma levels
        Outputs :
          self.sig_u : array of the sigma values at u-point
                       (along the vertical)
          self.sig_w : array of the sigma values at w-point
                       (along the vertical)
          self.dsig_u : array of the layer thicknesses (in the sigma framework)
                        around u-point (along the vertical)
          self.dsig_w : array of the layer thicknesses (in the sigma framework)
                        around w-point (along the vertical)
        """
        self.sig_u = [((k - self.kmax) - 0.5) / self.kmax for k in range(nk)]
        self.sig_u.append(abs(self.sig_u[-1]))
        self.sig_w = [.5 * (self.sig_u[k] + self.sig_u[k + 1])
                      for k in range(nk)]
        self.dsig_w = [self.sig_u[k + 1] - self.sig_u[k] for k in range(nk)]
        self.dsig_u = [self.sig_w[k] - self.sig_w[k - 1] for k in range(nk)]
        self.sig_u = np.array(self.sig_u)
        self.sig_w = np.array(self.sig_w)
        self.dsig_u = np.array(self.dsig_u)
        self.dsig_w = np.array(self.dsig_w)

    def create_outputfile(self, fileout='out.nc'):
        """ Create a netCDF4 file for output time step
        """
        self.nc = netCDF4.Dataset(fileout, 'w')
        # Create dimensions
        self.nc.createDimension('time', None)
        self.nc.createDimension('longitude', self.imax - self.imin + 1)
        self.nc.createDimension('latitude', self.jmax - self.jmin + 1)
        self.nc.createDimension('level', self.kmax - self.kmin + 1)

        # Create dimension variables
        self.nc.createVariable('time', 'd', ('time',))
        self.nc.variables['time'].units = 'seconds since 1900-01-01T00:00:00Z'
        self.nc.variables['time'].long_name = 'time in seconds (UT)'
        self.nc.variables['time'].time_origin = '01-JAN-1900 00:00:00'
        self.nc.variables['time'].axis = 'T'

        self.nc.createVariable('longitude', 'f', ('longitude',))
        self.nc.variables['longitude'].units = 'degrees_east'
        self.nc.variables['longitude'].long_name = 'longitude'
        self.nc.variables['longitude'].axis = 'X'
        self.nc.variables['longitude'][:] = range(self.imax - self.imin + 1)

        self.nc.createVariable('latitude', 'f', ('latitude',))
        self.nc.variables['latitude'].units = 'degrees_north'
        self.nc.variables['latitude'].long_name = 'latitude'
        self.nc.variables['latitude'].axis = 'Y'
        self.nc.variables['latitude'][:] = range(self.jmax - self.jmin + 1)

        self.nc.createVariable('level', 'f', ('level',))
        self.nc.variables['level'].units = ''
        self.nc.variables['level'].long_name = 'sigma level'
        self.nc.variables['level'].axis = 'Z'
        self.nc.variables['level'].positive = 'up'
        self.nc.variables['level'].formula_terms = "sigma: level; eta:\
         ssh; depth: h0"
        self.nc.variables['level'].formula_definition =\
            "z(n,k,j,i) = eta(n,j,i) + sigma(k)*(depth(j,i)+eta(n,j,i))"
        self.nc.variables['level'][:] = self.sig_u[:-1]

    def create_variables(self):
        """ Create variables in the netCDF file
        """
        self.nc.createVariable('ssh', 'f', ('time', 'longitude', 'latitude'),
                               fill_value=-999.)
        self.nc.variables['ssh'].units = 'm'
        self.nc.variables['ssh'].long_name = 'sea surface elevation'

        self.nc.createVariable('u2d', 'f', ('time', 'longitude', 'latitude'),
                               fill_value=-999.)
        self.nc.variables['u2d'].units = 'm.s-1'
        self.nc.variables['u2d'].long_name = 'barotropic zonal velocity'

        self.nc.createVariable('v2d', 'f', ('time', 'longitude', 'latitude'),
                               fill_value=-999.)
        self.nc.variables['v2d'].units = 'm.s-1'
        self.nc.variables['v2d'].long_name = 'barotropic meridional velocity'

        self.nc.createVariable('u3d', 'f', ('time', 'level', 'longitude',
                                            'latitude'), fill_value=-999.)
        self.nc.variables['u3d'].units = 'm.s-1'
        self.nc.variables['u3d'].long_name = '3d zonal velocity'

        self.nc.createVariable('v3d', 'f', ('time', 'level', 'longitude',
                                            'latitude'), fill_value=-999.)
        self.nc.variables['v3d'].units = 'm.s-1'
        self.nc.variables['v3d'].long_name = '3d meridional velocity'

    def write_variables(self, ind_t, time):
        """ Write variables at each output time step
        """
        self.nc.variables['time'][ind_t] = time
        self.nc.variables['ssh'][ind_t, :, :] = self.zeta
        self.nc.variables['u2d'][ind_t, :] = self.u2d
        self.nc.variables['v2d'][ind_t, :] = self.v2d
        self.nc.variables['u3d'][ind_t, :] = self.u3d
        self.nc.variables['v3d'][ind_t, :] = self.v3d
