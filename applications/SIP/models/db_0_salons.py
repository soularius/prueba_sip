db.define_table('salons',
                Field('uuid', 'string', length=16, unique=True),
                Field('name', 'string', length=45),
                Field('description', 'text'))

# Validation for 'salons'
db.salons.name.requires = IS_NOT_EMPTY()
db.salons.description.requires = IS_NOT_EMPTY()