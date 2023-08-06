from typing import List

from .version import Version


class FolderVersionCreator(object):
    """
    utility class that allows to create quickly `Version` object from  SQL file
    in a folder
    """

    def __init__(self, path_prefix):
        """
        Create an instant.

        :param path_prefix: the folder path. "/" should NOT be at the end.
        """
        if path_prefix[-1] == '/':
            raise Exception("please do not put / at the end of path prefix")

        self.path_prefix = path_prefix

    def create_version(self, version_code, version_file, version_comment):
        return Version(
            version_code, version_comment,
            sql_file=f"{self.path_prefix}/{version_file}"
        )


def create_multiple_empty_versions(version_codes: List[str]) -> List[Version]:
    """Create empty versions. Can be useful when "compressing" versions
    """
    versions: List[Version] = []
    for version_code in version_codes:
        version = Version(version_code, "", "select 1")
        versions.append(version)

    return versions
