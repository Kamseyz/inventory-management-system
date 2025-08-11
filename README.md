# Mazi Inventory Management System (IMS)

A modern inventory management system built with Django, Bootstrap, and AJAX. Mazi IMS helps businesses streamline stock management, order processing, and user access control with a beautiful, responsive interface.

## Features

- **Custom User System:** Email-based login, roles (Admin/Worker), access control.
- **Product Management:** Add, edit, delete products; low stock alerts; product search.
- **Order Management:** Place orders, prevent over-ordering, automatic stock deduction, order history.
- **Dashboards:** Separate dashboards for Admin and Worker, with quick stats and recent activity.
- **Reporting:** View sales, revenue, and low stock items; export data to CSV.
- **Profile & Authentication:** User profile page, secure login/logout.
- **Responsive UI:** Built with Bootstrap 5 and modern design elements.

## Usage

- **Admin:** Can manage products, view orders, access all dashboards, and create accounts for workers.  
- **Worker:** Can view inventory, place orders, see assigned tasks.  
- **Note:** Self-registration is disabled. Only the admin (superuser) can create accounts for workers via the admin dashboard.

## Project Structure

```
ims/
  core/           # Product and order logic
  users/          # Custom user model, authentication
  templates/      # HTML templates (base, dashboard, worker, accounts)
  static/         # CSS, JS, images
  manage.py       # Django management script
  db.sqlite3      # SQLite database
myenv/            # Python virtual environment
requirements.txt  # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd IMS
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```sh
   python ims/manage.py migrate
   ```

5. **Create a superuser:**
   ```sh
   python ims/manage.py createsuperuser
   ```

6. **Run the development server:**
   ```sh
   python ims/manage.py runserver
   ```

7. **Access the app:**
   - Visit [http://localhost:8000/](http://localhost:8000/) in your browser.



## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

---

> Built with Django, Bootstrap, and love by Ebuka.