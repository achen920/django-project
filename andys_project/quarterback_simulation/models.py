from django.db import models
import random

class Team_db(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    history = models.CharField(max_length=20)

class Coach_db(models.Model):
    name = models.CharField(max_length=100)
    experience = models.IntegerField()

    def motivate(self, quarterback):
        # function to motivate the quarterback
        quarterback.improve()

    def demotivate(self, quarterback):
        # function to demotivate the quarterback
        quarterback.regress()

class Skillset_db(models.Model):
    throw_accuracy = models.IntegerField()
    pocket_awareness = models.IntegerField()
    arm_strength = models.IntegerField()
    speed = models.IntegerField()

    def improve_skill(self, skill_name):
        # increment the specified skill by 1
        setattr(self, skill_name, getattr(self, skill_name) + 1)

    def regress_skill(self, skill_name):
        # decrement the specified skill by 1
        setattr(self, skill_name, getattr(self, skill_name) - 1)

class CareerStats_db(models.Model):
    games_played = models.IntegerField()
    pass_attempts = models.IntegerField()
    pass_completions = models.IntegerField()
    pass_yards = models.IntegerField()
    pass_touchdowns = models.IntegerField()
    rush_yards = models.IntegerField()
    rush_touchdowns = models.IntegerField()
    interceptions = models.IntegerField()

class Quarterback_db(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    coach = models.ForeignKey(Coach_db, on_delete=models.CASCADE)
    team = models.ForeignKey(Team_db, on_delete=models.CASCADE)
    experience = models.IntegerField()
    skillset = models.ForeignKey(Skillset_db, on_delete=models.CASCADE)
    career_stats = models.ForeignKey(CareerStats_db, on_delete=models.CASCADE)

    def improve(self):
        # function to simulate improvement in skills over time
        skill_to_improve = random.choice(['throw_accuracy', 'pocket_awareness', 'arm_strength', 'speed'])
        self.skillset.improve_skill(skill_to_improve)  # increase the selected skill by 1

    def regress(self):
        # function to simulate decline in skills over time
        skill_to_regress = random.choice(['throw_accuracy', 'pocket_awareness', 'arm_strength', 'speed'])
        self.skillset.regress_skill(skill_to_regress)  # decrease the selected skill by 1

class HallOfFame_db(models.Model):
    quarterback = models.ForeignKey(Quarterback_db, on_delete=models.CASCADE)

    def is_eligible(self, career_stats):
        if (career_stats.pass_yards >= 50000 and         
            career_stats.pass_touchdowns >= 300 and
            career_stats.rush_yards >= 2500 and
            career_stats.rush_touchdowns >= 50 and
            career_stats.interceptions <= 350):
            return True
        else:
            return False
