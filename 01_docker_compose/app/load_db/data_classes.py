from dataclasses import dataclass


@dataclass
class Movie:
    id: str = None
    title: str = None
    description: str = None
    creation_date: str = ''
    file_path: str = None
    rating: float = None
    type: str = None
    created_at: str = ''
    updated_at: str = ''


@dataclass
class Style:
    id: str = None
    name: str = None
    description: str = None
    created_at: str = ''
    updated_at: str = ''


@dataclass
class StyleMovie:
    id: str = None
    film_work_id: str = None
    genre_id: str = None
    created_at: str = ''


@dataclass
class People:
    id: str = None
    full_name: str = None
    created_at: str = ''
    updated_at: str = ''


@dataclass
class PeopleMovie:
    id: str = None
    film_work_id: str = None
    person_id: str = None
    role: str = None
    created_at: str = ''
