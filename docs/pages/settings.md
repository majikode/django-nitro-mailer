# Settings

`django-nitro-mailer` allows you to configure its behavior using Django settings. 

You can set these settings in your Django project's `settings.py` file.

## Settings list

### `NITRO_EMAIL_DATABASE_LOGGING`

- **Default**: `True`
- **Description**: Enables or disables logging the result of sending an email to the database. If disabled, sending will still be logged, but only in the module logger.

### `NITRO_EMAIL_SEND_THROTTLE_MS`

- **Default**: `0`
- **Description**: The minimum time in **milliseconds** between sending emails. This setting is used to throttle the sending of emails. Useful to avoid hitting rate limits of email providers. Set to `0` to disable throttling.

