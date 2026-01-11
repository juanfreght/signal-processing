import librosa
import numpy as np
import os

def extract_features(file_path):
    """
    Extract MFCC and cepstrum features from an audio file
    
    Parameters:
    file_path (str): Path to the audio file
    
    Returns:
    numpy.ndarray: Combined feature vector (MFCCs + cepstrum)
    """
    try:
        # Load audio file
        signal, sr = librosa.load(file_path, sr=None)
        
        # Extract MFCC features (13 coefficients)
        mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfccs, axis=1)
        mfcc_std = np.std(mfccs, axis=1)
        
        # Extract cepstrum features (first 13 coefficients)
        spectrum = np.abs(np.fft.fft(signal))
        log_spectrum = np.log(spectrum + 1e-10)  # Add small value to avoid log(0)
        cepstrum = np.real(np.fft.ifft(log_spectrum))[:13]
        
        # Combine all features
        return np.concatenate([mfcc_mean, mfcc_std, cepstrum])
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

# Example usage for your directory
def process_directory(directory_path):
    """
    Process all audio files in a directory and extract features
    
    Parameters:
    directory_path (str): Path to directory containing audio files
    """
    features = []
    file_names = []
    
    # Supported audio formats
    audio_extensions = ('.ogg', '.wav', '.mp3', '.flac')
    
    # Check if directory exists
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return None
    
    # Process each file in directory
    for file in os.listdir(directory_path):
        if file.lower().endswith(audio_extensions):
            file_path = os.path.join(directory_path, file)
            print(f"Processing: {file_path}")
            
            feature_vector = extract_features(file_path)
            if feature_vector is not None:
                features.append(feature_vector)
                file_names.append(file)
    
    if not features:
        print("No valid audio files found or features extracted!")
        return None
    
    return np.array(features), file_names

# How to use with your specific path:
if __name__ == "__main__":
    audio_dir = "C:/Users/Ozair/Downloads/rec"
    features, file_names = process_directory(audio_dir)
    
    if features is not None:
        print(f"\nSuccessfully extracted features from {len(features)} files:")
        for name, feature in zip(file_names, features):
            print(f"{name}: Feature vector length {len(feature)}")