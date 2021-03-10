import sys
import dbus
import argparse
import os
import requests
import shutil


def get_all_data():
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object(
        'org.mpris.MediaPlayer2.spotify',
        '/org/mpris/MediaPlayer2'
    )
    spotify_properties = dbus.Interface(
        spotify_bus,
        'org.freedesktop.DBus.Properties'
    )

    metadata = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
    status = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
    desired_values = ['xesam:artist', 'xesam:title', 'xesam:album', 'mpris:trackid']
    return {v.split(':')[1]: metadata[v] for v in desired_values}


def update_cover(data):
    path_to_covers = os.path.abspath(__file__).replace('spotify.py', 'covers')
    path_to_current_cover = os.path.abspath(__file__).replace('spotify.py', 'cover.jpg')

    covers_list = os.listdir(path_to_covers)
    short_track_id = data["trackid"].split(':')[-1]

    def set_new_cover():
        try:
            current_cover = [x for x in covers_list if '_current.jpg' in x][0]
            os.rename(
                os.path.join(path_to_covers, current_cover),
                os.path.join(path_to_covers, current_cover.replace('_current', ''))
            )
        except IndexError as e:
            pass
        os.rename(
            os.path.join(path_to_covers, f'{short_track_id}.jpg'),
            os.path.join(path_to_covers, f'{short_track_id}_current.jpg'),
        )
        shutil.copy(os.path.join(path_to_covers, f'{short_track_id}_current.jpg'), path_to_current_cover)

    if f'{short_track_id}_current.jpg' in covers_list:
        return
    elif f'{short_track_id}.jpg' in covers_list:
        set_new_cover()
        return

    if len(covers_list) > 10:
        _ = [os.remove(os.path.join(path_to_covers, i)) for i in covers_list]
        covers_list.clear()

    new_cover_url = requests.get(f'https://open.spotify.com/oembed?url={data["trackid"]}').json()['thumbnail_url']
    new_cover_bytes = requests.get(new_cover_url).content

    with open(os.path.join(path_to_covers, f'{short_track_id}.jpg'), 'wb') as f:
        f.write(new_cover_bytes)

    set_new_cover()


if __name__ == '__main__':
    try:
        data = get_all_data()
    except dbus.DBusException as e:
        print('')
    else:
        variants = {
            'title': lambda data: data['title'],
            'artist': lambda data: data['artist'][0],
            'album': lambda data: data['album'],
            'update_cover': update_cover
        }

        arg = sys.argv[1]

        print(variants[arg](data))