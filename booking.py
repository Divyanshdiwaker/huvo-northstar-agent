def book_site_visit(date, time, should_succeed=True):
    """
    Simulates a site-visit booking.
    """

    if should_succeed:
        return {
            "success": True,
            "message": f"Site visit booked for {date} at {time}."
        }

    return {
        "success": False,
        "message": "The site-visit booking could not be completed."
    }