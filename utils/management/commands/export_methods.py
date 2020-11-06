from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from methodologies.models import Method as M
from methodologies.models import Project_Type as PT
from methodologies.models import Phase as Ph
from files.models import Associated_File as AF
import os
import shutil
import zipfile
import json
from copy import deepcopy


class Command(BaseCommand):
    help = "Exports a methodology: requires the guid of the project_type"

    def add_arguments(self, parser):
        parser.add_argument(
            "-g", dest="guid", help="Specify <guid> of model to serialize"
        )

    def handle(self, *args, **options):
        export_list = []
        flag = True

        if options["guid"]:
            guid = options["guid"]
            for pts in PT.objects.all():
                if guid == pts.guid:
                    self.stdout.write("%s matches %s\n" % (options["guid"], pts.title))
                    self.stdout.write("Exporting Methodology: %s" % pts.title)
                    pt = pts
                    export_dir = "/django/exports/%s" % pt.guid
                    file_name = "%s." % pt.guid
                    flag = False
                    method_list = []
                    phase_list = []
                    file_list = []
                    delte_list = []
                    if os.access(export_dir, os.F_OK):
                        pass
                    else:
                        os.mkdir(export_dir)
                    for phase in pt.phase.all():
                        phase_list.append(phase)
                        for method in phase.method_set.all():
                            if pt in list(method.project_type.all()):
                                mCopy = M()
                                mCopy.guid = method.guid
                                mCopy.title = method.title
                                mCopy.tier = method.tier
                                mCopy.sequence = method.sequence
                                mCopy.command = method.command
                                mCopy.description = method.description
                                mCopy.automate = method.automate
                                mCopy.mangle = method.mangle
                                mCopy.help_base = method.help_base
                                mCopy.help_import = method.help_import
                                mCopy.est_time = method.est_time
                                mCopy.version = method.version
                                mCopy.phase = method.phase
                                mCopy.save()
                                mCopy.project_type.add(pt)
                                # method_list.append(method)
                                for file in method.files.all():
                                    fCopy = deepcopy(file)
                                    fCopy.id = None
                                    fCopy.content_type = None
                                    fCopy.object_id = None
                                    fCopy.save()
                                    mCopy.files.add(fCopy)
                                    file_list.append(fCopy)
                                    delte_list.append(fCopy)
                                    shutil.copy(str(file.file._get_path()), export_dir)
                                method_list.append(mCopy)
                                delte_list.append(mCopy)
                    export_list += phase_list
                    export_list.append(pt)
                    export_list += method_list + file_list
                    export = serializers.serialize(
                        "json",
                        export_list,
                        indent=2,
                        use_natural_foreign_keys=True,
                        use_natural_primary_keys=True,
                    )
                    # self.stdout.write('%s'%export)
                    export_file = open(
                        "%s/%s%s" % (str(export_dir), str(file_name), "json"), "w"
                    )
                    # json.dump(export,export_file)
                    export_file.write(export)
                    export_file.close()
                    zipf = zipfile.ZipFile(
                        "%s/%s%s" % (export_dir, file_name, "zip"),
                        "w",
                        zipfile.ZIP_DEFLATED,
                    )
                    for root, dirs, files in os.walk(export_dir):
                        for file in files:
                            zipf.write(os.path.join(root, file))
                    zipf.close()
                    for method in delte_list:
                        method.delete()
                    self.stdout.write("\n")
                    self.stdout.write("  Export Complete -> %s" % export_dir)
                    self.stdout.write("\n")
                    break
            if flag:
                self.stdout.write("\n")
                self.stdout.write("  Invalid guid - No matching Project_Type")
                self.stdout.write("\n")
        else:
            self.stdout.write("\n")
            self.stdout.write("********\n")
            self.stdout.write(
                "  Please Provide a guid for the Project_Type you wish to export\n"
            )  # '%s'%export)
            self.stdout.write(
                "  All of its related objects will be exported as well.\n"
            )
            self.stdout.write("********\n")
            self.stdout.write("\n")
