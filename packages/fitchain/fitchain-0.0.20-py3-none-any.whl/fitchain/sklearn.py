import joblib
import os


def store_train_params(runtime, model_id, **kwargs):
    for key, val in kwargs.items():
        joblib.dump(val, '%s/%s_%s_train.pkl' % (runtime.build_path, model_id, key), True)


def store_validate_params(runtime, model_id, **kwargs):
    for key, val in kwargs.items():
        joblib.dump(val, '%s/%s_%s_test.pkl' % (runtime.build_path, model_id, key), True)


def fit(runtime, model_id, model, args):
    model.fit(**args)

    joblib.dump(model, '%s/%s.sklearn.old' % (runtime.build_path, model_id), True)
    os.rename('%s/%s.sklearn.old' % (runtime.build_path, model_id), '%s/%s.sklearn' % (runtime.build_path, model_id))

