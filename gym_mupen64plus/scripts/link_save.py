from gym_mupen64plus.scripts.link_rom import copy_mupen64_file


def main():
    copy_mupen64_file(output_dir_rel='../saves',
                      expect_extension=r'\.st%d')