from subprocess import run, CalledProcessError
from sys import exit

from termcolor import cprint


def gen_csr_with_new_cert(fqdn, subject, password, altnames=None):
    command = [
        'openssl', 'req', '-newkey', 'rsa:4096', '-keyout',
        '{}.key'.format(fqdn), '-out', '{}.req'.format(fqdn), '-subj',
        subject
    ]
    if altnames != None:
        for domain in altnames:
            command.append('-addext')
            command.append('"subjectAltName = {}"'.format(domain))
        print(command)
    if not password:
        command.append('-nodes')
    try:
        run(command, check=True)
    except CalledProcessError:
        cprint('There was an error in openssl, please check the output', 'red')
        exit(1)
    with open('{}.req'.format(fqdn)) as f:
        return f.read()


def gen_csr_with_existing_cert(key_path, fqdn, subject, additional=None):
    try:
        run([
            'openssl', 'req', '-new', '-key', key_path, '-out',
            '{}.req'.format(fqdn), '-subj', subject
        ])
    except CalledProcessError:
        cprint('There was an error in openssl, please check the output', 'red')
        exit(1)
    with open('{}.req'.format(fqdn)) as f:
        return f.read()
