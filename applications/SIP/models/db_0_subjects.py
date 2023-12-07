if not 'subjects' in db.tables:
    db.define_table('subjects',
                    Field('uuid', 'string', length=16, unique=True),
                    Field('name', 'string', length=55),
                    Field('description', 'text'))

    # Validation for 'subjects'
    db.subjects.name.requires = IS_NOT_EMPTY()
    db.subjects.description.requires = IS_NOT_EMPTY()