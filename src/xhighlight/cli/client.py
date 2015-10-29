def client(control_path, regions):

    with open(control_path, 'w') as control:

        for region in regions:

            print(
                '{width}×{height}+{x}+{y}'.format(**region),
                file=control
            )
