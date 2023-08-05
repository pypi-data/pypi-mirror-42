import pendulum

class Task:

    run_every = False
    run_at = False
    run_every_hour = False
    run_every_minute = False
    twice_daily = False
    run_weekly = False

    _date = None

    name = ''

    def __init__(self):
        """
        Should only be on the child class. Also needs to be resolved by the container.
        """

        pass


    def handle(self):
        """
        Fires the task
        """

        pass


    def log(self):
        """
        Log into scheduler cache
        """
        pass


    def should_run(self, date=None):
        """
        If the task should run
        """

        # set the date
        self._set_date()

        if self._verify_run():
            return True

        return False


    def _set_date(self):
        if not self._date:
            self._date = pendulum.now()
            if hasattr(self, 'timezone'):
                self._date.in_timezone(self.timezone)


    def _verify_run(self):
        if self.run_every:
            time = self.run_every.split(' ')

            if time[1] in ('minute', 'minutes'):
                time = int(time[0])
                if self._date.minute == 0 or self._date.minute % time == 0 or time == 1:
                    return True

            elif time[1] in ('hour', 'hours'):
                time = int(time[0])
                if self._date.hour % time == 0 and self._date.minute == 0:
                    return True

            elif time[1] in ('day', 'days'):
                time = int(time[0])
                if self._date.day_of_year % time == 0 and (self._date.hour == 0 and self._date.minute == 0 or self._verify_run_at()):
                    return True
            elif time[1] in ('month', 'months'):
                time = int(time[0])
                if self._date.month % time == 0 and self._date.day == 1 and (self._date.hour == 0 and self._date.minute == 0 or (self._date.day == 0 and self._verify_run_at())):
                    return True

        elif self.run_at:
            return self._verify_run_at()
                
        if self.run_every_minute:
            if self._date.minute / 1  == 1:
                return True
        elif self.run_every_hour:
            if self._date.hour / 1 == 1:
                return True  
        elif self.twice_daily:
            if self._date.hour in self.twice_daily:
                return True
 
        return False

    def _verify_run_every():
        pass
    
    def _verify_run_at(self):
        if self._date.minute < 10:
            minute = "0{}".format(self._date.minute)
        else:
            minute = self._date.minute

        if "{0}:{1}".format(self._date.hour, minute) == self.run_at:
            return True
        
        return False