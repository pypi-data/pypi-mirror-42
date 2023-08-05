from keras.callbacks import Callback
import joblib
import os


def store_train_params(runtime, model_id, x, y):
    joblib.dump(x, '%s/%s_x_train.pkl' % (runtime.build_path, model_id), True)
    joblib.dump(y, '%s/%s_y_train.pkl' % (runtime.build_path, model_id), True)


def store_validate_params(runtime, model_id, x, y):
    joblib.dump(x, '%s/%s_x_test.pkl' % (runtime.build_path, model_id), True)
    joblib.dump(y, '%s/%s_y_test.pkl' % (runtime.build_path, model_id), True)


def fit(runtime, model_id, model, x_train, y_train, **kwargs):
    checkpoint = FitchainCheckpoint(runtime, model_id)
    callbacks_list = []
    # -- check if there are already callbacks defined
    if "callbacks" in kwargs:
        callbacks_list = kwargs["callbacks"]
    callbacks_list.append(checkpoint)
    return model.fit(x_train, y_train, callbacks=callbacks_list, **kwargs)


def fit_generator(runtime, model_id, model, x_train, y_train, batch_size, generator, **kwargs):
    """ Fit model with a batch generated from the original dataset (x_train, y_train) """
    checkpoint = FitchainCheckpoint(runtime, model_id)
    callbacks_list = []

    # -- check if there are already callbacks defined
    if "callbacks" in kwargs:
        callbacks_list = kwargs["callbacks"]
    callbacks_list.append(checkpoint)
    return model.fit_generator(generator(x_train, y_train, batch_size),
                               callbacks=callbacks_list,
                               **kwargs)


class FitchainCheckpoint(Callback):
    """
    Save the model after every epoch.

    Arguments
        model_id: string, a unique identifier of the model being trained
    """

    def __init__(self, runtime, model_id):
        super(FitchainCheckpoint, self).__init__()
        self.model_id = model_id
        self.path = "%s/%s" % (runtime.build_path, self.model_id)

    def on_epoch_end(self, epoch, logs=None):
        self.model.save("%s_%d.keras.tmp" % (self.path, epoch), overwrite=True)
        os.rename("%s_%d.keras.tmp" % (self.path, epoch), "%s_%d.keras" % (self.path, epoch))
