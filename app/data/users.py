from flask import current_app
from hashids import Hashids

hashids = Hashids(
    salt=current_app.config['SALT'],
    min_length=32
)

# mock data
USERS = {
    hashids.encode(199412015852): {
        'name': 'Kalle Testarsson',
        'age': 44,
        'spec': 'Ensam',
    },
    hashids.encode(199612240201): {
        'name': 'Therese Blom',
        'age': 42,
        'spec': 'Sambo med barn',
    },
}
