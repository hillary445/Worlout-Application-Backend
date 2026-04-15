from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    pushups = Exercise(name="Push Ups", category="Strength", equipment_needed=False)
    running = Exercise(name="Running", category="Cardio", equipment_needed=False)

    workout1 = Workout(date=date.today(), duration_minutes=30, notes="Morning workout")

    db.session.add_all([pushups, running, workout1])
    db.session.commit()

    we1 = WorkoutExercise(workout=workout1, exercise=pushups, reps=20, sets=3)
    we2 = WorkoutExercise(workout=workout1, exercise=running, duration_seconds=900)

    db.session.add_all([we1, we2])
    db.session.commit()

    print("Database seeded!")