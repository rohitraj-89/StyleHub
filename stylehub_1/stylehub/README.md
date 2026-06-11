# StyleHub - Django Fashion Store

## Quick Setup (5 minutes)

### Step 1: Install Django
```bash
pip install Django Pillow
```

### Step 2: Project Setup
```bash
cd stylehub
python manage.py makemigrations users
python manage.py makemigrations store
python manage.py migrate
```

### Step 3: Seed Sample Data (40 products + users)
```bash
python manage.py seed_data
```

### Step 4: Run Server
```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## Login Credentials

| Role  | Username | Password |
|-------|----------|----------|
| Admin | admin    | admin123 |
| Staff | staff1   | staff123 |
| User  | user1    | user123  |

---

## Features

- **Home Page** - 5 categories with 8 products each, hero banner, offers
- **Category Pages** - Women, Men, Kids, Boys, Shoes with sort filters
- **Product Detail** - Full details, related products, ratings
- **Cart** - Add/remove/update quantities
- **Checkout** - Address form, payment options
- **Orders** - Order history, order tracking status
- **Login** - Role-based login (Admin/Staff/User dropdown)
- **Signup** - New user registration (actually works)
- **Dashboard** - Admin & Staff stats, orders table, inventory
- **Profile** - Edit personal details & default address

## Project Structure

```
stylehub/
├── manage.py
├── requirements.txt
├── stylehub/          # Django project settings
│   ├── settings.py
│   └── urls.py
├── store/             # Main shopping app
│   ├── models.py      # Product, Cart, Order, OrderItem
│   ├── views.py       # All store views
│   ├── urls.py        # Store URLs
│   ├── admin.py
│   └── management/commands/seed_data.py
├── users/             # Auth app
│   ├── models.py      # CustomUser with roles
│   ├── views.py       # Login, Signup, Dashboard, Profile
│   ├── urls.py
│   └── forms.py
└── templates/
    ├── base.html      # Navbar, footer, layout
    ├── store/         # Home, category, product, cart, checkout, orders
    └── users/         # Login, signup, dashboard, profile
```

## Color Theme
- Primary: #e8470a (burnt orange - casual, not Flipkart blue)
- Accent: #ff9f1c (golden yellow)
- Dark: #1a1a2e (navy dark)
- Background: #f7f3ef (warm cream)
