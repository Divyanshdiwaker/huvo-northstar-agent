def generate_analytics(messages):
    """
    Extract simple lead information from the conversation.
    No AI/API call is used here.
    """

    conversation = ""

    for message in messages:
        conversation += message["content"].lower() + " "

    analytics = {
        "budget": "Not provided",
        "configuration": "Not provided",
        "purpose": "Not provided",
        "interest_level": "Unknown",
        "site_visit_status": "Not requested",
        "follow_up_required": False,
        "language": "English",
    }


    # --------------------------------------------------
    # BUDGET
    # --------------------------------------------------

    budget_values = [
        "1 crore",
        "1.25 crore",
        "1.5 crore",
        "1.75 crore",
        "2 crore",
        "2.5 crore",
        "3 crore",
    ]

    for budget in budget_values:

        if budget in conversation:

            analytics["budget"] = f"₹{budget}"
            break


    # --------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------

    if (
        "3 bhk" in conversation
        or "3bhk" in conversation
        or "three bhk" in conversation
    ):

        analytics["configuration"] = "3 BHK"

    elif (
        "2 bhk" in conversation
        or "2bhk" in conversation
        or "two bhk" in conversation
    ):

        analytics["configuration"] = "2 BHK"


    # --------------------------------------------------
    # PURPOSE
    # --------------------------------------------------

    if any(
        phrase in conversation
        for phrase in [
            "self use",
            "self-use",
            "for myself",
            "for my family",
            "to live"
        ]
    ):

        analytics["purpose"] = "Self-use"

    elif any(
        phrase in conversation
        for phrase in [
            "investment",
            "invest",
            "rental income",
            "rent it out"
        ]
    ):

        analytics["purpose"] = "Investment"


    # --------------------------------------------------
    # INTEREST LEVEL
    # --------------------------------------------------

    if any(
        phrase in conversation
        for phrase in [
            "not interested",
            "don't want",
            "do not want",
            "no interest",
            "not looking"
        ]
    ):

        analytics["interest_level"] = "Not interested"

    elif any(
        phrase in conversation
        for phrase in [
            "site visit",
            "book a visit",
            "schedule a visit",
            "want to visit",
            "like to visit",
            "interested"
        ]
    ):

        analytics["interest_level"] = "High"

    elif any(
        phrase in conversation
        for phrase in [
            "maybe",
            "thinking",
            "considering",
            "just exploring"
        ]
    ):

        analytics["interest_level"] = "Medium"


    # --------------------------------------------------
    # SITE VISIT
    # --------------------------------------------------

    if any(
        phrase in conversation
        for phrase in [
            "booked for",
            "site visit has been booked",
            "site visit is booked"
        ]
    ):

        analytics["site_visit_status"] = "Booked"

    elif any(
        phrase in conversation
        for phrase in [
            "site visit",
            "book a visit",
            "schedule a visit",
            "want to visit"
        ]
    ):

        analytics["site_visit_status"] = "Requested"


    # --------------------------------------------------
    # FOLLOW-UP
    # --------------------------------------------------

    if any(
        phrase in conversation
        for phrase in [
            "call me later",
            "contact me later",
            "call me tomorrow",
            "contact me tomorrow",
            "follow up",
            "follow-up",
            "get back to me"
        ]
    ):

        analytics["follow_up_required"] = True


    # --------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------

    hindi_words = [
        "mujhe",
        "chahiye",
        "aap",
        "haan",
        "nahi",
        "karna",
        "raha",
        "rahi",
        "kya",
        "mera",
        "meri",
        "hai",
    ]

    hindi_count = sum(
        f" {word} " in f" {conversation} "
        for word in hindi_words
    )

    if hindi_count >= 2:
        analytics["language"] = "Hindi/Hinglish"


    return analytics