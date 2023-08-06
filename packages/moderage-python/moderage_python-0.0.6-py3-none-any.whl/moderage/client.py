import re
import magic
import requests
from tqdm import tqdm
import json
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from pathlib import Path
import logging


class ModeRageClient():

    def __init__(self, host='http://localhost', port='8118', cache_location=None):

        self._logger = logging.getLogger("Mode Rage client")

        self._host = host
        self._port = port

        self._root_url = '%s:%s/v0/experiment' % (host, port)

        if not cache_location:
            self._cache_location = Path.home().joinpath('.moderage')
            if not self._cache_location.exists():
                self._cache_location.mkdir()

        self._logger.debug('Cache location: [%s]' % str(self._cache_location))

    def save(self, meta_category, meta, files):
        """

        :param meta_category: A category name for this experiment, or this dataset
        :param meta: meta information for this experiment or dataset
        :param files: A list of files and metadata associated with this experiment or dataset

        Files must be in the following format:

        [
            "filename": "./path/to/my/file.xyz",
            "caption": "This is a description of my file"
        ]

        :return:
        """

        self._logger.info('Saving data to category %s' % meta_category)

        create_payload = {
            'metaCategory': meta_category,
            'meta': meta,
        }

        file_info_payload = {
            'files': [self._process_file_info(f) for f in files]
        }

        create_response = requests.post('%s/create' % self._root_url, json=create_payload)

        assert create_response.status_code == 201, create_response.json()

        experiment = create_response.json()
        id = experiment['id']

        multipart_payload = [('files', (f['filename'], open(f['filename'], 'rb'))) for f in files]
        multipart_payload.append(('file_metadata', (None, json.dumps(file_info_payload))))
        multipart_encoder = MultipartEncoder(multipart_payload)

        self._logger.info('Experiment saved with id [%s]' % id)
        self._logger.info('Uploading %d files to experiment [%s]' % (len(files), id))

        # Set up a progress bar for upload progress
        with(tqdm(total=multipart_encoder.len, ncols=100, unit="bytes")) as progress_bar:
            last_bytes_read = 0

            # Callback for progress to be output by tqdm progress bar
            def _upload_progress(monitor):
                nonlocal last_bytes_read
                progress_diff = monitor.bytes_read - last_bytes_read
                progress_bar.update(progress_diff)
                last_bytes_read = monitor.bytes_read

            multipart_monitor = MultipartEncoderMonitor(multipart_encoder, _upload_progress)

            upload_response = requests.post(
                '%s/%s/%s/uploadFiles' % (self._root_url, meta_category, id),
                data=multipart_monitor,
                headers={'Content-Type': multipart_encoder.content_type}
            )

        assert upload_response.status_code == 200, upload_response.json()

        return upload_response.json()

    def load(self, id, meta_category):

        self._logger.info('Loading data with id [%s] in category [%s]' % (id, meta_category))

        get_response = requests.get('%s/%s/%s' % (self._root_url, meta_category, id))
        assert get_response.status_code == 200, get_response.json()
        experiment = get_response.json()

        self._logger.info('Meta Info:')
        for k_m, v_m in experiment['meta'].items():
            self._logger.info('%s: %s' % (k_m, str(v_m)))

        self._logger.info('%d files found' % len(experiment['files']))

        # download the files from their uris
        for file_info in experiment['files']:

            cache_folder = self._cache_location.joinpath(meta_category, id)

            if not cache_folder.exists():
                cache_folder.mkdir(parents=True)

            cached_filename = cache_folder.joinpath(file_info['id'])

            # If we have not cached the file already, download it and move it to the cache directory
            if not cached_filename.exists():
                self._logger.info('Downloading file: %s' % file_info['filename'])
                self._download_file(file_info, str(cached_filename))
            else:
                self._logger.info('File found in cache: %s' % file_info['filename'])

            file_info['file'] = open(str(cached_filename), 'rb')

        return experiment

    def _download_file(self, file_info, cached_filename):

        location = file_info['location']
        startswith = location.startswith('https://s3.amazonaws.com')
        if startswith:
            import boto3
            import botocore
            # Download the file
            s3 = boto3.client('s3')

            m = re.search('https://s3.amazonaws.com/(?P<bucket>\w+)/(?P<key>.+)', location)

            bucket = m.group('bucket')
            key = m.group('key')

            file_size = s3.head_object(Bucket=bucket, Key=key)['ContentLength']

            with(tqdm(total=file_size, ncols=100, unit="bytes", ascii="Downloading %s" % file_info['filename'])) as progress_bar:

                # Callback for progress to be output by tqdm progress bar
                def _download_progress(chunk):
                    progress_bar.update(chunk)

                s3.download_file(bucket, key, cached_filename, Callback=_download_progress)

        elif location.startswith('http'):

            # Download the file
            with requests.get(location) as r:
                with open(cached_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)

    def _process_file_info(self, file):
        """
        Get the mime type of the file
        :param file:
        :return:
        """
        file['contentType'] = magic.from_file(file['filename'], True)

        return file
