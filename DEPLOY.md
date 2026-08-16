# Deployment notes — joshuashneider.com

## Local dev

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit as needed
python manage.py migrate
python manage.py seed  # loads scraped content + images
python manage.py createsuperuser
python manage.py runserver
```

Admin panel: http://127.0.0.1:8000/admin/
Default superuser: admin / admin1234 (change this)

## VPS deployment (gunicorn + nginx)

### 1. Install packages
```bash
pip install gunicorn
```

### 2. .env on the server
```
DEBUG=False
SECRET_KEY=<long-random-string>
ALLOWED_HOSTS=joshuashneider.com,www.joshuashneider.com
DATABASE_URL=sqlite:////home/youruser/josh-website/db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-app-password
CONTACT_EMAIL=josh@joshuashneider.com
```

### 3. Collect static files
```bash
python manage.py collectstatic --noinput
```

### 4. gunicorn systemd unit — /etc/systemd/system/joshsite.service
```ini
[Unit]
Description=Joshua Shneider website
After=network.target

[Service]
User=youruser
WorkingDirectory=/home/youruser/josh-website
ExecStart=/home/youruser/josh-website/venv/bin/gunicorn config.wsgi:application \
    --workers 3 --bind unix:/tmp/joshsite.sock
Restart=always

[Install]
WantedBy=multi-user.target
```

### 5. nginx config — /etc/nginx/sites-available/joshsite
```nginx
server {
    listen 80;
    server_name joshuashneider.com www.joshuashneider.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name joshuashneider.com www.joshuashneider.com;

    ssl_certificate     /etc/letsencrypt/live/joshuashneider.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/joshuashneider.com/privkey.pem;

    location /static/ {
        alias /home/youruser/josh-website/staticfiles/;
    }

    location /media/ {
        alias /home/youruser/josh-website/media/;
    }

    location / {
        proxy_pass http://unix:/tmp/joshsite.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6. TLS — certbot
```bash
certbot --nginx -d joshuashneider.com -d www.joshuashneider.com
```

## Tailwind for production
The dev version uses the Tailwind CDN play script (fine for testing).
For production, switch to the compiled CLI build:
```bash
npm install -D tailwindcss @tailwindcss/typography
npx tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.css --minify
```
Then replace the `<script src="https://cdn.tailwindcss.com">` tag in base.html
with `<link rel="stylesheet" href="{% static 'css/tailwind.css' %}">`.

## Adding Stripe payments (Phase 2)
Install: `pip install stripe`
Set: `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY` in .env
Create a `store` Django app with Product + Order models.
Webhook endpoint at `/store/webhook/` for payment confirmation.
Digital file delivery via signed URLs or email after payment.
