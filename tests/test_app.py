import os
import datetime
from app import format_date, url_for_char
from app.models import Death


def test_format_date():
    dt = datetime.datetime(2019, 12, 1, 10, 0, 0)
    assert 'Sunday, 01 Dec' == format_date(dt)


def test_index(client, seed):
    rv = client.get('/')
    assert 200 == rv.status_code
    assert b'Rubini' in rv.data
    assert b'Nattank Fazendo Historia' in rv.data
    assert rv.data.count(b'Elite Knight') == 2
    # ensure deaths are align left (Almighty Os)
    # and right (Skeletin Alliance)
    assert b'has-text-left' in rv.data
    assert b'has-text-right' in rv.data
    for death in Death.query.all():
        # ensure deaths are grouped by date
        assert format_date(death.date).encode() in rv.data
        # ensure links are present
        assert url_for_char(death.char_name).encode() in rv.data
    # ensures deaths are sorted desc by date
    assert rv.data.find(b'Nattank Fazendo Historia') < rv.data.find(b'Rubini')


def test_url_for_char():
    expected = ('https://www.tibia.com/community/'
                '?subtopic=characters&amp;name=Nattank+Fazendo+Historia')
    assert expected == url_for_char('Nattank Fazendo Historia')
    assert expected == url_for_char('Nattank+Fazendo+Historia')
