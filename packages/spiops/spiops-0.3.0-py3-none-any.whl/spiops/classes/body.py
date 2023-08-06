import spiceypy as cspice
import numpy as np
from spiops.utils import utils



class Body(object):
    def __init__(self, body, time=object(), target=None):

        if isinstance(body, str):
            name = body
            id = cspice.bodn2c(body)
        else:
            id = body
            name = cspice.bodc2n(body)

        if target:
            self.target = target

        self.name = name
        self.id = id
        self.time = time

        #
        # Parameters for the Geometry Computation
        #
        self.previous_tw = []
        self.geometry_flag = False


    def __getattribute__(self, item):

        if item in ['altitude',
                    'distance',
                    'zaxis_target_angle'
                    'myaxis_target_angle',
                    'groundtrack']:
            self.__Geometry()
            return object.__getattribute__(self, item)
        elif item in ['sa_ang_p',
                      'sa_ang_n',
                      'sa_ang',
                      'saa_sa',
                      'saa_sc',
                      'hga_earth',
                      'hga_el_az']:
            self.__Structures()
            return object.__getattribute__(self, item)
        else:
            return object.__getattribute__(self, item)


    def __getattr__(self, item):

        if item in ['state_in_window']:
            self.__StateInWindow()
            return object.__getattribute__(self, item)


    def State(self, target=False, reference_frame=False, current=False):

        if self.target and not target and not reference_frame:
            target = self.target.name
            reference_frame = self.target.frame

        if not self.target:
            if target is False: target = 'J2000'
            if reference_frame is False: reference_frame = 'J2000'

        self.trajectory_reference_frame = reference_frame

        if not current:
            current = self.time.current

        state, lt = cspice.spkezr(target, current, reference_frame,
                                  self.time.abcorr, self.name)

        return state


    def Orientation(self, frame='', target_frame='', current=False,
                    format='msop quaternions'):

        if self.target and not target_frame:
            target_frame = self.target.frame

        if not self.target and not target_frame:
            target_frame = 'J2000'

        if not frame:
            frame = self.frame

        if not current:
            current = self.time.current
        else:
            #TODO: need to add a time conversion here
            current = current

        rot_mat = cspice.pxform(target_frame, frame, current)

        if format == 'spice quaternions':
            orientation = cspice.m2q(rot_mat)

        if format == 'msop quaternions':
            quaternions = cspice.m2q(rot_mat)
            orientation = [-quaternions[1],
                           -quaternions[2],
                           -quaternions[3],
                            quaternions[0]]

        elif format == 'euler angles':
            orientation = (cspice.m2eul(rot_mat, 3, 2, 1))

        elif format == 'rotation matrix':
            orientation = rot_mat

        return orientation


    def __StateInWindow(self, target=False, reference_frame=False, start=False,
                     finish=False):

        state_in_window = []
        for et in self.time.window:
            state_in_window.append(self.State(target, reference_frame, et))

        self.state_in_window = state_in_window

        return


    def __Structures(self):

        if self.structures_flag is True and \
                        self.time.window.all() == self.previous_tw.all():
            return

        time = self.time
        import spiops as spiops

        #
        # We determine the mission
        #
        if self.name == 'TGO':
            plus_array = 'TGO_SA+Z'
            minus_array = 'TGO_SA-Z'
        elif self.name == 'MPO':
            plus_array = 'MPO_SA'
            minus_array = ''
        elif self.name == 'MTM':
            plus_array = 'MTM_SA+X'
            minus_array = 'MTM_SA-X'


        #
        # Solar Arrays
        #
        sa_ang_p_list = []
        sa_ang_n_list = []
        saa_sa_p_list = []
        saa_sa_n_list = []
        saa_sc_x_list = []
        saa_sc_y_list = []
        saa_sc_z_list = []
        hga_earth = []
        hga_angles_el = []
        hga_angles_az = []

        #
        # High Gain Antennas
        #


        for et in time.window:

            #
            # Of course we need to include all possible cases including only one
            # Solar Array
            #
            sa_ang_p = spiops.solar_array_angle(plus_array, et)
            if minus_array:
                sa_ang_n = spiops.solar_array_angle(minus_array, et)
            saa = spiops.solar_aspect_angles(self.name, et)

            sa_ang_p_list.append(sa_ang_p)
            if minus_array:
                sa_ang_n_list.append(sa_ang_n)
            saa_sa_p_list.append(saa[0][0])
            saa_sa_n_list.append(saa[0][1])
            saa_sc_x_list.append(saa[1][0])
            saa_sc_y_list.append(saa[1][1])
            saa_sc_z_list.append(saa[1][2])

            #
            # HGA mechanisms
            #
            if self.name != 'MTM':
                (hga_angles_ang, hga_earth_ang) = spiops.hga_angles(self.name, et)
                hga_earth.append(hga_earth_ang)
                hga_angles_el.append(hga_angles_ang[0])
                hga_angles_az.append(hga_angles_ang[1])

        self.sa_ang_p = sa_ang_p_list
        self.sa_ang_n = sa_ang_n_list
        self.sa_ang = [sa_ang_p_list, sa_ang_n_list]
        self.saa_sa = [saa_sa_p_list, saa_sa_n_list]
        self.saa_sc = [saa_sc_x_list, saa_sc_y_list, saa_sc_z_list]

        self.hga_earth = hga_earth
        self.hga_angles = [hga_angles_el, hga_angles_az]

        self.structures_flag = True
        self.previous_tw = self.time.window

        return


    def __Geometry(self):

        #if self.geometry_flag is True and \
        #                self.time.window.all() == self.previous_tw.all():
        #    return

        import spiops as spiops

        distance = []
        altitude = []
        latitude = []
        longitude = []
        subpoint_xyz = []
        subpoint_pgc = []
        subpoint_pcc = []
        zaxis_target_angle = []
        myaxis_target_angle = []
        beta_angle = []

        tar = self.target
        time = self.time

        for et in time.window:

            #
            # Compute the distance
            #
            ptarg, lt = cspice.spkpos(tar.name, et, tar.frame, time.abcorr,
                                      self.name)
            vout, vmag = cspice.unorm(ptarg)
            distance.append(vmag)

            #
            # Compute the geometric sub-observer point.
            #
            spoint, trgepc, srfvec = cspice.subpnt(tar.method, tar.name, et,
                                                   tar.frame, time.abcorr,
                                                   self.name)
            subpoint_xyz.append(spoint)

            #
            # Compute the observer's altitude from SPOINT.
            #
            dist = cspice.vnorm(srfvec)
            altitude.append(dist)


            #
            # Convert the sub-observer point's rectangular coordinates to
            # planetographic longitude, latitude and altitude.
            #
            spglon, spglat, spgalt = cspice.recpgr(tar.name, spoint,
                                                   tar.radii_equ, tar.flat)

            #
            # Convert radians to degrees.
            #
            spglon *= cspice.dpr()
            spglat *= cspice.dpr()

            subpoint_pgc.append([spglon, spglat, spgalt])

            #
            #  Convert sub-observer point's rectangular coordinates to
            #  planetocentric radius, longitude, and latitude.
            #
            spcrad, spclon, spclat = cspice.reclat(spoint)


            #
            # Convert radians to degrees.
            #
            spclon *= cspice.dpr()
            spclat *= cspice.dpr()

            subpoint_pcc.append([spclon, spclat, spcrad])
            latitude.append(spclat) #TODO: Remove with list extraction
            longitude.append(spclon)  # TODO: Remove with list extraction

            #
            # Compute the angle between the observer's S/C axis and the
            # geometric sub-observer point
            #
            obs_tar, ltime = cspice.spkpos(tar.name, et,
                                                   'J2000', time.abcorr,
                                                   self.name)
            obs_zaxis  = [0,  0, 1]
            obs_myaxis = [0, -1, 0]

            #
            # We need to account for when there is no CK attitude available.
            #
            try:
                matrix = cspice.pxform(self.frame, 'J2000', et)

                z_vecout = cspice.mxv(matrix, obs_zaxis)
                zax_target_angle = cspice.vsep(z_vecout, obs_tar)
                zax_target_angle *= cspice.dpr()
                zaxis_target_angle.append(zax_target_angle)

                my_vecout = cspice.mxv(matrix, obs_myaxis)
                myax_target_angle = cspice.vsep(my_vecout, obs_tar)
                myax_target_angle *= cspice.dpr()
                myaxis_target_angle.append(myax_target_angle)
            #
            # TODO: Include a thorough error message here
            #
            except:
                zaxis_target_angle.append(0.0)
                myaxis_target_angle.append(0.0)

            beta_angle.append(spiops.beta_angle(self.name, self.target.name,
                                                et))


        self.distance = distance
        self.altitude = altitude
        #self.latitude = [for subpoint in subpoint_pcc]
        self.latitude = latitude
        self.longitude = longitude
        #self.longitude = [subpoint_pcc ]
        self.subpoint_xyz = subpoint_xyz
        self.subpoint_pgc = subpoint_pgc
        self.subpoint_pcc = subpoint_pcc
        self.zaxis_target_angle = zaxis_target_angle
        self.myaxis_target_angle = myaxis_target_angle
        self.beta_angle = beta_angle

        self.geometry_flag = True
        self.previous_tw = self.time.window

        return


    def Plot(self, yaxis = 'distance', date_format='TDB', external_data=[],
             notebook=False):

        self.__Geometry()
        self.__Structures()

        #
        # Not Time in X axis
        #
        if yaxis == 'groundtrack':
            utils.plot(self.__getattribute__('longitude'),
                       self.__getattribute__('latitude'),
                       notebook=notebook, xaxis_name = 'Longitude',
                       yaxis_name='Latitude', mission=self.name,
                       target=self.target.name, background_image=True)

            return

        #
        # Time in X axis
        #
        if yaxis == 'sa_ang':
            yaxis_name = ['sa_ang_p', 'sa_ang_n']
        elif yaxis == 'saa_sc':
            yaxis_name = ['saa_sc_x', 'saa_sc_y', 'saa_sc_z']
        elif yaxis == 'saa_sa':
            if self.name != 'MPO':
                yaxis_name = ['saa_sa_p', 'saa_sa_n']
            else:
                yaxis_name = ['saa_sa']
        elif yaxis == 'hga_angles':
            yaxis_name = ['hga_el', 'hga_az']
        elif yaxis == 'hga_earth':
            yaxis_name = 'hga_earth'
        else:
            yaxis_name = yaxis

        utils.plot(self.time.window, self.__getattribute__(yaxis), notebook=notebook,
                   external_data=external_data, yaxis_name=yaxis_name,
                   mission = self.name, target = self.target.name,
                   date_format=date_format)

        return



    def Plot3D(self, data='trajectory', reference_frame=False):


        #TODO: Arrange the reference frame flow
        if not self.state_in_window:
            self.__StateInWindow(reference_frame=reference_frame)


        data = self.state_in_window

        utils.plot3d(data, self, self.target)

        return


