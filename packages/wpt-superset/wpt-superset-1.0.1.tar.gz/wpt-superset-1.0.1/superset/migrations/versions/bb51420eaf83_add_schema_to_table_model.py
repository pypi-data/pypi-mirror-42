# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""add schema to table model

Revision ID: bb51420eaf83
Revises: 867bf4f117f9
Create Date: 2016-04-11 22:41:06.185955

"""

# revision identifiers, used by Alembic.
revision = 'bb51420eaf83'
down_revision = '867bf4f117f9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    #op.add_column('tables', sa.Column('schema', sa.String(length=255), nullable=True))
    try:
        #op.create_unique_constraint(
        #    '_customer_location_uc', 'tables',
        #    ['database_id', 'schema', 'table_name'])
        pass
    except Exception:
        pass


def downgrade():
    try:
        #op.drop_constraint(u'_customer_location_uc', 'tables', type_='unique')
        pass
    except Exception:
        pass
    #op.drop_column('tables', 'schema')
