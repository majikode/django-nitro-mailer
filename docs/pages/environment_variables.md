# Environment Variables

Environment variables allow you to configure the application without modifying the source code. This section outlines the available environment variables and their significance.

## List of Environment Variables

### `EMAIL_DB_LOGGING_ENABLED`

- **Description**: Determines whether logging of sent emails to the database is enabled.
- **Accepted Values**: 
  - `true` (default): Logging is enabled.
  - `false`: Logging is disabled.

### `EMAIL_SEND_THROTTLE_MS`

- **Description**: Allows setting a delay in email sending in milliseconds. Useful for avoiding overwhelming the SMTP server.
- **Example Value**: `1000` (represents a delay of 1 second).
- **Default Value**: `0` (no delay).

## How to Use Environment Variables

Environment variables can be used in various ways, depending on the environment in which the application is running:

1. **On a Local Machine**:

    You can set environment variables in the terminal before running the application. For example:

        export EMAIL_DB_LOGGING_ENABLED=true
        export EMAIL_SEND_THROTTLE_MS=1000


2. **In Configuration Files**:

    You can use `.env` files (if you are using a library like `python-dotenv`) to store environment variables:
    
        EMAIL_DB_LOGGING_ENABLED=true
        EMAIL_SEND_THROTTLE_MS=1000


3. **In Docker Containers**:

    You can define environment variables in the `docker-compose.yml` file:

        version: '3.8'
        services:
        app:
            image: your_image
            environment:
            - EMAIL_DB_LOGGING_ENABLED=true
            - EMAIL_SEND_THROTTLE_MS=1000

## Usage in Code

In your application code, you can access these variables using the `os` module:

    import os

    email_db_logging = os.getenv("EMAIL_DB_LOGGING_ENABLED", "true").lower() == "true"
    throttle_delay = int(os.getenv("EMAIL_SEND_THROTTLE_MS", "0"))
