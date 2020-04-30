from hashids import Hashids

hashids = Hashids(
    salt='6Ujh)XSDB+.39DO`/R|/wWa>64*k=T3>?Xn-*$1:g T&Vv`|X 5<!CzC,YaM&e#U',
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

