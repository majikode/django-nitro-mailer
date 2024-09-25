# Email Sending Guide

This documentation covers how to send emails using the two available backends, `SyncBackend` and `DatabaseBackend`, as well as how to configure throttling and logging features.

## Available Backends

### SyncBackend

The `SyncBackend` is designed for synchronous email sending. When using this backend, emails are sent immediately, and the application waits for a response from the email server to confirm whether the email was successfully delivered or failed.

#### How to Use `SyncBackend`

To send emails synchronously using `SyncBackend`, you need to create an `EmailMessage` object and pass it to the backend's connection.

