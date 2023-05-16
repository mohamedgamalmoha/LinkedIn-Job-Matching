from flask import request, url_for
from flask_jwt_extended import create_access_token, get_jwt_identity

import httpx

from web import app, db
from web.status import HTTPStatus
from web.models import User, user_exists
from web.decerators import jwt_required_v2
from web.forms import SignupForm, LoginForm, JobMatchingForm
from web.parser import parse_search_response, get_detail_responses
from web.utils import extract_job_requirements, calculate_matching_score


@app.route('/api/auth/login', methods=['POST'], endpoint='login')
def login():
    form = LoginForm(request.form)
    if form.validate():
        email, password = form.email.data, form.password.data
        user = user_exists(email=email, password=password)
        if not user:
            return {'message': 'Invalid email or password'}, HTTPStatus.UNAUTHORIZED
        access_token = create_access_token(identity=user.id)
        user_info = user.as_dict()
        user_info.update({'access_token': access_token})
        return user_info, HTTPStatus.OK
    return {'message': form.form_errors}, HTTPStatus.BAD_REQUEST


@app.route('/api/auth/signup', methods=['POST'], endpoint='signup')
def signup():
    form = SignupForm(request.form)
    if form.validate():
        email, password = form.email.data, form.password.data
        user = user_exists(email=email, password=password)
        if user:
            return {'message': 'Email already exists'}, HTTPStatus.CONFLICT
        user = User.create_user(**form.as_dict())
        db.session.add(user)
        db.session.commit()
        return {'message': 'User has successfully created', 'login': url_for('login', _external=True)}, HTTPStatus.CREATED
    return {'message': form.errors}, HTTPStatus.BAD_REQUEST


@app.route("/api/auth/delete", methods=['DELETE'], endpoint='delete')
@jwt_required_v2
def delete():
    user_id = request.args.get('user_id')
    if not user_id:
        return {'message': 'User ID is required'}, HTTPStatus.BAD_REQUEST

    current_user = get_jwt_identity()
    if not current_user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    user = db.session.get(User, current_user)
    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    if user.id != int(user_id):
        return {'message': 'You can only delete your own account'}, HTTPStatus.FORBIDDEN

    db.session.delete(user)
    db.session.commit()

    return {'message': 'User has successfully delete'}, HTTPStatus.OK


@app.route("/api/job-matching", methods=['GET'], endpoint='job_matching')
@jwt_required_v2
async def job_matching():
    form = JobMatchingForm(request.form)

    if not form.validate():
        return {'message': form.errors}, HTTPStatus.BAD_REQUEST

    # Extract data from the form
    start = form.start.data
    keywords = form.keywords.data
    location = form.location.data

    api_url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&start={start}'
    async with httpx.AsyncClient() as HttpxAsyncClient:
        req = HttpxAsyncClient.build_request("GET", api_url)
        # Send the request to get the search result
        response = await HttpxAsyncClient.send(req)
        # Parse the result
        parsed_response = parse_search_response(response)
        # Send other requests to get the details
        jobs = await get_detail_responses(parsed_response)

        # Iterate over jobs and extract job requirements, then calculate the  matching score
        job_list = []
        for job in jobs:
            description = job.get('description', None)
            if description is None:
                continue
            job_requirements = extract_job_requirements(description)
            matching_score = calculate_matching_score(form.employee_criteria, job_requirements)
            # Filter jobs based on score, ignore in case of being less than 0
            if matching_score > 0:
                job_list.append({'title': job['title'], 'company': job['company'], 'score': matching_score,
                                 'description': description})

        # Return sorted job listings as JSON response
        return {'job_listings': sorted(job_list, key=lambda i: i.get('score'))}, HTTPStatus.OK
