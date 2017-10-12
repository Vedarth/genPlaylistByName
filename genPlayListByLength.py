#!/usr/bin/env python

'''
Created on Apr 4, 2014

@author: Alejandro Alcalde

Licensed under GPLv3

More info: http://wp.me/p2kdv9-Bq
'''

import argparse
import fnmatch

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC

from collections import deque
from os.path import os, basename
from sys import argv
from random import shuffle

curr_length = 0
playlist_number = 1

def main():

    parser = argparse.ArgumentParser(description='Generate playlists with the indicated length')
    parser.add_argument('-d','--directory', help='Directory with music files',type=str, required=True)
    parser.add_argument('-l', '--length', help='Length of the playlist, in minutes', type=int, required=True)

    args = parser.parse_args()

    directory = args.directory
    length =  args.length * 60

    path = r'./playlists/'
    if not os.path.exists(path): os.makedirs(path)
    
    playlist_basename = 'playlist_' #basename(argv[0][:-3]) + '_'
    curr_items = []
    too_long_items = []
    all_items = []

    dir_queue = deque([directory])
    while len(dir_queue) != 0:
        cur_directory = dir_queue.popleft()
        for node in os.listdir(cur_directory):
            node = os.path.join(cur_directory, node)
            if os.path.isdir(node):
                dir_queue.append(node)
            elif fnmatch.fnmatch(node, '*.mp[43]') or fnmatch.fnmatch(node, '*.flac'):
                all_items.append(node)
        
    shuffle(all_items)

    for item in all_items:
        global curr_length
        if curr_length >= length:
            create_playlist(path, playlist_basename, curr_items)
        else:
            encoding = item[-4:]
            encodings = {'.mp3': MP3, '.mp4': MP4, 'flac': FLAC}
            try:
                music_file = encodings[encoding](item)
            except Exception as e:
                handleException(e)
            else:
                file_length = music_file.info.length
                if file_length > length:
                    too_long_items.append(item)
                    print("File %s exceed the given length (%s min)" % (item, file_length/60))
                else:
                    curr_length += file_length
                    curr_items.append(item+'\n')

    if curr_items:
        create_playlist(path, playlist_basename, curr_items)

    if too_long_items:
        print("\nThis files exceeded the given length and were not added to any playlist...\n")
        for i in too_long_items:
            print(basename(i))

def create_playlist(path, playlist_basename, curr_items):
    global playlist_number, curr_length
    name = path + str(playlist_number) + '. ' + playlist_basename + str(int(curr_length/60)) + 'min' + '.m3u'
    playlist_file = open(name, 'w')
    playlist_file.writelines(curr_items)
    playlist_file.close()
    print('Playlist generated, name: ', name , ' length ', curr_length/60 , 'min')
    playlist_number += 1
    curr_length = 0
    del curr_items[:]

def handleException(e):
    print(type(e))     # the exception instance
    print(e.args)      # arguments stored in .args
    print(e)           # __str__ allows args to printed directly

if __name__ == '__main__':
    main()
