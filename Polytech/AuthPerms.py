def is_student(user):
    return user.groups.filter(name='Students').exists()