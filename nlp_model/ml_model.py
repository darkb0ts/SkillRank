import tensorflow as tf

model = tf.keras.models.load_model(
    "resume_scorer.h5")  # Load pre-trained model


def score_resume(preprocessed_text):
    # Convert preprocessed text into model-compatible input
    features = prepare_features(preprocessed_text)
    score = model.predict(features)
    return score
