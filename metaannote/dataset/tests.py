import unittest
from pathlib import Path
from metaannote.dataset.dataset import CocoDataset


class DatasetTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.ann_p = Path('/home/lizard/PycharmProjects/annotation_tool/output/results.json')
        self.im_p = Path('/media/lizard/New Volume/Data/Drone/CustomeCocoDataset/Mobius/Train/Annotations/images')

    def test_create_new_coco_dataset_object(self):
        """
        create a coco dataset
        :return:
        """
        ds = CocoDataset()
        ds.build(image_dir=self.im_p, annotation=self.ann_p)
        self.assertIsNotNone(next(ds.get_data_iter))


if __name__ == '__main__':
    unittest.main()
