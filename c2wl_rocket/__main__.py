from __future__ import absolute_import
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="C2WL-Rocket",
        description='Customizable CWL Rocket - A highly flexible CWL execution engine.'
    )

    parser.add_argument('-p', '--exec-profile',
        help="Specify an exec profile."
    )

    parser.add_argument('cwl_document',
        help="Provide a CWL workflow or tool."
    )
    
    parser.add_argument('input_params',
        help="Provide input parameters in YAML or JSON format."
    )

    args = parser.parse_args()
    
    # hand arguments over to main exec function:
    pass

if __name__ == "__main__":
    main()