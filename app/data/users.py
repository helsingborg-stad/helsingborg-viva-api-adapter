from flask import current_app
from hashids import Hashids

hashids = Hashids(
    salt=current_app.config['SALT'],
    min_length=32
)

# mock data
USERS = {
    hashids.encode(197608191234): {
        'name': 'Dan Nilsson',
        'age': 44,
        'spec': 'Is Cool!',
    },
    hashids.encode(197801084321): {
        'name': 'Jenny Jensen',
        'age': 42,
        'spec': 'Is Love!',
    },
}

