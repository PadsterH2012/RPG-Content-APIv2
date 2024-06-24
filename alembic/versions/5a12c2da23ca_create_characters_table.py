from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5a12c2da23ca'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create the new table
    op.create_table(
        'characters',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('sex', sa.String, nullable=True),
        sa.Column('age', sa.String, nullable=True),
        sa.Column('traits', sa.String, nullable=True),
        sa.Column('behaviors', sa.String, nullable=True),
        sa.Column('background', sa.String, nullable=True)
    )
    op.create_index('ix_characters_name', 'characters', ['name'])
    op.create_index('ix_characters_sex', 'characters', ['sex'])
    op.create_index('ix_characters_traits', 'characters', ['traits'])
    op.create_index('ix_characters_behaviors', 'characters', ['behaviors'])

def downgrade():
    # Drop the table and indexes if downgrading
    op.drop_index('ix_characters_name', table_name='characters')
    op.drop_index('ix_characters_sex', table_name='characters')
    op.drop_index('ix_characters_traits', table_name='characters')
    op.drop_index('ix_characters_behaviors', table_name='characters')
    op.drop_table('characters')
