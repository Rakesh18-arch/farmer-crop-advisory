import re

def validate_registration_data(data: dict) -> tuple[bool, str]:
    """Validates registration fields."""
    if not data:
        return False, "Request payload is empty."

    required_fields = ["full_name", "phone_number", "email", "password", "state", "district"]
    for field in required_fields:
        if not data.get(field) or str(data.get(field)).strip() == "":
            return False, f"Missing or empty required field: '{field}'."

    # Validate email
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, data["email"].strip()):
        return False, "Invalid email address format."

    # Validate phone (digits, min length 10)
    phone = re.sub(r"[\s\-\+]", "", str(data["phone_number"]))
    if not phone.isdigit() or len(phone) < 10:
        return False, "Phone number must contain at least 10 digits."

    # Validate password length
    if len(data["password"]) < 6:
        return False, "Password must be at least 6 characters long."

    return True, ""

def validate_login_data(data: dict) -> tuple[bool, str]:
    """Validates login credentials."""
    if not data or not data.get("email") or not data.get("password"):
        return False, "Both email and password are required."
    return True, ""

def validate_soil_inputs(n, p, k, ph, moisture=None) -> tuple[bool, str]:
    """Validates agricultural soil telemetry."""
    try:
        n_val = float(n)
        p_val = float(p)
        k_val = float(k)
        ph_val = float(ph)
    except (ValueError, TypeError):
        return False, "N, P, K, and pH must be valid numbers."

    if not (0 <= n_val <= 300):
        return False, "Nitrogen (N) value must be between 0 and 300 kg/ha."
    if not (0 <= p_val <= 300):
        return False, "Phosphorus (P) value must be between 0 and 300 kg/ha."
    if not (0 <= k_val <= 300):
        return False, "Potassium (K) value must be between 0 and 300 kg/ha."
    if not (0 <= ph_val <= 14):
        return False, "Soil pH must be between 0.0 and 14.0."

    if moisture is not None:
        try:
            m_val = float(moisture)
            if not (0 <= m_val <= 100):
                return False, "Soil moisture must be between 0% and 100%."
        except (ValueError, TypeError):
            return False, "Soil moisture must be a numeric percentage."

    return True, ""

def validate_environmental_inputs(temperature, humidity, rainfall) -> tuple[bool, str]:
    """Validates weather / environmental variables."""
    try:
        t_val = float(temperature)
        h_val = float(humidity)
        r_val = float(rainfall)
    except (ValueError, TypeError):
        return False, "Temperature, humidity, and rainfall must be valid numbers."

    if not (-10 <= t_val <= 60):
        return False, "Temperature must be between -10°C and 60°C."
    if not (0 <= h_val <= 100):
        return False, "Relative humidity must be between 0% and 100%."
    if not (0 <= r_val <= 1000):
        return False, "Rainfall must be between 0 mm and 1000 mm."

    return True, ""

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Checks if the uploaded file has a permissible extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
