# utils.py

import logging
import os
import json
import datetime
import pytz
from flask import current_app, request
from . import db
from . import constants

def get_current_user():
    """Returns the current user object"""
    return current_app.user_datastore.get_user()

def get_current_user_id():
    """Returns the current user's ID"""
    return get_current_user().id

def get_current_bucket():
    """Returns the current user's bucket object"""
    return db.Bucket.query.get(get_current_user_id())

def get_current_bucket_id():
    """Returns the current user's bucket ID"""
    return get_current_bucket().id

def get_current_project():
    """Returns the current user's project object"""
    return db.Project.query.get(get_current_bucket_id())

def get_current_project_id():
    """Returns the current user's project ID"""
    return get_current_project().id

def get_timezone():
    """Returns the current user's timezone"""
    return get_current_user().timezone

def get_project_total_pages(project_id):
    """Returns the total number of pages in a project"""
    return db.ProjectPage.query.filter_by(project_id=project_id).count()

def get_project_page_count(project_id):
    """Returns the count of pages in a project"""
    return db.ProjectPage.query.filter_by(project_id=project_id).count()

def get_project_page(project_id, page_number):
    """Returns a specific page in a project"""
    return db.ProjectPage.query.filter_by(project_id=project_id, page_number=page_number).first()

def get_project_pages(project_id, page_number, page_size):
    """Returns a list of pages in a project"""
    return db.ProjectPage.query.filter_by(project_id=project_id).paginate(page=page_number, per_page=page_size).items

def get_project_pages_count(project_id, page_number, page_size):
    """Returns the total count of pages in a project"""
    return db.ProjectPage.query.filter_by(project_id=project_id).paginate(page=page_number, per_page=page_size).total

def get_project_pages_total(project_id):
    """Returns the total count of pages in a project"""
    return db.ProjectPage.query.filter_by(project_id=project_id).count()

def get_page_stats(project_id, page_number):
    """Returns statistics for a specific page in a project"""
    page = get_project_page(project_id, page_number)
    if page:
        return {
            'id': page.id,
            'title': page.title,
            'created_at': page.created_at,
            'updated_at': page.updated_at,
            'type': page.type,
            'status': page.status,
            'notes': page.notes,
        }
    else:
        return None

def get_page_stats_project(project_id):
    """Returns statistics for all pages in a project"""
    pages = get_project_pages(project_id, 1, 100)
    return {
        'total_pages': get_project_pages_total(project_id),
        'pages': [
            get_page_stats(project_id, page.id) for page in pages
        ],
    }

def get_project_stats(project_id, date_from, date_to):
    """Returns statistics for a project in a specific date range"""
    from_date = datetime.datetime.fromtimestamp(date_from, pytz.utc)
    to_date = datetime.datetime.fromtimestamp(date_to, pytz.utc)
    project = db.Project.query.get(project_id)
    pages = db.ProjectPage.query.filter_by(project_id=project_id).filter(db.ProjectPage.created_at >= from_date, db.ProjectPage.created_at <= to_date).all()
    return {
        'pages': [page for page in pages],
    }

def to_utc(timestamp):
    """Converts a timestamp to UTC"""
    return pytz.utc.localize(datetime.datetime.fromtimestamp(timestamp))

def to_local(timestamp, timezone):
    """Converts a timestamp to a specific timezone"""
    return datetime.datetime.fromtimestamp(timestamp).astimezone(timezone)