def detect_area(text):
    areas = [
        "Roof", "Attic", "Hall", "Bedroom", "Kitchen", "Bathroom", "Balcony", "Parking", 
        "Living Room", "Dining Room", "Stairs", "Basement", "Exterior", "Interior",
        "Foundation", "Plumbing", "Electrical", "HVAC", "Garage", "Driveway"
    ]

    for area in areas:
        if area.lower() in text.lower():
            return area

    return "General"