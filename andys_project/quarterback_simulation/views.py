from django.http import JsonResponse
from .models import Quarterback_db, Coach_db, Team_db, Skillset_db, CareerStats_db, HallOfFame_db
import os
import json
from .simulation import Simulator
from django.shortcuts import render

def load_data(file_name):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def simulate_quarterback_career(request):
    # load in quarterback data from the JSON file
    quarterbacks_data = load_data('quarterbacks.json')
    if request.method == 'GET':
        # extract quarterback names
        quarterbacks = [qb_data['name'] for qb_data in quarterbacks_data]
        context = {'quarterbacks': quarterbacks}
        return render(request, 'quarterback_search_form.html', context)

    elif request.method == 'POST':
        # handle form submission
        selected_quarterback_name = request.POST.get('quarterback')
        # find the selected quarterback from the loaded data
        selected_quarterback_data = next(qb_data for qb_data in quarterbacks_data if qb_data['name'] == selected_quarterback_name)
    

    if selected_quarterback_data:
        # create instances of the model objects
        team = Team_db.objects.create(name=selected_quarterback_data['team']['name'], 
                                      location=selected_quarterback_data['team']['location'], 
                                      history=selected_quarterback_data['team']['history'])
        coach = Coach_db.objects.create(name=selected_quarterback_data['coach']['name'], 
                                        experience=selected_quarterback_data['coach']['experience'])
        skillset = Skillset_db.objects.create(throw_accuracy=selected_quarterback_data['skillset']['throw_accuracy'],
                                              pocket_awareness=selected_quarterback_data['skillset']['pocket_awareness'],
                                              arm_strength=selected_quarterback_data['skillset']['arm_strength'],
                                              speed=selected_quarterback_data['skillset']['speed'])
        career_stats = CareerStats_db.objects.create(games_played=selected_quarterback_data['career_stats']['games_played'], 
                                                     pass_attempts=selected_quarterback_data['career_stats']['pass_attempts'], 
                                                     pass_completions=selected_quarterback_data['career_stats']['pass_completions'],
                                                     pass_yards=selected_quarterback_data['career_stats']['pass_yards'], 
                                                     pass_touchdowns=selected_quarterback_data['career_stats']['pass_touchdowns'],
                                                     rush_yards=selected_quarterback_data['career_stats']['rush_yards'], 
                                                     rush_touchdowns=selected_quarterback_data['career_stats']['rush_touchdowns'],
                                                     interceptions=selected_quarterback_data['career_stats']['interceptions'])
        quarterback = Quarterback_db.objects.create(name=selected_quarterback_data['name'],
                                                    age=selected_quarterback_data['age'],
                                                    coach=coach,
                                                    team=team,
                                                    experience=selected_quarterback_data['experience'],
                                                    skillset=skillset,
                                                    career_stats=career_stats)

        # instantiate the Simulator with the created model objects
        simulator = Simulator(quarterback, coach, team)

        # simulate career for the quarterback
        updated_career_stats = simulator.simulate_career(number_games_per_season=17)

        # extract career statistics from the dictionary
        games_played = updated_career_stats['games_played']
        pass_attempts = updated_career_stats['pass_attempts']
        pass_completions = updated_career_stats['pass_completions']
        pass_yards = updated_career_stats['pass_yards']
        pass_touchdowns = updated_career_stats['pass_touchdowns']
        rush_yards = updated_career_stats['rush_yards']
        rush_touchdowns = updated_career_stats['rush_touchdowns']
        interceptions = updated_career_stats['interceptions']

        # create new CareerStats_db object
        final_career_stats = CareerStats_db.objects.create(games_played=games_played,
                                                              pass_attempts=pass_attempts,
                                                              pass_completions=pass_completions,
                                                              pass_yards=pass_yards,
                                                              pass_touchdowns=pass_touchdowns,
                                                              rush_yards=rush_yards,
                                                              rush_touchdowns=rush_touchdowns,
                                                              interceptions=interceptions)

        # decide Hall of Fame eligibility
        hof_status = "Eligible for Hall of Fame" if HallOfFame_db.objects.create(quarterback=quarterback).is_eligible(final_career_stats) else "Not eligible for Hall of Fame"
    
        # collect final career stats and Hall of Fame status
        final_stats = {
            'Quarterback Name': quarterback.name,
            'Predicted Career Stats': updated_career_stats,
            'Predicted Hall of Fame Status': hof_status
        }
    
    # return the simulation results as a JSON response
    return JsonResponse(final_stats)