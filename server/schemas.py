from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()

    exercises = fields.Nested(ExerciseSchema, many=True)