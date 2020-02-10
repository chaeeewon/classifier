import codecs
import pdb

POKE_LIST = 'gen1.txt'
ALIAS_LIST = 'gen1_alias.txt'
SUFFIXES = ['pokemon', 'pokemon_image']
PREFIXES = ['cute']

def generate_alias():
    poke_names = codecs.open(POKE_LIST, 'r', encoding='utf8').readlines()
    alias_poke_names = codecs.open(ALIAS_LIST, 'w', encoding='utf8')

    for name in poke_names:
        name = name.strip().replace('\'', '').replace('\.', '')
        alias = list()
        alias.append(name)
        for suffix in SUFFIXES:
            alias.append('{}_{}'.format(name, suffix.strip()))
        for prefix in PREFIXES:
            alias.append('{}_{}'.format(prefix.strip(), name))
        
        aliasline = name.strip() + ' ' + ' '.join([x for x in alias])
        alias_poke_names.write(aliasline + '\n')
        
    return ALIAS_LIST


            


