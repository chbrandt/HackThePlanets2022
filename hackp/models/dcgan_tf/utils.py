import matplotlib.pyplot as plt

def generate_and_save_images(model, epoch, test_input):
  # Notice `training` is set to False.
  # This is so all layers run in inference mode (batchnorm).
  predictions = model(test_input, training=False)

  fig = plt.figure(figsize=(4, 4))
  # print(f"predictions shape: {predictions.shape}")
  images = range(predictions.shape[0])
  for i in images[0:16]:
      plt.subplot(4, 4, i+1)
      plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5, cmap='magma')
      plt.axis('off')

  fig.savefig('image_at_epoch_{:04d}.png'.format(epoch))
  plt.close()
  # plt.show()
