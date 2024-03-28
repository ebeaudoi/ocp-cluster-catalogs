#!/usr/bin/env python3

import sys
import yaml
from copy import deepcopy

mirrors = {}

basic_manifest = None

while len(sys.argv) > 1:
    arg = sys.argv.pop()
    if arg == __file__:
        break
    with open(arg) as f:
        for manifest in yaml.safe_load_all(f):
            if basic_manifest is None:
                basic_manifest = deepcopy(manifest)
            manifest_mirrors = manifest.get('spec', {})
            manifest_mirrors = manifest_mirrors.get('repositoryDigestMirrors', [])
            for mirror in manifest_mirrors:
                mirrors[mirror['source']] = mirror

mirrors = [mirror for _, mirror in mirrors.items()]

basic_manifest['metadata']['name'] = 'oc-mirror-combined'
basic_manifest['spec']['repositoryDigestMirrors'] = mirrors

print('---\n' + yaml.dump(basic_manifest))
