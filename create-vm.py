#!/usr/bin/env python3

import subprocess
import argparse

os_links = {'debian8': "'http://ftp.jaist.ac.jp/pub/Linux/debian/dists/jessie/main/installer-amd64/'",
            'debian7': "'http://ftp.nl.debian.org/debian/dists/jessie/main/installer-amd64/'",
            'centos7': "'http://mirror.i3d.net/pub/centos/7/os/x86_64/'",
            'centos66': "'http://mirror.i3d.net/pub/centos/6.6/os/x86_64/'",
            'centos6': "'http://mirror.i3d.net/pub/centos/6/os/x86_64/'",
            'ubuntu1504': "'http://archive.ubuntu.com/ubuntu/dists/vivid/main/installer-amd64/'",
            'ubuntu1410': "'http://archive.ubuntu.com/ubuntu/dists/utopic/main/installer-amd64/'",
            'ubuntu1404': "'http://archive.ubuntu.com/ubuntu/dists/trusty/main/installer-amd64/'",
            }


def get_os_names():
    names = ''
    for k in os_links.keys():
        names += k + '\n'

    return names


def get_args():
    """
    -n VM name
    -i What os to Install (see below)
    -r RAM
    -c # of CPUs
    -d Disk image name (located in /media/nas/vm/
    -t OS type e.g. linux, windows
    -v OS variant e.g. debianwheezy, centos6

    We support the following OS installations:
    centos7
    centos66
    centos6
    debian8
    debian7
    ubuntu1504
    ubuntu1410
    ubuntu11404
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help="Name of VM")
    parser.add_argument("-i", "--install", required=True, help="OS to install: " + get_os_names())
    parser.add_argument("-d", "--disk", required=True,
                        help="Name for disk image")
    parser.add_argument("-r", "--ram", help="Ram in MB")
    parser.add_argument("-c", "--cpus", help="Number of vCPUs")
    parser.add_argument("-t", "--ostype", help="OS type")
    parser.add_argument("-v", "--variant", help="OS Variant")

    args = parser.parse_args()
    arg_dict = {'name': args.name, 'disk': args.disk, 'install': args.install}
    if args.ram is not None:
        arg_dict['ram'] = args.ram
    if args.cpus is not None:
        arg_dict['cpus'] = args.cpus
    if args.ostype is not None:
        arg_dict['type'] = args.ostype
    if args.variant is not None:
        arg_dict['variant'] = args.variant

    return arg_dict


def generate_command(args):
    command = "virt-install --name " + args.get('name') \
              + " --ram " + args.get('ram', "1024") \
              + " --cpus " + args.get('cpus', "2") \
              + " --disk path=/media/nas/vm/" + args.get('disk') + ",size=10" \
              + " --os-type " + args.get('type', "linux") \
              + " --location " + os_links.get(args.get('install')) \
              + " --console pty,target_type=serial" \
              + " --noautoconsole" \
              + " --extra-args 'console=ttyS0,115200n8 serial'"
    if "variant" in args:
        command = command + " --os-variant " + args.get('variant')

    return command


def main():
    args = get_args()
    command = generate_command(args)

    print("Right, let's get " + args['name'] + " installed!")

    output = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, shell=True)
    for line in output.stdout:
        print(line, end='')

    print("\nUse 'sudo virsh console " + args['name'] + "' to connect to the VM to finish the install.")


if __name__ == "__main__":
    main()
