
from json import dumps

from . import name_constant, add_enum_constant, set_constant
from ..stoats.calculate.climb import Climb, MAX_CLIMB_GRADIENT, MIN_CLIMB_GRADIENT, MAX_CLIMB_REVERSAL, \
    MIN_CLIMB_ELEVATION

CLIMB_CNAME = 'Climb'


def add_climb(s, activity_group, phi=0.7):
    '''
    Add the constants necessary to auto-detect climbs.
    '''
    activity_group_constraint = str(activity_group)
    fatigue_name = name_constant(CLIMB_CNAME, activity_group)
    fatigue = add_enum_constant(s, fatigue_name, Climb, single=True, constraint=activity_group_constraint,
                                description='Data needed to cdetect climbs - see Climb enum')
    set_constant(s, fatigue, dumps({'phi': phi,
                                    'min_gradient': MIN_CLIMB_GRADIENT,
                                    'max_gradient': MAX_CLIMB_GRADIENT,
                                    'min_elevation': MIN_CLIMB_ELEVATION,
                                    'max_reversal': MAX_CLIMB_REVERSAL}))
