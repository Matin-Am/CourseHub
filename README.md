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
- **Database**: PostgreSQL
- **Asynchronous Tasks**: Celery + RabbitMQ (if used)
- **Storage**: ArvanCloud (S3-compatible bucket)
- **Docs**: drf-spectacular (OpenAPI/Swagger)
- **Other**: Custom user model, sessions, signals, throttling, etc.

---

# Project Structure

```bash
CourseHub/
├── accounts/           # User registration, login, verification
├── home/               # Courses, episodes, comments
├── order/              # Cart, orders, coupons
├── media/              # Uploaded videos/images
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates (password reset, etc.)
├── my_project/         # Core Django settings and URLs
├── utils.py            # Helper classes for sessions/emails
├── bucket.py           # S3/ArvanCloud file manager
├── .env                # Environment variables
└── manage.py
