# Copyright 2022 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from dash import dcc, html
import datetime
from formatting import *

from dwave.cloud.api import exceptions, Problems


__all__ = ["job_bar", "TERMINATED", "RUNNING", "cancel", "elapsed", "get_status",
    "no_solver_msg", ]

job_bar = {"READY": [0, "link"],
#          "WAITING": [0, "dark"],     Placeholder, to remember the color
           "NO_SOLVER": [100, "danger"],
           "SUBMITTED": [10, "info"],
           "PENDING": [50, "warning"],
           "IN_PROGRESS": [75 ,"primary"],
           "COMPLETED": [100, "success"],
           "CANCELLED": [100, "light"],
           "FAILED": [100, "danger"], }

TERMINATED = ["COMPLETED", "CANCELLED", "FAILED"]
RUNNING = ["PENDING", "IN_PROGRESS"]

no_solver_msg = [
    html.Div([
    html.Div("Could not connect to a Leap hybrid CQM solver."),
    html.Div(["""
If you are running locally, set environment variables or a
dwave-cloud-client configuration file as described in the
""",
    dcc.Link(children=[html.Div(" Ocean")],
        href="https://docs.ocean.dwavesys.com/en/stable/overview/sapi.html",
        style={"display":"inline-block"}),
    "documentation."],
        style={"display":"inline-block"}),
    html.Div(["If you are running in the Leap IDE, see the ",
    dcc.Link(children=[html.Div("Leap IDE dumentation")],
        href="https://docs.dwavesys.com/docs/latest/doc_ide_user.html",
        style={"display":"inline-block"}),
    "documentation"],
        style={"display":"inline-block"}),])]

def cancel(client, job_id):
    """Try to cancel a job submission."""

    p = Problems(endpoint=client.endpoint, token=client.token)
    try:
        status = p.cancel_problem(job_id)
        return status
    except Exception as err:
        return err

def elapsed(ref_time):
    """Return elapsed time in seconds."""

    return (datetime.datetime.now() -
        datetime.datetime.strptime(ref_time, "%c")).seconds

def get_status(client, job_id, job_submit_time):
    """Return status of submitted job."""

    p = Problems(endpoint=client.endpoint, token=client.token)
    try:
        status = p.get_problem_status(job_id)
        label_time = dict(status)["label"].split("submitted: ")[1]
        if label_time == job_submit_time:
            return status.status.value
        else:
            return None
    except exceptions.ResourceNotFoundError as err:
        return None