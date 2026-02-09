# visionary-nexus
podman-compose exec web python manage.py shell
from django.contrib.auth.models import User
print(User.objects.values_list('username', flat=True))
exit()
podman-compose exec web python manage.py changepassword numele_utilizatorului

podman-compose build
podman-compose up