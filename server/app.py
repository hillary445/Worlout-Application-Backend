from flask import Flask, request
from flask_migrate import Migrate
from models import db, Workout, Exercise, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

@app.route('/')
def home():
    return {"message": "Workout API running"}

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return workout_schema.dump(workout)

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.json
    workout = Workout(
        date=data['date'],
        duration_minutes=data['duration_minutes'],
        notes=data.get('notes')
    )
    db.session.add(workout)
    db.session.commit()
    return workout_schema.dump(workout), 201

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return {"message": "Workout deleted"}


#Exercise

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_schema.dump(exercise)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.json
    exercise = Exercise(
        name=data['name'],
        category=data['category'],
        equipment_needed=data.get('equipment_needed', False)
    )
    db.session.add(exercise)
    db.session.commit()
    return exercise_schema.dump(exercise), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return {"message": "Exercise deleted"}

#Linking exercise to workout
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    data = request.json

    link = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )

    db.session.add(link)
    db.session.commit()

    return {"message": "Exercise added to workout"}

if __name__ == '__main__':
    app.run(port=5555, debug=True)