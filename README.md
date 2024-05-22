For running cronjob :

crontab -e

# Add the following line to run the command every Sunday at midnight
0 0 * * SUN /path/to/your/virtualenv/bin/python /path/to/your/project/manage.py export_data
