import os
import resend

resend.api_key = os.environ.get("RESEND_API_KEY")

SENDER_EMAIL = "PakExplorer AI <onboarding@resend.dev>"  # Resend's default test sender
SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL", "support@pakexplorer.ai")


def send_booking_confirmation(booking, destination_name=None, hotel_name=None, transport_name=None):
    if not resend.api_key:
        print("WARNING: RESEND_API_KEY not set. Skipping email send.")
        return False

    subject = "Your PakExplorer AI Booking is Confirmed!"

    html_body = f"""
    <p>Hi {booking.full_name},</p>
    <p>Great news — your booking has been approved!</p>

    <h3>Booking Details:</h3>
    <ul>
        <li><strong>Destination:</strong> {destination_name or 'N/A'}</li>
        <li><strong>Hotel:</strong> {hotel_name or 'N/A'}</li>
        <li><strong>Transportation:</strong> {transport_name or 'N/A'}</li>
        <li><strong>Travel Date:</strong> {booking.travel_date or 'N/A'}</li>
        <li><strong>Nights:</strong> {booking.nights or 'N/A'}</li>
        <li><strong>Travelers:</strong> {booking.members}</li>
    </ul>

    <p>If you have any questions, feel free to reach out to us at {SUPPORT_EMAIL}.</p>
    <p>Safe travels!<br>PakExplorer AI Team</p>
    """

    try:
        resend.Emails.send({
            "from": SENDER_EMAIL,
            "to": booking.email,
            "subject": subject,
            "html": html_body,
        })
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_ticket_email(booking, destination=None, hotel_name=None, transport_name=None,
                       package_name=None, inclusions=None):
    """
    Sends the full ticket + destination-specific checklist (best time to visit,
    required documents, included/excluded activities, policy notes) to the
    user's email. Triggered by the "Save & Email" button on the User Dashboard
    for an already-approved booking.
    """
    if not resend.api_key:
        print("WARNING: RESEND_API_KEY not set. Skipping email send.")
        return False

    subject = f"Your PakExplorer AI Ticket — Booking #{booking.id}"

    checklist_lines = []
    if destination:
        if destination.best_time_to_visit:
            checklist_lines.append(f"<li>Best time to visit: {destination.best_time_to_visit}</li>")
        if destination.required_documents:
            docs = [d.strip() for d in destination.required_documents.split(",") if d.strip()]
            docs_html = "".join(f"<li>{d}</li>" for d in docs)
            checklist_lines.append(f"<li>Documents required:<ul>{docs_html}</ul></li>")
        if destination.fun_fact:
            checklist_lines.append(f"<li>Good to know: {destination.fun_fact}</li>")

    included_lines = []
    excluded_lines = []
    if destination:
        if destination.included_activities:
            included_lines = [a.strip() for a in destination.included_activities.split(",") if a.strip()]
        if destination.excluded_activities:
            excluded_lines = [a.strip() for a in destination.excluded_activities.split(",") if a.strip()]

    included_html = "".join(f"<li>{a}</li>" for a in included_lines) if included_lines else "<li>N/A</li>"
    excluded_html = "".join(f"<li>{a}</li>" for a in excluded_lines) if excluded_lines else "<li>N/A</li>"
    checklist_html = "".join(checklist_lines) if checklist_lines else "<li>No specific checklist items for this destination.</li>"

    destination_policy = destination.policy_notes if (destination and destination.policy_notes) else None
    inclusions_text = ", ".join(inclusions) if inclusions else "N/A"

    html_body = f"""
    <p>Hi {booking.full_name},</p>
    <p>Here is your confirmed travel ticket and pre-trip checklist.</p>

    <h2>Ticket — Booking #{booking.id}</h2>
    <ul>
        <li><strong>Destination:</strong> {destination.name if destination else 'N/A'}</li>
        <li><strong>Package:</strong> {package_name or 'N/A'}</li>
        <li><strong>Hotel:</strong> {hotel_name or 'N/A'}</li>
        <li><strong>Transportation:</strong> {transport_name or 'N/A'}</li>
        <li><strong>Travelers:</strong> {booking.members}</li>
        <li><strong>Travel Date:</strong> {booking.travel_date or 'N/A'}</li>
        <li><strong>Nights:</strong> {booking.nights or 'N/A'}</li>
        <li><strong>Payment Method:</strong> {booking.payment_method or 'N/A'}</li>
        <li><strong>Total Amount:</strong> Rs. {booking.total_amount if booking.total_amount is not None else 'N/A'}</li>
        <li><strong>What's Included:</strong> {inclusions_text}</li>
    </ul>

    <h3>Pre-Trip Checklist</h3>
    <ul>{checklist_html}</ul>

    <h3>What's Included in This Trip</h3>
    <ul>{included_html}</ul>

    <h3>What's Not Included</h3>
    <ul>{excluded_html}</ul>

    <h3>Terms & Conditions</h3>
    <ul>
        <li>Please carry a valid CNIC (and Nikah Nama if travelling as a couple, where applicable) for verification at check-in.</li>
        <li>Cancellations follow our standard refund policy (see your dashboard for details).</li>
        {f"<li>{destination_policy}</li>" if destination_policy else ""}
        <li>Contact us at {SUPPORT_EMAIL} for any changes to your booking.</li>
    </ul>

    <p>Safe travels!<br>PakExplorer AI Team</p>
    """

    try:
        resend.Emails.send({
            "from": SENDER_EMAIL,
            "to": booking.email,
            "subject": subject,
            "html": html_body,
        })
        return True
    except Exception as e:
        print(f"Failed to send ticket email: {e}")
        return False