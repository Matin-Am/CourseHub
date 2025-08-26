# CourseHub

CourseHub is a web-based e-learning platform built with Django. It allows users to register, browse courses, watch video lessons, and manage their accounts securely. The project includes features like JWT authentication, email verification, comment system, order/payment handling, and admin functionalities.

---

# Features

-  **User Registration & Login** (with email OTP verification)
-  **JWT Authentication** using `SimpleJWT`
-  **Email Services** (verification & password reset via Gmail SMTP)
-  **Course & Episode Management** (video upload, duration calculation)
-  **Comment System** with support for replies
-  **Shopping Cart** and Order system
-  **Zarin Pal Gateway** for Payment (Sandbox mode)
-  **Coupon Support** for discounts
-  **File Storage** using Arvan Cloud (compatible with AWS S3)
-  **API Documentation** with Swagger and Redoc via `drf-spectacular`
-  **Rate Limiting / Throttling** to prevent abuse
-  Custom validations and session handling
- 🛠 Built with `PostgreSQL` and support for scaling with `Celery`

---

# Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: PostgreSQL, Redis(for caching)
- **Asynchronous Tasks**: Celery + RabbitMQ (if used)
- **Storage**: ArvanCloud (S3-compatible bucket)
- **Docs**: drf-spectacular (OpenAPI/Swagger)
- **Other**: Custom user model, sessions, signals, throttling, etc.

---

# Project Structure

```bash
CourseHub/
├── accounts/           # User registration, login, verification, OTP
│   ├── models.py       # Custom User model
│   ├── views.py        # Login/Signup views
│   ├── tasks.py        # Celery tasks (e.g., send emails/SMS)
│   ├── signals.py      # User-related signals
│   └── serializers.py  # DRF serializers
│
├── home/               # Courses, episodes, comments
│   ├── models.py       # Course & Episode models
│   ├── views.py        # Course list/detail
│   ├── serializers.py  # DRF serializers
│   └── permissions.py  # Custom permissions
│
├── order/              # Cart, orders, coupons
│   ├── cart.py         # Session-based cart
│   ├── models.py       # Order, Coupon
│   ├── views.py        # Checkout flow
│   └── context_processors.py  # Cart context
│
├── my_project/         # Core Django project
│   ├── settings.py     # Django settings
│   ├── urls.py         # Project URLs
│   ├── celery_conf.py  # Celery configuration
│   └── wsgi.py         # WSGI entry point
│
├── templates/          # Global HTML templates
│   ├── base.html       # Base layout
│   ├── 403.html        # Forbidden page
│   └── inc/            # Reusable partials (navbar, messages)
│
├── static/             # Static files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript
│   └── img/            # Images
│
├── media/              # Uploaded media files (videos, images)
│
├── utils.py            # Helper classes (sessions, emails, etc.)
├── bucket.py           # S3/ArvanCloud file manager
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker services (backend, db, redis, rabbitmq)
├── Dockerfile          # Backend image definition
├── manage.py           # Django management script
└── .env                # Environment variables

