from django.contrib.auth.models import User

# superusers = User.objects.filter(is_superuser=True)

# for user in superusers:
#     print(user.username)

user = User.objects.get(username='dudegfa5')
user.set_password('dudegfa5dudegfa5')
user.save()