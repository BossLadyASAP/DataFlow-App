# INF232 EC2 - Data Collection and Analysis Application

## Overview

This is a **Python Flask-based web application** designed for the INF232 EC2 course (Analyse de Données). The application provides a simple yet robust platform for collecting customer feedback and performing descriptive statistical analysis on the collected data.

## Features

### Core Functionality
- **Online Data Collection**: User-friendly web form for submitting feedback
- **Descriptive Statistics**: Comprehensive analysis of collected data including:
  - Total number of responses
  - Average rating
  - Median and mode calculations
  - Standard deviation
  - Rating distribution
  - Minimum and maximum values
- **Data Export**: Export collected data and statistics as JSON

### User Interface
- **Multilingual Support**: Full support for English and French
- **Dark Mode**: Toggle between light and dark themes for comfortable viewing
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Intuitive Navigation**: Easy-to-use interface with clear navigation

### Technical Features
- **Robust Error Handling**: Comprehensive error management and validation
- **Secure Data Storage**: SQLite database for reliable data persistence
- **RESTful API**: Clean API endpoints for data operations
- **Session Management**: Persistent user preferences (language, theme)

## Project Structure

```
inf232_ec2_app/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── feedback.db                     # SQLite database (auto-created)
├── app/
│   ├── templates/
│   │   ├── base.html              # Base template with navigation
│   │   ├── index.html             # Home page with feedback form
│   │   ├── analytics.html         # Analytics and statistics page
│   │   ├── 404.html               # 404 error page
│   │   └── 500.html               # 500 error page
│   └── static/
│       ├── css/
│       │   └── style.css          # Main stylesheet (light & dark mode)
│       └── js/
│           └── main.js            # JavaScript for interactivity
└── README.md                       # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd inf232_ec2_app
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

## Usage

### Submitting Feedback
1. Navigate to the **Home** page
2. Fill in the feedback form:
   - **Product/Service**: Enter the product or service name
   - **Rating**: Click on stars to rate (1-5)
   - **Comments**: (Optional) Add detailed feedback
3. Click **Submit Feedback**
4. Your feedback will be recorded and you'll see a success message

### Viewing Analytics
1. Click on the **Analytics** link in the navigation
2. View descriptive statistics:
   - Total responses count
   - Average rating
   - Highest and lowest ratings
   - Rating distribution chart
   - Additional statistics (median, mode, standard deviation)
3. Browse recent feedback submissions
4. Export data as JSON using the **Export Data** button

### Language Switching
- Use the language dropdown in the top navigation
- Available languages: English, Français
- Your preference is saved in the session

### Dark Mode
- Click the moon icon in the top navigation to toggle dark mode
- Your preference is saved in browser localStorage
- The app respects your system's dark mode preference by default

## API Endpoints

### Submit Feedback
**POST** `/api/feedback`
```json
{
  "product": "Product Name",
  "rating": 4,
  "comment": "Great product!"
}
```

### Get Statistics
**GET** `/api/stats`
Returns descriptive statistics of all feedback

### Get Recent Feedback
**GET** `/api/feedback`
Returns the 20 most recent feedback entries

### Change Language
**GET** `/api/language/<lang>`
Sets the application language (en or fr)

### Export Data
**GET** `/api/export`
Exports all feedback and statistics as JSON

## Data Analysis Features

The application performs the following descriptive analyses:

| Statistic | Description |
|-----------|-------------|
| **Count** | Total number of feedback submissions |
| **Mean** | Average rating value |
| **Median** | Middle value when ratings are sorted |
| **Mode** | Most frequently occurring rating |
| **Std Dev** | Standard deviation (measure of spread) |
| **Min/Max** | Minimum and maximum ratings |
| **Distribution** | Count of each rating (1-5 stars) |

## Technical Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python Flask 2.3.3 |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Icons** | Font Awesome 6.4.0 |
| **Styling** | Custom CSS with CSS Variables |

## Design Highlights

### Light & Dark Mode
- Automatic theme detection based on system preferences
- Manual toggle available in the navigation
- Smooth transitions between themes
- Carefully chosen color palettes for both modes

### Responsive Design
- Mobile-first approach
- Breakpoints for tablet and desktop
- Touch-friendly interface elements
- Optimized for all screen sizes

### Accessibility
- Semantic HTML structure
- Clear visual hierarchy
- Keyboard navigation support
- Color-blind friendly design

## Deployment

### Local Deployment
```bash
python app.py
```

### Production Deployment
For production deployment, consider using:
- **Gunicorn**: WSGI HTTP Server
- **Nginx**: Reverse proxy
- **Docker**: Containerization
- **Heroku/PythonAnywhere**: Cloud platforms

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Database

The application uses SQLite for data persistence. The database file (`feedback.db`) is automatically created on first run.

### Database Schema
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Security Considerations

- Input validation on all form submissions
- SQL injection prevention using parameterized queries
- CSRF protection through Flask sessions
- Secure session management
- Error handling without exposing sensitive information

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
python app.py --port 8000
```

### Database Issues
To reset the database:
```bash
rm feedback.db
python app.py
```

### Language Not Changing
- Clear browser cookies
- Try a different browser
- Check browser console for errors

## Future Enhancements

- User authentication and roles
- Advanced data visualization (charts, graphs)
- Data filtering and search
- Bulk data import/export
- Email notifications
- API rate limiting
- Database backup functionality

## License

This project is created for educational purposes as part of the INF232 EC2 course.

## Support & Contact

For questions or issues, please contact the course instructor:
- **Email**: rollinfrancis28@gmail.com

## Course Information

- **Course**: INF232 - Analyse de Données
- **Topic**: Data Collection and Descriptive Analysis
- **Institution**: University/Educational Institution

---

**Last Updated**: April 2026
**Version**: 1.0.0
