import os
import time
import argparse
import numpy as np
from tqdm import tqdm
from os import listdir
import tensorflow as tf
from pathlib import Path
import matplotlib.pyplot as plt

from hackp.models.dcgan_tf.utils import *
from hackp.models.dcgan_tf.generator import *
from hackp.models.dcgan_tf.discriminator import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

# Notice the use of `tf.function`
# This annotation causes the function to be "compiled".
@tf.function
def train_step(images):
    noise = tf.random.normal([BATCH_SIZE, noise_dim])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
      generated_images = generator(noise, training=True)

      real_output = discriminator(images, training=True)
      fake_output = discriminator(generated_images, training=True)

      gen_loss = generator_loss(fake_output)
      disc_loss = discriminator_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, help='The path to .npy dataset files')
    args = parser.parse_args()

    data_path = Path(args.dataset)

    data_files = [data_path.joinpath(f) for f in listdir(data_path)]
    
    image_size = 1024

    
    train_images = np.concatenate( [np.load(df).astype('float32').reshape(-1, image_size, image_size) for df in data_files[0:2]] )

    print(train_images.shape)

    BUFFER_SIZE = 781
    BATCH_SIZE = 32
    
    train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
    

    generator = make_generator_model(image_size)

    noise = tf.random.normal([1, 100])
    
    generated_image = generator(noise, training=False)

    plt.figure()
    ax = plt.subplot()
    ax.imshow(generated_image[0, :, :, 0], cmap='gray')
    plt.savefig(f"noise.png")

    discriminator = make_discriminator_model(image_size)
    decision = discriminator(generated_image)
    print (decision)


    cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)


    generator_optimizer = tf.keras.optimizers.Adam(1e-4)
    discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)


    checkpoint_dir = './training_checkpoints'
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
    checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                    discriminator_optimizer=discriminator_optimizer,
                                    generator=generator,
                                    discriminator=discriminator)

    EPOCHS = 50
    noise_dim = 100
    num_examples_to_generate = 16

    # You will reuse this seed overtime (so it's easier)
    # to visualize progress in the animated GIF)
    seed = tf.random.normal([num_examples_to_generate, noise_dim])


    for epoch in range(EPOCHS):

        start = time.time()

        for image_batch in train_dataset:
            
            train_step(image_batch)

            # Produce images for the GIF as you go
            # display.clear_output(wait=True)
            generate_and_save_images(generator, epoch + 1, seed)

            # Save the model every 15 epochs
            if (epoch + 1) % 15 == 0:
                checkpoint.save(file_prefix = checkpoint_prefix)

            print ('Time for epoch {} is {} sec'.format(epoch + 1, time.time()-start))

    generate_and_save_images(generator, EPOCHS, seed)