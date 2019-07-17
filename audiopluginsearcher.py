#!/usr/bin/env python

import os
import webbrowser

def get_bundle_id(plugin):
    try:
        with open(f'{plugin}/Contents/Info.plist', 'r') as info:
            found = False
            for line in info:
                if found:
                    return line.partition('>')[2].partition('<')[0]
                if 'CFBundleIdentifier' in line:
                    found = True
    except:
        return


def scan_aax_plugins(aaxDirectory='/Library/Application Support/Avid/Audio/Plug-Ins'):
    for item in os.scandir(aaxDirectory):
        bundleId = get_bundle_id(item.path)
        if bundleId:
            developer = bundleId.partition('.')[2].lower().split('.')[0]
            name = bundleId.rpartition('.')[2].lower()
            yield developer, name


def search_for_plugin_downloads(
        format='aax', developerOnly=True,
        pluginDirectory='/Library/Application Support/Avid/Audio/Plug-Ins'
    ):
    searched = set()
    for developer, plugin in scan_aax_plugins(
            aaxDirectory=pluginDirectory
        ):
        if (
                'avid' in developer
                or 'digidesign' in developer
                or (developerOnly and developer in searched)
            ):
            continue
        searched.add(developer)
        url = 'https://www.google.com.tr/search?q={}'.format(
                f'{developer} {plugin} {format} download'
            )
        webbrowser.open(url)


if __name__ == '__main__':
    search_for_plugin_downloads()
