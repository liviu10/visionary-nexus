# Utilizăm o versiune stabilă de Python (3.12-slim)
# Versiunea 'slim' este mult mai mică, iar 3.12 are deja pachete pre-compilate (wheels) 
# pentru NumPy și Scikit-learn, deci nu mai trebuie să le compileze de la zero.
FROM python:3.12-slim-bookworm

# Instalăm dependențele de sistem necesare pentru pachetele de date
# libpq-dev ar fi pentru Postgres, în caz că treci de la SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Setăm variabilele de mediu
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copiem doar fișierul de cerințe pentru a profita de cache-ul Docker
COPY requirements.txt /app/

# Instalăm dependențele
# Folosim --prefer-binary pentru a forța utilizarea versiunilor deja compilate
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copiem restul codului
COPY . /app/

# Comanda de start
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]