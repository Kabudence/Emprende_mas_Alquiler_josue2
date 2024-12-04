from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..models import Feedback
from ..database import db
from . import feedbacks

@feedbacks.route('/')
@login_required
def index():
    return render_template('feedbacks/index.html')
