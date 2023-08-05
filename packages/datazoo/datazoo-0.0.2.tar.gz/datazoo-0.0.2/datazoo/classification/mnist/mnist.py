from __future__ import print_function
from PIL import Image

from datazoo.common.utils import *


class MNIST:
    def __init__(self, data_dir, split, download):
        """
        Create a MNIST dataset instance.
        :param data_dir: source/target folder with data
        :param split: 'train' or 'test'
        :param download: download dataset and place to `data_dir`
        """

        self.urls = [
            'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz',
        ]
        
        self.training_file = 'train.pkl'
        self.test_file = 'test.pkl'

        self.data_dir = data_dir

        if download:
            self.download()

        if split == 'train':
            data_file = self.training_file
        else:
            data_file = self.test_file

        self.data, self.targets = load_dict(os.path.join(data_dir, data_file))
        self.classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        """
        Args:
            index (int): Index
        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        img, target = self.data[index], int(self.targets[index])

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = Image.fromarray(img, mode='L')

        return {
            'index': index,
            'image': img,
            'class': target,
        }

    def _check_exists(self):
        return os.path.exists(os.path.join(self.data_dir, self.training_file)) and \
            os.path.exists(os.path.join(self.data_dir, self.test_file))

    def download(self):
        """Download the MNIST data if it doesn't exist in processed_folder already."""

        if self._check_exists():
            return

        makedir_exist_ok(self.data_dir)

        # download files
        for url in self.urls:
            filename = url.rpartition('/')[2]
            file_path = os.path.join(self.data_dir, filename)
            download_url(url, root=self.data_dir, filename=filename, md5=None)
            extract_gzip(gzip_path=file_path, remove_finished=False)

        # process and save as torch files
        print('Processing...')

        training_set = (
            read_image_file(os.path.join(self.data_dir, 'train-images-idx3-ubyte')),
            read_label_file(os.path.join(self.data_dir, 'train-labels-idx1-ubyte'))
        )
        test_set = (
            read_image_file(os.path.join(self.data_dir, 't10k-images-idx3-ubyte')),
            read_label_file(os.path.join(self.data_dir, 't10k-labels-idx1-ubyte'))
        )

        save_dict(os.path.join(self.data_dir, 'train.pkl'), training_set)
        save_dict(os.path.join(self.data_dir, 'test.pkl'), test_set)

        print('Done!')