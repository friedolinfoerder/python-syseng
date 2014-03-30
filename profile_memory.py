from app import app

@profile
def profiling():
    app.test_client().get('/memory')

profiling()