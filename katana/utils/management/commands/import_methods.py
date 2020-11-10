from django.core.management.base import BaseCommand, CommandError
from methodologies.models import Method as M
from methodologies.models import Phase as Ph
from methodologies.models import Project_Type as P
from django.core import serializers
import sys
import os
import shutil
import zipfile
import json
from pprint import pprint


class Command(BaseCommand):
    help = "Imports a methodology: requires a django fixture"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            dest="input",
            help="Specify input file - must be a json django fixture",
            type=file,
        )

    def handle(self, *args, **options):
        if options["input"]:
            self.stdout.write("\n")
            self.stdout.write("Got the file thanks\n")
            self.stdout.write("\n")
            self.stdout.write("Beginning deserialization.....\n")
            self.stdout.write("\n")
            data_file = options["input"]
            data = json.load(data_file)
            phase_list = []
            method_list = []
            file_list = []
            for obj in data:
                prep = obj["model"][obj["model"].rfind(".") + 1 :]
                module = obj["model"][: obj["model"].find(".")]
                if "_" in prep:
                    idx = prep.find("_")
                    final = prep[0].capitalize()
                    final += prep[1 : idx + 1]
                    final += prep[idx + 1].capitalize()
                    final += prep[idx + 2 :]
                    final = str(final)
                else:
                    final = prep[0].capitalize() + prep[1:]
                    final = str(final)
                manager = getattr(sys.modules["%s.models" % str(module)], "%s" % final)
                model = manager()
                for field in obj["fields"]:
                    if "project_type" in obj["model"]:
                        if field == "phase":
                            model.save()
                            for p in phase_list:
                                model.phase.add(p)
                            continue
                    if "method" in obj["model"]:
                        if field == "phase" or field == "project_type":
                            model.save()
                            if field == "project_type":
                                model.project_type.add(ptype)
                                continue
                            if field == "phase":
                                if obj["fields"][field] != None:
                                    phase = Ph.objects.get(
                                        guid=str(obj["fields"][field][0])
                                    )
                                    model.phase = phase
                                continue
                        if field == "files":
                            continue
                    if field != "project":
                        setattr(model, field, obj["fields"][field])
                    if "file" in obj["model"]:
                        file_list.append(model)
                model.save()
                if "phase" in obj["model"]:
                    phase_list.append(model)
                if "project_type" in obj["model"]:
                    ptype = model
                if "file" in obj["model"]:
                    item = M.objects.get(guid=model.a_i_guid)
                    model.associated_item = item
                    model.save()
                    model.method_set.add(model.associated_item)
            self.stdout.write("\n")
            self.stdout.write(
                "Deserialization Complete - Please Enjoy Your New Methodology"
            )
            self.stdout.write("\n")

        else:
            self.stdout.write("\n")
            self.stdout.write("************\n")
            self.stdout.write(
                " Please enter a valid File containing a json django fixture"
            )
            self.stdout.write("************\n")
            self.stdout.write("\n")
