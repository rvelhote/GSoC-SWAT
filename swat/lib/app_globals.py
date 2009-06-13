"""The application's Globals object"""

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        import sys
        
        sys.path.append('/usr/local/samba/lib/python2.6/site-packages')
        sys.path.append('/usr/local/samba/lib/python2.6/site-packages/samba')
        sys.path.append('/usr/local/samba/lib/python2.6/site-packages/samba/dcerpc')
        
        import param, samba
        
        self.samba_lp = param.LoadParm()
        self.samba_lp.load_default()
        
        self.samba_version = samba.version
