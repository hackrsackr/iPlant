from crontab import CronTab

# Create a new crontab object
cron = CronTab(tab='')

# Add a new cron job to run the script every day at 6 AM
job = cron.new(command='python /src/main.py')
job.minute.every(2)

# Write the job to the user's crontab
cron.write()