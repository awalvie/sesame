import json
import subprocess
from datetime import datetime, timedelta, timezone


def search_role(term=None):
    command = ""
    if term:
        command = f"gcloud iam roles list --format=json --filter='title:{term}'"

    else:
        command = f"gcloud iam roles list --format=json --limit=10"

    output = subprocess.run([command], shell=True, stdout=subprocess.PIPE)
    return json.loads(output.stdout.decode("utf-8"))



def create_permission(project, email, roles, duration):
    for role in roles:
        expiration_timestamp = (
            (datetime.now(timezone.utc) + timedelta(minutes=duration))
            .replace(microsecond=0)
            .isoformat()
        )

        base_command = f"gcloud projects add-iam-policy-binding {project} "
        member = f"--member 'user:{email}' "
        role_flag = f"--role {role} "
        condition = f"--condition=\"expression=request.time < timestamp('{expiration_timestamp}'),title=temporary_permission\" "

        command = base_command + member + role_flag + condition

        subprocess.run(
            [f"{command}"],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

        #  logger.info(f"Successfully gave permission: {role} for user: {email} for duration {duration}m")


