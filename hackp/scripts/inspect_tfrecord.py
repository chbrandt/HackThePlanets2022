import argparse
import tensorflow as tf

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help='The path to an input tfrecord file')
    args = parser.parse_args()

    for example in tf.python_io.tf_record_iterator(args.file):
        print(tf.train.Example.FromString(example))
