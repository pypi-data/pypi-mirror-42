import io
import tensorflow as tf
import PIL


def iterate_tfrecord(filename):
    """Iterate through a tfrecord file.

    Args:
        filename (str): Filename to iterate.
        decode (bool): Optionally pass all records to example decoder function.
            False by default.

    Returns: Iterator of tfrecords.
    """
    for record in tf.python_io.tf_record_iterator(filename):
        example = tf.train.Example()
        example.ParseFromString(record)
        yield example


def save_tfrecords(records, output_filename):
    """Save all tfrecord examples to file.

    Args:
        records (Iterator[tf.train.Example]): Iterator of records to save.
        output_filename (str): Output file to save to.
    """
    with tf.python_io.TFRecordWriter(output_filename) as tfrecord_writer:
        for record in records:
            tfrecord_writer.write(record.SerializeToString())


def get_jpeg_string(image):
    """Builds PNG string from mask array.

    Args:
        image (PIL.Image): Mask array to generate PNG string from.

    Returns: String of mask encoded as a PNG.
    """
    # Save the new image to a PNG byte string.
    byte_buffer = io.BytesIO()
    image.save(byte_buffer, format='jpeg')
    byte_buffer.seek(0)
    return byte_buffer.read()


def get_png_string(mask_array):
    """Builds PNG string from mask array.

    Args:
        mask_array (HxW): Mask array to generate PNG string from.

    Returns: String of mask encoded as a PNG.
    """
    # Convert the new mask back to an image.
    image = PIL.Image.fromarray(mask_array.astype('uint8')).convert('RGB')
    # Save the new image to a PNG byte string.
    byte_buffer = io.BytesIO()
    image.save(byte_buffer, format='png')
    byte_buffer.seek(0)
    return byte_buffer.read()


class TFRecordHelper(object):
    """"Base class for interfacing with TFRecords. """

    def __init__(self, *filenames, output_filename=None):
        """
        Args:
            filenames: List of filenames to read from
            output_filename: Optional output_filename to use if multiple
                input filenames.
        """
        self.filenames = filenames
        self.output_filename = output_filename
        self._generator = None

    def __iter__(self):
        self._generator = self.read()
        return self

    def __next__(self):
        return next(self._generator)

    def read(self, decode=False):
        for filename in self.filenames:
            for record in iterate_tfrecord(filename):
                if decode:
                    yield self.decode_single_example(record)
                else:
                    yield record

    def write(self, records):
        if len(self.filenames) > 1 and not self.output_filename:
            raise Exception("Must provide output filename if more than one "
                            "input filename.")
        save_tfrecords(records, self.filename)

    @classmethod
    def decode_tensor(cls, example):
        """Decodes a tensor, used when creating dataset for training.

        Arguments:
            example (what type????): example tensor
        Returns: Dict[str, tf.Tensor (CHANGE)]
        """
        raise NotImplementedError()

    @classmethod
    def decode_single_example(cls, example):
        """Decode example to dictionary for easy interactive use.
        """
        raise NotImplementedError()

    @classmethod
    def build_example(cls, *args):
        """Build tfrecord example from input data.

        Used to create initial dataset.
        """
        raise NotImplementedError()
