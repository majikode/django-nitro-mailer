# About the Application

This application is designed to manage the sending of email messages in an organized and efficient manner. It serves as a system that enables:

1. **Storage of Email Messages**: 

    The application utilizes the `Email` model to store email data, including recipients, subject, and sending priority. This allows for managing the order of email dispatch based on their priorities.

2. **Logging of Email Sends**: 

    Each email sent is logged in the `EmailLog` model, enabling tracking of successes and failures in sending. The logs contain information about the status (success or failure) along with details about the sent message.

3. **Sending Email Messages**: 

    The application supports various methods for sending emails. It includes two backend classes:

    - `DatabaseBackend`: This class saves messages to the database.
    - `SyncBackend`: This class sends email messages synchronously, with optional throttling between sends, allowing adaptation to external mail server requirements.

4. **Email Delivery Throttling**: 

    The throttling mechanism allows for introducing delays between email sends, preventing server overload and controlling the throughput of the sending process.

5. **Priority Management**: 

    By allowing the setting of priorities for messages, the application can adjust the order of dispatch, which is particularly useful when not all messages can be sent simultaneously.


