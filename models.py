"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info['pdes']
        self.name = None if len(info['name']) == 0 else info['name']
        self.diameter = float('nan') if len(info['diameter']) == 0 else float(info['diameter'])
        self.hazardous = True if info['pha'] == 'Y' else False 

        # Create an empty initial collection of linked approaches.
        ##This will be linked upon instantiating `NEODatabase`.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return (f'{self.name}-{self.designation}')

    def __str__(self):
        """Return `str(self)`: human-readable string."""
        return f'NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {"is" if self.hazardous else "is not"} potentially hazardous.'

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """Serialize.
        sample output: {'designation': '433', 'name': 'Eros', 'diameter_km': 16.84, 'potentially_hazardous': False}
        """ 
        res = {'designation': self.designation, 'name': self.name, 'diameter_km': self.diameter,
                'potentially_hazardous': str(self.hazardous)}



class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info['des']
        self.time = cd_to_datetime(info['cd'].strip())
        self.distance = float(info['dist'])
        self.velocity = float(info['v_rel'])

        # Create an attribute for the referenced NEO, originally None.
        ##It will eventually be populated in `NEODatabase`
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    @property
    def fullname(self):
        """Full name."""
        return f'{self._designation}'

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, '{self.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """
        Sample output: {'datetime_utc': '2025-11-30 02:18', 'distance_au': 0.39, 'velocity_km_s': 3.72}"""
        # (, , '', '', 'name', '', '')
        res = {'datetime_utc': datetime_to_str(self.time),
               'distance_au': self.distance,
               'velocity_km_s': self.velocity,
               'neo': {
                   'designation': self.neo.designation,
                   'potentially_hazardous': self.neo.hazardous,
                   'diameter_km': self.neo.diameter,
                   'name': '' if self.neo.name is None else self.neo.name
               }
              }
        return res