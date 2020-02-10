# from google_images_download import google_images_download as gd
import google_images_download as gd
import codecs
import alias_generator as ag
import pdb
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--add_alias', help='boolean option to add aliases', type=bool, default='True')
parser.add_argument('-f', '--keywords_file', help='file name for list of keywords', type=str, default='gen1.txt')
parser.add_argument('-l', '--limit', help='str type of limit size per keyword', type=str, default='10')

args = vars(parser.parse_args())

if args['add_alias'] == True:
    alias_list = codecs.open(ag.generate_alias(), 'r', encoding='utf8').readlines()
else:
    alias_list = codecs.open(args['keywords_file'], 'r', encoding='utf8').readlines()

downloader = gd.googleimagesdownload()
arguments = dict()

for aliases in alias_list:
    aliases = aliases.strip()
    splits = aliases.split(' ')
    dir_name = splits[0].strip()
    keywords = ', '.join([keyword.replace('_', ' ') for keyword in splits[1:]])
    pdb.set_trace()

    arguments['keywords'] = keywords
    arguments['image_directory'] = dir_name
    arguments['limit'] = args['limit']
    arguments['no_numbering'] = True

    paths, errors = downloader.download_executor(arguments)


