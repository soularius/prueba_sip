if not 'schedules' in db.tables:      
    db.define_table('schedules',
                    Field('uuid', 'string', length=16, unique=True),
                    Field('block_start', 'time'),
                    Field('block_end', 'time'))

    # validation for 'schedules'
    db.schedules.block_start.requires = IS_NOT_EMPTY()
    db.schedules.block_end.requires = IS_NOT_EMPTY()