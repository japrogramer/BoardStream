#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


celery -A medicalboard.taskapp worker -l INFO
