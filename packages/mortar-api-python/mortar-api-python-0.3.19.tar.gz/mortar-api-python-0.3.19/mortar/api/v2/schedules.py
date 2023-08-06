JOB_TYPE_LUIGI = "luigi"

JOB_FREQUENCIES = ['MINUTE', 'HOURLY', 'DAILY', 'WEEKLY', 'MONTHLY']
JOB_DAYS_OF_WEEK = ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY",
                    "FRIDAY" "SATURDAY"]

"""
Example Usage:

from mortar.api.v2 import API

email = "mortar.staging@datadoghq.com"
key = "<USER_ACCESS_KEY>"
api = API(email, key)


from mortar.api.v2 import schedules

# Get all schedules for users.
schedules.get_schedules(api)

# Create a new monthly schedule
schedules.create_schedule(api, "BEN", "dd-analytics", "marlo", "MONTHLY", "09:00 pm", 1)

# View a specific schedule
schedules.get_schedule(api, "BEN")

# Update a schedule
schedules.update_schedule(api, "BEN", "dd-analytics", "marlo", "DAILY", "09:00 am")

# Delete a schedule.
schedules.delete_schedule(api, "BEN")
"""


def get_schedules(api, params=None):
    """
    Get all schedules for user.
    
    :type api: :class:`mortar.api.v2.api.API`
    :param api: API
    
    :raises: requests.exception.HTTPError: if a 40x or 50x error occurs
    
    :rtype: dict:
    :returns: schedules
    """
    return api.get('schedules', params)


def get_schedule(api, schedule_name):
    """
    Get a schedule.
    
    :type api: :class:`mortar.api.v2.api.API`
    :param api: API

    :type schedule_name: str
    :param schedule_name: Name of the schedule to return.
    
    :raises: requests.exception.HTTPError: if a 40x or 50x error occurs
    
    :rtype: dict:
    :returns: schedule
    """
    return api.get('schedules/%s' % schedule_name)


def create_schedule(api, schedule_name, project_name, luigiscript_name, frequency, exec_time=None,
    day_of_month=None, day_of_week=None, script_parameters=None, project_script_path="luigiscripts/",
    project_build="master", schedule_enabled=True, num_hours_to_retry_luigi=0, send_datadog_events=True):
    """
    Create a new Luigi schedule.

    :type api: :class:`mortar.api.v2.api.API`
    :param api: API

    :type schedule_name: str
    :param schedule_name: Name of the schedule.  This is the permanent identifier of the schedule and can not be changed later.

    :type project_name: str
    :param project_name: Name of the project.  Ex: `dd-analytics`

    :type luigiscript_name: str
    :param luigiscript_name: Name of the luigiscript to be run without the path or extension.  Ex: "marlo"

    :type frequency: str
    :param frequency: One of JOB_FREQUENCIES.  

    :type exec_time: str
    :param exec_time: "HH:MM PM" format.  Required if frequency is DAILY, WEEKLY, or MONTHLY

    :type day_of_month: str
    :param day_of_month: 1-based integer for day of the month.  Required if frequency is MONTHLY.

    :type day_of_week: integer
    :param day_of_week: One of JOB_DAYS_OF_WEEK.  Required if frequency is WEEKLY

    :type script_parameters: dict
    :param script_parameters: A dictionary of parameters to be set in the schedule.

    :type project_script_path: str
    :param project_script_path: The path in dd-analytics where the luigi script lives.  Doesn't include the actual file name.  Defaults to root directory of "luigiscripts/".

    :type project_build: str
    :param project_buld: This should be the branch that you want to run on when you always want to use the latest code on that branch.  It should be a commit hash if you want to peg the schedule to a specific build.

    :type schedule_enabled: bool
    :param schedule_enabled: If the schedule is enabled and running.  

    :type num_hours_to_retry_luigi: integer
    :param num_hours_to_retry_luigi: If a Task in your Luigi pipeline fails or is incomplete (missing required data), rerun the pipeline every 15 minutes until it succeeds or we hit this limit.

    :type send_datadog_events: bool
    :param send_datadog_events: Send events start/stop/failure events to Datadog.
    
    :raises: requests.exception.HTTPError: if a 40x or 50x error occurs
    
    :rtype: str:
    :returns: schedule_id for the newly created schedule

    """

    # Deprecated parameters or hardcoded parameters.
    email_on_completion = False
    email_on_failure = False
    git_ref = project_build
    script_type = JOB_TYPE_LUIGI
    job_type = script_type

    body = {
        "schedule_name": schedule_name,
        "project_name": project_name,
        "luigiscript_name": luigiscript_name,
        "frequency": frequency,
        "exec_time": exec_time,
        "day_of_month": day_of_month,
        "day_of_week": day_of_week,
        "script_parameters": script_parameters,
        "project_script_path": project_script_path,
        "project_build": project_build,
        "schedule_enabled": schedule_enabled,
        "num_hours_to_retry_luigi": num_hours_to_retry_luigi,
        "send_datadog_events": send_datadog_events,

        "email_on_completion": email_on_completion,
        "email_on_failure": email_on_failure,
        "git_ref": git_ref,
        "script_type": script_type,
        "job_type": job_type
    }

    return api.post("schedules", body)["schedule_id"]


