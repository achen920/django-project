import random

class Quarterback:
    def __init__(self, name, age, coach, team, experience, skillset, career_stats):
        self.name = name
        self.age = age
        self.coach = coach
        self.team = team
        self.experience = experience
        self.skillset = skillset
        self.career_stats = career_stats

    def improve(self):
        # function to simulate improvement in skills over time
        skill_to_improve = random.choice(['throw_accuracy', 'pocket_awareness', 'arm_strength', 'speed'])
        self.skillset.improve_skill(skill_to_improve)  # increase the selected skill by 1

    def regress(self):
        # function to simulate decline in skills over time
        skill_to_regress = random.choice(['throw_accuracy', 'pocket_awareness', 'arm_strength', 'speed'])
        self.skillset.regress_skill(skill_to_regress)  # decrease the selected skill by 1

class HallOfFame:
    def __init__(self, quarterback):
        self.quarterback = quarterback

    def is_eligible(self, career_stats):
        # setting thresholds for Hall of Fame eligibility
        if (career_stats["pass_yards"] >= 50000 and         
            career_stats["pass_touchdowns"] >= 300 and
            career_stats["rush_yards"] >= 2500 and
            career_stats["rush_touchdowns"] >= 50 and
            career_stats["interceptions"] <= 350):
            return True
        else:
            return False

class CareerStats:
    def __init__(self, games_played, pass_attempts, pass_completions, pass_yards, pass_touchdowns, rush_yards, rush_touchdowns, interceptions):
        self.games_played = games_played
        self.pass_attempts = pass_attempts
        self.pass_completions = pass_completions
        self.pass_yards = pass_yards
        self.pass_touchdowns = pass_touchdowns
        self.rush_yards = rush_yards
        self.rush_touchdowns = rush_touchdowns
        self.interceptions = interceptions

class Team:
    def __init__(self, name, location, history):
        self.name = name
        self.location = location
        self.history = history

class Coach:
    def __init__(self, name, experience):
        self.name = name
        self.experience = experience

    def motivate(self, quarterback):
        # function to motivate the quarterback
        quarterback.improve()

    def demotivate(self, quarterback):
        # function to demotivate the quarterback
        quarterback.regress()
            
class Skillset:
    def __init__(self, throw_accuracy, pocket_awareness, arm_strength, speed):
        self.throw_accuracy = throw_accuracy
        self.pocket_awareness = pocket_awareness
        self.arm_strength = arm_strength
        self.speed = speed
    
    def improve_skill(self, skill_name):
        # increment the specified skill by 1
        setattr(self, skill_name, getattr(self, skill_name) + 1)

    def regress_skill(self, skill_name):
        # decrement the specified skill by 1
        setattr(self, skill_name, getattr(self, skill_name) - 1)
