# LogiCommerce

LogiCommerce is a comprehensive web application designed to streamline logistics and e-commerce operations. Built using the Django framework, this project incorporates features like customer management, supplier tracking, shipping logistics, and notification systems.

## Features

- **Customer Management**: Keep track of customer details and interactions.
- **Supplier Tracking**: Manage and monitor suppliers seamlessly.
- **Shipping Logistics**: Organize shipping companies, oil tankers, and port authorities.
- **Notification System**: Stay updated with notifications about critical events or actions.
- **Dynamic Templates**: User-friendly interface built with HTML templates.

## Installation

Follow these steps to set up and run the project locally:

### Prerequisites
- Python (version 3.8 or higher)
- pip (Python package manager)
- A virtual environment (recommended)

### Steps

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/talhaStti/Ship_Track_Pro
   cd LogiCommerce
   ```

2. **Set up a Virtual Environment**  
   ```bash
   python -m venv env
   source env/bin/activate    # For Linux/macOS
   env\Scripts\activate       # For Windows
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**  
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000`.

## Project Structure

```
LogiCommerce/
├── CustomAuthority/
├── Customer/
├── db.sqlite3
├── eCom/
├── manage.py
├── media/
├── notification/
├── OilTanker/
├── PortAuthority/
├── ShippingCompany/
├── signup/
├── static/
├── Supplier/
├── templates/
└── requirements.txt
```

- **Apps**: CustomAuthority, Customer, OilTanker, etc.
- **Database**: SQLite database to store data.
- **Static Files**: CSS, JS, and image assets.
- **Templates**: HTML templates for frontend rendering.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any bug fixes or enhancements.

## License

This project is open-source and available under the MIT License. Feel free to use and modify it.

---

## Contact

For questions or suggestions, contact:  
- **Name**: Talha Satti  
- **Email**: [basittalha181@gmail.com]  
- **GitHub**: [talhaStti](https://github.com/talhaStti)  
