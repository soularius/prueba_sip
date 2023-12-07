db.define_table('day_of_week',
                Field('uuid', 'string', length=16, unique=True),
                Field('name', 'string', length=45))

# validation for 'day_of_week'
db.day_of_week.name.requires = IS_NOT_EMPTY()