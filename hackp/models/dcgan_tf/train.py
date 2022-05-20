import os
import time
import argparse
import numpy as np
from os import listdir
import tensorflow as tf
from pathlib import Path

import wandb
#from wandb.keras import WandbCallback

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

    return gen_loss, disc_loss


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, help='The path to .npy dataset files')
    args = parser.parse_args()

    data_path = Path(args.dataset)

    data_files = [data_path.joinpath(f) for f in listdir(data_path)]

    image_size = 256

    train_images = np.concatenate( [np.load(df).astype('float32').reshape(-1, image_size, image_size) for df in data_files])
    print("Train images: ",len(train_images))

    train_images = np.expand_dims(train_images, axis=-1)
    print(train_images.shape)

    BUFFER_SIZE = len(train_images)
    BATCH_SIZE = 128

    train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)


    generator = make_generator_model(image_size)

    noise = tf.random.normal([1, 100])

    generated_image = generator(noise, training=False)

    #plt.figure()
    #ax = plt.subplot()
    #ax.imshow(generated_image[0, :, :, 0], cmap='gray')
    #plt.savefig(f"noise.png")

    discriminator = make_discriminator_model(image_size)
    decision = discriminator(generated_image)
    print (decision)


    cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

    learning_rate = 1e-4
    generator_optimizer = tf.keras.optimizers.Adam(learning_rate)
    discriminator_optimizer = tf.keras.optimizers.Adam(learning_rate)


    checkpoint_dir = './training_checkpoints'
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
    checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                    discriminator_optimizer=discriminator_optimizer,
                                    generator=generator,
                                    discriminator=discriminator)



    EPOCHS = 50
    noise_dim = 100
    num_examples_to_generate = 16

    """
    config = dict (
        entity="leobaro_",
        architecture = "DCGAN",
        machine = "ibmtest",
        job_type='train',
        batch_size = BATCH_SIZE,
        model = args.model_name,
        epochs = EPOCHS
    )
    run = wandb.init(
        project="hack-the-planets-2022",
        config=config
    )
    """


    # You will reuse this seed overtime (so it's easier)
    # to visualize progress in the animated GIF)
    seed = tf.random.normal([num_examples_to_generate, noise_dim])


    for epoch in range(EPOCHS):

        start = time.time()

        for ii, image_batch in enumerate(train_dataset):

            gen_loss, disc_loss = train_step(image_batch)

            # wandb.tensorflow.log(tf.summary.merge_all())

            # Produce images for the GIF as you go
            # display.clear_output(wait=True)
            generate_and_save_images(generator, epoch + 1, seed)

            # Save the model every 5 epochs
            if (epoch + 1) % 5 == 0:
                checkpoint.save(file_prefix = checkpoint_prefix)

            print (f'Time for epoch {epoch + 1} batch {ii} with shape {image_batch.shape} is {round(time.time()-start, 4)} sec. Gen loss {round(gen_loss, 4)} Disc loss {round(disc_loss, 4)}')

    generate_and_save_images(generator, EPOCHS, seed)
