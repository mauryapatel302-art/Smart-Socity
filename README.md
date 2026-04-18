# 🏘️ Smart Society

A full-featured **Apartment & Society Management System** built with Django. Smart Society digitizes the day-to-day operations of a residential society — from billing and complaints to visitor management and community events — with dedicated dashboards for each user role.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [User Roles](#-user-roles)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [Database Seeding](#-database-seeding)
- [Modules Overview](#-modules-overview)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **Role-based access control** — Secretary, Resident, and Security Guard roles with separate dashboards
- **Billing & Payments** — Monthly maintenance bill generation, payment tracking (UPI / Card / Cash), late fine support, and payment receipts
- **Complaints Management** — Residents can raise complaints with photos; Secretary tracks and updates status
- **Notices & Announcements** — Post categorized notices (Emergency, General, Maintenance, Event) with file attachments and expiry dates
- **Events & Polls** — Create society events with RSVP, and community polls with live voting
- **Visitor Management** — Temporary and permanent gate pass system; Security guards log visitor entry/exit
- **Resident Directory** — Wing and flat-based resident listing with parking slot info
- **Emergency Contacts** — Quick-access emergency contact widget on dashboards
- **Profile Management** — Profile photo upload, personal info editing
- **Admin Panel** — Full Django admin interface for superuser management

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.x, Django 5.x |
| Database | SQLite (default) |
| Frontend | HTML5, Bootstrap 5, CSS3 |
| Forms | django-crispy-forms + crispy-bootstrap5 |
| Image Handling | Pillow |
| Environment | python-dotenv |

---

## 📁 Project Structure

```
smartsociety/           ← Django project config (settings, urls, wsgi)
accounts/               ← Custom user model, auth, role-based login & signup
core/                   ← Wings, Flats, Parking, Notices, Emergency Contacts
billing/                ← Maintenance bills, payments, receipts
complaints/             ← Complaint submission and tracking
events/                 ← Events, RSVPs, Polls, Voting
visitors/               ← Visitor logs, Gate pass requests
templates/              ← All HTML templates organized by app
static/                 ← CSS, JS, and image assets
media/                  ← User-uploaded files (profile photos, attachments)
manage.py
init_db.py              ← Script to initialize database structure
seed_db.py              ← Script to seed demo data
requirements.txt
```

---

## 👥 User Roles

| Role | Capabilities |
|---|---|
| **Secretary** | Full access — manage bills, update complaint status, post notices, create events/polls, view all residents |
| **Resident** | View & pay bills, raise complaints, view notices, RSVP to events, vote in polls, manage gate passes |
| **Security Guard** | Log visitor entry/exit, view and verify gate passes, access security dashboard |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/smart-society.git
   cd smart-society
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** *(for admin panel access)*
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit** `http://127.0.0.1:8000/`

---

## ⚙️ Configuration

Key settings in `smartsociety/settings.py`:

| Setting | Default | Description |
|---|---|---|
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `[]` | Add your domain/IP for production |
| `DATABASE` | SQLite (`db.sqlite3`) | Can be swapped for PostgreSQL |
| `MEDIA_ROOT` | `media/` | Storage for uploaded files |
| `AUTH_USER_MODEL` | `accounts.CustomUser` | Custom user model |
| `LOGIN_URL` | `/` | Redirects unauthenticated users |
| `LOGIN_REDIRECT_URL` | `/dashboard/` | Post-login redirect |

> ⚠️ **Important:** The `SECRET_KEY` in `settings.py` is for development only. Always use a secure, environment-variable-based key in production and set `DEBUG = False`.

---

## 🌱 Database Seeding

The project includes two helper scripts:

```bash
# Initialize base database structure (wings, flats, parking slots)
python init_db.py

# Seed with demo users and sample data
python seed_db.py
```

These are helpful for quickly spinning up a demo environment.

---

## 📦 Modules Overview

### `accounts`
- Custom `CustomUser` model extending Django's `AbstractUser`
- Fields: `role`, `phone`, `profile_photo`, `flat` (FK), `is_on_duty`
- Role-specific signup forms for Secretary, Resident, and Security Guard
- Universal login page with role verification

### `core`
- **Wing** & **Flat** models — society structure
- **ParkingSlot** — one-to-one assignment per flat
- **Notice** — categorized announcements with date range and file attachments
- **EmergencyContact** — quick-access emergency numbers

### `billing`
- **MaintenanceBill** — per flat, per month/year, with due date and late fine
- **Payment** — linked to a bill; supports UPI, Card, Cash with transaction ID
- Bill generation (Secretary), payment (Resident), receipt download

### `complaints`
- **Complaint** — raised by residents with title, description, category, photo
- Categories: Plumbing, Electricity, Parking, Noise, Other
- Status flow: `OPEN` → `IN_PROGRESS` → `RESOLVED` (managed by Secretary)

### `events`
- **Event** — title, date, time, venue, description
- **EventRSVP** — residents confirm attendance
- **Poll** — question with multiple options
- **PollVote** — one vote per resident per poll

### `visitors`
- **VisitorLog** — entry/exit log managed by Security Guard
- **GatePassRequest** — residents pre-authorize visitors
  - `TEMPORARY`: valid for a specific date
  - `PERMANENT`: active until cancelled by the resident

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please make sure your code follows the existing style and includes relevant comments.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built as part of a B.Tech Computer Science project. Feedback and suggestions are always welcome!