class Target(Body):

    def __init__(self, body, time=object(),
                 target=False, frame='',
                 method='INTERCEPT/ELLIPSOID'):
        """

        :param body:
        :type body:
        :param time:
        :type time:
        :param target: It no target is provided the default is 'SUN'
        :type target:
        :param frame:
        :type frame:
        :param method:
        :type method:
        """

        #
        # In the target parameter for the following if statement we need to use
        # the class object(), which is empty, to avoid A Recursion Error.
        #
        if not target:
            target = Target('SUN', time=time, target=object())

        super(Target, self).__init__(body, time=time, target=target)

        if not frame:
            self.frame = 'IAU_{}'.format(self.name)
        else:
            self.frame = frame

        self.method = method


        self.__getRadii()


    def __getRadii(self):

        try:
            self.radii = cspice.bodvar(self.id, 'RADII', 3)

        except:
            print("Ephemeris object has no radii")
            return

        self.radii_equ = self.radii[0]
        self.radii_pol = self.radii[2]
        self.flat = (self.radii_equ - self.radii_pol) / self.radii_equ

        return


class Observer(Body):
    def __init__(self, body, time=object(), target=False, frame=''):

        super(Observer, self).__init__(body, time=time, target=target)

        if not frame:
            self.frame = '{}_SPACECRAFT'.format(self.name)
            if cspice.namfrm(self.frame) == 0:
                self.frame = self.name
            if cspice.namfrm(self.frame) == 0:
                #TODO: Fix this shit
                self.frame = '{}_LANDER'.format(self.name)
                print('The frame name has not been able to be built; please introduce it manually')
        else:
            self.frame = frame


