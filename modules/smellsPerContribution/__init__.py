config = {
    'wantdiff': False,
    'wantsfiles': True,
    'threadsafe': False,
    'behavior': {
        'creates': [['dump', 'smellsPerContribution']],
        'uses': [['resource', 'smell']]
    }
}

from .program import run
#from .test import test
