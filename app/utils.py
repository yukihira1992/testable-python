def calculate_age(birthday, at):
    if at < birthday:
        raise ValueError('Parameter at is older than birthday.')
    age = at.year - birthday.year
    if (at.month, at.day) < (birthday.month, birthday.day):
        age -= 1
    return age
