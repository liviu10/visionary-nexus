# visionary-nexus_web_1
podman-compose exec web python manage.py shell
from django.contrib.auth.models import User
print(User.objects.values_list('username', flat=True))
exit()
podman-compose exec web python manage.py changepassword numele_utilizatorului

podman-compose build
podman-compose up

podman exec -it <nume_container> python manage.py startapp <nume_aplicatie>
podman exec -it <nume_container> python manage.py makemigrations
podman exec -it <nume_container> python manage.py migrate
podman exec -it <nume_container> python manage.py createsuperuser
podman restart <nume_container>