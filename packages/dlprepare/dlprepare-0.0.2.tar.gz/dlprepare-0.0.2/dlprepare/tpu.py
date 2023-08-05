import os
import tensorflow as tf

def to_tpu(build_func):
    def inner():
        model  = build_func()
        if os.environ['COLAB_TPU_ADDR']:#USE_TPU:
            strategy = tf.contrib.tpu.TPUDistributionStrategy(
                tf.contrib.cluster_resolver.TPUClusterResolver(tpu='grpc://' + os.environ['COLAB_TPU_ADDR']))
            model = tf.contrib.tpu.keras_to_tpu_model(model, strategy=strategy)
        return model
    return inner 