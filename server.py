import sys
from pymongo import MongoClient

from data_getters import get_terms, get_schools



# Initializations -----------------------------------------------------------------

# Command line arguments
load_all = False
load_term = None

for i, argument in enumerate(sys.argv[1:]): # Exclude name of script
    if argument == '--load-all':
        load_all = True
    if argument == '--load-term':
        # Next argument is term id
        load_term = str(sys.argv[i])

# Initialize mongodb connection
client = MongoClient()



# DB Setup ------------------------------------------------------------------------

# If there are no term databases
if not any(database[:5] == 'term_' for database in client.database_names()):
    print('Running first time setup...')

    # By default, load the most recent term in the database
    if not load_all and not load_term:
        print('Loading most recent term data into database...')

        most_recent_term_id = get_terms()[0]['id']
        
        db = client['term_{0}'.format(most_recent_term_id)]
        col = db.schools
        col.insert_many(get_schools(most_recent_term_id))

