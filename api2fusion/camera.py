"""
Represents a camera.
"""


class Camera(object):
    """Class representing a general camera.
    Attributes
    ----------
    cameraID : str
        Id of the camera.
    legacy_cameraID : int, optional
        Id of the camera in previous CAM2 camera database.
    camera_type: str
        Type of the camera.
    source : str, optional
    country : str, optional
    state : str, optional
    city : str, optional
    longitude : float, optional
    latitude : float, optional
    is_active_image : bool, optional
    is_active_video : bool, optional
    resolution_width : int, optional
    resolution_height : int, optional
    utc_offset : int, optional
    timezone_id : str, optional
    timezone_name : str, optional
    reference_logo : str, optional
    reference_url : str, optional
    """

    def __init__(self, **dict_entries):
        """Client initialization method.

        Parameters
        ----------
        dict_entries: dict
            Dictionary of all field values of a camera.

        Note
        ----
            User should not construct any camera object on his/her own.
            Camera should only be initialized by results returned from the API.
            Documentation of camera constructor is for CAM2 API team only.
        """
        self.__dict__.update(dict_entries)

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def process_json(**dict_entries):
        dict_entries['camera_type'] = dict_entries['type']
        dict_entries.pop('type', None)
        dict_entries.update(dict_entries['retrieval'])
        dict_entries.pop('retrieval', None)

        if dict_entries['camera_type'] == 'ip':
            return IPCamera(**dict_entries)
        if dict_entries['camera_type'] == 'non_ip':
            return NonIPCamera(**dict_entries)
        return StreamCamera(**dict_entries)

    @property
    def id(self):
        """

        Returns str
        -------
            returns string representation of the camera id
        """
        return self.__dict__.pop('cameraID', None)

    @property
    def legacy_id(self):
        """

        Returns str
        -------
            returns string representation of the camera's legacy id

        """
        return self.__dict__.pop('legacy_cameraID', None)

    @property
    def is_active_image(self):
        """

        Returns bool
        -------
            returns whether the camera has active image.
        """
        return bool(self.__dict__.pop('is_active_image'))

    @property
    def city(self):
        """

        Returns str
        -------
            city of the camera
        """
        return str(self.__dict__.pop('city', None))

    @property
    def state(self):
        """

        Returns str
        -------
            state of the camera
        """
        return str(self.__dict__.pop('state', None))

    @property
    def country(self):
        """

        Returns  str
        -------
             country of the camera
        """
        return str(self.__dict__.pop('country', None))


class IPCamera(Camera):
    """Represent a single ip camera.
    This is a subclass of Camera.

    Attributes
    ----------
    ip : str
    port : str
    brand : str, optional
    model : str, optional
    image_path : str, optional
    video_path : str, optional
    """

    def __init__(self, **dictentries):
        """

        Parameters
        ----------
        dictentries : dict
             dictionary contatining all the cameras parameters
        """
        self.__dict__.update(**dictentries)

    def __str__(self):
        """

        Returns str
        -------
            string representation of the dict storing the camera parameters.
        """
        return str(self.__dict__)

    @property
    def ip(self):
        """

        Returns  str
        -------
             ip of the camera
        """
        return str(self.__dict__.pop('ip', None))

    @property
    def port(self):
        """

        Returns  str
        -------
             port of the camera
        """
        return str(self.__dict__.pop('port', None))

    @property
    def brand(self):
        """

        Returns  str
        -------
             brand of the camera
        """
        return str(self.__dict__.pop('brand', None))

    @property
    def model(self):
        """

        Returns  str
        -------
             model of the camera
        """
        return str(self.__dict__.pop('model', None))

    @property
    def image_path(self):
        """

        Returns  str
        -------
             image path of the camera
        """
        return str(self.__dict__.pop('image_path', None))

    @property
    def video_path(self):
        """

        Returns  str
        -------
             video path of the camera
        """
        return str(self.__dict__.pop('video_path', None))





class NonIPCamera(Camera):
    """Represent a single non-ip camera.
    This is a subclass of Camera.

    Attributes
    ----------
    snapshot_url : str
    """

    def __init__(self, **dictentries):
        """

       Parameters
       ----------
       dictentries : dict
            dictionary contatining all the cameras parameters
       """
        self.__dict__.update(**dictentries)

    def __str__(self):
        """

        Returns str
        -------
            string representation of the dict storing the camera parameters.
        """
        return str(self.__dict__)

    @property
    def snapshot_url(self):
        """

        Returns  str
        -------
             snapshort url of the camera
        """
        return str(self.__dict__.pop('snapshot_url', None))


class StreamCamera(Camera):
    """Represent a single stream camera.
    This is a subclass of Camera.

    Attributes
    ----------
    m3u8_url : str
    """

    def __init__(self, **dictentries):
        """

       Parameters
       ----------
       dictentries : dict
            dictionary contatining all the cameras parameters
       """
        self.__dict__.update(**dictentries)

    def __str__(self):
        """

        Returns str
        -------
            string representation of the dict storing the camera parameters.
        """
        return str(self.__dict__)

    @property
    def m3u8_url(self):
        """

        Returns  str
        -------
             m3u8 url of camera
        """
        return str(self.__dict__.pop('m3u8_url', None))
