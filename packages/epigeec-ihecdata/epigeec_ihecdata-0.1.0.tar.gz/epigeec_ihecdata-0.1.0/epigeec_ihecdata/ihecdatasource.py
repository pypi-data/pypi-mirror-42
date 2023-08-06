# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os.path
import glob

from .ihecdata import IhecData

class IhecDatasource(object):
    @staticmethod
    def get_ihecdatas(basenames, assembly, release):
        raise NotImplementedError

class Mp2bMountIhecDatasource(IhecDatasource):
    DIR = '/nfs3_ib/10.4.217.32/home/genomicdata/ihec_datasets/{release}/*/{assembly}/*'
    SPECIAL_HG38_SHIRAHIGE = '/nfs3_ib/10.4.217.32/home/genomicdata/ihec_datasets/{release}/shirahige/*'

    @staticmethod
    def _create_cache(assembly, release):
        files = glob.glob(Mp2bMountIhecDatasource.DIR.format(
            release=release,
            assembly=assembly
        ))

        if 'hg38' == assembly:
            files.extend(glob.glob(Mp2bMountIhecDatasource.SPECIAL_HG38_SHIRAHIGE.format(
                release=release
            )))

        return {
            os.path.basename(path): path
            for path in files
        }

    @staticmethod
    def get_ihecdatas(basenames, assembly, release):
        cache = Mp2bMountIhecDatasource._create_cache(assembly, release)
        return [
            IhecData(
                uri=cache.get(basename),
                basename=basename,
                assembly=assembly,
                release=release
            )
            for basename in basenames
        ]

class LocalIhecDatasource(IhecDatasource):
    DIR = '{release}/{assembly}/*'

    @staticmethod
    def _create_cache(assembly, release):
        return {
            os.path.basename(path): path
            for path in glob.glob(LocalIhecDatasource.DIR.format(
                release=release,
                assembly=assembly
            ))
        }
    
    @staticmethod
    def get_ihecdatas(basenames, assembly, release):
        cache = LocalIhecDatasource._create_cache(assembly, release)
        return [
            IhecData(
                uri=cache.get(basename),
                basename=basename,
                assembly=assembly,
                release=release
            )
            for basename in basenames
        ]