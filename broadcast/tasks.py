from .helpers import send_notifications, check_bin_expiry


def schedule_all(config):
    tasks = config['tasks']
    tasks.schedule(send_notifications,
                   args=(config,),
                   delay=config['notifications.send_interval'],
                   periodic=True)
    tasks.schedule(check_bin_expiry,
                   args=(config,),
                   delay=config['bin.check_interval'],
                   periodic=True)

