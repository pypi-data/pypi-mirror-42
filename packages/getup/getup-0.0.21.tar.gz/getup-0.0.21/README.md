
# Getup

Projectless Django setup tool. Getup combines functionality of manage.py and wsgi module. It allows one Django app to be used as a service.

See Gitlab repository for app examples.

## Getup config command

Run `getup/up.py` or add as package to virtual env. It will work everywhere there's a Django app with configuration instantiation.

All settings can be set by configuration object or using environment variables or both. Configuration object is a Pydantic schema along with extension schemas. See `getup/conf.py` for complete set or accompanying example apps. This schema corresponds to usual Django settings.
