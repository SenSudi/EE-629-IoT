def project_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<project_id>/<subdirectory>/<filename>
    try:
        project = instance.project.id
    except Exception as e:
        pass
    else:
        return "{0}/{1}/{2}".format(
            instance.project.id, instance.subdirectory, filename
        )
        # If no project is associated with the instance, use the subdirectory
    return "{0}/{1}".format(instance.subdirectory, filename)


def issue_file_path(instance, filename):
    num = instance.issue_number
    pid = instance.associated_project.id
    return "{0}/{1}/{2}/{3}".format(pid, "issues", num, instance.filename)


def feedback_file_path(instance, filename):
    user_id = instance.sender.id
    return "{0}/{1}".format(user_id, filename)


def size_conversion(fsize):
    system = [
        (1024 ** 0, " b"),
        (1024 ** 1, " Kb"),
        (1024 ** 2, " Mb"),
        (1024 ** 3, " Gb"),
    ]
    # fsize = str(fsize)
    # if len(fsize) <= 3:
    # 	return size(fsize)
    # if len(fsize > 3 and fsize < 7):
    # 	fsize = size(fsize)
    # 	return fsize
    return size(fsize, system=system)


"""
The code below is taken from hurry.filesize v0.9
https://pypi.python.org/pypi/hurry.filesize/

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY EXPRESSED
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

traditional = [
    (1024 ** 5, "P"),
    (1024 ** 4, "T"),
    (1024 ** 3, "G"),
    (1024 ** 2, "M"),
    (1024 ** 1, "K"),
    (1024 ** 0, "B"),
]

alternative = [
    (1024 ** 5, " Pb"),
    (1024 ** 4, " Tb"),
    (1024 ** 3, " Gb"),
    (1024 ** 2, " Mb"),
    (1024 ** 1, " Kb"),
    (1024 ** 0, (" byte", " bytes")),
]

verbose = [
    (1024 ** 5, (" petabyte", " petabytes")),
    (1024 ** 4, (" terabyte", " terabytes")),
    (1024 ** 3, (" gigabyte", " gigabytes")),
    (1024 ** 2, (" megabyte", " megabytes")),
    (1024 ** 1, (" kilobyte", " kilobytes")),
    (1024 ** 0, (" byte", " bytes")),
]

iec = [
    (1024 ** 5, "Pi"),
    (1024 ** 4, "Ti"),
    (1024 ** 3, "Gi"),
    (1024 ** 2, "Mi"),
    (1024 ** 1, "Ki"),
    (1024 ** 0, ""),
]

si = [
    (1000 ** 5, "P"),
    (1000 ** 4, "T"),
    (1000 ** 3, "G"),
    (1000 ** 2, "M"),
    (1000 ** 1, "K"),
    (1000 ** 0, "B"),
]


def size_conversion(size, system=alternative):
    """Human-readable file size.

	Using the alternative system, where a factor of 1024 is used::
	>>> size_conversion(10)
    '10 bytes'

    >>> size_conversion(1)
    '1 byte'

    >>> size_conversion(1024)
    '1 Kb'

    alternative = [
    (1024 ** 5, ' Pb'),
    (1024 ** 4, ' Tb'), 
    (1024 ** 3, ' Gb'), 
    (1024 ** 2, ' Mb'), 
    (1024 ** 1, ' Kb'),
    (1024 ** 0, (' byte', ' bytes')),
    ]
	"""

    for factor, suffix in system:
        if size >= factor:
            break
    amount = float(float(size) / float(factor))

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount)[: str(amount).rfind(".") + 3] + suffix
