import pytest 
from website.models import Hawkins, User, Team, Note, Nutrition, Sleep, Readiness

@pytest.fixture(scope = 'module')
def new_user():
    user = User(email = "adimit23@colby.edu", first_name = "Cal", last_name = "Cium", password = "12345678", role = "athlete")
    return user

def test_new_user_entry(new_user):
    # signing up is tested more extensively in conftest.py
    added_user = new_user
    assert added_user.email == "adimit23@colby.edu"
    assert added_user.first_name == "Cal"
    assert added_user.last_name == "Cium"
    assert added_user.password == "12345678"
    assert added_user.role == "athlete"

def test_new_readiness_entry(new_user):
    readiness = Readiness(RecoveryIndexScore = 12,  ReadinessScore = 32, user = new_user) 
    user_readiness = new_user.readiness[-1] 
    assert readiness.user_id == new_user.id
    assert readiness.RecoveryIndexScore == user_readiness.RecoveryIndexScore
    assert readiness.RecoveryIndexScore == 12
    assert readiness.ReadinessScore == user_readiness.ReadinessScore
    assert readiness.ReadinessScore == 32


def test_new_sleep_entry(new_user):
    sleep = Sleep(TotalSleepScore = 99,  TotalSleepDuration = 8, user = new_user) 
    user_sleep = new_user.sleep[-1]
    assert sleep.user_id == new_user.id
    assert sleep.TotalSleepScore == user_sleep.TotalSleepScore
    assert sleep.TotalSleepScore == 99
    assert sleep.TotalSleepDuration == user_sleep.TotalSleepDuration
    assert sleep.TotalSleepDuration == 8


def test_new_hawkins_entry(new_user):
    hawkins = Hawkins(peak_force = 12, user = new_user) 
    user_hawkins = new_user.hawkins[-1]
    assert hawkins.user_id == new_user.id
    assert hawkins.peak_force == user_hawkins.peak_force
    assert hawkins.peak_force == 12


def test_new_note_entry(new_user):
    note = Note(content = "here's a note about an athlete", user = new_user)
    user_note = new_user.notes[-1]
    assert note.user_id == new_user.id
    assert note.content == user_note.content
    assert note.content == "here's a note about an athlete"


def test_new_nutrition_entry(new_user):
    nutrition = Nutrition(calories = 2000, user = new_user)
    user_nutrition = new_user.nutrition[-1]
    assert nutrition.user_id == new_user.id
    assert nutrition.calories == user_nutrition.calories
    assert nutrition.calories == 2000


def test_team():
    team = Team(name="Men's Ultimate")
    assert team.name == "Men's Ultimate"