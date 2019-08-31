from argparse import ArgumentParser
import os
import shutil


def main():
    copy_mupen64_file(output_dir_rel='../ROMS',
                      expect_extension='\.[zn]64')


def copy_mupen64_file(output_dir_rel, expect_extension):
    args = parse_args()
    if not os.path.exists(args.filename):
        raise Exception('No such file: ' + args.filename)

    dest_filename = os.path.basename(args.filename)
    if args.link_name:
        dest_filename = args.link_name

    check_file_extension(dest_filename, expect_extension)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, output_dir_rel)
    dest_path = os.path.join(output_dir, dest_filename)

    print('Copying %s to %s' % (args.filename, dest_path))
    shutil.copyfile(args.filename, dest_path)


def check_file_extension(filename, expect_extension):
    actual_ext = os.path.splitext(filename)[1]
    if actual_ext.lower() == expect_extension.lower():
        return

    prompt = (f'WARNING: The extension {actual_ext} does not match expected '
              f'file extension {expect_extension}, copy file anyway? (y/n)')

    if input(prompt).lower().strip() != 'y':
        print('Aborting copy.')
        exit(1)


def parse_args():
    p = ArgumentParser()
    p.add_argument('--link-name', '-ln', help='Filename of copied file (default to source filename).')
    p.add_argument('filename', help='Name of ROM/save file to link')
    return p.parse_args()


if __name__ == '__main__':
    main()