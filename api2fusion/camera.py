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


    def __getitem__(self, key):
        """Overrides indexing operator.

        Parameters
        ----------
        key :  str
            the key of the camera parameter required.
        Returns str
        -------
            value corresponding the key given.

        """
        return self.__dict__.get(key, None)

    def __setitem__(self, key, value):
        """Overrides the assignment operator.

        Parameters
        ----------
        key : str
            parameter to set in __dict__
        value : str
            new value of the parameter.

        """
        self.__dict__[key] = value

    def __delitem__(self, key):
        """Overrides 'del' operator

        Parameters
        ----------
        key : str
            key to delete from __dict__.

        """
        del self.__dict__[key]

    def __len__(self):
        """Overrides len() method.

        Returns int
        -------
            number of items in __dict__

        """
        return len(self.__dict__)

    def __contains__(self, item):
        """Overrides 'in' operator.

        Parameters
        ----------
        item : str
            item to check if it's in __dict__.

        Returns bool
        -------
            True if item exists.
            False if item doesn't exist

        """
        return (item in self.__dict__)



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


        dictentries['url'] = 'http://' + dictentries['ip'] + (dictentries['video_path'] or dictentries['image_path'] or '')

        self.__dict__.update(**dictentries)






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
        dictentries['url'] = dictentries.get('snapshot_url', None)
        self.__dict__.update(**dictentries)




class StreamCamera(Camera):
    """Represent a single stream camera.
    This is a subclass of Camera.

    Attributes
    ----------
    m3u8_url : str
    ur: str
    """

    def __init__(self, **dictentries):
        """

       Parameters
       ----------
       dictentries : dict
            dictionary contatining all the cameras parameters
       """
        dictentries['url'] = dictentries.get('m3u8_url', None)
        self.__dict__.update(**dictentries)


