import app
from datetime import datetime

def datetimeformat(value, format="%Y-%m-%d"):
    if value is None:
        return ""
    return value.strftime(format)

# Register the custom filter with Jinja2
app.jinja_env.filters['datetimeformat'] = datetimeformat