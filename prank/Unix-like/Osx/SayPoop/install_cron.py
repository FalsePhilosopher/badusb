from crontab import CronTab

user_cron = CronTab(user=True)
sys_cron = CronTab()

# edit this line if you want a different command
job = user_cron.new(command = 'say poop')
job.minute.every(30)

# sample pranks

# every 30 minutes say poop
# job = user_cron.new(command = 'say poop')
# job.minute.every(30)

# every 6 hours open dog thing YouTube video
# job = user_cron.new(command = 'open https://www.youtube.com/watch?v=taWzoLpdxaI')
# job.setall('6 */4 * * *');

# every time the computer reboots, rick roll em
# job = user_cron.new(command = 'open https://www.youtube.com/watch?v=dQw4w9WgXcQ')
# job.every_reboot()


job.enable()
if job.is_valid():
   user_cron.write()