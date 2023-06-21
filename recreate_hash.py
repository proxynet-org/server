from users.models import User

users = User.objects.all()
for user in users:
    user.change_user_hash()
