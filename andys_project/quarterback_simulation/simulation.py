import random
import os
import json
from .simulation_models import Quarterback, HallOfFame, CareerStats, Team, Coach, Skillset

class Simulator:
    def __init__(self, quarterback, coach, team):
        self.quarterback = quarterback
        self.coach = coach
        self.team = team

    def simulate_game(self, game_number):
        # function to simulate a game
        print(f"Simulating Game {game_number}:")

        # accessing quarterback's skills
        throw_accuracy = self.quarterback.skillset.throw_accuracy
        pocket_awareness = self.quarterback.skillset.pocket_awareness
        arm_strength = self.quarterback.skillset.arm_strength
        speed = self.quarterback.skillset.speed

        # define skill weights
        arm_strength_weight = 0.5  
        throw_accuracy_weight = 0.3  
        speed_weight = 0.3  
        pocket_awareness_weight = 0.5  

        # generate random values for game statistics and apply weights
        pass_attempts = random.randint(20, 50) # generate random number of pass attempts within the range
        pass_completions = random.randint(0, pass_attempts)  # ensure pass completions <= pass attempts
        pass_yards = random.randint(0, int(arm_strength * arm_strength_weight) * 7)  # assume maximum pass yards is 350
        pass_touchdowns = random.randint(0, int(0.1 * throw_accuracy * throw_accuracy_weight)) # assume maximum pass touchdowns is 3
        rush_yards = random.randint(0, int(5 * speed * speed_weight)) # assume maximum rush yards is 150
        rush_touchdowns = random.randint(0, int(0.1 * speed * speed_weight)) # assume maximum rush touchdowns is 3
        interceptions = random.randint(0, 5 - (int(int(pocket_awareness * pocket_awareness_weight) / 15))) # assume maximum interceptions is 5

        # Print game statistics
        print(f"{self.quarterback.name} completes {pass_completions} out of {pass_attempts} passes.")
        print(f"{self.quarterback.name} throws for {pass_yards} yards with {pass_touchdowns} passing touchdowns.")
        print(f"{self.quarterback.name} rushes for {rush_yards} yards with {rush_touchdowns} rushing touchdowns.")
        print(f"{self.quarterback.name} throws {interceptions} interceptions.")

        # Return game statistics
        game_stats = {
            "games_played": 1,
            "pass_attempts": pass_attempts,
            "pass_completions": pass_completions,
            "pass_yards": pass_yards,
            "pass_touchdowns": pass_touchdowns,
            "rush_yards": rush_yards,
            "rush_touchdowns": rush_touchdowns,
            "interceptions": interceptions
        }
        
        return game_stats
    
    def simulate_season(self, number_games_per_season):
        # accessing quarterback's skills
        throw_accuracy = self.quarterback.skillset.throw_accuracy
        pocket_awareness = self.quarterback.skillset.pocket_awareness
        arm_strength = self.quarterback.skillset.arm_strength
        speed = self.quarterback.skillset.speed

        # ensure maximum stat number is 99
        throw_accuracy = min(99, throw_accuracy)
        pocket_awareness = min(99, pocket_awareness)
        arm_strength = min(99, arm_strength)
        speed = min(99, speed)

        # accessing coach's experience 
        coach_experience = self.coach.experience

        # accessing team's history
        team_history = self.team.history

        # adjusting skillset based on coach's experience
        if coach_experience > 10:
            self.coach.motivate(self.quarterback)
        else:
            self.coach.demotivate(self.quarterback)

        # adjusting skillset based on team's history
        if team_history == "winning":
            self.quarterback.improve()

        if team_history == "losing":
            self.quarterback.regress()

        season_stats = {
            "games_played": 0,
            "pass_attempts": 0,
            "pass_completions": 0,
            "pass_yards": 0,
            "pass_touchdowns": 0,
            "rush_yards": 0,
            "rush_touchdowns": 0,
            "interceptions": 0
        }
        for game_number in range(1, number_games_per_season + 1):  # track game number
            game_stats = self.simulate_game(game_number)
            # update season statistics
            for stat in season_stats:
                season_stats[stat] += game_stats[stat]


        print() # print empty line 
        print(f"{self.quarterback.name}'s season {self.quarterback.experience} simulation completed.")
        print("Season Statistics:")
        for stat, value in season_stats.items():
            print(f"{stat}: {value}")
        return season_stats
    
    def simulate_career(self, number_games_per_season):
        career_stats = {
            "games_played": self.quarterback.career_stats.games_played,
            "pass_attempts": self.quarterback.career_stats.pass_attempts,
            "pass_completions": self.quarterback.career_stats.pass_completions,
            "pass_yards": self.quarterback.career_stats.pass_yards,
            "pass_touchdowns": self.quarterback.career_stats.pass_touchdowns,
            "rush_yards": self.quarterback.career_stats.rush_yards,
            "rush_touchdowns": self.quarterback.career_stats.rush_touchdowns,
            "interceptions": self.quarterback.career_stats.interceptions
        }
        number_seasons = 44 - self.quarterback.age  # use Tom Brady retirement age as threshold
        for season in range(1, number_seasons + 1):
            print(f"Season {season}:")
            season_stats = self.simulate_season(number_games_per_season)
            self.coach.experience += 1   # increment coach experience
            self.quarterback.experience += 1 # increment quarterback experience
            # update career statistics with season statistics
            for stat in season_stats:
                career_stats[stat] += season_stats[stat]
        print()  # printing an empty line between seasons for separation
        print(f"{self.quarterback.name}'s career simulation completed.")
        print("Career Statistics:")
        for stat, value in career_stats.items():
            print(f"{stat}: {value}")
        
        # evaluate Hall of Fame eligibility
        hof = HallOfFame(self.quarterback)
        if hof.is_eligible(career_stats):
            print(f"{self.quarterback.name} is predicted to be a Hall of Famer.")
        else:
            print(f"{self.quarterback.name} is not predicted to be a Hall of Famer.")

        # return career statistics
        return career_stats
        
