import time
import sys
import os
import random
import zipfile
import shutil
import json
import re
import csv

from decimal import Decimal

from auditor.views import action_audit
from auditor.utils import initial_audits

from django.conf import settings

from django.core import serializers
from django.core.files import File

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from django.db.models import Q, Sum, Count, F
from django.db.models.query import EmptyQuerySet as EQS
from django.db.models.functions import Coalesce

from django.http import HttpResponseRedirect as HRR
from django.http import HttpResponse as HR
from django.http import JsonResponse as JR
from django.http import Http404

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from django.utils.safestring import mark_safe
from django.utils import timezone

# from project.views import get_context_items

from utils.tools import get_guid
from utils.permtools import *

from utils.formutils import input_list

context = {}

OBJECT_FORM_SUCCESS = "object form success"
