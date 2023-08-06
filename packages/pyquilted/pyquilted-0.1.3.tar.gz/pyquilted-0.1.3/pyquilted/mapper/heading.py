from pyquilted.quilted.heading import Heading


class HeadingMapper:
    """Heading data mapper object"""
    def __init__(self, odict):
        self.odict = odict

    def deserialize(self):
        heading_section = Heading(**self.odict)
        return heading_section