# function to load in data from JSON file
def load_data(file_name):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# function to save simulation data into JSON file
def save_simulation_results(results):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'simulation_results.json')
    with open(file_path, 'w') as file:
        json.dump(results, file, indent=4)

def simulate_and_store_results(quarterbacks_data):
    simulation_results = []

    for qb_data in quarterbacks_data:
        team = Team(qb_data['team']['name'], 
                    qb_data['team']['location'], 
                    qb_data['team']['history'])
        coach = Coach(qb_data['coach']['name'], 
                      qb_data['coach']['experience'])
        skillset = Skillset(qb_data['skillset']['throw_accuracy'],
                            qb_data['skillset']['pocket_awareness'],
                            qb_data['skillset']['arm_strength'],
                            qb_data['skillset']['speed'])
        career_stats = CareerStats(qb_data['career_stats']['games_played'], 
                                   qb_data['career_stats']['pass_attempts'], 
                                   qb_data['career_stats']['pass_completions'],
                                   qb_data['career_stats']['pass_yards'], 
                                   qb_data['career_stats']['pass_touchdowns'],
                                   qb_data['career_stats']['rush_yards'], 
                                   qb_data['career_stats']['rush_touchdowns'],
                                   qb_data['career_stats']['interceptions'])
        quarterback = Quarterback(qb_data['name'],
                                  qb_data['age'],
                                  coach,
                                  team,
                                  qb_data['experience'],
                                  skillset,
                                  career_stats)

        print()
        print(f"Loaded quarterback: {quarterback.name}")

        # intiate simulation
        simulator = Simulator(quarterback, coach, team)
        updated_career_stats = simulator.simulate_career(number_games_per_season=17)

        # check Hall of Fame eligibility
        hall_of_fame = HallOfFame(quarterback)
        if hall_of_fame.is_eligible(updated_career_stats):
            hof_status = "Eligible for Hall of Fame"
        else:
            hof_status = "Not eligible for Hall of Fame"
    
        # collect final career stats and hof status
        final_stats = {
            'quarterback': quarterback.name,
            'career_stats': updated_career_stats,
            'hof_status': hof_status
        }
    
        # add final career stats and status to the list
        simulation_results.append(final_stats)

        # save the simulation results to a JSON file
        save_simulation_results(simulation_results)
    

# load in quarterback data
file_path = 'quarterbacks.json'
quarterbacks_data = load_data(file_path)

# call function to simulate and save
simulate_and_store_results(quarterbacks_data)

