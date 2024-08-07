import os
from dotenv import load_dotenv
from sinch import SinchClient

def send_sms(recipient, message_body):
    load_dotenv()

    key_id = os.getenv('KEY_ID')
    key_secret = os.getenv('KEY_SECRET')
    project_id = os.getenv('PROJECT_ID')
    client = SinchClient(key_id, key_secret, project_id)
    sinch_number = "+447520651503"

    message_body_str = ', '.join([f"{key}: {value}" for key, value in message_body.items()])

    message = client.sms.batches.send(
        body= message_body_str,
        from_= sinch_number,
        to=[recipient],
        delivery_report="none"
    )
    print(f"Message sent: {message}")