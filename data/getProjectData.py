from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ..db.db import get_db


bp = Blueprint('getData', __name__, url_prefix='/getData')


@bp.route('getProject', methods=('GET', 'POST'))
def getProject(user, para=None):
    return 'haha'

@bp.route('getProjectNum', methods=('GET', 'POST'))
def getProjectNum(user):
    return 1

