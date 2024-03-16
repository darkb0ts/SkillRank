import tensorflow as tf


def score_resume(preprocessed_text):
    # Convert preprocessed text into model-compatible input
    features = prepare_features(preprocessed_text)
    score = model.predict(features)
    return score
