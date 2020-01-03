import threading

lock = threading.Lock()
import os 

application_state = {
    'license_check': {
        'license_valid': False,
        'message': [],
        'retry_active': False
    },
    'install': {
        'progress': 50,
        'messages': ['Starting installation...'],
        'success': None,
        'error_code': ''
    },
    'app_location': os.path.abspath(os.getcwd()),
    'superuser': {

    }
}