def update_schedule(api, schedule_name, project_name, luigiscript_name, frequency, exec_time=None,
    day_of_month=None, day_of_week=None, script_parameters=None, project_script_path="luigiscripts/",
    project_build="master", schedule_enabled=True, num_hours_to_retry_luigi=0, send_datadog_events=True):
    """
    Update an existing Luigi schedule.

    :type api: :class:`mortar.api.v2.api.API`
    :param api: API

    :type schedule_name: str
    :param schedule_name: Name of the schedule.  This is the permanent identifier of the schedule and can not be changed later.

    :type project_name: str
    :param project_name: Name of the project.  Ex: `dd-analytics`

    :type luigiscript_name: str
    :param luigiscript_name: Name of the luigiscript to be run without the path or extension.  Ex: "marlo"

    :type frequency: str
    :param frequency: One of JOB_FREQUENCIES.  

    :type exec_time: str
    :param exec_time: "HH:MM PM" format.  Required if frequency is DAILY, WEEKLY, or MONTHLY

    :type day_of_month: str
    :param day_of_month: 1-based integer for day of the month.  Required if frequency is MONTHLY.

    :type day_of_week: integer
    :param day_of_week: One of JOB_DAYS_OF_WEEK.  Required if frequency is WEEKLY

    :type script_parameters: dict
    :param script_parameters: A dictionary of parameters to be set in the schedule.

    :type project_script_path: str
    :param project_script_path: The path in dd-analytics where the luigi script lives.  Doesn't include the actual file name.  Defaults to root directory of "luigiscripts/".

    :type project_build: str
    :param project_buld: This should be the branch that you want to run on when you always want to use the latest code on that branch.  It should be a commit hash if you want to peg the schedule to a specific build.

    :type schedule_enabled: bool
    :param schedule_enabled: If the schedule is enabled and running.  

    :type num_hours_to_retry_luigi: integer
    :param num_hours_to_retry_luigi: If a Task in your Luigi pipeline fails or is incomplete (missing required data), rerun the pipeline every 15 minutes until it succeeds or we hit this limit.

    :type send_datadog_events: bool
    :param send_datadog_events: Send events start/stop/failure events to Datadog.
    
    :raises: requests.exception.HTTPError: if a 40x or 50x error occurs
    """

    # Deprecated parameters or hardcoded parameters.
    email_on_completion = False
    email_on_failure = False
    git_ref = project_build
    script_type = JOB_TYPE_LUIGI
    job_type = script_type

    body = {
        "schedule_name": schedule_name,
        "project_name": project_name,
        "luigiscript_name": luigiscript_name,
        "frequency": frequency,
        "exec_time": exec_time,
        "day_of_month": day_of_month,
        "day_of_week": day_of_week,
        "script_parameters": script_parameters,
        "project_script_path": project_script_path,
        "project_build": project_build,
        "schedule_enabled": schedule_enabled,
        "num_hours_to_retry_luigi": num_hours_to_retry_luigi,
        "send_datadog_events": send_datadog_events,

        "email_on_completion": email_on_completion,
        "email_on_failure": email_on_failure,
        "git_ref": git_ref,
        "script_type": script_type,
        "job_type": job_type
	}

    api.put("schedules/%s" % (schedule_name), body)


def delete_schedule(api, schedule_name):
    """
    Delete a schedule for a user.
    
    :type api: :class:`mortar.api.v2.api.API`
    :param api: API

    :type schedule_name: str
    :param schedule_name: Name of the schedule to delete.
    
    :raises: requests.exception.HTTPError: if a 40x or 50x error occurs
    """
    api.delete("schedules/%s" % schedule_name)



