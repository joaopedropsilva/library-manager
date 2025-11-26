from api.run import setup_api
from api.db.session import get_session
from api.tests.integration.db import db_session_override


app = setup_api()
app.dependency_overrides[get_session] = db_session_override
