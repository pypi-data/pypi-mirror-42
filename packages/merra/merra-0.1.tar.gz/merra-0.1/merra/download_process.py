from merra.download import main

if __name__ == '__main__':

    # define args
    args = [
        '/home/fzaussin/shares/radar/Datapool_raw/'
        'Earth2Observe/MERRA2/datasets/download_test',
        '-s',
        '1980-01-01',
        '-e',
        '1980-01-01',
        '--username',
        'fzaussin',
        '--password',
        'HeT8zzDzOEea']

    # run command line script here for debugging
    main(args)