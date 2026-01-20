from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Deleting old data...'))
            # Delete in order: Activity, Leaderboard, Workout, User, Team (individually)
            for obj in Activity.objects.all():
                obj.delete()
            for obj in Leaderboard.objects.all():
                obj.delete()
            for obj in Workout.objects.all():
                obj.delete()
            for obj in User.objects.all():
                obj.delete()
            for obj in Team.objects.all():
                obj.delete()

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
            dc = Team.objects.create(name='DC', description='DC Superheroes')

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            users = [
                User.objects.create(email='tony@stark.com', name='Iron Man', team=marvel, is_superhero=True),
                User.objects.create(email='steve@rogers.com', name='Captain America', team=marvel, is_superhero=True),
                User.objects.create(email='bruce@wayne.com', name='Batman', team=dc, is_superhero=True),
                User.objects.create(email='clark@kent.com', name='Superman', team=dc, is_superhero=True),
            ]

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(user=users[0], type='Flight', duration=60, date='2023-01-01')
            Activity.objects.create(user=users[1], type='Shield Training', duration=45, date='2023-01-02')
            Activity.objects.create(user=users[2], type='Martial Arts', duration=50, date='2023-01-03')
            Activity.objects.create(user=users[3], type='Strength Training', duration=70, date='2023-01-04')

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            w1 = Workout.objects.create(name='Super Strength', description='Strength workout for superheroes')
            w2 = Workout.objects.create(name='Flight Practice', description='Flight workout for superheroes')
            w1.suggested_for.set([marvel, dc])
            w2.suggested_for.set([marvel])

            self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
            Leaderboard.objects.create(team=marvel, score=200)
            Leaderboard.objects.create(team=dc, score=180)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
